# samtools/samtools

Repositório: https://github.com/samtools/samtools

## Metadados

- Linguagem: C

## Releases sorteadas

### Release 1

Link: https://github.com/samtools/samtools/releases/tag/1.12
- Tag: `1.12`
- Nome: 1.12
- Publicada em: 2021-03-17
- Release anterior (cronológica): `1.11`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/samtools/samtools/releases/tag/1.13
- Tag: `1.13`
- Nome: 1.13
- Publicada em: 2021-07-09
- Release anterior (cronológica): `1.12`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 3

Link: https://github.com/samtools/samtools/releases/tag/1.16
- Tag: `1.16`
- Nome: 1.16
- Publicada em: 2022-08-18
- Release anterior (cronológica): `1.15.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 4

Link: https://github.com/samtools/samtools/releases/tag/1.19
- Tag: `1.19`
- Nome: 1.19
- Publicada em: 2023-12-12
- Release anterior (cronológica): `1.18`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 5

Link: https://github.com/samtools/samtools/releases/tag/1.22.3
- Tag: `1.22.3`
- Nome: 1.22.3
- Publicada em: 2026-07-10
- Release anterior (cronológica): `1.21.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 69

-  Refactor the bam_sort_core_ext function
-  Extend samtools sort -M to distinguish between mapped and unmapped files
-  Correct the example for 1:1 consensus coords
-  Improve htslib#PRnum support for Cirrus-CI and GitHub Actions
-  View: add --save-counts option
-  Change how markdup looks for single reads. (#2119)
-  Fix samtools merge crash on BAM files with malformed headers
-  Documents the fastq* options used in htslib's hts.c and sam.c
-  tview: add -i to hide inserts
-  faidx/fqidx indexes along with output creation, uncompressed output through bgzf
-  Tidy up the faidx --write-index code.
-  Further fqidx --write-index updates post review
-  bedcov header from bed-file
-  review updates
-  Clarify consensus -@N speed expectations.
-  fix to use proper offset in faidx allocidx
-  Fix samtools fastq -i to force CRAM aux tag decoding.
-  Use MD/NM on CRAM for samtools consensus (#2156)
-  Fix various plot-bamstats issues in qual plots.
-  More plot-bamstats qual-hm improvements.
-  Add cigdup and cigarx options to samtools view -z sanitizer.
-  Add a "samtools checksum" command.  Needs htslib#1850
-  Address comments in review.
-  cat man page update
-  Add samtools consensus -T ref.fa functionality. (#2153)
-  Update samtools-merge.1 to include --template-coordinate (#2164)
-  Make reheader -h use /tmp and honour TMPDIR.
-  Fix depth counts when overlap removal is enabled
-  sets sort order as unsorted when ordering is lost during merge
-  Add a warning for samtools fastq on coordinate sorted data. (#2176)
-  Add multi-threading to samtools consensus. Needs htslib#1875
-  This fixes broken tests due to msys2 changes. (#2196)
-  stats update to correct checksum calculation for quality values
-  Allow the merge message to be silenced. (#2197)
-  Added clarification to sort type. (#2198)
-  Don't use consensus N for "*" calls that are of insufficient depth.
-  Added fish completion, renamed bash completion
-  Miscellaneous tidy ups (#2213)
-  Fix samtools checksum long options
-  Copyright updates for the Spring 2025 release. (PR #2209)
- ... e mais 29 commits
