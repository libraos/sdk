# Comparing Search Backends

A side-by-side comparison of the five `web_search_config` backends LibraOS supports. Public-source data only; vendor pricing changes — verify against each vendor's docs before committing to a budget.

## At a glance

| Option | Layer | Cost (per query) | Bundled extraction | Citations | Domain allow/block | Geo localization |
|---|---|---|---|---|---|---|
| `meganova` | SDK backend | 50/day free + $0.002/group overage | ✅ | ✗ (URLs returned, partner cites) | ✗ | ✗ |
| `tavily` | SDK backend | Paid tier with monthly free quota | ✅ | ✗ (URLs + snippets) | Per-call `include_domains` | ✗ |
| `brave` | SDK backend | Free tier + per-CPM paid | ✗ (keyword-only) | ✗ | ✗ | ✗ |
| `exa` | SDK backend | Paid per-query | ✗ (keyword + neural) | ✗ | ✗ | ✗ |
| `searxng` | SDK backend | Free (self-hosted) | ✗ | ✗ | ✗ | ✗ |

Verify exact pricing/limits on each vendor's docs:
- MegaNova — [docs.meganova.ai/api-reference/platform-api/search](https://docs.meganova.ai/api-reference/platform-api/search)
- Tavily — [docs.tavily.com](https://docs.tavily.com)
- Brave Search API — [api.search.brave.com](https://api.search.brave.com)
- Exa — [docs.exa.ai](https://docs.exa.ai)
- SearXNG — [docs.searxng.org](https://docs.searxng.org)

## Backends vs model-native search tools

Some model providers offer their own web search tool inside their API (Anthropic's web search tool is one). Those run at the provider, are tied to that provider's models, and are not configured through LibraOS. The backends above run inside LibraOS: you pin one per persona, control the fallback chain, and get the same search whichever model family the agent routes to.

## Bundled extraction vs keyword-only

A real-cost factor that the per-query price hides: whether the backend returns full page content or just URLs.

- **Bundled extraction** (`tavily`, `meganova`): one API call returns search + extracted page text. The deep-research skill consumes it directly.
- **Keyword-only** (`brave`, `exa`, `searxng`): the backend returns URLs and snippets; the partner / skill follows up with separate fetches via Firecrawl / crawl4ai / similar to get full page text.

If you're doing multi-aspect research with N hits per query, keyword-only multiplies your fetch cost: 1 search + N fetches at ~5-15 seconds and per-fetch fees, vs 1 search-with-extraction call. For partners on a tight latency or cost budget, prefer bundled-extraction backends.

## Latency expectations

| Option | P50 (verified) | Notes |
|---|---|---|
| `meganova` | 1-3s plain, 3-10s with `enrich=true` | P95 with `enrich`: ~15s |
| `tavily` | Sub-second to low single-digit | Vendor-published; varies with depth |
| `brave` | Sub-second | Keyword backend, fast |
| `exa` | Low single-digit | Neural ranking adds time |
| `searxng` | Variable | Aggregator latency = slowest underlying source |

`meganova`'s latency table is the only one with public P50/P95 numbers from a vendor doc — others are general industry expectations.

## Which to pick

```
Is cost the dominant constraint?
├── Yes, plus you're below $0.002/query budget → meganova (free tier first, $0.002 overage)
├── Yes, plus you can self-host → searxng
└── No → next question

Do you need bundled extraction (search + page text in one call)?
├── Yes → meganova or tavily
└── No → next question

Do you need privacy-first or no third-party dependency?
├── Yes → brave (privacy-first) or searxng (self-hosted)
└── No → next question

Is the workload technical / academic / paraphrased queries?
├── Yes → exa (neural ranking helps)
└── No → tavily (most reliable for current events)
```

## Two concrete partner patterns

### Cost-conscious general-purpose

```yaml
web_search_config:
  primary_backend: meganova   # 50/day free + $0.002/group overage; extraction included
  fallback_chain: [brave]     # cheap keyword fallback when MegaNova quota exhausts
  reformulator: true
```

Free tier covers low-volume tenants; overage is the cheapest paid extraction-included option in the table.

### Premium current-events

```yaml
web_search_config:
  primary_backend: tavily
  fallback_chain: [exa]       # exa for technical follow-ups
  reformulator: false         # tavily handles reformulation internally
```

Pay for Tavily on the freshness-dominant majority; fall through to Exa for the long tail.

## Caveats

- **Vendor pricing changes.** All numbers in this doc were captured at the time of writing. Verify against each vendor's docs before committing to a partner-tier price.
- **Per-query is not per-call.** Some backends bill "groups" (multi-aspect deep research counts as one); some bill per individual search. Read the vendor's billing-unit definition.
- **Free tiers are real but rate-limited.** Don't size capacity assuming the free tier scales — per-key concurrency caps usually kick in first.

## See also

- [`web-search.md`](web-search.md) — full reference for the SDK's `web_search_config`
- [`getting-started.md`](getting-started.md) — front-door + scenario matrix
