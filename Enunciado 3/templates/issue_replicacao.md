# Replicação cruzada: divergência / falha ao reproduzir resultados

## Comando executado

```bash
$command
```

## Mensagem de erro

```
$error
```

## Valores esperados vs. obtidos

- Repositórios em comum: $n_common (apenas no esperado: $n_only_a | apenas no obtido: $n_only_b)
- Tolerância relativa usada: $tolerance

### Classificação DORA

$category_summary

### Maiores divergências numéricas

| Repositório | Coluna | Esperado | Obtido | Dif. relativa |
|---|---|---|---|---|
$divergence_table

## Ambiente

- SO / versão do Python:
- Commit do repositório replicado:
- `config.toml` usado (alterações em relação ao original):

## Passos para reproduzir

1. 
2. 

> Relatório completo: anexar `diff_report.md` gerado por `python scripts/diff_datasets.py`.
