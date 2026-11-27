# Ameaças à validade (T17, #114)

Versão completa das ameaças da proposta (§10), com o que as coletas das 3 máquinas mostraram
(`bernardo` em 23/11, `luisa` e `pedro` em 24 e 25/11/2026: 2.160 instalações medidas, sem
nenhuma falha). A classificação segue Wohlin et al. (2012).

Cada ameaça tem uma situação:

- **Mitigada:** o desenho ou a instrumentação reduz o efeito.
- **Declarada:** não dá para eliminar, então limita o que o artigo pode afirmar.
- **Aberta:** ainda depende de uma decisão ou de um dado.

## O que muda nas conclusões

1. **A inferência vale para estas 3 máquinas.** As repetições não são amostras independentes de
   "máquinas Windows" (C1). O sentido dos resultados se repete nas 3 máquinas em 48 das 51
   comparações significativas contra o npm.
2. **`wall_s` e o disco sustentam comparações. CPU e RAM do Bun, não** (Co1).
3. **O cenário `cold` não instala exatamente a mesma árvore dos cenários com lockfile.** Entre as
   máquinas, a árvore é a mesma porque as 3 usam o mesmo `registry/storage/` (I1).

---

## 1. Validade de conclusão

| # | Ameaça | Evidência ou efeito | Mitigação ou limite | Situação |
|---|---|---|---|---|
| C1 | **Pseudorreplicação** (Hurlbert, 1984): `stats.py` pareia por máquina × repetição e trata os 30 blocos como independentes | Repetições na mesma máquina compartilham hardware, disco e configuração. Os p-valores podem sair otimistas se lidos como generalização para outras máquinas | Os testes são lidos como comparação **nestas 3 máquinas**, e a conclusão se apoia no tamanho do efeito e na consistência entre blocos. Com só 3 medianas, um Wilcoxon bicaudal não passa de p = 0,25, então não dá para testar no nível da máquina. Decisão da #115: o dashboard repete a análise **separadamente por máquina**. Das 51 comparações contra o npm significativas no conjunto, 48 têm o mesmo sentido nas 3 máquinas e 32 também são significativas em cada máquina sozinha (139 de 180 no total por máquina). O mais rápido de cada célula é o mesmo nas 3 máquinas em 8 de 12 | Declarada |
| C2 | Variância do ambiente inflando o erro | 11 de 1.450 medições em células com mediana ≥ 1 s passaram de 3× a mediana da célula: 10 do npm e 1 do Yarn Berry PnP. Sete delas são da máquina `luisa` (I9) | Protocolo fixo, aquecimento descartado, 10 repetições, mediana e testes não paramétricos. **Nenhuma linha é removida por ser "estranha"** | Mitigada |
| C3 | Poder insuficiente | Na simulação sobre o piloto, `express-api cold` teve poder de 2% para speedup de 1,2×, por causa do ruído do npm naquela amostra | N = 10 pela análise de poder (`poder.md`); células com pouco poder não sustentam "não há diferença" | Declarada |
| C4 | Poder estimado com cenários que o piloto não teve | `ci` e `reinstall` herdaram o ruído de `cold` e `warm-cache` | Recalcular a variância com a coleta completa e reportar a observada | Declarada |
| C5 | Múltiplas comparações | 5 comparações contra o npm por projeto × cenário | Correção de Holm; só comparações contra o controle, não todos os pares | Mitigada |
| C6 | Supor normalidade em tempo assimétrico | Cauda à direita, com picos | Wilcoxon, Friedman, Cliff's δ e bootstrap | Mitigada |
| C7 | Significância sem relevância | Com N alto, diferenças de décimos de segundo (`reinstall` fica entre 0,2 s e 0,9 s) podem ser "significativas" | Sempre reportar speedup, diferença absoluta e Cliff's δ junto do p | Mitigada |

## 2. Validade interna

| # | Ameaça | Evidência ou efeito | Mitigação ou limite | Situação |
|---|---|---|---|---|
| I1 | **`cold` resolve versões mais novas que os lockfiles** e o `registry warm` não as guarda | Sem lockfile, o gerenciador pega a versão mais nova permitida: `router` 2.3.0 em vez de 2.2.0, `csstype` 3.2.4 em vez de 3.2.3, `baseline-browser-mapping` 2.11.38 em vez de 2.11.37. No `express-api`, o `cold` instala 5 arquivos a mais. Na máquina `bernardo`, o `router` 2.3.0 foi baixado da internet durante o piloto, e a coleta completa já o encontrou no cache. Numa máquina sem piloto, a primeira instalação `cold` poderia baixar da internet, e a árvore dependeria do dia do `warm` | As 3 máquinas usam o **mesmo `registry/storage/`**, publicado numa release com SHA-256, sem rodar `warm` (`protocolo.md`, passo 3). O `cold` do npm foi testado offline nos 3 projetos com esse storage. Na validação (#110), o `n_files` foi **idêntico entre as 3 máquinas nas 72 células** (projeto × cenário × gerenciador). A diferença entre `cold` e os cenários com lockfile permanece e faz parte do cenário | Mitigada |
| I2 | **"A frio" não é totalmente frio** | O runner apaga o cache dos gerenciadores, mas não o cache de arquivos do Windows; pacotes lidos há pouco podem vir da RAM | A ordem aleatorizada distribui o efeito entre os tratamentos. O construto é "sem cache do gerenciador", não "máquina recém-ligada" | Declarada |
| I3 | Verdaccio disputa CPU e disco com a instalação medida | Roda na mesma máquina, e gerenciadores com mais downloads simultâneos o exigem mais | Igual para todos os tratamentos; a T19 (#116) confere contra o registry real | Declarada |
| I4 | Efeito de ordem e aquecimento | Correlação de Spearman entre ordem e tempo relativo (tempo ÷ mediana da célula) de -0,16 a 0,02 por cenário, nas 3 máquinas juntas | Ordem aleatória por repetição com semente fixa; aquecimento marcado e descartado | Mitigada |
| I5 | Cache residual entre medições | O pnpm do piloto reutilizou um store fora da pasta isolada e nenhum `cold` foi frio | Cache apagado a cada instalação; a coleta aborta se cache ou registry estiverem fora do lugar; as 30 linhas do pnpm foram recoletadas | Mitigada |
| I6 | Versões diferentes entre máquinas | Yarn 1.22 pode virar Berry por um `.yarnrc.yml` em pasta acima | Ambiente portátil com versões fixadas; a coleta aborta se alguma divergir | Mitigada |
| I7 | Defender e serviços do Windows durante a coleta | Os picos de C2 tiveram CPU próxima da normal e tempo de 3 a 6× maior, o que indica espera. O Defender é suspeito, mas **não foi isolado** | Defender fixo no padrão, Windows Update pausado, apps fechados, WSL desligado | Declarada |
| I8 | Diferenças de hardware e de configuração entre máquinas | Cada integrante tem CPU, RAM e disco próprios. Além disso, `pedro` coletou com o perfil de energia "Legion Performance Mode" e o Windows build 26100, e as outras duas com "Alto desempenho" e build 26200 | Máquina como bloco; comparações sempre dentro da mesma máquina. O perfil e a build são parte do bloco e ficam registrados no `specs.json` | Mitigada |
| I9 | **Memória apertada e suspensão na máquina `luisa`** | 7,69 GB de RAM, com 0,34 GB livres no início da coleta. O Windows suspendeu por cerca de 40 min entre duas medições (14:14 e 14:53 de 24/11); a medição seguinte (`next-app`, `ci`, Yarn Berry PnP, repetição 2) levou 21,2 s, contra mediana de 13,1 s na célula | A pausa caiu entre medições, não dentro de uma, e a linha foi mantida pela regra de C2. A memória apertada é parte do bloco e pode explicar a concentração de picos do npm nessa máquina. O protocolo ganhou o item 10 (desligar a suspensão na tomada), já aplicado na coleta do `pedro` | Declarada |

## 3. Validade de construto

| # | Ameaça | Evidência ou efeito | Mitigação ou limite | Situação |
|---|---|---|---|---|
| Co1 | **`cpu_s` e `peak_rss_mb` subestimados, sobretudo no Bun** | A amostragem é a cada 50 ms e, no Windows, não há complemento do sistema. Nas 3 máquinas, a razão CPU/tempo mediana do Bun é 0,23 (os outros ficam entre 0,86 e 1,22); 55 linhas do Bun têm CPU igual a zero, todas no `reinstall` (13 em `bernardo`, 20 em `luisa` e 22 em `pedro`), e o pico mediano de RAM é de 20 MB | CPU e RAM ficam como secundárias e **não sustentam conclusão sobre o Bun**. `wall_s` e disco não são afetados | Declarada |
| Co2 | **Tipo de disco ambíguo em `specs.json`** | `media_type` lista todos os discos físicos (`SSD,SSD,HDD,SSD` em `bernardo`), não o da pasta de trabalho. Não comprova que o `F:` é SSD. Em `luisa` e `pedro`, com a pasta em `C:`, o campo traz só `SSD` | O coletor foi **mantido** para as 3 máquinas registrarem o mesmo formato, já que uma coleta completa foi feita com ele. Confirmar o disco manualmente ao descrever os blocos. Ver [trabalhos futuros](#5-trabalhos-futuros) | Declarada |
| Co3 | Lei de Goodhart: tempo de instalação como alvo | Um gerenciador pode ganhar em tempo adiando trabalho ou verificando menos | Medir também disco e `build_ok`; não apresentar o tempo como "qualidade" | Declarada |
| Co4 | Tempo de instalação ≠ produtividade | A instalação é só parte do fluxo de quem desenvolve | O impacto (T20) fala em horas de CI, não em produtividade | Declarada |
| Co5 | **Downloads ≠ uso** | O npm vem com o Node, o pnpm pode ser baixado a cada job de CI, o Bun tem instalador próprio e o Berry é versionado no projeto. Na série coletada (T15) o `npm` fica com 6,2 % dos downloads da semana e o `pnpm` com 88,8 %, o inverso do uso declarado | Ler junto do Stack Overflow Survey, que mede uso declarado; **não comparar níveis entre o npm e os outros**, só tendências e comparações entre os não-npm. A RQ4 descreve, não explica. Detalhado em [fonte_downloads.md §4](fonte_downloads.md) | Declarada |
| Co12 | **Nome de pacote mais velho que a ferramenta** | `bun`, `pnpm` e `yarn` já existiam no registry como pacotes sem relação: **24,1 % de todo o download histórico do nome `bun` é de outro software**, que passava de mil downloads/dia em 2017, quatro anos antes do Bun | Coluna `tool_era` em `data/npm_downloads/*.csv` marca o dia em que o nome passou a servir a ferramenta (datas do campo `time` do registry); a série bruta é preservada e a análise filtra. Ver [fonte_downloads.md §3](fonte_downloads.md) | Mitigada |
| Co6 | `build_ok` como proxy de instalação válida | Prova que o projeto compila, não que funciona em runtime | Declarado como proxy | Declarada |
| Co7 | Build ajustado por causa do PnP | `vite build` sem `tsc -b` e `next build --webpack`, nos 6 tratamentos | Mesmo build para todos, mas o sucesso do PnP vale **nessa configuração** | Declarada |
| Co8 | npm com `--no-audit --no-fund` ≠ npm de fábrica | Retira trabalho que só o npm faz por padrão | Medimos "npm como em CI"; a auditoria é um recurso que os outros não executam na instalação | Declarada |
| Co9 | Políticas de idade desligadas no pnpm e no Berry | Sem isso, eles falhariam onde os outros concluem | Mede desempenho, não política de segurança | Declarada |
| Co10 | Lockfiles diferentes por gerenciador | `n_files` varia entre gerenciadores no mesmo projeto (620 a 728 no `express-api`, sem contar o PnP) | Mesmo `package.json`; a árvore faz parte de como cada gerenciador funciona | Declarada |
| Co11 | Pegada em disco com hard links | O mesmo byte pode estar no projeto e no cache | `disk_mb + cache_mb`, com cada inode contado uma vez | Mitigada |

## 4. Validade externa

| # | Ameaça | Limite do que se pode afirmar | Situação |
|---|---|---|---|
| E1 | Só Windows 11, em NTFS e com Defender ativo | Não fala de Linux, macOS, Dev Drive ou runners de CI em Linux | Declarada |
| E2 | Três máquinas de estudantes, por conveniência | Não representa o parque de empresas | Declarada |
| E3 | Registry local ≠ internet real | Sem latência de rede, o ganho de downloads paralelos pode aparecer menor. A T19 (#116) confere numa rodada contra o registry público | Aberta (S03) |
| E4 | Três projetos pequenos e médios | Não fala de monorepos nem de árvores com milhares de pacotes | Declarada |
| E5 | Versões congeladas em nov/2026 | É um retrato datado; o npm medido é o 11.19.1, que vem com o Node 24, não o 12 | Declarada |
| E6 | Benchmarks dos fabricantes em outro ambiente | A comparação da RQ3 confronta ordens de grandeza, não valida os números deles | Declarada |

## 5. Trabalhos futuros

- **Refatorar o coletor de specs (`src/specs.py`)** para registrar em `media_type` só o disco
  físico da pasta de trabalho. A mudança fica para depois do estudo porque uma coleta completa já
  foi feita com o formato atual, e alterar o coletor agora deixaria os três blocos com registros
  diferentes (Co2).
- Medir CPU e RAM com contadores do Windows (Job Objects ou ETW) em vez de amostragem (Co1).
- Isolar o efeito do Defender, com pasta excluída e Dev Drive como fatores (I7, E1).
- Limpar o cache de arquivos do Windows entre as medições do cenário `cold` (I2).
- Repetir em mais máquinas, para testar a generalização no nível da máquina (C1, E2), e em Linux
  (E1).
- Incluir um monorepo grande como projeto-carga (E4).

## Referências

- Hurlbert, S. H. (1984). Pseudoreplication and the design of ecological field experiments.
  *Ecological Monographs*, 54(2), 187–211.
- Wohlin, C. et al. (2012). *Experimentation in Software Engineering*. Springer.
