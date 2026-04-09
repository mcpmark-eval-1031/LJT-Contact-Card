# Source Priority Policy — `finalpool-personal-website-construct_10`

## Workflow Context

Repository: **`mcpmark-eval-1031/LUFFY`**  
Task: Reconstruct the reviewed change set for the personal website construction workflow (finalpool, trial 10).  
Subject pair: `bugmaker00/My-Homepage` (fork destination) ← `academicpages/academicpages.github.io` (upstream template)  
Review branch: `review/personal-website-construct-finalpool`  
Prior review branch: `review/personal-website-construct-pair-1` (snapshot 2026-04-08)  
Current snapshot date: 2026-04-09

---

## Source Catalogue

| Priority | Source ID | Description |
|----------|-----------|-------------|
| **1** | `github_api_live` | Live GitHub REST API `/repos/bugmaker00/My-Homepage` snapshot taken at task time (pushed_at: 2026-04-09T00:18:30Z). Reflects the actual current state of the fork destination. The destination has `size: 0`, `fork: false`, indicating a bootstrap failure — template content was never propagated. |
| **2** | `github_api_live_upstream` | Live GitHub REST API `/repos/academicpages/academicpages.github.io` snapshot at task time (last push: 2026-04-08T17:19:38Z). Provides authoritative template field values: `description`, `language`, `topics`, `homepage`, `size`, `is_template`. Used as fallback when the destination has empty or failure-marker values. |
| **3** | `readme_opening_upstream` | Opening sentence of `academicpages/academicpages.github.io` `README.md` on `master` at the same snapshot. Used for description-type fields when the API field requires corroboration or when both `github_api_live` and `github_api_live_upstream` are ambiguous. |
| **4** | `review_analysis` | Analytical conclusions committed in `review/personal-website-construct-pair-1` (files: `review_table_pair_1.csv`, `decision_summary_pair_1.md`). Used only for derived meta-fields with no direct API equivalent (e.g. `scope_decision`). |

---

## Priority Ordering

**General rule** (highest → lowest):

```
github_api_live  >  github_api_live_upstream  >  readme_opening_upstream  >  review_analysis
```

**Bootstrap-failure exception:**

The destination repository `bugmaker00/My-Homepage` has `size: 0` and `fork: false`, confirming the template instantiation failed to bootstrap (no template content was propagated). When `github_api_live` returns an empty, null, or failure-marker value for a field because of this bootstrap failure, that source is treated as below-threshold and the next non-empty source in the priority chain wins.

Fields affected by this exception: `description`, `upstream_template_identity`, `language`, `homepage`, `topics`, `size`.

**Unconditional `github_api_live` wins (no exception):**  
`canonical_owner_repo` and `bootstrap_status` always use `github_api_live` — the destination's actual namespace and actual failure state are never overridden by the upstream template.

---

## Per-Field Source Decisions

| Field | Winning Source | Rationale |
|-------|----------------|-----------|
| `bootstrap_status` | `github_api_live` | Actual destination state (`size: 0`, `fork: false`) is authoritative; upstream "health" is informational only |
| `canonical_owner_repo` | `github_api_live` | Destination retains its own namespace; template identity is a separate field |
| `upstream_template_identity` | `github_api_live_upstream` | Destination `template_repository` field is absent (bootstrap failed → exception); upstream self-identifies as `is_template: true` |
| `description` | `github_api_live_upstream` | Destination description is empty (bootstrap failed → exception); upstream API description is the intended inherited value pending user customisation |
| `description.readme_opening` | `readme_opening_upstream` | Destination has no README (bootstrap failed); upstream README opening is the only available value; corroborates upstream API description in substance |
| `default_branch` | `github_api_live` (unchallenged) | Both sources agree: `master` |
| `language` | `github_api_live_upstream` | Destination `HTML` is only an initialization artifact (bootstrap failed → exception); upstream `SCSS` is the true template primary language |
| `homepage` | `github_api_live_upstream` | Destination homepage is not set (bootstrap failed → exception); upstream carries `https://academicpages.github.io` |
| `license` | `github_api_live` (unchallenged) | Both sources agree: MIT |
| `topics` | `github_api_live_upstream` | Destination topics are empty (bootstrap failed → exception); upstream carries 7 canonical topics |
| `is_template` | `github_api_live` | An instantiated destination should not be a template (`false` is correct); the upstream `true` value applies only to the source template |
| `fork` | `github_api_live` (unchallenged) | Both sources agree: `false` |
| `size` | `github_api_live_upstream` | Destination `0` is a bootstrap failure marker (exception); upstream `58150` kB is the expected content footprint after successful bootstrap |
| `scope_decision` | `review_analysis` | No API equivalent; sole source; value: KEEP |

---

## Tie-Breaking Rules

1. When `github_api_live` and `github_api_live_upstream` agree on the same value, `github_api_live` is the cited primary source by convention.
2. A `github_api_live` value that is `(empty)`, `(not set)`, `0` (size), or `(not set — bootstrap failed)` triggers the bootstrap-failure exception and cedes to `github_api_live_upstream`.
3. `readme_opening_upstream` is used only when neither API source supplies a usable value for the field, or as a third-tier corroboration.
4. All textual description candidates are preserved verbatim; no punctuation normalisation is applied before choosing.

---

## Snapshot Provenance

- **`github_api_live`** (`bugmaker00/My-Homepage`): created_at 2026-04-09T00:18:25Z, pushed_at 2026-04-09T00:18:30Z (live at task run)
- **`github_api_live_upstream`** (`academicpages/academicpages.github.io`): pushed_at 2026-04-08T17:19:38Z, updated_at 2026-04-08T19:37:47Z (repo ID: 68287594)
- **`readme_opening_upstream`**: from `master` HEAD at the same snapshot
- **`review_analysis`**: committed 2026-04-08 in `review/personal-website-construct-pair-1`
- **Policy file committed before `resolved_values.json`** to ensure traceability
