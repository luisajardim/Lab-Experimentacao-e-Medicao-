# cloudflare/vinext

Repositório: https://github.com/cloudflare/vinext

## Metadados

- Linguagem: TypeScript

## Releases sorteadas

### Release 1

Link: https://github.com/cloudflare/vinext/releases/tag/v0.0.45
- Tag: `v0.0.45`
- Nome: v0.0.45
- Publicada em: 2026-04-28
- Release anterior (cronológica): `v0.0.44`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 35

-  chore(deps): bump postcss from 8.5.3 to 8.5.10 (#889)
-  fix knip issues (#890)
-  try gpt 5.5 for bonk (#894)
-  try gpt 5.5 for bonk (#895)
-  bump opencode (#896)
-  switch bonk back to opus (#897)
-  Switch bonk and bigbonk workflows to GPT-5.5 xhigh variant (#898)
-  ci(opencode): register openai/gpt-5.5 under cloudflare-ai-gateway (#899)
-  ci(bonk): downgrade bots from gpt-5.5 to gpt-5.4 (#900)
-  ci(bonk): pin opencode to 1.4.6 to dodge cf-ai-gateway ProviderInitError (#902)
-  ci(bonk): bump opencode to 1.4.11 to unblock OAI through cf-ai-gateway (#903)
-  chore(ci): switch bonk back to opus 4.7 (#904)
-  port Next.js Google Fonts metadata + URL pipeline (PR 1 of 2 for #885) (#892)
-  Return leaf selected layout segment for named slots (#909)
-  fix(app-router): block javascript: URLs in router.push/replace/prefetch (#906)
-  Preserve middleware headers on app boundary responses (#908)
-  fix(dev): swallow socket errors so peer disconnects don't crash dev server (#911)
-  fix(app-router): surface Error.cause in dev-server error output (#912)
-  fix(dev): backstop uncaughtException for socket errors pipe() misses (#913)
-  fix(next/font/google): use real axis range, validate options at build time (#885) (#893)
-  fix(dev): hoist socket-error backstop to module top-level so lifecycle events can't remove it (#916)
-  fix(fonts): google fonts building perfectly (it was just a regex 😭) (#920)
-  Make revalidatePath expire route-scoped fetch cache reads (#917)
-  fix(app-router): action redirects (#910)
-  chore(ci): change bonk back to opus 4.6 (#934)
-  chore(ci): change bigbonk permissions prereq (#935)
-  chore(ci): change bonk perms back to normal (#936)
-  chore(ci): change bonk opencode version (#937)
-  fix: normalize NextRequest.url through nextUrl (#931)
-  fix(cache): scope use cache entries by build id (#924)
-  fix(router): ignore pre-root parallel slots for routed layouts (#927)
-  fix(app-router): keep ownerless URL commits from releasing snapshots (#930)
-  test(app-router): stabilize RSC fetch error redirects (#925)
-  fix(cache): serve stale unstable_cache entries (#932)
-  fix(app-router): restore hash anchors on history traversal (#929)

### Release 2

Link: https://github.com/cloudflare/vinext/releases/tag/%40vinext/cloudflare%400.1.2
- Tag: `@vinext/cloudflare@0.1.2`
- Nome: @vinext/cloudflare@0.1.2
- Publicada em: 2026-06-15
- Release anterior (cronológica): `@vinext/cloudflare@0.1.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 49

-  fix(pages-router): restore scroll across reload history traversal (#1905)
-  feat(web): expose latest compatibility failures (#1941)
-  fix(cache): honor fetch opt-outs and force-dynamic revalidate parity (#1907)
-  fix(shims): match next/error RSC diagnostic (#1939)
-  chore: standardize prod-build project commands in playwright.config.ts (#1932)
-  perf: cache fs probes and precompute route sort keys in scan/deploy paths (#1930)
-  fix(shims): add useUntrackedPathname hook for error boundary parity (#1933)
-  refactor(router): classify server-action results and RSC navigation errors in planner (#1901)
-  test(e2e): disable hash fixture query prefetch (#1948)
-  fix(css): load local CommonJS PostCSS plugins (#1961)
-  fix(router): hard navigate Pages links to App routes (#1960)
-  fix(app-router): preserve page notFound precedence during metadata failure (#1957)
-  fix(config): honor resolve extensions and improve webpack config processing (#1959)
-  fix(deploy): improve deployment id parity (#1949)
-  fix(config): share CommonJS module fallback (#1990)
-  fix(headers): prioritize config cache headers for metadata assets (#1953)
-  fix(link): preserve basePath hash navigation (#1952)
-  fix(app-router): support extensionless variable imports (#1958)
-  test(compat): classify runtime cli-output deploy suite (#1954)
-  fix(deploy): prevent Windows shell injection (#1946)
-  fix(actions): bound Flight payload graph validation (#1942)
-  fix(pages): harden cookie parsing (#1947)
-  fix(image): prevent optimizer cache-key amplification (#1944)
-  fix(app-router): fold typeof window before resolution (#1956)
-  perf: skip unnecessary import parsing (#1991)
-  fix(pages-router): block fallback shell for crawler UAs on prerender (#1543) (#1663)
-  chore: add codex to gitignore (#1992)
-  fix(build): honour experimental.lightningCssFeatures include/exclude (#1498) (#1664)
-  fix(deploy): preserve app module identity with deployment ids (#2005)
-  fix(app-router): expose active source page on window.next (#1995)
-  fix(pages-router): pass rewrite URL to edge API requests (#1998)
-  fix(app-router): preserve front redirects through fallback route handlers (#2000)
-  fix(router): restore pages scroll traversal state (#1999)
-  refactor(navigation): route prefetch reuse through planner (#1962)
-  fix(ppr): gate fallback shells until request-time resume is supported (#1716)
-  test(shims): normalize expected og shim path for Windows (#2006)
-  fix(router): share Pages Router context across chunks (#2010)
-  fix(routing): re-encode trailing-slash Location for non-Latin-1 paths (#2011)
-  fix(pages): preserve module identity with deployment ids (#2012)
-  fix(pages): preserve app props for GSSP requests (#1996)
- ... e mais 9 commits

### Release 3

Link: https://github.com/cloudflare/vinext/releases/tag/%40vinext/cloudflare%401.0.0-beta.9
- Tag: `@vinext/cloudflare@1.0.0-beta.9`
- Nome: @vinext/cloudflare@1.0.0-beta.9
- Publicada em: 2026-09-21
- Release anterior (cronológica): `vinext@1.0.0-beta.11`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(nenhum commit novo)_

### Release 4

Link: https://github.com/cloudflare/vinext/releases/tag/vinext%401.0.1
- Tag: `vinext@1.0.1`
- Nome: vinext@1.0.1
- Publicada em: 2026-10-01
- Release anterior (cronológica): `@cloudflare/workers-response-store@1.0.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(nenhum commit novo)_

### Release 5

Link: https://github.com/cloudflare/vinext/releases/tag/vinext%401.1.0
- Tag: `vinext@1.1.0`
- Nome: vinext@1.1.0
- Publicada em: 2026-10-08
- Release anterior (cronológica): `@vinext/cloudflare@1.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(nenhum commit novo)_
