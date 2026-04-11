# Source Identifier vs Canonicalized GitHub Path — Audit Report

## Purpose
This document explicitly separates what the tutorial source **named** (verbatim source identifiers)
from what GitHub **currently resolves** to (canonical paths after any redirects or org renames).

---

## The Four Source Identifiers (verbatim, exactly as cited in the tutorial)

```
openai/codex
google-gemini/gemini-cli
QwenLM/Qwen3-Coder
All-Hands-AI/OpenHands
```

> These four identifiers are copied verbatim before any probing. The probe results below
> must not silently overwrite these identifiers — each verbatim identifier is preserved
> as a named field in `target_set.csv` and in this document.

---

## Probe Results: Tutorial Source vs GitHub Canonical

### 1. `openai/codex`
| Field | Value |
|---|---|
| **Tutorial-cited identifier (verbatim)** | `openai/codex` |
| **GitHub redirect?** | **No** |
| **Canonical path** | `openai/codex` |
| **Canonical URL** | https://github.com/openai/codex |
| **API evidence** | GitHub Search API returns `full_name=openai/codex`; all `html_url` fields → `https://github.com/openai/codex/...` |
| **Description** | Lightweight coding agent that runs in your terminal |
| **Language** | Rust |
| **Stars** | ~74,615 |
| **Notes** | Resolves directly. No org rename or redirect detected. |

---

### 2. `google-gemini/gemini-cli`
| Field | Value |
|---|---|
| **Tutorial-cited identifier (verbatim)** | `google-gemini/gemini-cli` |
| **GitHub redirect?** | **No** |
| **Canonical path** | `google-gemini/gemini-cli` |
| **Canonical URL** | https://github.com/google-gemini/gemini-cli |
| **API evidence** | GitHub Search API returns `full_name=google-gemini/gemini-cli`; all `html_url` fields → `https://github.com/google-gemini/gemini-cli/...` |
| **Description** | An open-source AI agent that brings the power of Gemini directly into your terminal. |
| **Language** | TypeScript |
| **Stars** | ~100,938 |
| **Notes** | Resolves directly. No org rename or redirect detected. |

---

### 3. `QwenLM/Qwen3-Coder`
| Field | Value |
|---|---|
| **Tutorial-cited identifier (verbatim)** | `QwenLM/Qwen3-Coder` |
| **GitHub redirect?** | **No** |
| **Canonical path** | `QwenLM/Qwen3-Coder` |
| **Canonical URL** | https://github.com/QwenLM/Qwen3-Coder |
| **API evidence** | GitHub Search API returns `full_name=QwenLM/Qwen3-Coder`; all `html_url` fields → `https://github.com/QwenLM/Qwen3-Coder/...` |
| **Description** | Qwen3-Coder is the code version of Qwen3, the large language model series developed by Qwen team. |
| **Language** | Python |
| **Stars** | ~16,340 |
| **Notes** | Resolves directly. No org rename or redirect detected. |

---

### 4. `All-Hands-AI/OpenHands`
| Field | Value |
|---|---|
| **Tutorial-cited identifier (verbatim)** | `All-Hands-AI/OpenHands` |
| **GitHub redirect?** | **YES — org renamed/transferred** |
| **Canonical path** | `OpenHands/OpenHands` |
| **Canonical URL** | https://github.com/OpenHands/OpenHands |
| **API evidence** | API call with `owner=All-Hands-AI, repo=OpenHands` returns all `html_url` fields pointing to `https://github.com/OpenHands/OpenHands/...` |
| **Supporting evidence** | GitHub issue OpenHands/OpenHands#11376 states: *"Update: This has been executed. Before: All-Hands-AI/OpenHands; After: OpenHands/OpenHands"* |
| **Search API note** | Search API returns 422 for `repo:All-Hands-AI/OpenHands` (resource moved) — confirms the redirect |
| **Notes** | The GitHub organization was renamed/transferred from `All-Hands-AI` to `OpenHands`. The GitHub API transparently redirects all requests for `All-Hands-AI/OpenHands` to `OpenHands/OpenHands`. The source identifier `All-Hands-AI/OpenHands` is preserved verbatim in this document and in `target_set.csv`; the canonical path `OpenHands/OpenHands` is recorded separately in the `canonical_path` and `github_html_url` columns. |

---

## Summary Table — What Tutorial Named vs What GitHub Resolves To

| # | Tutorial Source Identifier (verbatim) | GitHub Canonical Path | Redirect? |
|---|---|---|---|
| 1 | `openai/codex` | `openai/codex` | No |
| 2 | `google-gemini/gemini-cli` | `google-gemini/gemini-cli` | No |
| 3 | `QwenLM/Qwen3-Coder` | `QwenLM/Qwen3-Coder` | No |
| 4 | `All-Hands-AI/OpenHands` | `OpenHands/OpenHands` | **YES** |

---

## Evidence of Redirect for `All-Hands-AI/OpenHands`

When the GitHub API was queried with `owner=All-Hands-AI, repo=OpenHands`, the response
returned content where **all `html_url` fields** pointed to:
```
https://github.com/OpenHands/OpenHands/...
```
instead of the expected:
```
https://github.com/All-Hands-AI/OpenHands/...
```

Additionally, the GitHub Search API returned a `422 Validation Failed` error for
`repo:All-Hands-AI/OpenHands`, indicating the resource is no longer findable at the old path.

The GitHub issue [OpenHands/OpenHands#11376](https://github.com/OpenHands/OpenHands/issues/11376)
explicitly confirms:
> "Update: This has been executed. Before: All-Hands-AI/OpenHands; After: OpenHands/OpenHands"

This confirms the `All-Hands-AI` organization was **canonically renamed/transferred** to `OpenHands`
on GitHub. GitHub transparently redirects the old path to the new canonical path.

The tutorial source identifier `All-Hands-AI/OpenHands` is:
- **Preserved verbatim** in the `source_identifier` column of `target_set.csv`
- **Preserved verbatim** in this document
- **Separated** from the canonical `OpenHands/OpenHands` path (stored in `canonical_path`)

---

## Verbatim Identifier Preservation Checklist

All four source identifiers confirmed present verbatim in this document:
- [x] `openai/codex` — preserved verbatim above ✓
- [x] `google-gemini/gemini-cli` — preserved verbatim above ✓
- [x] `QwenLM/Qwen3-Coder` — preserved verbatim above ✓
- [x] `All-Hands-AI/OpenHands` — preserved verbatim above ✓ (redirect to `OpenHands/OpenHands` noted separately)

---

## Machine-Readable Target Set

See [`target_set.csv`](../target_set.csv) at the root of this branch for the full
machine-readable target set with columns:
- `source_identifier` — verbatim tutorial-cited identifier
- `redirects_or_canonicalizes` — yes/no
- `canonical_owner` — owner after resolution
- `canonical_repo` — repo name after resolution
- `canonical_path` — full `owner/repo` canonical path
- `source_url` — GitHub URL constructed from source identifier
- `github_html_url` — actual resolved GitHub URL
- `redirect_detected` — Yes/No flag
- `notes` — probe evidence and details
