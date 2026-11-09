# Lab04 — Roteiro da apresentação oral

**Pearson × Spearman: o tamanho da classe está associado aos defeitos?**

**Grupo:** Bernardo Souza Alvim · Luísa Oliveira Jardim · Pedro Augusto Santos Seabra
**Disciplina:** Laboratório de Experimentação de Software · **Professor:** Danilo Maia
**Dashboard:** _link após o deploy (#93)_ · local: `uv run lab04`
**Repositório:** [Lab-Experimentacao-e-Medicao-](https://github.com/luisajardim/Lab-Experimentacao-e-Medicao-) · **Board:** [Kanban Lab](https://github.com/users/luisajardim/projects/2)

## Regras (enunciado §5)

- Até **7 minutos** no total → **~30 s por pergunta** (60 a 75 palavras faladas).
- Respondemos **usando o dashboard**: cada resposta diz em que seção/gráfico apontar.
- Cada integrante responde ≥ 4 perguntas, mas **o professor pode pedir qualquer pergunta a qualquer um**.
  Por isso, todos devem ler o roteiro inteiro, não só a própria parte.
- Antes de começar: dashboard aberto no topo, α = 0,05 selecionado, tela em tela cheia.

## Quadro geral

| # | Pergunta (resumo) | Quem | Mostrar no dashboard |
|---|---|---|---|
| 1 | Cenário, H₀ e H₁ | Bernardo | Topo (pergunta) + Seção 1 (hipóteses) |
| 2 | Unicaudal ou bicaudal | Bernardo | Seção 1 (direção) + G2 (duas faixas cinza) |
| 3 | Coleta dos dados reais e forma da distribuição | Bernardo | Seção 2 — G1 |
| 4 | Dados reais → parâmetros da simulação | Bernardo | Seção 1 (parâmetros) + G1 |
| 5 | O que cada teste compara | Luísa | Seção 3 — G2 |
| 6 | Distribuição da estatística sob H₀ e região de rejeição | Luísa | Seção 3 — G2 |
| 7 | O que o p-valor do exemplo significa (e não significa) | Luísa | Seção 3 — G2 + exemplo |
| 8 | Erro tipo I e tipo II no cenário | Pedro | Seção 1 / Seção 7 |
| 9 | G3: algum teste se afastou de 5%? | Luísa | Seção 4 — G3 |
| 10 | G4: qual teste tem mais poder? | Pedro | Seção 5 — G4 |
| 11 | Violação simulada e por que afeta mais um teste | Bernardo | Seção 1 (situações) + G3 + G4 |
| 12 | α = 0,01 no lugar de 0,05 | Pedro | Seletor de α no topo → G3 e G4 |
| 13 | A simulação confirmou o esperado? | Pedro | Seção 1 (expectativa) × Seção 7 |
| 14 | Dados reais: mesma conclusão? Efeito prático? | Luísa | Seção 6 |
| 15 | Recomendação, quando muda, principal limitação | Pedro | Seção 7 |

---

## 1. Qual é o cenário de vocês e o que H₀ e H₁ afirmam, em palavras simples?

**Quem:** Bernardo · **Mostrar:** a pergunta no topo do dashboard e a tabela de hipóteses da Seção 1.

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

**Quem:** Bernardo · **Mostrar:** a linha "Direção" na Seção 1 e, no G2, as **duas** faixas cinza.

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

**Quem:** Bernardo · **Mostrar:** Seção 2 — G1 (histogramas de LOC em escala log e de defeitos).

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

**Quem:** Bernardo · **Mostrar:** "Parâmetros ajustados no KC1" na Seção 1 e o G1 (simulado em roxo × real).

**Resposta (~30 s):**
> "Ajustamos as distribuições nas 145 classes. Para o LOC, testamos a lognormal, mas ela errava a mediana e exagerava
> a cauda; a Gamma não foi rejeitada pelo teste KS. Para os defeitos, usamos a binomial negativa, que reproduz os
> zeros: 57% simulados contra 59% reais. Uma cópula gaussiana liga as duas, e o tamanho do efeito vai até 0,6,
> perto do efeito observado. E a frequência da classe extrema virou a situação S-outlier."

**Números para lembrar:** LOC ~ Gamma(0,607; 487,9), KS p = 0,22 (lognormal: 0,001) · defeitos ~ BinNeg(r = 0,170;
média = 4,61), zeros 56,8% × 58,6% · grade de ρ latente 0 a 0,6 · S-outlier: 1 classe extrema em 145.

**Se o professor aprofundar:**
- *"Por que não usar só os 30?"* → Com 30 classes, os parâmetros ficam instáveis; as 145 dão um ajuste melhor, e a
  amostra de 30 fica para aplicar os testes (Seção 6).
- *"O que a cópula não reproduz?"* → Ela quase nunca gera um ponto dominante como a classe de 101 defeitos. Por isso
  criamos a S-outlier.

---

## 5. O que cada um dos dois testes compara de fato (médias, postos, proporções...)?

**Quem:** Luísa · **Mostrar:** Seção 3 — G2.

**Resposta (~30 s):** _a preencher por @luisajardim (#89)_

**Números para lembrar:** _a preencher_

**Se o professor aprofundar:** _a preencher_

---

## 6. No G2: o que é a distribuição da estatística sob H₀, e por que a região de rejeição fica onde fica?

**Quem:** Luísa · **Mostrar:** Seção 3 — G2 (curva t, histogramas sob H₀, faixas cinza).

**Resposta (~30 s):** _a preencher por @luisajardim (#89)_

**Números para lembrar:** _a preencher_

**Se o professor aprofundar:** _a preencher_

---

## 7. O que significa o p-valor do exemplo mostrado no G2? E o que ele não significa?

**Quem:** Luísa · **Mostrar:** Seção 3 — área colorida do G2 e o texto do exemplo logo abaixo.

**Resposta (~30 s):** _a preencher por @luisajardim (#89)_

**Números para lembrar:** _a preencher_

**Se o professor aprofundar:** _a preencher_

---

## 8. No cenário de vocês, o que seria um erro tipo I e um erro tipo II? Qual dos dois seria mais grave?

**Quem:** Pedro · **Mostrar:** Seção 1 (hipóteses) ou Seção 7.

**Resposta (~30 s):** _a preencher por @pedroseabra27 (#90)_

**Números para lembrar:** _a preencher_

**Se o professor aprofundar:** _a preencher_

---

## 9. No G3, algum teste se afastou de 5%? Ele ficou liberal ou conservador, e por quê?

**Quem:** Luísa · **Mostrar:** Seção 4 — G3 (linha em 5% e faixa de Monte Carlo).

**Resposta (~30 s):** _a preencher por @luisajardim (#89)_

**Números para lembrar:** _a preencher_

**Se o professor aprofundar:** _a preencher_

---

## 10. No G4, qual teste tem mais poder? A diferença entre eles muda conforme o tamanho do efeito?

**Quem:** Pedro · **Mostrar:** Seção 5 — G4.

**Resposta (~30 s):** _a preencher por @pedroseabra27 (#90)_

**Números para lembrar:** _a preencher_

**Se o professor aprofundar:** _a preencher_

---

## 11. Que violação de pressuposto vocês simularam, e por que ela afeta mais um teste do que o outro?

**Quem:** Bernardo · **Mostrar:** tabela de situações na Seção 1 → G3 (S-outlier) → G4.

**Resposta (~30 s):**
> "Simulamos três violações: dados assimétricos com muitos zeros, amostra pequena com 10 classes, e a S-outlier,
> em que de vez em quando aparece uma classe gigante com muitos defeitos. A que mais pesa é a S-outlier: sem
> efeito nenhum, o Pearson rejeita H₀ em 20% das vezes, contra 5% do Spearman. O Pearson usa os valores, então um
> único ponto extremo domina o cálculo; o Spearman usa postos, e esse ponto vira só o maior posto."

**Números para lembrar:** erro tipo I (ρ = 0, α = 0,05) — S-base 5,0% / 4,8% · S-real 5,3% / 5,1% · S-real-n10
**6,5%** / 5,2% · S-outlier **20,1%** / 5,4% (Pearson / Spearman).

**Se o professor aprofundar:**
- *"E com mais dados o problema some?"* → Não: na S-outlier, o erro tipo I do Pearson cresce com o n, de 11% com
  10 classes para 58% com 200 (bloco extra "Para discutir"). Mais classes, mais chances de uma classe extrema.
- *"E a amostra pequena?"* → Com 10 classes, o Pearson fica levemente liberal (6,5%), e o Spearman perde poder por
  causa dos empates: com ~57% de zeros, sobram poucos postos distintos.

---

## 12. Se vocês usassem α = 0,01 em vez de 0,05, o que mudaria no G3 e no G4?

**Quem:** Pedro · **Mostrar:** trocar o seletor de α no topo e mostrar o G3 e o G4 mudando.

**Resposta (~30 s):** _a preencher por @pedroseabra27 (#90)_

**Números para lembrar:** _a preencher_

**Se o professor aprofundar:** _a preencher_

---

## 13. A simulação confirmou o que o grupo esperava antes de simular? Se não, o que explica a diferença?

**Quem:** Pedro · **Mostrar:** "Expectativa registrada antes de simular" (Seção 1) × Seção 7.

**Resposta (~30 s):** _a preencher por @pedroseabra27 (#90)_

**Números para lembrar:** _a preencher_

**Se o professor aprofundar:** _a preencher_

---

## 14. Nos dados reais, os dois testes chegaram à mesma conclusão? O tamanho do efeito tem importância prática?

**Quem:** Luísa · **Mostrar:** Seção 6 — tabela dos dados reais.

**Resposta (~30 s):** _a preencher por @luisajardim (#89)_

**Números para lembrar:** _a preencher_

**Se o professor aprofundar:** _a preencher_

---

## 15. Qual teste vocês recomendam para o cenário, em que situação mudariam a recomendação, e qual é a principal limitação do estudo?

**Quem:** Pedro · **Mostrar:** Seção 7 — Conclusão.

**Resposta (~30 s):** _a preencher por @pedroseabra27 (#90)_

**Números para lembrar:** _a preencher_

**Se o professor aprofundar:** _a preencher_

---

## Cola: números-chave

| O quê | Valor |
|---|---|
| Dados reais | KC1 (NASA, C++), 145 classes; amostra de 30 com `SEED = 42` |
| Forma dos dados | LOC: mediana 162, máx. 2.883 · defeitos: 58,6% zeros, máx. 101 |
| Correlação no KC1 inteiro | r = 0,69 · ρₛ = 0,57 (sem a classe de 101 defeitos: r = 0,57 · ρₛ = 0,56) |
| Correlação na amostra de 30 | r = 0,84 · ρₛ = 0,515 |
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
