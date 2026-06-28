---
name: local-vram-orchestrator
description: SRE guidelines and code patterns for VRAM optimization and serialization of local models (LLM, TTS, Whisper, Stable Diffusion, CLIP) on consumer GPUs with limited video memory (e.g. 6GB RTX 4050). Use when running multiple heavy models on one GPU, debugging CUDA out-of-memory (OOM) errors, designing a task queue that shares a single GPU across FastAPI/Docker microservices, or deciding between quantization and offloading strategies.
---

# local-vram-orchestrator

Operating manual for running heavy AI models on a single consumer GPU without hitting `CUDA out of memory`. Built for the constraint of ~6GB VRAM (RTX 4050 class) where two large models cannot coexist in memory.

## Core principle: one heavy model on the GPU at a time

On 6GB you cannot hold an LLM + SD + Whisper resident simultaneously. The architecture must **serialize** GPU-intensive work: load → run → fully unload → load next. Concurrency is for I/O and CPU work, never for two resident models.

## 1. Aggressive VRAM release

`torch.cuda.empty_cache()` alone does **not** free memory still referenced by a live Python object. You must delete the references first, then collect, then empty the cache — in that order.

```python
import gc
import torch

def release_model(model):
    """Fully evict a model from VRAM. Call before loading the next heavy model."""
    try:
        model.to("cpu")          # move weights off-GPU first (helps fragmentation)
    except Exception:
        pass
    del model                    # drop the Python reference
    gc.collect()                 # collect any cyclic refs holding tensors
    torch.cuda.empty_cache()     # return freed blocks to the driver
    torch.cuda.ipc_collect()     # release cross-process cached allocations
```

Common leak sources to delete explicitly: the model, the pipeline wrapper, optimizer/scheduler objects, any `output` tensors still in local scope, and `**inputs` dicts moved to CUDA. A single tensor retained in a closure or a logging list pins the whole allocation block.

```python
# After inference, before unloading:
del outputs, inputs
gc.collect(); torch.cuda.empty_cache()
```

### Verify, don't trust

Always confirm memory actually dropped — agent-reported "freed" is not evidence.

```python
def vram_report(tag=""):
    a = torch.cuda.memory_allocated() / 1024**2
    r = torch.cuda.memory_reserved() / 1024**2
    print(f"[VRAM {tag}] allocated={a:.0f}MB reserved={r:.0f}MB")
```

`reserved` staying high after release usually means a reference is still alive somewhere — hunt it down rather than ignoring it.

## 2. Quantization and precision

Pick the lightest representation that meets quality needs. Rough VRAM trade-offs:

| Strategy | Relative VRAM | Notes |
|---|---|---|
| FP32 | 100% | Default; almost never needed for inference on 6GB |
| FP16 / BF16 | ~50% | First thing to try; `model.half()` or load with `torch_dtype=torch.float16` |
| INT8 (bitsandbytes) | ~25% | `load_in_8bit=True`; small quality hit, big savings for LLMs |
| INT4 / NF4 | ~12-15% | `load_in_4bit=True`, `bnb_4bit_quant_type="nf4"`; for larger LLMs on tiny VRAM |
| ONNX Runtime | varies | Good for Whisper/CLIP; better CPU/GPU offload control, lower overhead |

```python
# Diffusers on low VRAM — FP16 + attention/VAE slicing + sequential CPU offload
pipe = StableDiffusionPipeline.from_pretrained(
    model_id, torch_dtype=torch.float16, safety_checker=None
)
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()
pipe.enable_sequential_cpu_offload()   # streams layers GPU<->CPU; slower but fits 6GB
```

For LLMs, prefer 4-bit (NF4) loading over trying to fit FP16 weights that won't fit. For Whisper/CLIP, ONNX or FP16 is usually enough.

## 3. Dynamic offloading

When a model is *almost* too big, offload instead of refusing to run:
- `enable_sequential_cpu_offload()` (diffusers) — lowest VRAM, slowest.
- `enable_model_cpu_offload()` — keeps whole submodules on GPU only while active; faster than sequential, more VRAM.
- `device_map="auto"` + `max_memory={0: "5GiB", "cpu": "16GiB"}` (accelerate) — let accelerate split layers across GPU/CPU automatically.

Trade-off is always speed for memory. On 6GB, accept the slowdown rather than the crash.

## 4. GPU serialization across microservices

The dangerous failure mode: two FastAPI requests (e.g. a TTS job and an SD job) both try to load a model and OOM each other. Enforce a **single global GPU lock** so only one heavy task touches the card at a time.

```python
import asyncio

# Module-level, shared across all requests in the process
gpu_lock = asyncio.Lock()

async def run_gpu_task(job):
    async with gpu_lock:                 # serialize: one heavy model at a time
        model = load_model(job.kind)     # load INSIDE the lock
        try:
            return await asyncio.to_thread(model.infer, job.payload)
        finally:
            release_model(model)         # always unload, even on error
```

Key rules:
- **Load inside the lock**, not at startup, if models rotate. Resident-at-startup only works if a single model fits with headroom.
- **Release in `finally`** so a failed job doesn't leak VRAM and starve the next one.
- For multi-process (Gunicorn workers, separate Docker containers sharing one GPU), an in-process `asyncio.Lock` is **not enough** — use a cross-process lock: a file lock (`filelock` / `flock`), a Redis lock, or a dedicated single-worker "GPU service" that all others queue against. Prefer the single GPU-worker service: it makes serialization structural instead of cooperative.

```python
# Cross-process file lock pattern (filelock)
from filelock import FileLock
gpu_flock = FileLock("/tmp/gpu.lock")

def run_gpu_task_sync(job):
    with gpu_flock:                      # blocks other processes
        model = load_model(job.kind)
        try:
            return model.infer(job.payload)
        finally:
            release_model(model)
```

### Docker / container notes
- Pass the GPU through (`--gpus all` or `deploy.resources` in compose) but **do not** run multiple GPU containers expecting them to share gracefully — they won't coordinate VRAM. Route all GPU work through one worker.
- Set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` to reduce fragmentation-driven OOM on long-running workers.
- A warm model held resident in a dedicated worker beats reloading per request *if and only if* that one model fits alone with headroom.

## 5. OOM debugging checklist

When you hit `CUDA out of memory`:
1. `vram_report()` before and after each load to find which model overflows.
2. Confirm previous model was actually released (reserved dropped near baseline).
3. Drop precision one tier (FP16 → INT8 → INT4) before adding offload.
4. Add attention/VAE slicing for diffusion models.
5. Reduce batch size to 1 and shrink resolution / context length.
6. Set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.
7. If two tasks still collide, the lock isn't covering both code paths — audit every entry point that loads a model.

## Anti-patterns (do not ship)
- Calling `empty_cache()` without deleting references first (frees nothing).
- Loading all models at startup "to be fast" on a GPU that can't hold them.
- Trusting an agent/script that *reports* memory was freed — verify with `memory_reserved()`.
- Using an in-process lock when workers are separate processes/containers.
- Silently swapping the intended strategy (e.g. dropping quantization) without an explicit note — record what was actually loaded.
