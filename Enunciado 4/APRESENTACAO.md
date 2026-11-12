# Lab04 — Roteiro da apresentação

**App:** <https://experimentacao-lab04-spearman.streamlit.app> · página **Dashboard** (menu do topo)
**Formato:** três falas corridas (Bernardo abre, Pedro apresenta o dashboard e Luísa conclui), em **~6 min**.
As falas já respondem às 15 perguntas do enunciado; se o professor perguntar alguma, a resposta curta está na
[parte 2](#parte-2--as-15-perguntas-para-consultar). Respostas longas, para estudar:
[`docs/respostas_detalhadas.md`](docs/respostas_detalhadas.md).

**Antes de começar:** app aberto no Dashboard, α = 0,05, todas as situações marcadas, tela cheia. No celular,
deixar aberta **esta página** (não a versão longa).

---

# Parte 1 — As falas

## Bernardo · abertura e cenário (~1,5 min) · cobre as perguntas 1, 2, 3, 4 e 11

> Nosso trabalho compara os testes de **Pearson e Spearman** numa pergunta de engenharia de software: **classes maiores
> têm mais defeitos? E essa relação é geral, ou é puxada por poucas classes gigantes?**
>
> Escolhemos o **KC1, um sistema C++ da NASA**, porque é um dataset público e documentado que traz, para cada classe,
> exatamente as duas variáveis do nosso par: o tamanho em linhas de código e o número de defeitos. Baixamos os dados
> do repositório PROMISE, pelo OpenML, e sorteamos **30 das 145 classes** com semente fixa.
>
> A **hipótese nula** é que o tamanho da classe não tem relação com os defeitos; a **alternativa**, que tem. O teste é
> **bicaudal**: a gente espera uma relação positiva, mas não apostou na direção.
>
> *(apontar o G1 e a dispersão)* Os dados são muito assimétricos: a maioria das classes é pequena, **59% não têm
> nenhum defeito**, e uma única classe tem **2.883 linhas e 101 defeitos**. Para simular, ajustamos uma **Gamma** ao
> tamanho e uma **binomial negativa** aos defeitos (o roxo no G1 é o simulado e acompanha o real) e montamos
> **quatro situações**: uma ideal, com dados normais; uma realista, com a forma do KC1; a mesma com só 10 classes; e
> uma em que aparece uma classe extrema, como a do KC1. São 10 mil simulações para cada situação e tamanho de efeito.
>
> Das violações, a classe extrema é a que mais pesa: ela **domina o cálculo do Pearson**, mas no Spearman vira só o
> maior posto. O Pedro mostra agora o que isso faz com os testes.

## Pedro · o dashboard (~3 min) · cobre as perguntas 5, 6, 7, 9, 10 e 12

> Este é o nosso dashboard: em cima, os filtros de α e de situações e seis indicadores; embaixo, os gráficos na
> ordem do estudo.
>
> *(G2)* Os dois testes **medem associação, não comparam médias**: o **Pearson usa os valores**, então uma classe
> gigante pesa muito; o **Spearman usa os postos**, e cada classe pesa igual. Este gráfico mostra como a estatística t
> se comporta **quando não há efeito**: a curva é a teoria, e as barras são 10 mil simulações. A **região de
> rejeição** fica nas duas caudas, nas faixas cinza, onde esse t é raro. Repare que o Spearman segue a curva, mas o
> Pearson tem a **cauda direita longa**. A área colorida é o **p-valor do exemplo**: a chance de um t tão extremo se
> H₀ fosse verdadeira, e **não** a chance de H₀ ser verdadeira. Nesse exemplo nenhum teste rejeita, mas o efeito
> existe: os dois cometem erro tipo II.
>
> *(G3)* Aqui é o **erro tipo I**, sem efeito nenhum. O Spearman fica perto de 5% em todas as situações. O Pearson
> fica **liberal**: 6,5% com 10 classes e **20% na situação com a classe extrema**.
>
> *(G4)* No **poder**: com dados normais, o Pearson tem um pouco mais; com dados como os do KC1, o Spearman passa à
> frente a partir de ρ = 0,3 e chega a **85% contra 70%**. *(trocar o α para 0,01)* Com **α = 0,01**, tudo cai:
> menos falso positivo, menos poder. O Spearman fica perto de 1%, e o Pearson continua liberal, com 15% na situação
> com a classe extrema. *(voltar o α para 0,05)*
>
> A Luísa fecha com o que isso significa para os dados reais.

## Luísa · conclusão (~1,5 min) · cobre as perguntas 8, 13, 14 e 15

> *(gráfico da correlação na amostra real)* Nos dados reais, **os dois testes rejeitam H₀**, mas contam histórias
> diferentes. O Pearson dá **r = 0,84**, inflado por aquela classe gigante: sem ela, cai para 0,58. O Spearman dá
> **ρₛ = 0,51**, que é o retrato fiel da tendência geral. E isso importa na prática: **a metade maior das classes
> concentra 93% dos defeitos**.
>
> No nosso cenário, o erro mais grave é o **tipo I**: achar uma relação que não existe e concentrar os testes nas
> classes grandes à toa. É justamente o erro que a classe gigante provoca no Pearson. O tipo II seria perder esse
> sinal.
>
> A simulação **confirmou quase tudo** o que esperávamos: Pearson melhor com dados normais, Spearman nos realistas.
> **Erramos com 10 classes**: os muitos zeros deixam o Spearman com poucos postos, e o Pearson rejeita mais, mas parte
> disso é falso positivo.
>
> Por isso, **recomendamos o Spearman**. Usaríamos o Pearson só com dados quase normais ou para medir relação linear
> nos valores. A **principal limitação** é que tudo depende do nosso gerador e de dados antigos da NASA. Obrigada!

---

# Parte 2 — As 15 perguntas (para consultar)

Responde quem apresentou o assunto, mas o professor pode perguntar a qualquer um.

| # | Pergunta | Quem | Resposta curta |
|---|---|---|---|
| 1 | Cenário, H₀ e H₁ | Bernardo | KC1, sistema C++ da NASA. H₀: o tamanho da classe não tem relação com os defeitos; H₁: tem. Queremos saber se a relação é geral ou puxada por poucas classes gigantes. |
| 2 | Unicaudal ou bicaudal? | Bernardo | Bicaudal: esperamos relação positiva, mas não apostamos na direção; a rejeição fica nas duas caudas. |
| 3 | Coleta e forma dos dados | Bernardo | PROMISE pelo OpenML, 30 de 145 classes com semente fixa. Muito assimétricos: 59% sem defeito e uma classe com 2.883 linhas e 101 defeitos. |
| 4 | Dados reais → parâmetros da simulação | Bernardo | Gamma no tamanho e binomial negativa nos defeitos, ajustadas nas 145 classes (o roxo do G1 acompanha o real). A classe extrema virou a situação S-outlier. |
| 5 | O que cada teste compara | Pedro | Os dois medem associação, não médias: o Pearson usa os valores (classe gigante pesa muito); o Spearman, os postos (cada classe pesa igual). |
| 6 | Distribuição sob H₀ e região de rejeição (G2) | Pedro | É o t sem efeito: curva teórica e 10 mil simulações. A rejeição fica nas duas caudas, onde t é raro; o Pearson tem a cauda direita longa. |
| 7 | O p-valor do exemplo | Pedro | Área colorida: a chance de um t tão extremo se H₀ fosse verdadeira, não a chance de H₀ ser verdadeira. Nenhum rejeita, mas há efeito: erro tipo II. |
| 8 | Erro tipo I e tipo II; qual é pior | Luísa | Tipo I: achar relação que não existe e concentrar testes nas classes grandes à toa. Tipo II: perder esse sinal. O tipo I é pior, e é o que a classe gigante provoca no Pearson. |
| 9 | G3: alguém se afastou de 5%? | Pedro | O Spearman fica perto de 5% em tudo. O Pearson fica liberal: 6,5% com 10 classes e 20% na S-outlier. |
| 10 | G4: qual tem mais poder? | Pedro | Com dados normais, o Pearson; com dados como os do KC1, o Spearman a partir de ρ = 0,3 (85% contra 70% em ρ = 0,6). |
| 11 | Violação simulada e por que afeta mais um teste | Bernardo | Assimetria, amostra pequena e classe extrema. A classe extrema domina o cálculo do Pearson; no Spearman vira só o maior posto. |
| 12 | E com α = 0,01? | Pedro | Tudo cai: menos falso positivo, menos poder. O Spearman fica perto de 1%; o Pearson continua liberal (15% na S-outlier). |
| 13 | A simulação confirmou o esperado? | Luísa | Quase tudo. Erramos com 10 classes: os zeros deixam o Spearman com poucos postos, e o Pearson rejeita mais, mas parte é falso positivo. |
| 14 | Dados reais: mesma conclusão? Importância prática? | Luísa | Os dois rejeitam H₀, mas r = 0,84 é inflado (0,58 sem a classe gigante); ρₛ = 0,51 é o fiel. A metade maior das classes concentra 93% dos defeitos. |
| 15 | Recomendação, quando muda e limitação | Luísa | Spearman. Pearson só com dados quase normais ou para relação linear nos valores. Limitação: depende do gerador e de dados antigos da NASA. |

## Se o professor perguntar outra coisa

Três frases que respondem quase tudo:

1. **"Uma classe gigante (2.883 LOC, 101 defeitos) infla o Pearson; o Spearman quase não muda."** (KC1 inteiro: r 0,69 →
   0,57 sem ela; ρₛ 0,57 → 0,56)
2. **"O Spearman segura o erro tipo I perto de 5% em todas as situações; o Pearson, não."** (S-outlier: 20% contra 5%)
3. **"Com 30 classes, o Spearman tem 85% de poder e precisaria de ~28 classes para 80%; o Pearson, de ~43."** (bloco de
   tamanho da amostra, no fim do Dashboard)

Os textos completos de cada gráfico estão na página **Relatório** do app.

| Números para lembrar | |
|---|---|
| Amostra real | 30 de 145 classes · r = 0,84 · ρₛ = 0,51 |
| Erro tipo I com α = 5% (Pearson / Spearman) | S-base 5,0 / 4,8 · S-real 5,3 / 5,1 · n = 10: 6,5 / 5,2 · S-outlier 20,1 / 5,4 |
| Poder com ρ = 0,6 (Pearson / Spearman) | S-real 70 / 85 · n = 10: 38 / 33 · S-outlier 75 / 86 |
| Simulação | 4 situações × 7 efeitos × 10.000 réplicas, semente 42 |
