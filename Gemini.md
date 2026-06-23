# 🛠️ toolbelt — Contexto do Agente

Coleção de ferramentas e scripts modulares (AI Agent Skills) para fluxos de trabalho autônomos.

## Tech Stack
- **Languages:** Python 3.10+ (using `uv` package manager) and Node.js 18+
- **Testing:**
  - Python: `pytest` + `pytest-cov`
  - Node.js: `jest`
- **Linting:** `ruff` (Python) and `eslint` (Node.js)

## Diretórios-chave
- `skills/context/`       <skills de engenharia de contexto>
- `skills/devops/`        <skills de CI/CD e Git>
- `skills/integration/`   <skills de scraping e APIs>
- `skills/automation/`    <skills de banco de dados e fluxos n8n>
- `.github/workflows/`    <workflow de CI Pipeline>

## Comandos Operacionais
| Ação | Comando |
| :--- | :--- |
| Instalar dependências Python | `uv sync` |
| Rodar testes Python | `uv run pytest` |
| Instalar dependências Node.js | `npm ci` |
| Rodar testes Node.js | `npm test` |
| Executar formatador Python | `uv run ruff format` |

## Critérios de Sucesso (Definição de Pronto)
- [ ] Todos os testes Python (`uv run pytest`) passam localmente com sucesso.
- [ ] Todos os testes Node.js (`npm test`) passam localmente com sucesso.
- [ ] O código modificado passa no ruff e não adiciona warnings de sintaxe.
- [ ] Modificações no CI usam ambientes isolados (`uv sync --frozen` e `uv run pytest`) para evitar colisão com dependências de sistema do GitHub Actions.
- [ ] Commits seguem o padrão de Conventional Commits em inglês.

## Acordos do Projeto
- **Isolamento de Mock:** Ao criar mocks para abertura de arquivos nos testes de Python, evite mockar `builtins.open` globalmente se o escopo puder ser restrito (prefira mockar `generator.open` ou usar gerenciadores de contexto estreitos) para evitar que o mock intercepte bibliotecas internas do Python (como `gettext` na inicialização de argumentos no Python 3.14+).
- **Sem Segredos:** Segredos locais devem ser obtidos através de variáveis de ambiente (`GEMINI_API_KEY`) ou via arquivo `.env`, nunca hardcoded no código ou repositório.
- **Git Push:** Sempre apresente as alterações e o diff completo antes de realizar o push para o GitHub.
