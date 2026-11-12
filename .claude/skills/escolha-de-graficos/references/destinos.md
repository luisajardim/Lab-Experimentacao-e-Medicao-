# Destino: onde o gráfico vai aparecer

## Artigo científico (SBC, IEEE, ACM)

- **Largura:** coluna única (~8 cm em duas colunas) ou a página inteira (`figure*`). Desenhe já no tamanho final, para a fonte não encolher.
- **Fonte:** ao menos 7 a 8 pt no tamanho final, igual à do texto sempre que possível.
- **Preto e branco:** artigos costumam ser impressos. Diferencie por padrão (hachura, marcador, tracejado) e por luminosidade, não só por cor.
- **Vetorial:** PDF ou SVG para linhas e texto nítidos; PNG a 300 dpi só para imagens raster.
- **Legenda curta;** a explicação e a interpretação ficam no texto, e o texto cita a figura antes dela.
- **Crédito:** "Fonte: elaborada pelos autores" ou a origem dos dados.
- **Não repita no texto** os números que a figura ou a tabela já mostram.
- **Tabela ou gráfico?** Tabela quando o leitor precisa de valores exatos; gráfico quando precisa ver padrão, tendência ou distribuição.
- **LaTeX:** TikZ ou pgfplots mantêm a fonte do documento e permitem versionar a figura no `.tex`; matplotlib com `pgf` ou PDF serve quando os dados são grandes.

## Slides

- **Uma mensagem por slide.** O título afirma o achado ("A revisão não reduz o acoplamento"), não descreve o gráfico ("Gráfico de razão de chances").
- **Fonte grande** (18 pt ou mais), poucos elementos, destaque o que importa e deixe o resto em cinza.
- **Rotule direto** nas barras e linhas; legendas distantes não funcionam em sala.
- **Revele em etapas** se o gráfico for denso.

## Dashboard

- **Leitura em segundos:** KPIs no topo, gráficos de tendência e distribuição embaixo.
- **Mesma escala e cores com o mesmo significado** em todos os gráficos.
- **Mostre meta e variação** ao lado do número; sparkline em KPIs.
- **Filtros** com padrão sensato; não faça o usuário configurar para ver algo útil.
- **Data da última atualização** visível.

## Exploração (notebook)

- Vários gráficos rápidos são bons; só rotule bem o que for sair do notebook.
- Comece pela distribuição de cada variável, depois pares, depois grupos.

## Acessibilidade (todos os destinos)

- Contraste suficiente; evite vermelho × verde como único contraste.
- Use paletas seguras para daltonismo (viridis, cividis; Okabe-Ito para categorias).
- Redundância: cor + forma ou rótulo.
- Texto alternativo ou descrição da figura quando o destino permitir.
