# Decision Summary — GitHub Fork Flow Pair 1

**Subproblem:** Upstream template identity from destination namespace when invoking
GitHub fork flows (HuggingFace-to-GitHub mirror bootstrap, 1 pair — 2 datasets).  
**Review branch:** `review/github-fork-flow-pair-1`  
**Companion surface:** `review_table_pair_1.csv` (24 rows, both review dimensions combined)  
**Snapshot date:** 2026-04-09  
**Source priority rule:** `github_api_live` > `huggingface_api_live` > `review_analysis`  

---

## Pair 1 Identity

This pair covers the two HuggingFace companion datasets in the `Annoy-DataSync` project
that require GitHub mirrors in the `bugmaker00` destination namespace.

| Role | Repository / Dataset | Platform | Status |
|------|---------------------|----------|--------|
| Upstream Template (Raw) | `dongbobo/Annoy-PyEdu-Rs-Raw` | HuggingFace | ✅ Dataset exists, accessible |
| Fork Destination (Raw) | `bugmaker00/Annoy-PyEdu-Rs-Raw` | GitHub | ❌ **Repo absent — bootstrap not started** |
| Upstream Template (Processed) | `dongbobo/Annoy-PyEdu-Rs` | HuggingFace | ✅ Dataset exists, accessible |
| Fork Destination (Processed) | `bugmaker00/Annoy-PyEdu-Rs` | GitHub | ❌ **Repo absent — bootstrap not started** |

### Bootstrap Failure Explanation

Both destination repositories (`bugmaker00/Annoy-PyEdu-Rs-Raw` and
`bugmaker00/Annoy-PyEdu-Rs`) were expected to be created as GitHub mirrors of their
respective HuggingFace canonical datasets after commit `120c992` resolved the namespace
placeholders in `bugmaker00/Annoy-DataSync`.

At the 2026-04-09 snapshot:
- A GitHub API search of `bugmaker00` namespace returns only **1 result** (`Annoy-DataSync`)
  — the two mirror repos are **completely absent** from GitHub
- The HuggingFace datasets (`dongbobo/Annoy-PyEdu-Rs-Raw`, `dongbobo/Annoy-PyEdu-Rs`)
  **do exist** and are confirmed accessible via the live HuggingFace API
- This is a **more severe** bootstrap failure than the My-Homepage case (where the repo
  existed but was empty): here the destination repos have **never been created**

The **blocking prerequisite** (repository existence in the destination namespace at GitHub)
**is NOT satisfied** for either mirror — `repo_exists = false` for both. A re-plan is
required to create the GitHub mirror repos before any content can be propagated.

### Upstream Source Context

`bugmaker00/Annoy-DataSync` is a fork of `hkust-nlp/CodeIO` (commits by `lockon-n`,
Sep 2025). The `hkust-nlp/CodeIO` upstream **does not exist on GitHub** at the
2026-04-08/2026-04-09 snapshot (0 search results — existence-blocking for CodeIO itself,
but the fork (`Annoy-DataSync`) has already been customised and the namespace resolved).

---

## Review Dimensions

This review combines two dimensions in `review_table_pair_1.csv`:

| Dimension | Source | Description |
|-----------|--------|-------------|
| **dim1** | `huggingface_api_live` | Upstream canonical source (HuggingFace datasets in `dongbobo` namespace) — field values from the live HuggingFace API. This dimension establishes the authoritative template identity and all field values since the GitHub destination is absent. |
| **dim2** | `github_api_live` | Fork destination check (`bugmaker00` GitHub namespace) — live GitHub API response for the intended mirror repos. This dimension checks the blocking prerequisite (repo existence). |

---

## Finalized Values — Safe to Apply

Only rows with `selected = YES` are reproduced here.

### `bugmaker00/Annoy-PyEdu-Rs-Raw` (Raw dataset mirror)

| Field | Finalized Value | Source | Note |
|-------|----------------|--------|------|
| repo_exists | false | github_api_live (dim2) | ❌ **Blocking prerequisite NOT satisfied** — GitHub mirror absent; re-plan required to create `bugmaker00/Annoy-PyEdu-Rs-Raw` |
| bootstrap_status | not_started – GitHub mirror absent | github_api_live (dim2) | ⚠️ **Bootstrap not started** — destination repo does not exist; cannot populate |
| canonical_owner_repo | dongbobo/Annoy-PyEdu-Rs-Raw | huggingface_api_live (dim1) | **dim1 winner** — HuggingFace canonical (P1 live-HF); dim2 absent |
| upstream_template_identity | dongbobo/Annoy-PyEdu-Rs-Raw | huggingface_api_live (dim1) | **dim1 winner** — HF canonical is the authoritative upstream; dim2 absent |
| description | Raw Python educational resource dataset (CodeI/O spec_* format) | huggingface_api_live (dim1) | **dim1 winner** — HF metadata; dim2 absent |
| license | (null – no license specified) | huggingface_api_live (dim1) | **Unchallenged** — both dim1 and dim2 agree: null; tracked by open issue #1 in `bugmaker00/Annoy-DataSync` |
| scope_decision | KEEP | review_analysis | HuggingFace-level entry is valid; GitHub mirror bootstrap failure is documented and actionable |

### `bugmaker00/Annoy-PyEdu-Rs` (Processed dataset mirror)

| Field | Finalized Value | Source | Note |
|-------|----------------|--------|------|
| repo_exists | false | github_api_live (dim2) | ❌ **Blocking prerequisite NOT satisfied** — GitHub mirror absent; re-plan required to create `bugmaker00/Annoy-PyEdu-Rs` |
| bootstrap_status | not_started – GitHub mirror absent | github_api_live (dim2) | ⚠️ **Bootstrap not started** — destination repo does not exist; cannot populate |
| canonical_owner_repo | dongbobo/Annoy-PyEdu-Rs | huggingface_api_live (dim1) | **dim1 winner** — HuggingFace canonical (PyEdu casing). **Contested**: README commit 120c992 uses `Annoy-Pyedu-Rs` (lowercase) in 2 of 3 occurrences vs header badge `Annoy-PyEdu-Rs`; HF live canonical `dongbobo/Annoy-PyEdu-Rs` (PyEdu) wins per P1 priority |
| upstream_template_identity | dongbobo/Annoy-PyEdu-Rs | huggingface_api_live (dim1) | **dim1 winner** — HF canonical is authoritative; dim2 absent |
| description | Processed Python educational resource dataset with explanations (spec_* naming) | huggingface_api_live (dim1) | **dim1 winner** — HF metadata; dim2 absent |
| license | (null – no license specified) | huggingface_api_live (dim1) | **Unchallenged** — both dim1 and dim2 agree: null; tracked by open issue #1 in `bugmaker00/Annoy-DataSync` |
| scope_decision | KEEP | review_analysis | HuggingFace-level entry is valid; casing contest resolved (PyEdu wins); GitHub mirror bootstrap failure documented and actionable |

---

## Consistency Check

### `bugmaker00/Annoy-PyEdu-Rs-Raw`

| Field | selected=YES rows (CSV) | Notes |
|-------|------------------------|-------|
| repo_exists | 1 | dim2 only (false — blocking) |
| bootstrap_status | 1 | dim2 winner; dim1 row informational (not selected) |
| canonical_owner_repo | 1 | dim1 winner; dim2 discarded |
| upstream_template_identity | 1 | dim1 winner; dim2 discarded |
| description | 1 | dim1 winner; dim2 discarded |
| license | 2 | Both dims agree (null — both unchallenged=YES) |
| scope_decision | 1 | review_analysis only |
| **Total selected=YES rows** | **8** | **Matches CSV count for this repo** |

### `bugmaker00/Annoy-PyEdu-Rs`

| Field | selected=YES rows (CSV) | Notes |
|-------|------------------------|-------|
| repo_exists | 1 | dim2 only (false — blocking) |
| bootstrap_status | 1 | dim2 winner; dim1 row informational (not selected) |
| canonical_owner_repo | 1 | dim1 winner (PyEdu casing); dim2 discarded (Pyedu lowercase) |
| upstream_template_identity | 1 | dim1 winner; dim2 discarded |
| description | 1 | dim1 winner; dim2 discarded |
| license | 2 | Both dims agree (null — both unchallenged=YES) |
| scope_decision | 1 | review_analysis only |
| **Total selected=YES rows** | **8** | **Matches CSV count for this repo** |

**Grand total selected=YES rows:** 16  
**Grand total CSV rows:** 24 (12 per dataset, both dims)

---

## Evidence Trail

| Artifact | Branch | Purpose |
|----------|--------|----------|
| `review_table_pair_1.csv` | `review/github-fork-flow-pair-1` | Combined 2-dimension review surface (24 rows, both dim1 and dim2) |
| `decision_summary_pair_1.md` | `review/github-fork-flow-pair-1` | Finalized values with bootstrap failure analysis (this document) |
| `scope_matrix_single_1.csv` | `review/scope-matrix-single-1` | Prior single-source scope matrix (4 candidates; established HF canonical identities) |
| `evidence_notes_single_1.md` | `review/scope-matrix-single-1` | Evidence trail for namespace-resolution commit 120c992 |

### Upstream Template Provenance

**Dataset 1 — Raw**
- **HF canonical:** `dongbobo/Annoy-PyEdu-Rs-Raw`
- **Platform:** HuggingFace Datasets
- **Description:** Raw Python educational resource dataset (CodeI/O spec_* format)
- **License:** null (no license specified; flagged in open issue #1)
- **Confirmed via:** P1 live-HuggingFace query (Annoy-DataSync PR#2; snapshot 2026-04-08)

**Dataset 2 — Processed**
- **HF canonical:** `dongbobo/Annoy-PyEdu-Rs` (PyEdu casing — HF canonical wins over README Pyedu variant)
- **Platform:** HuggingFace Datasets
- **Description:** Processed Python educational resource dataset with explanations (spec_* naming)
- **License:** null (no license specified; flagged in open issue #1)
- **Confirmed via:** P1 live-HuggingFace query (Annoy-DataSync PR#2; snapshot 2026-04-08)
- **Casing contest:** README commit 120c992 shows 2× `Annoy-Pyedu-Rs` (lowercase) and 1× header `Annoy-PyEdu-Rs`; HF canonical `PyEdu` wins per source priority P1 > P2

### Fork Destination Provenance

**GitHub mirrors (both absent):**
- `bugmaker00/Annoy-PyEdu-Rs-Raw` — not found in GitHub API (0 results in namespace search at 2026-04-09)
- `bugmaker00/Annoy-PyEdu-Rs` — not found in GitHub API (0 results in namespace search at 2026-04-09)

**Re-plan action required:**
1. Create `bugmaker00/Annoy-PyEdu-Rs-Raw` as a GitHub repository (mirror of HF dataset)
2. Create `bugmaker00/Annoy-PyEdu-Rs` as a GitHub repository (mirror of HF dataset)
3. Resolve license for both datasets (open issue #1 in `bugmaker00/Annoy-DataSync`)
4. Resolve outstanding README placeholders (paper title, arXiv ID) in `bugmaker00/Annoy-DataSync`
