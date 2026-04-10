# Backlog Hotspots

> **Branch:** `dev` · **Generated:** 2026-04-10 17:09 UTC  
> Files ranked by total unresolved Python comment markers (TODO + FIXME combined).

## Top 5 Files by Unresolved Comment Count

| Rank | File | TODOs | FIXMEs | Total |
|-----:|------|------:|-------:|------:|
| 1 | `module_a.py` | 12 | 0 | **12** |
| 2 | `module_b.py` | 9 | 0 | **9** |
| 3 | `tests/test_module_a.py` | 3 | 0 | **3** |
| 4 | `utils/helpers.py` | 3 | 0 | **3** |
| 5 | `.python_tmp/setup_env.py` | 1 | 0 | **1** |

### Notes

- **`module_a.py`** (12 unresolved): Highest concentration of open work items. Covers input validation, caching, streaming, schema validation, type hints, option handling, config loading, config validation, network timeout handling, batch processing, error recovery, and graceful shutdown.
- **`module_b.py`** (9 unresolved): All network-layer TODOs — retry logic, memory-leak fix, connection pool config, timeout parameter, SSL handling, exponential backoff, request signing, response compression, and concurrent batch processing.
- **`tests/test_module_a.py`** (3 unresolved): Test coverage gaps — additional test cases, dependency mocking, and edge-case coverage.
- **`utils/helpers.py`** (3 unresolved): Utility-layer items — multi-threading support, concurrent-access race condition, and custom formatting templates.
- **`.python_tmp/setup_env.py`** (1 unresolved): Scaffolding script with one comment marker noting the creation of files with TODO comments.

_Scan method: Python `tokenize` module — only genuine `COMMENT` tokens containing `TODO` or `FIXME` are counted; markers embedded in string literals are excluded._
