# Lab04 — Roteiro da apresentação oral

**Pearson × Spearman: o tamanho da classe está associado aos defeitos?**

**Grupo:** Bernardo Souza Alvim · Luísa Oliveira Jardim · Pedro Augusto Santos Seabra
**Disciplina:** Laboratório de Experimentação de Software · **Professor:** Danilo Maia
**Dashboard:** <https://experimentacao-lab04-spearman.streamlit.app> (páginas **Dashboard** e **Relatório**, no menu do topo) · local: `uv run lab04`
**Repositório:** [Lab-Experimentacao-e-Medicao-](https://github.com/luisajardim/Lab-Experimentacao-e-Medicao-) · **Board:** [Kanban Lab](https://github.com/users/luisajardim/projects/2)

## Regras (enunciado §5)

- Até **7 minutos** no total → **~30 s por pergunta** (60 a 75 palavras faladas).
- Respondemos **usando o dashboard**: cada resposta diz em que gráfico ou indicador apontar. O painel só tem
  gráficos e rótulos; hipóteses, expectativa e recomendação são faladas (estão neste roteiro e em `docs/cenario.md`).
- Cada integrante responde ≥ 4 perguntas, mas **o professor pode pedir qualquer pergunta a qualquer um**.
  Por isso, todos devem ler o roteiro inteiro, não só a própria parte.
- Antes de começar: dashboard aberto no topo, α = 0,05 e as quatro situações selecionadas, tela em tela cheia.

## Quadro geral

| # | Pergunta (resumo) | Quem | Mostrar no dashboard |
|---|---|---|---|
| 1 | Cenário, H₀ e H₁ | Bernardo | Título + dispersão LOC × defeitos (falar as hipóteses) |
| 2 | Unicaudal ou bicaudal | Bernardo | G2 (duas faixas cinza) |
| 3 | Coleta dos dados reais e forma da distribuição | Bernardo | G1 + dispersão LOC × defeitos |
| 4 | Dados reais → parâmetros da simulação | Bernardo | G1 (simulado em roxo × real) |
| 5 | O que cada teste compara | Luísa | G2 |
| 6 | Distribuição da estatística sob H₀ e região de rejeição | Luísa | G2 |
| 7 | O que o p-valor do exemplo significa (e não significa) | Luísa | G2 (área colorida e t, p nos títulos dos painéis) |
| 8 | Erro tipo I e tipo II no cenário | Pedro | Indicadores de erro tipo I e de poder |
| 9 | G3: algum teste se afastou de 5%? | Luísa | G3 |
| 10 | G4: qual teste tem mais poder? | Pedro | G4 + mapa Spearman − Pearson |
| 11 | Violação simulada e por que afeta mais um teste | Bernardo | G3 (S-outlier) + G4 |
| 12 | α = 0,01 no lugar de 0,05 | Pedro | Filtro de α no topo → indicadores, G3, mapa e G4 |
| 13 | A simulação confirmou o esperado? | Pedro | Mapa Spearman − Pearson + G3 (falar a expectativa) |
| 14 | Dados reais: mesma conclusão? Efeito prático? | Luísa | Correlação com IC 95% + dispersão + indicadores r e ρₛ |
| 15 | Recomendação, quando muda, principal limitação | Pedro | Mapa Spearman − Pearson + indicadores |

---

## 1. Qual é o cenário de vocês e o que H₀ e H₁ afirmam, em palavras simples?

**Quem:** Bernardo · **Mostrar:** a dispersão LOC × defeitos (a classe de 2.883 LOC marcada); as hipóteses são faladas.

**Resposta (~30 s):**
> "Nosso cenário é um sistema C++ da NASA, o KC1. A pergunta é: classes maiores tendem a ter mais defeitos de
> modo geral, ou essa associação é puxada por poucas classes gigantes? A hipótese nula diz que o tamanho da
> classe, em linhas de código, não está associado ao número de defeitos. A alternativa diz que está associado.
> Comparar Pearson e Spearman responde à segunda parte: um olha os valores, o outro os postos."

**Números para lembrar:** KC1, 145 classes C++ · LOC × defeitos por classe · H₀: ρ = 0 · H₁: ρ ≠ 0.

**Se o professor aprofundar:**
- *"Por que essa pergunta?"* → No KC1 inteiro, uma única classe (2.883 LOC, 101 defeitos) sobe o r de 0,57 para
  0,69, enquanto o ρ de Spearman quase não muda (0,57 → 0,56). A pergunta nasceu dessa diferença.

---

## 2. O teste de vocês é unicaudal ou bicaudal? Por quê?

**Quem:** Bernardo · **Mostrar:** no G2, as **duas** faixas cinza ("Rejeita H₀" dos dois lados).

**Resposta (~30 s):**
> "Bicaudal. A gente espera que classes maiores tenham mais defeitos, mas preferiu não usar essa aposta no teste:
> o bicaudal é o padrão, é mais conservador e não depende de uma direção escolhida por nós. Na prática, a região
> de rejeição fica nas duas caudas, como mostram as duas faixas cinza do G2, e cada cauda recebe metade do α."

**Números para lembrar:** α = 0,05 → 2,5% em cada cauda · t crítico com 28 g.l. ≈ ±2,05.

**Se o professor aprofundar:**
- *"O unicaudal não teria mais poder?"* → Teria, porque toda a área de α fica de um lado. Mas só se justifica se a
  direção for decidida antes de olhar os dados e uma associação negativa não interessar; preferimos não assumir isso.

---

## 3. Como os dados reais foram coletados, e o que eles mostraram sobre a forma da distribuição?

**Quem:** Bernardo · **Mostrar:** G1 (histogramas de LOC em escala log e de defeitos) e a dispersão LOC × defeitos.

**Resposta (~30 s):**
> "Baixamos o dataset KC1 por classe do repositório PROMISE, pelo OpenML, com um script que confere o checksum do
> arquivo. Ele tem 145 classes; sorteamos 30 com semente fixa. As duas variáveis são muito assimétricas: a
> mediana é 162 linhas, mas a maior classe tem quase 2.900; e 59% das classes não têm nenhum defeito, enquanto uma
> chega a 101. Ou seja, nada de normal: cauda longa, outliers e muitos empates em zero."

**Números para lembrar:** OpenML 1070 · 145 classes → amostra de 30 (`SEED = 42`) · LOC: mediana 162, máx. 2.883,
assimetria 3,40 · defeitos: 58,6% zeros, máx. 101, assimetria 5,53.

**Se o professor aprofundar:**
- *"E a qualidade desses dados?"* → São de 2005 e há críticas conhecidas aos dados da NASA (Shepperd et al., 2013).
  Encontramos 4 pares de linhas duplicadas, de classes triviais, e mantivemos as 145, documentando em `docs/fonte_dados.md`.
- *"A amostra de 30 representa o KC1?"* → Ela pegou a maior classe e a com mais defeitos, então é até mais extrema.

---

## 4. Como os dados reais ajudaram a escolher os parâmetros da simulação?

**Quem:** Bernardo · **Mostrar:** o G1 (simulado em roxo × real); os parâmetros estão nos números abaixo.

**Resposta (~30 s):**
> "Ajustamos as distribuições nas 145 classes. Para o LOC, testamos a lognormal, mas ela errava a mediana e exagerava
> a cauda; a Gamma não foi rejeitada pelo teste KS. Para os defeitos, usamos a binomial negativa, que reproduz os
> zeros: 57% simulados contra 59% reais. Uma cópula gaussiana liga as duas, e o tamanho do efeito vai até 0,6,
> perto do efeito observado. E a frequência da classe extrema virou a situação S-outlier."

**Números para lembrar:** LOC ~ Gamma(0,607; 487,9), KS p = 0,22 (lognormal: 0,001) · defeitos ~ BinNeg(r = 0,170;
média = 4,61), zeros 56,8% × 58,6% · grade de ρ latente 0 a 0,6 · S-outlier: 1 classe extrema em 145.

**Se o professor aprofundar:**
- *"Por que não usar só os 30?"* → Com 30 classes, os parâmetros ficam instáveis; as 145 dão um ajuste melhor, e a
  amostra de 30 fica para aplicar os testes (gráfico de correlação com IC 95%).
- *"O que a cópula não reproduz?"* → Ela quase nunca gera um ponto dominante como a classe de 101 defeitos. Por isso
  criamos a S-outlier.

---

## 5. O que cada um dos dois testes compara de fato (médias, postos, proporções...)?

**Quem:** Luísa · **Mostrar:** G2 (os dois painéis, Pearson e Spearman).

**Resposta (~30 s):**
> "Nenhum dos dois compara médias nem proporções: os dois medem associação entre LOC e defeitos. O Pearson
> usa os **valores**: mede relação linear, e uma classe gigante pesa muito. O Spearman usa os **postos**: mede
> se uma variável sobe quando a outra sobe, e cada classe pesa igual. Os dois transformam o coeficiente na mesma
> estatística t e a comparam com a t de n − 2 graus de liberdade."

**Números para lembrar:** t = r·√((n−2)/(1−r²)) · com n = 30, 28 g.l. · empates recebem o posto médio · na
amostra real, r = 0,84 × ρₛ = 0,51: a diferença vem quase toda de uma classe.

**Se o professor aprofundar:**
- *"O que são os postos?"* → A posição de cada classe quando ordenamos por LOC (1 = menor) e por defeitos. As 19
  classes da amostra sem defeito empatam e recebem todas o mesmo posto médio.
- *"O Spearman é não paramétrico, então não tem pressuposto?"* → Ele não supõe normalidade, mas o p-valor pela t
  é uma aproximação da distribuição exata dos postos; com n = 10 essa aproximação piora (pergunta 9).
- *"Implementaram ou usaram o SciPy?"* → Implementamos em lote (10.000 réplicas de uma vez) e conferimos linha a
  linha contra `scipy.stats.pearsonr` e `spearmanr`.

---

## 6. No G2: o que é a distribuição da estatística sob H₀, e por que a região de rejeição fica onde fica?

**Quem:** Luísa · **Mostrar:** G2 (curva t, histogramas sob H₀, faixas cinza).

**Resposta (~30 s):**
> "É o que a estatística t valeria se não houvesse associação. A curva escura é a teoria, a t com 28 graus de
> liberdade; os histogramas são 10.000 amostras simuladas sem efeito. A rejeição fica nas duas caudas, onde
> estão os t raros sob H₀, porque o teste é bicaudal: com α de 5%, |t| acima de 2,05. O Spearman segue a curva;
> o Pearson é assimétrico, com a cauda direita longa."

**Números para lembrar:** t crítico ±2,05 (α = 0,05) ou ±2,76 (α = 0,01) · nula simulada: S-real, ρ = 0,
10.000 réplicas · Pearson: assimetria +1,55, rejeita 5,3% na cauda direita e 0,2% na esquerda · Spearman:
assimetria ≈ 0, 2,5% e 2,7%.

**Se o professor aprofundar:**
- *"Por que o Pearson fica assimétrico?"* → Com LOC e defeitos assimétricos, quando uma classe grande calha de ter
  muitos defeitos, o r sobe bastante; o contrário quase não acontece. Conferimos com uma nula por permutação e com
  dados normais (S-base), em que ele fica simétrico.
- *"Então a curva t está errada para o Pearson?"* → É só uma aproximação nesses dados: o total de rejeições ainda
  fica perto de 5%, mas quase todas de um lado. Isso aparece de novo no G3.
- *"De onde vem o 2,05?"* → É o quantil 97,5% da t com 28 g.l.: deixa 2,5% de área em cada cauda.

---

## 7. O que significa o p-valor do exemplo mostrado no G2? E o que ele não significa?

**Quem:** Luísa · **Mostrar:** a área colorida do G2 e o t e o p do exemplo no título de cada painel.

**Resposta (~30 s):**
> "O exemplo é uma amostra da S-real com efeito 0,3. O p-valor é a área colorida: a chance de um t tão ou mais
> extremo que o nosso **se H₀ fosse verdadeira**. O Pearson deu 0,55 e o Spearman 0,13: nenhum rejeita, mas o
> efeito existe, então os dois cometem erro tipo II. O p-valor não é a probabilidade de H₀ ser verdadeira, não
> mede o tamanho do efeito, e um p grande não prova que não há associação."

**Números para lembrar:** exemplo: S-real, ρ latente = 0,3, n = 30, semente 42 · Pearson r = 0,11, t = 0,61,
p = 0,548 · Spearman ρₛ = 0,28, t = 1,54, p = 0,134 · nesse efeito, cada teste só rejeita em ~25% das amostras
(25,0% / 27,1%).

**Se o professor aprofundar:**
- *"Por que mostrar um exemplo que não rejeita?"* → Não escolhemos o resultado: o efeito e a semente foram fixados
  antes. E ele é o caso típico: com ρ = 0,3 e 30 classes, não rejeitar acontece em ~75% das amostras.
- *"Então o p = 0,13 do Spearman é 'quase significativo'?"* → Não usamos esse termo: com α = 0,05, não rejeita. O
  p-valor menor só diz que o t dele ficou mais longe do centro.
- *"Uma amostra diz qual teste é melhor?"* → Não; isso vem da taxa de rejeição em muitas réplicas (G3 e G4).

---

## 8. No cenário de vocês, o que seria um erro tipo I e um erro tipo II? Qual dos dois seria mais grave?

**Quem:** Pedro · **Mostrar:** os indicadores de erro tipo I (S-outlier) e de poder (S-real) no topo.

**Resposta (~30 s):**
> "Erro tipo I seria concluir que o tamanho da classe está associado aos defeitos quando não está: o
> time passaria a concentrar revisão e testes nas classes grandes por causa de uma regra falsa, e as
> pequenas com defeito ficariam sem atenção. Erro tipo II seria não detectar uma associação que existe, e
> perder um sinal barato para priorizar testes. Para nós o tipo I é mais grave: é justamente o erro que uma
> única classe gigante provoca no Pearson, e ele muda onde o esforço de qualidade é gasto."

**Números para lembrar:** α = 0,05 controla o tipo I · na S-outlier o Pearson comete tipo I em **20,1%** das amostras (Spearman 5,4%) · tipo II = 1 − poder: na S-real com ρ = 0,6, o Pearson erra em 30% e o Spearman em 15%.

**Se o professor aprofundar:**
- *"Mas a NASA não preferiria nunca perder defeitos?"* → Se a decisão fosse testar menos as classes
  pequenas, o tipo II pesaria mais. Mas o teste é sobre a relação tamanho × defeitos, não sobre achar
  defeitos; uma regra falsa (tipo I) desvia recursos de forma sistemática.
- *"Como reduzir o tipo II sem aumentar o tipo I?"* → Mais classes na amostra ou um teste com mais poder
  para esse tipo de dado (o Spearman, na S-real).

---

## 9. No G3, algum teste se afastou de 5%? Ele ficou liberal ou conservador, e por quê?

**Quem:** Luísa · **Mostrar:** G3 (linha em 5% e faixa de Monte Carlo; valores no hover).

**Resposta (~30 s):**
> "O Spearman ficou dentro da faixa cinza, perto de 5%, nas quatro situações. O Pearson se afastou em duas e
> ficou liberal: 6,5% com 10 classes e 20% na S-outlier. Liberal quer dizer que ele rejeita H₀ verdadeira mais
> do que deveria. O motivo é o que vimos no G2: com dados assimétricos, a distribuição do Pearson tem a cauda
> direita longa, e quase todas as rejeições caem desse lado. Nenhum teste ficou conservador."

**Números para lembrar (α = 0,05, Pearson / Spearman):** faixa de Monte Carlo 4,57% a 5,43% (5% ± 0,43 pp, 10.000
réplicas) · S-base 4,98 / 4,82% · S-real 5,27 / 5,07% · S-real-n10 **6,51** / 5,16% · S-outlier **20,14** / 5,37% ·
na S-real-n10, o Pearson rejeita 6,34% à direita e 0,17% à esquerda.

**Se o professor aprofundar:**
- *"E com α = 0,01?"* → O Pearson também fica liberal na S-real (2,32% contra 1%), e o Spearman sai um pouco da
  faixa com 10 classes (1,35%), mas sem desequilíbrio entre as caudas.
- *"Na S-outlier é mesmo erro tipo I?"* → Não no sentido estrito: as classes extremas criam um r populacional de
  0,18 (ρₛ = 0,02), então não há relação entre as classes comuns, mas há nos valores. O Pearson rejeita em 86% das
  amostras que recebem uma classe extrema, contra 4,8% nas outras (o nível nominal): é exatamente o fenômeno da
  nossa pergunta.
- *"Como sabem que 5,27% é 'perto'?"* → Com 10.000 réplicas, o erro de Monte Carlo é ±0,43 pp; tudo dentro dessa
  faixa não se distingue de 5%.

---

## 10. No G4, qual teste tem mais poder? A diferença entre eles muda conforme o tamanho do efeito?

**Quem:** Pedro · **Mostrar:** G4 e o mapa Spearman − Pearson (verde: Spearman rejeita mais; laranja: Pearson).

**Resposta (~30 s):**
> "Depende dos dados. Na S-base, com dados normais, o Pearson tem um pouco mais de poder em todos os
> efeitos, como a teoria prevê. Nos dados com a forma do KC1, a vantagem troca de lado a partir de ρ ≈ 0,3,
> e com ρ = 0,6 o Spearman detecta 85% contra 70%. Com 10 classes os dois ficam abaixo de 40%. Na
> S-outlier, a curva do Pearson já começa em 20% com ρ = 0: isso não é poder, são rejeições falsas."

**Números para lembrar (α = 0,05, Pearson / Spearman):** S-base ρ = 0,4: 62,0 / 55,3% · S-real ρ = 0,3: 25,0 / 27,1% e ρ = 0,6: 69,8 / 84,5% · S-real-n10 ρ = 0,6: 38,3 / 33,1% · S-outlier ρ = 0: 20,1 / 5,4% e ρ = 0,6: 75,4 / 85,9%.

**Se o professor aprofundar:**
- *"O eixo x não favorece um dos testes?"* → O eixo é o ρ latente da cópula, o mesmo para os dois. No hover
  de cada ponto mostramos o r e o ρₛ populacionais: na S-real com ρ = 0,6, r = 0,47 e ρₛ = 0,52. Nesses
  dados a associação monotônica é mais forte que a linear, e o Spearman mede exatamente ela.
- *"E na amostra pequena o Pearson ganha?"* → Só na aparência: com ρ = 0 ele já rejeita 6,5% (acima de
  5%), então parte do poder é erro tipo I inflado. O Spearman sofre com os empates em zero.
- *"As barras nos pontos?"* → ±1,96 erro padrão de Monte Carlo (10.000 réplicas por ponto).

---

## 11. Que violação de pressuposto vocês simularam, e por que ela afeta mais um teste do que o outro?

**Quem:** Bernardo · **Mostrar:** G3 (S-outlier, ponto do Pearson fora da escala) → G4 (S-outlier).

**Resposta (~30 s):**
> "Simulamos três violações: dados assimétricos com muitos zeros, amostra pequena com 10 classes, e a S-outlier,
> em que de vez em quando aparece uma classe gigante com muitos defeitos. A que mais pesa é a S-outlier: sem
> efeito nenhum, o Pearson rejeita H₀ em 20% das vezes, contra 5% do Spearman. O Pearson usa os valores, então um
> único ponto extremo domina o cálculo; o Spearman usa postos, e esse ponto vira só o maior posto."

**Números para lembrar:** erro tipo I (ρ = 0, α = 0,05) — S-base 5,0% / 4,8% · S-real 5,3% / 5,1% · S-real-n10
**6,5%** / 5,2% · S-outlier **20,1%** / 5,4% (Pearson / Spearman).

**Se o professor aprofundar:**
- *"E com mais dados o problema some?"* → Não: na S-outlier, o erro tipo I do Pearson cresce com o n, de 11% com
  10 classes para 58% com 200 (último gráfico: poder e erro tipo I × tamanho da amostra). Mais classes, mais chances de uma classe extrema.
- *"E a amostra pequena?"* → Com 10 classes, o Pearson fica levemente liberal (6,5%), e o Spearman perde poder por
  causa dos empates: com ~57% de zeros, sobram poucos postos distintos.

---

## 12. Se vocês usassem α = 0,01 em vez de 0,05, o que mudaria no G3 e no G4?

**Quem:** Pedro · **Mostrar:** trocar o filtro de α no topo e mostrar os indicadores, o G3 e o G4 mudando.

**Resposta (~30 s):** *(trocar o filtro para 0,01 enquanto fala)*
> "No G3, a linha de referência desce para 1% e todas as taxas caem. O Spearman fica perto de 1% em todas
> as situações, mas o Pearson fica proporcionalmente mais liberal: 2,3% na S-real, mais que o dobro do
> nominal, e 15% na S-outlier. No G4, todas as curvas descem: menos falsos positivos custam poder. Na
> S-real com ρ = 0,6, o Spearman cai de 85% para 65% e o Pearson de 70% para 53%."

**Números para lembrar (α = 0,01, Pearson / Spearman):** erro tipo I — S-base 0,9 / 1,1% · S-real **2,3** / 1,1% · S-real-n10 **3,1** / 1,4% · S-outlier **15,4** / 1,1% · poder ρ = 0,6 — S-base 85,8 / 79,0% · S-real 53,2 / 65,0% · S-real-n10 24,4 / 13,7%.

**Se o professor aprofundar:**
- *"Por que o Pearson piora relativamente com α menor?"* → α = 0,01 olha mais longe na cauda da
  distribuição de t, e é justamente a cauda que as classes gigantes deformam (a cauda direita longa
  do Pearson no G2). A aproximação pela t vale perto do centro e falha nos extremos.
- *"E o ponto de troca no G4?"* → Na S-real ele vai de ρ ≈ 0,3 para ρ ≈ 0,5.
- *"Precisou re-simular?"* → Não: salvamos todos os p-valores, então trocar α é só mudar o limiar.

---

## 13. A simulação confirmou o que o grupo esperava antes de simular? Se não, o que explica a diferença?

**Quem:** Pedro · **Mostrar:** o mapa Spearman − Pearson (S-base laranja, S-real verde, S-real-n10 laranja) e o G3; a expectativa é falada.

**Resposta (~30 s):**
> "Em grande parte, sim. Acertamos que o Pearson teria um pouco mais de poder com dados normais e que o
> Spearman ganharia nos dados com a forma do KC1. Erramos com 10 classes: esperávamos vantagem do
> Spearman, mas o Pearson rejeitou mais. Isso tem duas causas: com ~57% de zeros, numa amostra de 10
> sobram poucos postos distintos para o Spearman, e o Pearson ficou liberal, rejeitando 6,5% sem efeito
> nenhum, então parte do 'poder' dele é falso."

**Números para lembrar:** expectativa registrada em 31/10 (`docs/cenario.md`) · S-base ρ = 0,4: 62,0 / 55,3% (confirmou) · S-real ρ = 0,6: 69,8 / 84,5% (confirmou) · S-real-n10 ρ = 0,6: 38,3 / 33,1% e erro tipo I 6,5 / 5,2% (não confirmou) · a S-outlier ficou fora da comparação porque foi criada depois da análise exploratória.

**Se o professor aprofundar:**
- *"E o erro tipo I, também bateu?"* → Para o Spearman, sim, em todas as situações. Para o Pearson, não
  com n = 10: 6,5% está fora da faixa de Monte Carlo (5% ± 0,43 pp). Esperávamos que, com X e Y
  independentes, a t continuasse valendo; com dados tão assimétricos e n pequeno, não vale.
- *"Por que a S-outlier não entrou?"* → Porque já tínhamos visto o resultado dela antes de registrar a
  expectativa; incluí-la seria "prever" algo já conhecido.

---

## 14. Nos dados reais, os dois testes chegaram à mesma conclusão? O tamanho do efeito tem importância prática?

**Quem:** Luísa · **Mostrar:** o gráfico de correlação com IC 95% (os círculos vazios são sem a classe gigante), a dispersão e os indicadores r e ρₛ.

**Resposta (~30 s):**
> "Sim: os dois rejeitam H₀, com α de 5% ou de 1%. Mas o tamanho difere: r = 0,84 e ρₛ = 0,51. O r é inflado
> por uma classe de 2.883 linhas e 101 defeitos; sem ela, cai para 0,58. Confiamos no Spearman: efeito grande,
> mas com IC de 0,18 a 0,75, ainda incerto. Na prática, a metade maior das classes concentra 93% dos defeitos:
> vale priorizar a revisão nelas."

**Números para lembrar:** Pearson r = 0,84, t = 8,27, p < 0,001, IC Fisher [0,69; 0,92] · Spearman ρₛ = 0,51,
t = 3,18, p = 0,004, IC bootstrap [0,18; 0,75] · sem a classe gigante: r = 0,58, ρₛ = 0,45 · metade maior: 93% dos
defeitos (44% vêm só da classe gigante), 53% com algum defeito × 20% na metade menor.

**Se o professor aprofundar:**
- *"Por que o IC do r é tão mais estreito?"* → O IC de Fisher supõe dados normais, o que não vale aqui. Um bootstrap
  do próprio r dá [0,17; 0,99]: a incerteza real é bem maior do que o Fisher mostra.
- *"Então LOC prevê defeitos?"* → Serve para priorizar, não para decidir caso a caso: 47% das classes da metade
  maior não têm defeito nenhum.
- *"Esse resultado vale para o KC1 inteiro?"* → É coerente: no KC1 inteiro, r = 0,69 e ρₛ = 0,57, e de novo uma
  única classe sobe o r.

---

## 15. Qual teste vocês recomendam para o cenário, em que situação mudariam a recomendação, e qual é a principal limitação do estudo?

**Quem:** Pedro · **Mostrar:** o mapa Spearman − Pearson e os indicadores de erro tipo I e de poder.

**Resposta (~30 s):**
> "Recomendamos o Spearman: ele mantém o erro tipo I perto de 5% em todas as situações e tem mais poder
> nos dados realistas. Mudaríamos para o Pearson se os dados fossem quase normais e sem classes extremas,
> ou se a pergunta fosse sobre a relação linear nos valores, como prever defeitos a cada 100 LOC. A
> principal limitação é que tudo depende do gerador: a S-outlier se apoia numa única classe real do KC1,
> e os dados da NASA são antigos e têm problemas de qualidade conhecidos."

**Números para lembrar:** S-real ρ = 0,6: Spearman 84,5% × Pearson 69,8% · S-outlier ρ = 0: Pearson 20,1% de falsos positivos × Spearman 5,4% · com n = 10, poder < 40% para os dois · amostra real: r = 0,84 × ρₛ = 0,515 (o r é puxado pela classe de 101 defeitos).

**Se o professor aprofundar:**
- *"Então a resposta à pergunta de pesquisa é?"* → Há uma tendência geral (o Spearman a detecta na
  maioria das amostras), mas a força que o Pearson mostra é inflada por poucas classes gigantes.
- *"E com amostras pequenas?"* → Nenhum dos dois é confiável; o melhor é coletar mais classes (último
  gráfico, tamanho da amostra: n ≈ 28 para 80% de poder com o Spearman, ≈ 43 com o Pearson).
- *"Outras limitações?"* → LOC da classe é a soma do LOC dos métodos, e a cópula gaussiana não tem
  dependência extra nas caudas.

---

## Cola: números-chave

| O quê | Valor |
|---|---|
| Dados reais | KC1 (NASA, C++), 145 classes; amostra de 30 com `SEED = 42` |
| Forma dos dados | LOC: mediana 162, máx. 2.883 · defeitos: 58,6% zeros, máx. 101 |
| Correlação no KC1 inteiro | r = 0,69 · ρₛ = 0,57 (sem a classe de 101 defeitos: r = 0,57 · ρₛ = 0,56) |
| Correlação na amostra de 30 | r = 0,84 [0,69; 0,92] · ρₛ = 0,515 [0,18; 0,75] (sem a classe gigante: r = 0,58 · ρₛ = 0,45) |
| Exemplo do G2 (S-real, ρ = 0,3) | r = 0,11 (p = 0,548) · ρₛ = 0,28 (p = 0,134): nenhum rejeita, erro tipo II |
| t crítico (28 g.l.) | ±2,05 (α = 0,05) · ±2,76 (α = 0,01) |
| Ajuste | LOC ~ Gamma(0,607; 487,9) · defeitos ~ BinNeg(r = 0,170; média = 4,61) |
| Simulação | 4 situações × 7 efeitos (ρ latente 0 a 0,6) × 10.000 réplicas |
| Erro tipo I (Pearson / Spearman) | S-base 5,0 / 4,8% · S-real 5,3 / 5,1% · S-real-n10 6,5 / 5,2% · S-outlier 20,1 / 5,4% |
| Poder com ρ latente = 0,6 (Pearson / Spearman) | S-real 69,8 / 84,5% · S-real-n10 38,3 / 33,1% · S-outlier 75,4 / 85,9% |
| Tamanho da amostra (efeito observado, S-real) | poder com n = 30: 69% / 85% · n para 80%: ~43 / ~28 |

## Ensaio cronometrado

- [ ] Dashboard aberto e testado na máquina da apresentação (ou URL pública funcionando, #93)
- [ ] Ensaio completo das 15 perguntas em até 7 minutos (data: ____ · tempo: ____)
- [ ] Cada integrante respondeu pelo menos 2 perguntas de outro colega no ensaio
- [ ] Números da cola conferidos com o dashboard final
