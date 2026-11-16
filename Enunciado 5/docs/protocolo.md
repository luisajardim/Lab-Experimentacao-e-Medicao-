# Protocolo de coleta (T07, #102)

Como cada integrante coleta na própria máquina, do jeito mais parecido possível com os outros
dois. **As três máquinas são blocos do experimento**: diferenças entre elas são esperadas e
ficam registradas em `specs.json`; o que não pode variar é o *procedimento*.

Se você só quer os comandos, leia a §0 e a §3. O resto explica por que cada regra existe.

---

## 0. Resumo: os comandos, na ordem

Na raiz do `Enunciado 5/`, numa janela aberta pelo ambiente portátil (§1.1):

```bash
uv sync                                        # dependências Python (uma vez)
uv run lab05 specs --machine <nome>            # specs + checklist automático -> conferir avisos
uv run lab05 registry up                       # Verdaccio local
uv run lab05 registry warm                     # enche o cache do Verdaccio (uma vez por máquina)
uv run lab05 collect --machine <nome> --dry-run    # confere a sequência e o nº de instalações
uv run lab05 collect --machine <nome> --reps <N>   # a coleta de verdade (N vem da T09)
uv run lab05 registry down                     # ao terminar
```

`<nome>` é sempre o mesmo para você, em todos os comandos: **`bernardo`, `luisa` ou `pedro`**.
Ele vira a pasta `data/raw/<nome>/` e a coluna `machine` do CSV.

---

## 1. Uma vez por máquina

### 1.1 Preparar o ambiente (forma oficial)

O grupo adota `scripts/windows_portable.ps1` como **a** forma de preparar o ambiente. Ele baixa
as versões fixadas para uma pasta só, confere o SHA-256 de cada download, aponta os caches para
dentro dessa pasta e abre uma janela do PowerShell com as variáveis prontas — **sem instalar
nada no sistema** (nada em Program Files, `%APPDATA%` ou no registro).

```powershell
powershell -NoExit -ExecutionPolicy Bypass -File scripts\windows_portable.ps1 -Root C:\lab05
```

Use um caminho **curto** e num disco comum (NTFS): `C:\lab05`, `D:\lab05`, `F:\lab05`. Para
desfazer tudo no fim do laboratório: o mesmo comando com `-Clean`.

> **Por que isso é obrigatório e não sugestão.** Versões diferentes entre as três máquinas
> seriam uma ameaça à validade interna difícil de detectar depois: um gerenciador uma minor mais
> novo pode mudar o algoritmo de resolução. Com o script, as três máquinas rodam exatamente as
> mesmas versões, e o `collect` **aborta** se alguma divergir.

As variáveis valem **só naquela janela**. Se fechar a janela, rode o script de novo (as
ferramentas já baixadas são reaproveitadas, leva segundos).

### 1.2 Pasta de trabalho (`LAB05_WORKDIR`)

É onde o runner copia os projetos, mantém os caches isolados e grava os logs. O ambiente
portátil já define `LAB05_WORKDIR = <Root>\work`. Se você preparar o ambiente de outro jeito,
copie `.env.example` para `.env` e preencha:

```
LAB05_WORKDIR=C:\lab05\work
```

Três regras que **mudam o resultado da medição** se forem quebradas:

| Regra | Por quê |
|---|---|
| Caminho **curto** (`C:\lab05\work`, não dentro de `Documentos\Faculdade\...`) | `node_modules` aninhado estoura o limite de 260 caracteres do Windows |
| **Sempre o mesmo disco**, do começo ao fim da coleta | pnpm e Yarn só criam hard links dentro do mesmo volume; em volumes diferentes eles **copiam**, e `disk_mb` muda de significado no meio da coleta |
| **Nunca** um `tmpfs` (o `/tmp` do WSL fica na RAM) | mediria a RAM, não o disco |

Também não ponha a pasta de trabalho dentro do OneDrive, Dropbox ou Google Drive: a sincronização
disputa os arquivos com o instalador e inventa variância do nada.

### 1.3 Espaço em disco

**Deixe pelo menos 20 GB livres** no volume da pasta de trabalho. Medido numa das máquinas do
grupo, depois de rodar os cenários `cold` e `ci` nas 18 células:

| O quê | Tamanho medido |
|---|---:|
| `LAB05_WORKDIR\run\` (18 pastas de projeto) | 2,8 GB |
| `LAB05_WORKDIR\cache\` (6 caches isolados) | 2,1 GB |
| `registry/storage/` (cache do Verdaccio) | 1,1 GB |
| Ambiente portátil (`tools` + `downloads` + `caches`) | 1,5 GB |
| **Total** | **≈ 7,5 GB** |

Os 20 GB são folga para os logs, para o arquivo temporário do antivírus e para o pico durante
uma instalação. O `uv run lab05 specs` avisa se houver menos que isso.

### 1.4 As versões fixadas

| Ferramenta | Versão | De onde vem |
|---|---|---|
| Node.js | 24.22.3 | `nodejs.org/dist` (zip, com SHA-256 conferido) |
| npm | 11.19.1 | vem junto com o Node |
| pnpm | 12.21.0 | `npm install -g pnpm@12.21.0` |
| Yarn Classic | 1.22.22 | `npm install -g yarn@1.22.22` |
| Yarn Berry | 4.18.1 | release versionado em `projects/*/lockfiles/yarn-berry-*/.yarn/releases/` |
| Bun | 1.4.4 | `github.com/oven-sh/bun/releases` (zip, com SHA-256 conferido) |
| uv | 0.13.8 | `github.com/astral-sh/uv/releases` |

**Os seis tratamentos, concretamente.** Só quatro binários são instalados: `npm` (vem com o
Node), `pnpm`, `yarn` e `bun`. Os três tratamentos de Yarn saem do **mesmo** binário `yarn`
1.22.22:

- `yarn-classic` — o Yarn 1.22 puro, sem nenhum `.yarnrc.yml` por perto;
- `yarn-berry-nm` e `yarn-berry-pnp` — o Yarn 1.22 lê o `yarnPath` do `.yarnrc.yml` que o runner
  copia do tratamento e **delega** para o Yarn Berry 4.18.1 versionado no projeto. A diferença
  entre os dois é só o `nodeLinker` (`node-modules` × `pnp`).

> **Cuidado que já nos mordeu:** o Yarn 1.22 procura `.yarnrc.yml` também nas **pastas acima** do
> projeto e na sua home. Um arquivo esquecido em `C:\Users\<você>\.yarnrc.yml` transformaria o
> tratamento `yarn-classic` em Berry **sem avisar**, e as linhas do CSV sairiam rotuladas errado.
> Por isso o `collect` confere as versões antes de começar e aborta. Não ignore esse erro com
> `--skip-version-check`.

Se precisar instalar à mão (sem o script), use exatamente essas versões e confira com
`uv run lab05 specs --machine <nome>`.

---

## 2. Checklist antes de cada sessão de coleta

Faça na ordem. Os itens marcados com 🤖 o `uv run lab05 specs` confere sozinho e avisa.

| # | Item | Como fazer | Por quê |
|---|---|---|---|
| 1 | 🤖 **Na tomada** | Conecte o carregador | Na bateria, o Windows reduz a frequência da CPU e os tempos despencam de qualidade |
| 2 | 🤖 **Perfil de energia "Alto desempenho"** | `powercfg /setactive SCHEME_MIN`, ou Configurações → Sistema → Energia | O perfil "Equilibrado" estaciona núcleos e muda o tempo entre repetições |
| 3 | **Windows Update pausado** | Configurações → Windows Update → Pausar por 1 semana | Um download ou instalação no meio da coleta contamina as células daquele intervalo |
| 4 | **Apps fechados** | Feche navegador, Teams, Discord, Spotify, Docker Desktop, WSL (`wsl --shutdown`) | Competem por CPU e disco; o navegador é o pior deles |
| 5 | 🤖 **Defender no padrão** | **Não mexa.** Proteção em tempo real **ligada** | É **fator fixo**, não variável: igual nas três máquinas. Desligar numa só inviabilizaria a comparação |
| 6 | 🤖 **Espaço em disco** | ≥ 20 GB livres (§1.3) | Disco cheio faz a instalação falhar no meio da sequência |
| 7 | 🤖 **Versões conferidas** | `uv run lab05 specs --machine <nome>` | Pega versão errada e `.yarnrc.yml` perdido antes de gastar horas coletando |
| 8 | **Temperatura inicial** | Máquina ligada e ociosa por ~10 min antes de começar; anote a temperatura se tiver como medir | Começar com a máquina fria e terminar com ela quente cria uma tendência ao longo da sequência |
| 9 | **Não usar a máquina** | Deixe coletando e vá fazer outra coisa | Qualquer uso entra na medição |

O item 8 e as observações do 3, 4 e 9 não dão para automatizar: registre-as com `--note`:

```bash
uv run lab05 specs --machine luisa --note "update pausado ate 23/11, 10 min ociosa, 24 C na sala"
```

> **Por que o Defender fica ligado.** É a configuração que 99 % dos desenvolvedores tem no
> Windows, então desligá-lo mediria um ambiente que quase ninguém usa. O custo é que ele
> escaneia cada arquivo criado — e `node_modules` tem dezenas de milhares. Isso entra no artigo
> como **limitação declarada** (o resultado vale para Windows com Defender no padrão), não como
> um fator que o experimento manipula.

---

## 3. Rodar a coleta

### Passo 1 — Abrir o ambiente

```powershell
powershell -NoExit -ExecutionPolicy Bypass -File scripts\windows_portable.ps1 -Root C:\lab05
```

Os comandos seguintes rodam nessa janela, na raiz do `Enunciado 5/`.

### Passo 2 — Specs e checklist

```bash
uv sync
uv run lab05 specs --machine <nome> --note "<o que o checklist pede e não é automático>"
```

Grava `data/raw/<nome>/specs.json` e imprime os avisos. **Resolva todos os avisos antes de
continuar.** Rode de novo depois de corrigir.

### Passo 3 — Subir o registry local

```bash
uv run lab05 registry up       # http://localhost:4873/
uv run lab05 registry warm     # uma vez por máquina: enche o cache com os 3 projetos
uv run lab05 registry status   # confere
```

O `warm` é o único passo que usa a internet de verdade: ele baixa cada pacote do registry
público **uma única vez**. Depois disso, as centenas de instalações da coleta são servidas do
storage local — é o que isola o gerenciador da velocidade da sua internet e o que evita martelar
um serviço público e gratuito.

### Passo 4 — Conferir a sequência

```bash
uv run lab05 collect --machine <nome> --dry-run
```

Mostra as primeiras células e o total de instalações. Confira se o número bate com o que o
grupo combinou (72 células × N). **Não coleta nada.**

### Passo 5 — Coletar

```bash
uv run lab05 collect --machine <nome> --reps <N>
```

O N definitivo vem da análise de poder (T09, `docs/poder.md`). Enquanto ele não sai, o piloto é:

```bash
uv run lab05 collect --machine <nome> --pilot --out data/raw/pilot/runs.csv
```

Cada linha aparece no terminal assim que termina, com o tempo, o disco e `ok`/`FALHOU`. Deixe
rodando e não use a máquina.

### Passo 6 — Encerrar

```bash
uv run lab05 registry down
```

Confira que `data/raw/<nome>/runs.csv` e `specs.json` existem, e **commite os dois**
(referenciando a issue da sua coleta).

---

## 4. Se parar no meio

Pode parar com `Ctrl+C` a qualquer momento. Cada linha é gravada com `flush`/`fsync` assim que a
instalação termina, então nada se perde.

**Para retomar, rode exatamente o mesmo comando de novo.** O runner lê o CSV, descobre o que já
está lá (mesma máquina, projeto, cenário, gerenciador, repetição, registry e aquecimento) e
**pula as células já gravadas** — não duplica e não recomeça.

Antes de retomar, refaça o checklist da §2: se a máquina dormiu, voltou para a bateria ou o
Windows atualizou, as condições mudaram.

---

## 5. Durante a coleta: o que não pode mudar

- **O disco da pasta de trabalho.** Trocar de volume no meio muda o comportamento de hard link
  do pnpm e do Yarn.
- **As versões** de Node ou de qualquer gerenciador. Não rode `npm update -g` no meio.
- **O perfil de energia** e o estado da tomada.
- **O Defender.** Nem ligar, nem desligar, nem adicionar exclusão de pasta.
- **Os projetos-carga** (`projects/`). Se alguém mexer num `package.json` ou num lockfile no meio
  da coleta do grupo, as linhas antes e depois deixam de ser comparáveis. Qualquer mudança ali
  obriga a **recoletar tudo** nas três máquinas.

---

## 6. Problemas conhecidos

| Sintoma | O que é | O que fazer |
|---|---|---|
| `collect` aborta com "versões fora do esperado" | Versão errada ou `.yarnrc.yml` numa pasta acima do projeto / na home | Rode `uv run lab05 specs`, compare com a §1.4, apague o `.yarnrc.yml` intruso. **Não** use `--skip-version-check` |
| `yarn-classic` responde 4.18.1 | O mesmo caso acima: o Yarn 1.22 obedeceu a um `yarnPath` de fora do projeto | Idem |
| `exit_code = 124` em várias linhas | Timeout (900 s por instalação) | Veja o log em `LAB05_WORKDIR/logs/<maquina>/<run_id>.log`; normalmente é o Verdaccio fora do ar ou disco cheio |
| Verdaccio não sobe | Porta 4873 ocupada ou processo órfão de uma sessão anterior | `uv run lab05 registry down` e depois `up`; veja `registry/verdaccio.log` |
| Erro de caminho muito longo | `LAB05_WORKDIR` fundo demais | Mude para um caminho curto (§1.2) e recomece aquela célula |
| Instalação falha só no `pnpm` ou no Yarn Berry, com "publicado há menos de 24 h" | Política de idade de versão desses dois gerenciadores | Não deveria acontecer: está desligada nas configs dos tratamentos. Se acontecer, avise o grupo — algum arquivo de `projects/` mudou |
| A coleta ficou muito mais lenta que a dos outros | Algum app subiu, o Windows atualizou ou a máquina esquentou | Pare, refaça o checklist da §2 e retome (§4) |

---

## 7. O que fica gravado e onde

| Arquivo | Conteúdo | Vai para o git? |
|---|---|---|
| `data/raw/<maquina>/runs.csv` | uma linha por instalação medida (formato em [`schema.md`](schema.md)) | **sim** |
| `data/raw/<maquina>/specs.json` | specs do bloco + checklist automático + sua `--note` | **sim** |
| `LAB05_WORKDIR/logs/<maquina>/<run_id>.log` | saída de cada instalação | não (só para depurar) |
| `LAB05_WORKDIR/run/`, `LAB05_WORKDIR/cache/` | projetos copiados e caches | não |
| `registry/storage/` | cache de pacotes do Verdaccio | não |

O `specs.json` é o que permite, na análise, explicar por que um bloco foi sistematicamente mais
lento que outro. Sem ele, a diferença entre máquinas vira ruído inexplicável.

Exemplo do que o `specs` imprime (máquina da Luísa, 16/11/2026):

```
  máquina   luisa
  SO        Microsoft Windows 11 Home Single Language 26200
  CPU       13th Gen Intel(R) Core(TM) i5-13450HX (10 núcleos físicos, 16 lógicos)
  RAM       7.69 GB
  disco     66.17 GB livres de 237.48 GB em C:\lab05\work (NTFS, SSD)
  trabalho  C:\lab05\work
  versões   node 24.22.3, npm 11.19.1, pnpm 12.21.0, bun 1.4.4, yarn-classic 1.22.22,
            yarn-berry-nm 4.18.1, yarn-berry-pnp 4.18.1
[lab05] fora do protocolo (docs/protocolo.md):
  - perfil de energia: 'Equilibrado' (o protocolo pede Alto desempenho)
```

---

## 8. De onde vem cada regra

Ligação entre o protocolo e as ameaças à validade de [`proposta.md`](proposta.md) (§10):

| Regra | Ameaça que ela mitiga |
|---|---|
| Ambiente portátil com versões fixadas | **Interna:** versões diferentes entre blocos |
| Checagem de versões antes de coletar | **Interna:** `yarn-classic` virar Berry sem aviso |
| Tomada, perfil de energia, apps fechados, máquina ociosa | **Conclusão:** variância do ambiente inflando o erro |
| Windows Update pausado | **Interna:** evento externo no meio da sequência |
| Defender fixo no padrão | **Externa:** o resultado vale para o Windows que as pessoas usam de fato |
| Registry local + `warm` uma única vez | **Interna:** velocidade da internet entrando na medição · **ética:** não sobrecarregar um serviço público |
| Mesmo disco, caminho curto, fora do OneDrive | **Construto:** hard links e `disk_mb` medindo a mesma coisa do começo ao fim |
| Ordem aleatorizada e aquecimento descartado (o runner faz) | **Interna:** efeito de ordem e de aquecimento do sistema de arquivos |
| `specs.json` por bloco | **Conclusão:** diferença entre máquinas explicada, não tratada como ruído |

---

Dúvidas sobre a instrumentação: [`runner.md`](runner.md). Sobre os dados: [`schema.md`](schema.md).
Sobre o registry: [`registry.md`](registry.md). Sobre o ambiente portátil:
[`windows_portable.md`](windows_portable.md).
