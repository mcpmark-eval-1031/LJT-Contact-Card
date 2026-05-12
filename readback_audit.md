# Readback Audit — `review/dataset-license-issue-finalpool-v2`

**Workflow:** Dataset License Issue — Pilot Fix & Readback  
**Task ID:** `finalpool-dataset-license-issue`  
**Branch:** `review/dataset-license-issue-finalpool-v2` → `main`  
**Audit timestamp:** 2026-05-12 UTC  
**Repo:** `mcpmark-eval-1031/temp-luffy`  
**Auditor:** bugmaker00

---

## 1. Issue Reference

- **Issue:** `bugmaker00/Annoy-DataSync#1` — "License info. needed"
- **Request:** Add license information for `Annoy-PyEdu-Rs-Raw` and `Annoy-PyEdu-Rs`
- **Required license:** `odc-by` (ODC-By 1.0), inherited from upstream `HuggingFaceTB/smollm-corpus` python-edu subset

---

## 2. Full Scope Verification (`full_scope.csv`)

Source of truth: `full_scope.csv` on branch `review/dataset-license-issue-finalpool-v2`

| # | hf_repo | file | current_license | required_license | in_pilot | change_applied |
|---|---------|------|-----------------|------------------|----------|----------------|
| 1 | `dongbobo/Annoy-PyEdu-Rs-Raw` | README.md | null → odc-by | odc-by | **yes** | applied |
| 2 | `dongbobo/Annoy-PyEdu-Rs` | README.md | null | odc-by | no | pending |

**Total scope rows:** 2  
**Pilot cohort rows:** 1 (Annoy-PyEdu-Rs-Raw)  
**Deferred rows:** 1 (Annoy-PyEdu-Rs)

---

## 3. Live State Readback — HuggingFace Datasets

Re-read performed against live HuggingFace Hub API at audit time.

### Pilot: `dongbobo/Annoy-PyEdu-Rs-Raw / README.md` ✅

| Field | Plan (full_scope.csv) | Live HF State | Match |
|-------|----------------------|---------------|-------|
| `current_license` | null → odc-by | odc-by | ✅ PASS |
| `change_applied` | applied | applied | ✅ PASS |
| YAML frontmatter present | YES | YES | ✅ PASS |
| `license: odc-by` in frontmatter | YES | YES | ✅ PASS |
| Body content unchanged | YES | YES (body identical to pre-change) | ✅ PASS |

**Live README first 5 lines (verified live):**
```
---
license: odc-by
---
# Annoy: This should be a paper Title

```

**Live SHA:** `db527ce8eec66b95a6a9ffd2b758c7dcf7fb875a`  
**Last commit:** `fix: add license: odc-by YAML frontmatter (resolves bugmaker00/Annoy-DataSync#1)`  
**HF URL:** https://huggingface.co/datasets/dongbobo/Annoy-PyEdu-Rs-Raw

---

### Deferred: `dongbobo/Annoy-PyEdu-Rs / README.md` ✅

| Field | Plan (full_scope.csv) | Live HF State | Match |
|-------|----------------------|---------------|-------|
| `change_applied` | pending | pending (no change) | ✅ PASS |
| YAML frontmatter present | NO (deferred) | NO | ✅ PASS |
| `license: odc-by` in frontmatter | NO | NO | ✅ PASS |
| Body content unchanged | YES | YES | ✅ PASS |

**Live README first line (verified live):**
```
# Annoy: This should be a paper Title
```
No YAML frontmatter block present — consistent with `pending` status.

**Live SHA:** `a45ac26947ff4644a1d47c03977a2ad4512e121d`  
**Last commit:** `Upload README.md with huggingface_hub` (original)  
**HF URL:** https://huggingface.co/datasets/dongbobo/Annoy-PyEdu-Rs

---

## 4. Pilot Cohort Workflow — Applied Actions

Per `pilot_scope.csv` (1 record) — action applied to live state:

| hf_repo | live_action_type | live_action_detail | Status |
|---------|-----------------|-------------------|--------|
| `dongbobo/Annoy-PyEdu-Rs-Raw` | prepend_yaml_frontmatter | Prepend `---\nlicense: odc-by\n---` to README.md | ✅ Applied — commit `bcba216cbaeb` on HF |

**Pilot actions applied: 1/1 (100%)** — Pilot record received exactly one fix commit.

**Non-pilot records (Annoy-PyEdu-Rs): 0 actions applied** ✅ — Live actions confined to pilot cohort only.

---

## 5. Cross-Validation Summary

| Check | Result |
|-------|--------|
| `full_scope.csv` contains exactly 2 rows (complete reviewed set) | ✅ PASS |
| `pilot_scope.csv` is a strict subset of `full_scope.csv` (1 ⊂ 2) | ✅ PASS |
| `full_scope.csv.in_pilot=true` rows match `pilot_scope.csv` exactly | ✅ PASS |
| SHA verification: pilot live SHA matches expected | ✅ PASS |
| Pilot workflow applied to exactly 1 record (no extra targets) | ✅ PASS |
| Deferred record confirmed untouched | ✅ PASS |
| Issue `bugmaker00/Annoy-DataSync#1` partially resolved (pilot only) | ✅ PASS |

**Overall audit verdict: ✅ PASS — Live state on HuggingFace Hub exactly matches the saved plan in `full_scope.csv`. Pilot workflow applied exclusively to `dongbobo/Annoy-PyEdu-Rs-Raw`. Deferred dataset `dongbobo/Annoy-PyEdu-Rs` confirmed pending.**

---

## 6. Deferred Actions (Non-Pilot, Full-Rollout Candidate)

| hf_repo | Current state | Required action |
|---------|--------------|----------------|
| `dongbobo/Annoy-PyEdu-Rs` | No YAML frontmatter; README starts with `# Annoy: This should be a paper Title` | Prepend `---\nlicense: odc-by\n---` to README.md (identical fix as pilot) |

---

## 7. Verification Commands

```bash
# 1. Confirm pilot dataset README has odc-by frontmatter
curl -sL https://huggingface.co/datasets/dongbobo/Annoy-PyEdu-Rs-Raw/raw/main/README.md | head -5
# Expected:
#   ---
#   license: odc-by
#   ---
#   # Annoy: This should be a paper Title

# 2. Confirm deferred dataset README has no frontmatter yet
curl -sL https://huggingface.co/datasets/dongbobo/Annoy-PyEdu-Rs/raw/main/README.md | head -2
# Expected:
#   # Annoy: This should be a paper Title
```
