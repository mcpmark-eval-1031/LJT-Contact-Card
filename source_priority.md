# Source Priority Policy — `finalpool-personal-website-construct_10`

## Workflow Context

Repository: **`mcpmark-eval-1031/LUFFY`**  
Task: Reconstruct the reviewed change set for the personal website construction workflow (finalpool, trial 10).  
Subject pair: `bugmaker00/My-Homepage` (fork destination) ← `academicpages/academicpages.github.io` (upstream template)  
Review branch: `review/personal-website-construct-finalpool-10`  
Prior review branch: `review/personal-website-construct-finalpool-9` (task-9 snapshot, 2026-04-09)  
Prior review analysis branch: `review/personal-website-construct-pair-1` (snapshot 2026-04-08)  
Current snapshot date: 2026-04-11

### Repository Recreation Note

The destination repository `bugmaker00/My-Homepage` was **recreated** between task-9 and task-10.
The task-9 snapshot recorded `created_at: 2026-04-08T20:43:49Z` and `pushed_at: 2026-04-09T00:18:30Z`.
The current live snapshot records `created_at: 2026-04-11T23:28:16Z` and `pushed_at: 2026-04-11T23:28:20Z`.
The new instance still exhibits the same bootstrap failure (`size: 0`, `fork: false`).

---

## Source Catalogue

| Priority | Source ID | Description |
|----------|-----------|-------------|
| **1** | `github_api_live` | Live GitHub REST API `/repos/bugmaker00/My-Homepage` snapshot taken at task time (pushed_at: 2026-04-11T23:28:20Z). Reflects the actual current state of the fork destination. The destination has `size: 0`, `fork: false`, indicating a bootstrap failure — template content was never propagated. |
| **2** | `github_api_live_upstream` | Live GitHub REST API `/repos/academicpages/academicpages.github.io` snapshot at task time (pushed_at: 2026-04-08T17:19:38Z; updated_at: 2026-04-11T22:16:44Z; 16787 stars). Provides authoritative template field values: `description`, `language`, `topics`, `homepage`, `size`, `is_template`. Used as fallback when the destination has empty or failure-marker values. |
| **3** | `readme_opening_upstream` | Opening sentence of `academicpages/academicpages.github.io` `README.md` on `master` at the same snapshot. Used for description-type fields when the API field requires corroboration or when both `github_api_live` and `github_api_live_upstream` are ambiguous. |
| **4** | `review_analysis` | Analytical conclusions committed in `review/personal-website-construct-pair-1` (files: `review_table_pair_1.csv`, `decision_summary_pair_1.md`). Used only for derived meta-fields with no direct API equivalent (e.g. `scope_decision`). |
| **5** | `review_snapshot_task9` | `resolved_values.json` and `conflict_resolution.csv` from `review/personal-website-construct-finalpool-9` (task-9 review branch, captured 2026-04-09). Used as a prior-snapshot source for timestamp-comparison fields (`destination.created_at`, `destination.pushed_at`, `upstream.stargazers_count`, `upstream.updated_at`). Lowest priority — superseded by current live sources for all non-temporal fields. |

---

## Priority Ordering

**General rule** (highest → lowest):

```
github_api_live  >  github_api_live_upstream  >  readme_opening_upstream  >  review_analysis  >  review_snapshot_task9
```

**Bootstrap-failure exception:**

The destination repository `bugmaker00/My-Homepage` has `size: 0` and `fork: false`, confirming the
template instantiation failed to bootstrap (no template content was propagated). When `github_api_live`
returns an empty, null, or failure-marker value for a field because of this bootstrap failure, that source
is treated as below-threshold and the next non-empty source in the priority chain wins.

Fields affected by this exception: `description`, `upstream_template_identity`, `language`, `homepage`,
`topics`, `size`.

**Unconditional `github_api_live` wins (no exception):**  
`canonical_owner_repo`, `bootstrap_status`, `destination.created_at`, and `destination.pushed_at` always
use `github_api_live` — the destination's actual namespace and actual failure state are never overridden
by the upstream template.

**Snapshot-comparison fields:**  
`destination.created_at`, `destination.pushed_at`, `upstream.stargazers_count`, and `upstream.updated_at`
compare the current live snapshot against the task-9 prior snapshot (`review_snapshot_task9`). Current live
sources always win; prior snapshots are recorded only as competing candidates for audit purposes.

**Description punctuation conflict:**  
`review_table_pair_1.csv` (source `review_snapshot_pair1`) records the upstream description **without**
the comma after "personal" — a transcription artefact. The verbatim `github_api_live_upstream` live text
("…for personal, portfolio-based websites.") is authoritative.

---

## Per-Field Source Decisions

| Field | Winning Source | Rationale |
|-------|----------------|-----------|
| `bootstrap_status` | `github_api_live` | Actual destination state (`size: 0`, `fork: false`) is authoritative; upstream "health" is informational only |
| `canonical_owner_repo` | `github_api_live` | Destination retains its own namespace; template identity is a separate field |
| `upstream_template_identity` | `github_api_live_upstream` | Destination `template_repository` field is absent (bootstrap failed → exception); upstream self-identifies as `is_template: true` |
| `description` | `github_api_live_upstream` | Destination description is empty (bootstrap failed → exception); upstream API description is the intended inherited value pending user customisation |
| `description.punctuation_variant` | `github_api_live_upstream` | Live upstream API text (with comma after "personal") is verbatim authoritative; `review_table_pair_1.csv` variant (no comma) is a transcription artefact |
| `default_branch` | `github_api_live` (unchallenged) | Both sources agree: `master` |
| `language` | `github_api_live_upstream` | Destination `HTML` is only an initialization artifact (bootstrap failed → exception); upstream `SCSS` is the true template primary language |
| `homepage` | `github_api_live_upstream` | Destination homepage is not set (bootstrap failed → exception); upstream carries `https://academicpages.github.io` |
| `license` | `github_api_live` (unchallenged) | Both sources agree: MIT |
| `topics` | `github_api_live_upstream` | Destination topics are empty (bootstrap failed → exception); upstream carries 7 canonical topics |
| `is_template` | `github_api_live` | An instantiated destination should not be a template (`false` is correct); the upstream `true` value applies only to the source template |
| `fork` | `github_api_live` (unchallenged) | Both sources agree: `false` |
| `size` | `github_api_live_upstream` | Destination `0` is a bootstrap failure marker (exception); upstream `58150` kB is the expected content footprint after successful bootstrap |
| `destination.created_at` | `github_api_live` | Current live snapshot (2026-04-11T23:28:16Z) is authoritative; task-9 snapshot records a prior now-deleted instance |
| `destination.pushed_at` | `github_api_live` | Current live snapshot (2026-04-11T23:28:20Z) is authoritative for the current task run |
| `upstream.stargazers_count` | `github_api_live_upstream` | Current live (16787) supersedes task-9 snapshot (16759); live source always wins for snapshot-comparison fields |
| `upstream.updated_at` | `github_api_live_upstream` | Current live (2026-04-11T22:16:44Z) supersedes task-9 snapshot (2026-04-08T19:37:47Z) |
| `scope_decision` | `review_analysis` | No API equivalent; sole source; value: KEEP |

---

## Tie-Breaking Rules

1. When `github_api_live` and `github_api_live_upstream` agree on the same value, `github_api_live` is
   the cited primary source by convention.
2. A `github_api_live` value that is `(empty)`, `(not set)`, `0` (size), or `(not set — bootstrap failed)`
   triggers the bootstrap-failure exception and cedes to `github_api_live_upstream`.
3. `readme_opening_upstream` is used only when neither API source supplies a usable value for the field,
   or as a third-tier corroboration.
4. For snapshot-comparison fields (`destination.created_at`, `destination.pushed_at`,
   `upstream.stargazers_count`, `upstream.updated_at`), the current live source always wins over
   `review_snapshot_task9`; prior values are recorded as competing candidates only for audit traceability.
5. All textual description candidates are preserved verbatim; no punctuation normalisation is applied
   before choosing the winner.

---

## Snapshot Provenance

- **`github_api_live`** (`bugmaker00/My-Homepage`): created_at 2026-04-11T23:28:16Z,
  pushed_at 2026-04-11T23:28:20Z (live at task-10 run); **repository was recreated** between task-9
  and task-10 (prior instance: created_at 2026-04-08T20:43:49Z)
- **`github_api_live_upstream`** (`academicpages/academicpages.github.io`): pushed_at
  2026-04-08T17:19:38Z, updated_at 2026-04-11T22:16:44Z (repo ID: 68287594)
- **`readme_opening_upstream`**: from `master` HEAD at the same snapshot
- **`review_analysis`**: committed 2026-04-08 in `review/personal-website-construct-pair-1`
- **`review_snapshot_task9`**: committed 2026-04-09 in `review/personal-website-construct-finalpool-9`
- **Policy file committed before `resolved_values.json`** to ensure traceability
