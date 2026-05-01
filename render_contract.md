# Render Contract — Full-Scope CSV File-Set Artifact

**Version:** 1.0.0  
**Repository:** mcpmark-eval-1031/LUFFY  
**Status:** FROZEN  
**Date:** 2026-05-01  
**Scan basis:** `review/finalpool-youtube-repo-7` branch — post-review change-set snapshot  
**Artifact source:** `full_scope.csv` (4 records) + `readback_audit.md` (audit report)

---

## 1. Purpose

This contract governs the exact structure, field names, field order,
empty-value representation, normalization rules, and ordering constraints
that every rendering of the **Full-Scope CSV File-Set Artifact** (hereafter
"the artifact") MUST satisfy.

The artifact is a machine-readable JSON document produced by parsing the
canonical `full_scope.csv` and serializing the extracted records. No
rendering may be produced, stored, or reviewed until this contract is frozen.

> **Contract-first rule:** The schema declared below is frozen before any
> preview JSON is written. `render_preview.json` is derived from this
> contract; the contract is never derived from the preview.

---

## 2. Source File Set

The reviewed change set that this artifact represents consists of the
following files added on branch `review/finalpool-youtube-repo-7`:

| File | Role | Description |
|------|------|-------------|
| `full_scope.csv` | Primary data source | Source of truth — 4 records (complete reviewed email-action set) |
| `readback_audit.md` | Audit report | Evidence proving live state on `main` matches the saved plan |

The artifact JSON is derived solely from `full_scope.csv`; the audit report
is preserved as auxiliary metadata.

---

## 3. Schema Declaration

### 3.1 Top-level Envelope Fields (field order canonical, positional)

| # | Field Name       | JSON Type          | Required | Description |
|---|------------------|--------------------|----------|-------------|
| 1 | `schema_version` | `string`           | YES      | Semver of this contract: `"1.0.0"`. |
| 2 | `repository`     | `string`           | YES      | Fully-qualified `owner/repo` slug. |
| 3 | `source_branch`  | `string`           | YES      | Branch from which the source CSV was taken. |
| 4 | `generated_at`   | `string` (ISO 8601)| YES      | UTC timestamp of generation (`YYYY-MM-DDTHH:MM:SSZ`). |
| 5 | `source_files`   | `array<string>`    | YES      | Sorted list of root-relative source file paths. |
| 6 | `total_records`  | `integer`          | YES      | Count of Scope Records in `records` (equals `len(records)`). |
| 7 | `records`        | `array`            | YES      | Ordered array of Scope Records (see §3.2). |

**Rule S-1:** Envelope fields MUST appear in the JSON object in exactly the
order shown (positions 1–7). No additional envelope fields are permitted.

### 3.2 Scope Record Fields (field order canonical, positional)

| # | Field Name             | JSON Type          | Required | Description |
|---|------------------------|--------------------|----------|-------------|
| 1 | `record_id`            | `string`           | YES      | Unique record identifier (e.g., `COML2026`). Upper-cased. |
| 2 | `conference`           | `string`           | YES      | Full conference name with year and subtitle in parentheses. |
| 3 | `paper_title`          | `string`           | YES      | Paper title verbatim; placeholder text used when not specified. |
| 4 | `author_email`         | `string`           | YES      | Author contact email address. |
| 5 | `publication_contact`  | `string`           | YES      | Publication committee or contact email address. |
| 6 | `primary_action`       | `string`           | YES      | Human-readable action description required for camera-ready. |
| 7 | `camera_ready_deadline`| `string`           | YES      | Deadline string; may include parenthetical annotations. |
| 8 | `registration_deadline`| `string`           | YES      | Registration deadline string; `"N/A"` when not applicable. |
| 9 | `status`               | `string` (enum)    | YES      | `"PENDING"` or `"OVERDUE"`. |
| 10| `priority`             | `string` (enum)    | YES      | `"HIGH"` or `"CRITICAL"`. |
| 11| `in_pilot`             | `boolean`          | YES      | `true` if record belongs to pilot cohort; otherwise `false`. |
| 12| `live_action_applied`  | `boolean`          | YES      | `true` if a live action was already applied; otherwise `false`. |
| 13| `review_verdict`       | `string` (enum)    | YES      | `"deferred"` or `"pilot_applied"`. |
| 14| `source_sha`           | `string`           | YES      | 40-character lowercase hex SHA-1 of the source plan file. |

**Rule S-2:** Record fields MUST appear in the JSON object in exactly the
order shown (positions 1–14). No additional record fields are permitted.

**Rule S-3:** Every field defined in §3.1 and §3.2 MUST be present in every
record. No field may be omitted.

---

## 4. Empty-Value Policy

| Situation                                        | Representation |
|--------------------------------------------------|----------------|
| `registration_deadline` not applicable           | `"N/A"` (string — NOT `null`) |
| `paper_title` not specified in source            | Descriptive placeholder string (e.g., `"(Title not specified in acceptance email)"`) — NOT `null` |
| Boolean fields that are false                    | `false` (JSON boolean — NOT string `"false"`) |
| Boolean fields that are true                     | `true` (JSON boolean — NOT string `"true"`) |
| `records` when no rows qualify                   | `[]` (empty JSON array — NOT `null`) |

**Rule E-1:** An empty string (`""`) MUST NOT appear as any field value in
any envelope field or record field.  
**Rule E-2:** No field defined in §3.1 or §3.2 may be omitted from any record.  
**Rule E-3:** `status` MUST always be `"PENDING"` or `"OVERDUE"`; it is never
`null` and never any other string.  
**Rule E-4:** `priority` MUST always be `"HIGH"` or `"CRITICAL"`; it is never
`null` and never any other string.  
**Rule E-5:** `review_verdict` MUST always be `"deferred"` or `"pilot_applied"`;
it is never `null` and never any other string.  
**Rule E-6:** `total_records` MUST equal the number of elements in `records`.
Mismatch is a contract violation.  
**Rule E-7:** `source_sha` MUST be exactly 40 lowercase hexadecimal characters.

---

## 5. Normalization Rules

**Rule N-1 (Record ID):** `record_id` MUST be preserved verbatim from the CSV.
It is an upper-cased alphanumeric token.  
Examples: `"COML2026"`, `"COAI2026"`, `"COLM2026"`, `"COMLW2026"`.

**Rule N-2 (Conference):** `conference` MUST preserve the full string including
the parenthetical subtitle.  
Example: `"COML 2026 (Conference on Machine Learning)"`.

**Rule N-3 (Paper Title):** `paper_title` MUST preserve the first character's
case as-is. If the source CSV contains a quoted value with internal commas,
the commas are preserved in the JSON string. Titles are never coerced to a
different case.

**Rule N-4 (Email Addresses):** `author_email` and `publication_contact` MUST
be preserved verbatim, lower-cased, with no surrounding whitespace.

**Rule N-5 (Boolean Parsing):** CSV boolean tokens `true` and `false` MUST be
converted to JSON native booleans `true` and `false`. They MUST NOT remain as
strings.

**Rule N-6 (Deadline Strings):** `camera_ready_deadline` and
`registration_deadline` MUST be preserved as verbatim strings, including any
parenthetical annotations such as `"(extended)"` or `"(MISSED)"`.

**Rule N-7 (Source SHA):** `source_sha` MUST be lower-case hex. No upper-case
letters permitted.

**Rule N-8 (Timestamp):** `generated_at` MUST be expressed in UTC using the
`Z` suffix (e.g., `"2026-05-01T00:00:00Z"`).

**Rule N-9 (Source Files Sort):** Entries in `source_files` MUST be sorted in
ascending lexicographic order (Unicode code-point order on the original-case
path string).

---

## 6. Ordering Constraints

**Rule O-1 (Primary Sort — Record ID):** Scope Records MUST be sorted in
ascending lexicographic order by `record_id`.

**Rule O-2 (id Assignment):** Records appear in the array in the sorted order;
no separate `id` field is used. The array index (0-based) is implicit.

**Rule O-3 (Stability):** The sort MUST be stable. Equal `record_id` values
MUST NOT occur; duplication is a contract violation.

**Rule O-4 (Field Order Immutability):** The field orders declared in §3.1
(positions 1–7) and §3.2 (positions 1–14) are immutable. They MUST NOT be
altered without incrementing `schema_version`.

---

## 7. Scan Scope

The canonical scan scope for this rendering is the `full_scope.csv` file on
the reviewed branch. All rows except the header row are included. The header
row is defined as the first line of the file and MUST be skipped during
parsing.

The canonical source file list is:

1. `full_scope.csv`
2. `readback_audit.md`

---

## 8. Blank and Tie Representation Summary

| Field | When value is absent / indeterminate | Representation |
|-------|--------------------------------------|----------------|
| `registration_deadline` | Not applicable for this record | `"N/A"` |
| `paper_title` | Not specified in acceptance email | Placeholder string |
| `source_files` | No source files found | `[]` |
| `total_records` | Zero qualifying records | `0` |
| `status` | Never absent | `"PENDING"` or `"OVERDUE"` only |
| `priority` | Never absent | `"HIGH"` or `"CRITICAL"` only |
| `review_verdict` | Never absent | `"deferred"` or `"pilot_applied"` only |
| Tie on `record_id` | Duplicate identifier | Contract violation — MUST NOT occur |

---

## 9. Review-Branch Convention

The artifact files MUST be committed to a branch named with the prefix
`review/`. The three deliverables that constitute a complete render package:

| File                    | Description |
|-------------------------|-------------|
| `render_contract.md`    | This document (frozen schema). |
| `render_preview.json`   | Contract-conforming JSON artifact. |
| `contract_checklist.md` | Line-by-line verification checklist. |

For this rendering cycle the target branch is
`review/finalpool-youtube-repo-7-artifact`, branched from `main` and
augmented with the reviewed change-set files from
`review/finalpool-youtube-repo-7`.

---

## 10. Contract Freeze Declaration

> **This contract is FROZEN as of 2026-05-01.**  
> No field names, field positions, empty-value policies, normalization rules,
> or ordering constraints may be altered after this declaration without
> incrementing `schema_version` and re-issuing a new frozen contract.
> `render_preview.json` and `contract_checklist.md` MUST be regenerated
> whenever this contract changes.
