# Fonte dos dados reais — NASA KC1 (nível de classe)

## Origem

| Item | Valor |
|---|---|
| Dataset | KC1, dados por classe com contagem de defeitos (`kc1-class-level-numericdefect`) |
| Repositório | PROMISE Software Engineering Repository, disponível no OpenML como dataset **1070** (`kc1-numeric`) |
| URL do arquivo | <https://openml.org/data/v1/download/53953/kc1-numeric.arff> |
| SHA-256 do ARFF | `e83d22835bc98e4602acce372900c2d75bae0b52d073f6fa1f13984a64c0f9da` |
| Criador / doador | A. Güneş Koru (21/02/2005), a partir do NASA Metrics Data Program (MDP) |
| Sistema | Software da NASA de gerenciamento de armazenamento para recepção e processamento de dados de solo; descrito na literatura como escrito em C++ |
| Data da coleta | 31/10/2026 |

**Citação pedida pelo PROMISE:** Sayyad Shirabad, J. e Menzies, T. J. (2005). *The PROMISE Repository of
Software Engineering Databases*. School of Information Technology and Engineering, University of Ottawa, Canada.

**Uso original do dataset por classe:** Koru, A. G. e Liu, H. (2005). *An Investigation of the Effect of Module
Size on Defect Prediction Using Static Measures*. PROMISE Workshop, ICSE 2005.

## Como os dados foram coletados

O script [`src/data.py`](../src/data.py) (`uv run python -m data`) faz tudo:

1. Baixa o ARFF do OpenML, **só se** `data/real/kc1-numeric.arff` não existir, e confere o SHA-256.
   O arquivo original fica versionado no repositório, então o resultado não depende do OpenML estar no ar.
2. Extrai as duas colunas usadas e as renomeia.
3. Salva o dataset completo em `data/real/kc1_full.csv`.
4. Sorteia **30 classes sem reposição** com `numpy.random.default_rng(42)` (`SEED` em `src/config.py`)
   e salva em `data/real/kc1_sample30.csv`, ordenadas por `class_id`.

Rodar o script de novo gera exatamente os mesmos arquivos.

## Colunas

| Coluna no CSV | Coluna original | Tipo | Unidade | Descrição |
|---|---|---|---|---|
| `class_id` | — | inteiro | — | Posição da linha no ARFF original (0 a 144). O dataset não traz nome nem identificador de classe. |
| `loc` | `sumLOC_TOTAL` | inteiro | linhas de código | Total de linhas de código da classe: soma do `LOC_TOTAL` de todos os métodos da classe (a métrica é medida por método e agregada por classe no próprio dataset). |
| `defects` | `NUMDEFECTS` | inteiro | defeitos | Número de defeitos registrados para a classe. |

## Estatísticas descritivas

| | n | LOC: mediana (Q1–Q3) | LOC: máx. | LOC: assimetria | Defeitos: mediana (Q1–Q3) | Defeitos: máx. | Defeitos: assimetria | Classes sem defeito |
|---|---|---|---|---|---|---|---|---|
| Dataset completo | 145 | 162 (44–315) | 2.883 | 3,40 | 0 (0–4) | 101 | 5,53 | 85 (59%) |
| Amostra (seed 42) | 30 | 214 (130–322) | 2.883 | 2,66 | 0 (0–6) | 101 | 3,85 | 19 (63%) |

As duas variáveis são muito assimétricas à direita, e mais da metade das classes não tem defeito
(muitos empates em zero). A amostra sorteada inclui a maior classe (2.883 LOC) e a classe com mais
defeitos (101), que são exatamente os valores extremos que podem afetar mais o Pearson do que o Spearman.

## Limitações

- **Dados antigos:** o dataset é de 2005, com dados do NASA MDP do início dos anos 2000.
- **Qualidade dos dados da NASA:** há críticas conhecidas a esses datasets, como registros duplicados e
  inconsistentes (Shepperd, Song, Sun e Mair, 2013, *Data Quality: Some Comments on the NASA Software
  Defect Datasets*, IEEE TSE).
- **Duplicatas:** 4 pares de linhas são idênticos nas 95 colunas do ARFF (classes de 3, 5, 6 e 10 LOC,
  `class_id` 21/117, 58/140, 38/136 e 22/118). Como é plausível que sejam classes triviais distintas, o grupo
  **manteve as 145 linhas**. Duas delas (117 e 140) caíram na amostra.
- **LOC agregado:** o LOC da classe é a soma do LOC dos métodos, então não conta linhas fora de métodos
  (declarações de atributos, por exemplo).
- **Linguagem:** o C++ vem de descrições na literatura que usa o KC1; nem o ARFF nem o OpenML informam a linguagem.
- **Uso no lab:** os dados reais servem para calibrar a simulação e para a aplicação final dos testes;
  as conclusões sobre erro tipo I e poder vêm da simulação.
