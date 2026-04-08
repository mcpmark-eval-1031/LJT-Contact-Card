# Cleanup Report – LUFFY dev branch

## Summary

| Category | Count |
|---|---|
| Well-mapped source files | 4 |
| Extra / internal-tooling files | 6 |
| Missing expected files | 0 |
| Ambiguous paths | 1 |
| Stale README entries removed | 35 |

---

## Extra Files (no production destination)

All six files reside inside `.python_tmp/` — a hidden directory created by a
previous agent to hold one-off scaffolding scripts.  None of these belong in the
production file tree.

| File | Reason |
|---|---|
| `.python_tmp/setup_env.py` | Scaffolding script that **embeds TODO comments inside Python string literals** (template content for generating project files). These string-literal TODOs were incorrectly harvested by the old README scan, producing 35 stale entries. No real code-level TODO exists in this file. |
| `.python_tmp/check_files.py` | One-off utility; zero code-level TODOs. |
| `.python_tmp/git_check.py` | One-off utility; zero code-level TODOs. |
| `.python_tmp/list_workspace.py` | One-off utility; zero code-level TODOs. |
| `.python_tmp/push_again.py` | One-off utility; zero code-level TODOs. |
| `.python_tmp/reinit_git.py` | One-off utility; zero code-level TODOs. |

**Recommended action:** Remove the entire `.python_tmp/` directory from the
`dev` branch (it should also be added to `.gitignore` if re-creation is
possible).

---

## Missing Files

None.  All expected project source files are present on the `dev` branch.

---

## Ambiguous Paths

| File | Issue |
|---|---|
| `.python_tmp/setup_env.py` | Ambiguous whether it should be treated as a source file. Its TODO-like strings are not code-level TODOs but Python string literals used to scaffold other files. Decision: **exclude from TODO scan**; flag as internal tooling. |

---

## Stale README Entries Removed

The previous `### 📝 Complete TODO List` section contained **35 entries**
referencing `.python_tmp/setup_env.py`.  These were all removed because:

1. The TODO text appears inside Python **string literals** (multi-line strings
   assigned to `files['module_a.py']`, `files['module_b.py']`, and
   `dev_module_a`, `dev_module_b` variables), not in executable comment lines.
2. A correct `# TODO …` regex scan on actual comment tokens finds **zero**
   TODO comments inside `setup_env.py`.
3. The file has no project-level purpose and is classified as internal tooling.

---

## Valid TODO Entries Retained (27 total)

| File | TODOs |
|---|---|
| `module_a.py` | 12 |
| `module_b.py` | 9 |
| `tests/test_module_a.py` | 3 |
| `utils/helpers.py` | 3 |

---

## Reconciliation Decision Log

| Decision | Rationale |
|---|---|
| Exclude `.python_tmp/` from TODO scan | Directory is internal tooling; no production source code resides there. |
| Remove 35 stale `.python_tmp/setup_env.py` README lines | TODOs were embedded in string literals, not real comment-level TODOs. |
| Keep all 27 entries from the 4 project source files | Confirmed by fresh line-by-line scan of actual file content on `dev` branch. |
| No file moves required | All 4 source files are already at their correct repo-relative paths. |
