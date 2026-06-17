# 🛠️ toolbelt

A curated collection of modular, production-ready **AI Agent Skills** and utility scripts designed to supercharge autonomous developer workflows. Built with an SRE (Site Reliability Engineering) and Unix-like philosophy: highly cohesive, loosely coupled, and token-efficient.

This repository serves as a portfolio demonstrating advanced concepts in **AI Engineering**, context optimization, secure automation, and robust error-handling.

---

## 🗂️ Registry of Skills

 Habilidades desenvolvidas estruturadas de forma lógica e sequencial:

### 🧠 Categoria: Engenharia de Contexto & Qualidade (Fase 1)
*   **[`ai-slop-detector`](skills/context/ai-slop-detector):** Auditador de prosa e código. Detecta jargões genéricos de IA (AI-slop) e higieniza os arquivos de saída para soar de forma humana, natural e direta.
*   **[`context-compactor`](skills/context/context-compactor):** Compactador de arquivos de código fonte. Varre árvores de arquivos extensos e gera resumos leves contendo apenas assinaturas, classes, métodos e docstrings para otimização de tokens de contexto do agente.

### 🛠️ Categoria: DevOps & Git Workflows (Fase 2)
*   *Em breve:* **`smart-pr-generator`** (CLI de geração automática de Pull Requests com regras anti-slop).
*   *Em breve:* **`unit-test-bootstrapper`** (CLI para gerar esqueletos de testes a partir de classes compactadas).

### 🌐 Categoria: Integração de Dados & APIs (Fase 3)
*   *Em breve:* **`structured-news-harvester`** (Scraper e limpador de discussões técnicas).
*   *Em breve:* **`schema-markup-builder`** (Gerador de marcação JSON-LD para SEO técnico).

---

## 🚀 Como Funciona

Cada habilidade nesta coleção é empacotada em uma pasta sob `skills/` seguindo a estrutura padrão do ecossistema Google Antigravity:

```text
skills/[categoria]/[nome-da-skill]/
├── SKILL.md        # Instruções declarativas de comportamento e metadados
└── scripts/        # Scripts utilitários de CLI (Python com uv, ou Node.js)
```

### Princípios de Engenharia Adotados:
1.  **Token Efficiency (Compactação):** Agentes consomem contexto e custam dinheiro. Nossas ferramentas minimizam o texto desnecessário enviado aos LLMs.
2.  **Rate Limiting Declarativo:** Todas as APIs integram algoritmos de recuo exponencial (exponential backoff) e manipulação estruturada do código `HTTP 429`.
3.  **Higienização de Prosa:** Escrita limpa, livre de clichês e com foco em clareza técnica.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter detalhes.
