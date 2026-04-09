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
| **API evidence** | All `html_url` fields → `https://github.com/openai/codex/...` |
| **Notes** | Resolves directly. No org rename or redirect detected. |

---

### 2. `google-gemini/gemini-cli`
| Field | Value |
|---|---|
| **Tutorial-cited identifier (verbatim)** | `google-gemini/gemini-cli` |
| **GitHub redirect?** | **No** |
| **Canonical path** | `google-gemini/gemini-cli` |
| **Canonical URL** | https://github.com/google-gemini/gemini-cli |
| **API evidence** | All `html_url` fields → `https://github.com/google-gemini/gemini-cli/...` |
| **Notes** | Resolves directly. No org rename or redirect detected. |

---

### 3. `QwenLM/Qwen3-Coder`
| Field | Value |
|---|---|
| **Tutorial-cited identifier (verbatim)** | `QwenLM/Qwen3-Coder` |
| **GitHub redirect?** | **No** |
| **Canonical path** | `QwenLM/Qwen3-Coder` |
| **Canonical URL** | https://github.com/QwenLM/Qwen3-Coder |
| **API evidence** | All `html_url` fields → `https://github.com/QwenLM/Qwen3-Coder/...` |
| **Notes** | Resolves directly. No org rename or redirect detected. |

---

### 4. `All-Hands-AI/OpenHands`
| Field | Value |
|---|---|
| **Tutorial-cited identifier (verbatim)** | `All-Hands-AI/OpenHands` |
| **GitHub redirect?** | **YES — org renamed** |
| **Canonical path** | `OpenHands/OpenHands` |
| **Canonical URL** | https://github.com/OpenHands/OpenHands |
| **API evidence** | All `html_url` fields → `https://github.com/OpenHands/OpenHands/...` |
| **Notes** | The GitHub organization was renamed from `All-Hands-AI` to `OpenHands`. The GitHub API transparently redirects all requests for `All-Hands-AI/OpenHands` to `OpenHands/OpenHands`. The source identifier `All-Hands-AI/OpenHands` is preserved verbatim in this document and in `target_set.csv`; the canonical path `OpenHands/OpenHands` is recorded separately in the `canonical_path` and `github_html_url` columns. |

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

This confirms the `All-Hands-AI` organization was **canonically renamed** to `OpenHands`
on GitHub. GitHub transparently redirects the old path to the new canonical path.

The tutorial source identifier `All-Hands-AI/OpenHands` is:
- **Preserved verbatim** in the `source_identifier` column of `target_set.csv`
- **Preserved verbatim** in this document
- **Separated** from the canonical `OpenHands/OpenHands` path (stored in `canonical_path`)

---

## Verbatim Identifier Preservation Checklist

All four source identifiers confirmed present verbatim in this document:
- [x] `openai/codex` — preserved verbatim above
- [x] `google-gemini/gemini-cli` — preserved verbatim above
- [x] `QwenLM/Qwen3-Coder` — preserved verbatim above
- [x] `All-Hands-AI/OpenHands` — preserved verbatim above (redirect to `OpenHands/OpenHands` noted separately)
