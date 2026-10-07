# Dicionário de Dados

## Tabela: `candidates.csv`

Esta tabela armazena a lista bruta de repositórios coletados pela Search API, antes de passarem pelo funil de filtragem.

| Coluna | Tipo | Unidade | Descrição / Fórmula / Origem na API |
|---|---|---|---|
| `full_name` | string | - | Nome completo do repositório no formato `owner/repo`. Origem: `full_name` ou `nameWithOwner`. |
| `html_url` | string | URL | Link para acessar o repositório no navegador. Origem: `html_url` ou `url`. |
| `stars` | inteiro | estrelas | Número de "stargazers" (favoritos). Origem: `stargazers_count` ou `stargazerCount`. |
| `language` | string | - | Linguagem de programação principal detectada pelo GitHub. Origem: `language` ou `primaryLanguage.name`. |
| `default_branch` | string | - | Nome do branch principal (ex: main, master). Origem: `default_branch` ou `defaultBranchRef.name`. |
| `created_at` | datetime | ISO-8601 | Data de criação original do repositório. Origem: `created_at` ou `createdAt`. |
| `pushed_at` | datetime | ISO-8601 | Data do último push feito no repositório. Origem: `pushed_at` ou `pushedAt`. |
