# Readback Audit — `personal-website-construct` finalpool Session 8

**Review branch:** `review/personal-website-construct-finalpool-8`  
**Base commit (inherited from finalpool):** `15df6812c241d88b9821f2f5b1b3c1d487954dcf`  
**Stage commit:** `ebbe42aafb6d1d230bbc0e9ea3d4ca52bf63e747`  
**Scope source-of-truth:** `full_scope.csv` (SHA `e84140e1097812cd0d9d147cb547d8923ae1492d`, 1313 bytes, 11 scope rows)  
**Audit generated:** 2026-04-12  
**Subject pair:** `bugmaker00/My-Homepage` ← `academicpages/academicpages.github.io`  

---

## Methodology

Each row in `full_scope.csv` is compared against the live GitHub API state of the
file on `review/personal-website-construct-finalpool-8`. Comparison checks:
1. **File present** — the path exists on the review branch.
2. **Blob SHA match** — the live blob SHA equals the SHA recorded in `full_scope.csv`.
3. **Size match** — the live size in bytes equals `full_scope.csv`.

Result codes: `MATCH` = all three checks pass · `MISMATCH` = any check fails · `MISSING` = file absent.

---

## Audit Table

| # | file_path | scope_blob_sha | scope_size_B | live_blob_sha | live_size_B | result |
|---|-----------|---------------|-------------|--------------|------------|--------|
| 1 | `review_table_pair_1.csv` | `2c629944` | 1384 | `2c629944` | 1384 | ✅ MATCH |
| 2 | `decision_summary_pair_1.md` | `a8627b4f` | 5838 | `a8627b4f` | 5838 | ✅ MATCH |
| 3 | `conflict_resolution.csv` | `6484b02f` | 3607 | `6484b02f` | 3607 | ✅ MATCH |
| 4 | `source_priority.md` | `2a5a1237` | 6261 | `2a5a1237` | 6261 | ✅ MATCH |
| 5 | `resolved_values.json` | `9186f565` | 7021 | `9186f565` | 7021 | ✅ MATCH |
| 6 | `README.md` | `14b4e0cc` | 2111 | `14b4e0cc` | 2111 | ✅ MATCH |
| 7 | `module_a.py` | `83c055ab` | 1267 | `83c055ab` | 1267 | ✅ MATCH |
| 8 | `module_b.py` | `f04fe17a` | 682 | `f04fe17a` | 682 | ✅ MATCH |
| 9 | `tests/test_module_a.py` | `5c41895d` | 153 | `5c41895d` | 153 | ✅ MATCH |
| 10 | `utils/helpers.py` | `3e4017ac` | 252 | `3e4017ac` | 252 | ✅ MATCH |
| 11 | `.gitignore` | `a81974ff` | 14 | `a81974ff` | 14 | ✅ MATCH |

**Summary: 11 / 11 MATCH — 0 MISMATCH — 0 MISSING**

---

## Live Branch Composition

The following files are present on `review/personal-website-construct-finalpool-8`
beyond the scope rows above (session-8 audit artifacts and base-inherited items):

| file_path | note |
|-----------|------|
| `full_scope.csv` | Session-8 scope index (SHA `e84140e1`, 1313 B; self-referential — not audited against itself) |
| `readback_audit.md` | This document |
| `.python_tmp/` | Inherited from finalpool base (ephemeral scratch directory) |

---

## Source-Priority Recap (from `source_priority.md`)

```
github_api_live > github_api_live_upstream > readme_opening_upstream > review_analysis
```

Bootstrap-failure exception applies to 6 fields where `bugmaker00/My-Homepage`
has `size: 0` (destination fields empty/null/failure-marker → next non-empty
source wins).

---

## Resolved-Values Summary (from `resolved_values.json`)

| Field | Chosen Value | Winning Source |
|-------|-------------|---------------|
| `bootstrap_status` | `failed` | `github_api_live` |
| `canonical_owner_repo` | `bugmaker00/My-Homepage` | `github_api_live` |
| `upstream_template_identity` | `academicpages/academicpages.github.io` | `github_api_live_upstream` |
| `description` | Github Pages template based upon HTML and Markdown for personal, portfolio-based websites. | `github_api_live_upstream` |
| `default_branch` | `master` | `github_api_live` (unchallenged) |
| `language` | `SCSS` | `github_api_live_upstream` |
| `homepage` | `https://academicpages.github.io` | `github_api_live_upstream` |
| `license` | `MIT` | `github_api_live` (unchallenged) |
| `topics` | academic-website, github-pages, jekyll, jekyll-theme, markdown, personal-website, portfolio-website | `github_api_live_upstream` |
| `is_template` | `false` | `github_api_live` |
| `fork` | `false` | `github_api_live` (unchallenged) |
| `size` | `58150 kB` | `github_api_live_upstream` |
| `scope_decision` | `KEEP` | `review_analysis` |

---

## Bootstrap-Failure Re-Plan Note

As documented in `decision_summary_pair_1.md` and `resolved_values.json`:

- **Blocking prerequisite:** SATISFIED — `bugmaker00/My-Homepage` exists in the destination namespace and is reachable via GitHub API.
- **Bootstrap status:** FAILED — destination has `size: 0` and `fork: false`; template content from `academicpages/academicpages.github.io` was never propagated.
- **Re-plan required:** The template file set must be manually bootstrapped into `bugmaker00/My-Homepage` from the upstream template `academicpages/academicpages.github.io` (repo ID 68287594, is_template: true, MIT, 16,759 ★).
- **Upstream template identity** (from destination namespace, via bootstrap-failure exception): `academicpages/academicpages.github.io`.

---

## Conclusion

All 11 files in `full_scope.csv` are present on `review/personal-website-construct-finalpool-8`
with exact blob-SHA and byte-size matches. The live state of the review branch is
**fully consistent** with the saved scope. No discrepancies detected.

Stage commit `ebbe42aa` successfully reconstructed the complete reviewed change set
for `finalpool-personal-website-construct_8`.
