# Miner

Subprojeto responsável por **coletar, processar e disponibilizar dados** para os experimentos de medição.  
O foco do Miner é automatizar a extração de informações e padronizar a execução em ambiente local e containerizado.

## Arquitetura detalhada

A proposta do Miner é seguir uma arquitetura modular e extensível, separando claramente as responsabilidades de especificação, execução, adaptação de fontes e armazenamento. O objetivo é permitir que o sistema colete dados de diferentes plataformas sem acoplar o núcleo da aplicação a uma implementação específica.

### 1. Camada de especificação

A execução da mineração é guiada por uma especificação declarativa, representada por um modelo de configuração que descreve:

- o identificador do job;
- a versão da especificação;
- o provedor a ser usado;
- a query ou configuração de requisição;
- as regras de extração de métricas a partir da resposta bruta.

Essa abordagem torna o fluxo mais flexível: novas consultas, novos endpoints e novas métricas podem ser adicionadas sem necessariamente alterar a lógica principal do código.

### 2. Camada de contratos e interfaces

O núcleo da aplicação é abstraído por interfaces bem definidas. Isso permite que diferentes provedores compartilhem o mesmo contrato de execução, mesmo quando usam protocolos distintos, como GraphQL, REST ou outros formatos de API.

No projeto atual, essa camada já aparece na estrutura:

- `IMiningProvider`: define o contrato comum para execução do processo de mineração;
- `MiningChunk`: representa uma página ou bloco de dados retornado pelo provedor;
- `JobSpecification`: descreve a configuração do job de mineração;
- `MiningTarget`: representa o alvo da extração, como repositório, projeto ou entidade equivalente.

Essa camada é essencial para garantir desacoplamento entre o motor de execução e os adaptadores específicos.

### 3. Camada de provedores (padrão Adapter)

Cada plataforma de dados é encapsulada por um provedor específico. O papel desse componente é transformar a lógica da fonte externa em um fluxo uniforme para o restante do sistema.

Exemplos conceituais:

- `GitHubGraphQLProvider`: responsável por consultar dados do GitHub via GraphQL;
- `GitLabRestProvider`: responsável por consumir endpoints REST do GitLab;
- `BitbucketRestProvider`: responsável por integrar com outra plataforma semelhante.

Cada provedor implementa o mesmo contrato, o que permite que o restante da aplicação trabalhe com uma interface única, independentemente da origem dos dados.

### 4. Camada de fábrica e registro de provedores

Para evitar acoplamento direto à implementação concreta, a aplicação usa uma fábrica de provedores. Essa fábrica é responsável por registrar e localizar o adaptador correto conforme o tipo de fonte solicitado.

Esse padrão facilita:

- adição de novas plataformas sem alterar o fluxo principal;
- troca de implementação sem impactar o restante do sistema;
- manutenção mais simples e previsível.

### 5. Fluxo de execução da mineração

O fluxo geral do sistema pode ser descrito em etapas:

1. Uma especificação de mineração é carregada ou recebida.
2. O sistema identifica o provedor apropriado.
3. O provedor executa a consulta ou requisição à fonte externa.
4. Os dados brutos são emitidos em blocos ou páginas.
5. As regras de extração são aplicadas para gerar métricas estruturadas.
6. Os resultados podem ser persistidos para posterior análise.

Esse modelo deixa a execução mais flexível e prepara o sistema para evoluir para cenários assíncronos, com filas, retries e paralelismo.

### 6. Estratégia de armazenamento

A arquitetura prevê armazenamento em duas camadas:

- camada raw: preserva a resposta bruta recebida da fonte externa;
- camada analítica: armazena as métricas e indicadores extraídos.

Essa divisão é importante porque permite reutilizar os dados já coletados para gerar novas métricas sem precisar refazer chamadas à API em cada mudança de análise.

### 7. Evolução esperada para produção

Em um estágio mais avançado, o Miner pode evoluir para um modelo assíncrono e resiliente, com:

- filas de processamento;
- controle de rate limit;
- retentativas automáticas;
- workers dedicados;
- observabilidade e logs distribuídos.

Essa evolução preserva o mesmo desenho arquitetural, mas adiciona escalabilidade, tolerância a falhas e maior capacidade de processamento em lote.

## Pré-requisitos

- Git
- Node v22+
- Docker e Docker Compose

## Como rodar

### 1) Clonar e acessar o diretório

```bash
git clone <URL_DO_REPOSITORIO>
cd "Lab-Experimentacao-e-Medicao-/Enunciado 1/Miner"
```

### 2) Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do subprojeto:

```env
# App Configuration
PORT=3000
NODE_ENV=development

# Target Infrastructure (Containers Locais)
DATABASE_URL="postgresql://miner_user:miner_password@localhost:5432/repository_miner?schema=public"
REDIS_HOST=localhost
REDIS_PORT=6379

# GitHub Tokens (Cada dev usa o seu próprio para não estourar rate limit durante os testes)
GITHUB_PERSONAL_ACCESS_TOKEN=github_pat_xxxxxxx
```

## Como rodar o script de mineração

Depois de configurar o `.env` (passo acima), a mineração roda direto com Node,
sem precisar do Docker:

```bash
npm install
npm run dev -- ./specs/<nome-da-spec>.yaml
```

Cada spec em `specs/` descreve uma consulta GraphQL diferente. Por exemplo:

```bash
npm run dev -- ./specs/github-rq1-rq4-v1.yaml
```

O script pagina automaticamente até atingir o limite configurado em
`src/index.ts` (`MAX_REPOSITORIES`, padrão **1000** na Sprint 2), imprime o
progresso no terminal (rate limit, chunks recebidos) e salva o resultado em
`data/<id-da-spec>_<timestamp>.csv`.

Para um teste curto:

```bash
# PowerShell
$env:MAX_REPOSITORIES=20
npm run dev -- ./specs/github-search-v1.yaml
```

Validar RQ05/RQ06 no último CSV coletado:

```bash
npm run validate:rq05
```

## Snapshot do GitHub Projects (Issue #14)

No fechamento de cada sprint, exporte o estado do board para CSV. O script
reusa o provider GraphQL (`fetch` + rate limit + backoff), sem Octokit.

No `.env`:

```env
GITHUB_PROJECT_OWNER=luisajardim
GITHUB_PROJECT_OWNER_TYPE=user
GITHUB_PROJECT_NUMBER=1
SPRINT_ID=S02
```

O PAT precisa de `public_repo` **e** `read:project` (classic) ou, no
fine-grained, permissão **Projects: Read**. Sem isso a API responde
`INSUFFICIENT_SCOPES`.

```bash
npm run snapshot
```

Saída: `data/snapshots/S02_<timestamp>.csv` e acumulado em
`data/snapshots/history.csv`. Se o Project for de organização, use
`GITHUB_PROJECT_OWNER_TYPE=organization`.

## Execução com Docker Compose

Subir os serviços:

```bash
docker compose up --build
```

Executar em segundo plano:

```bash
docker compose up --build -d
```

Parar serviços:

```bash
docker compose down
```

Ver logs:

```bash
docker compose logs -f
```

## Estrutura esperada de variáveis (`.env`)

| Variável | Descrição | Exemplo |
|---|---|---|
| `NODE_ENV` | Ambiente de execução | `development` |
| `PORT` | Porta da instância do Miner | `3003` |
| `DATABASE_URL` | String de conexão com o Postgres | `postgresql://miner_user:miner_password@localhost:5432/repository_miner?schema=public` |
| `REDIS_HOST` | Host do Redis | `localhost` |
| `REDIS_PORT` | Porta do Redis | `6379` |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | Token pessoal do GitHub, usado para autenticar a query GraphQL. Gere em GitHub → Settings → Developer settings → Personal Access Tokens. Para minerar repositórios públicos: `public_repo`. Para o snapshot do Projects: também `read:project`. | `ghp_xxxxxxx` |
| `MAX_REPOSITORIES` | Quantos repositórios coletar (S02 = 1000) | `1000` |
| `GITHUB_PROJECT_OWNER` | Login do dono do Project v2 | `luisajardim` |
| `GITHUB_PROJECT_OWNER_TYPE` | `user` ou `organization` | `user` |
| `GITHUB_PROJECT_NUMBER` | Número do Project (aparece na URL `/projects/N`) | `1` |
| `SPRINT_ID` | Rótulo gravado no CSV do snapshot | `S02` |

## Decisões técnicas do grupo

Estas decisões valem para a coleta e para a análise das RQs, e servem de
rascunho para a seção de metodologia do relatório final — se algo mudar aqui,
atualize também o relatório (`../RELATORIO.md`).

- **Definição de "PR aceita" (RQ02):** consideramos aceita a pull request com
  status `MERGED` no GitHub. Implementado nas specs via
  `pullRequests(states: MERGED) { totalCount }` (ver
  `specs/github-search-v1.yaml` e `specs/github-rq2-rq3-v1.yaml`). PRs
  fechadas sem merge (`CLOSED` sem merge) não contam como aceitas.
- **Repositórios sem releases (RQ03):** entram no cálculo com o valor `0`
  (não são excluídos da amostra). Implementado em `src/index.ts`, na função
  `flattenRepositories`, com o fallback `repo.releases?.totalCount || 0`.
- **Fonte para "linguagens mais populares" (RQ05/RQ07):** **GitHub Octoverse 2025**
  (https://octoverse.github.com/ e o
  [post oficial](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)).
  Ranking por contribuidores (agosto/2025): TypeScript, Python, JavaScript,
  Java, C#. Essa é a única fonte do laboratório — não misturar com TIOBE ou GitHut.

