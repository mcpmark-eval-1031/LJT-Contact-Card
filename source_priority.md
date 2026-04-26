# Source Priority Policy — `reconstruct-reviewed-change-set`

## Workflow Context

Repository: **`mcpmark-eval-1031/LUFFY`**  
Task: Reconstruct the reviewed change set for syncing Python-source TODO comments into the `README.md` TODO checklist and resolve conflicts arising from multiple sources.

The reviewed change-set is the 27-item TODO checklist in `README.md`.  The current `main` branch (commit `652b69ac35364af9e81d773dacddbde452fc8504`) incorrectly introduces a `src/nebula/` path prefix on the 21 TODO entries sourced from `module_a.py` and `module_b.py`; the remaining 6 entries (`tests/` and `utils/`) are correctly left unchanged.

---

## Source Catalogue

| Priority | Source ID | Description |
|---|---|---|
| **1** | `live_file_scan` | Live directory listing and file content of `mcpmark-eval-1031/LUFFY` at HEAD (`main` branch). The actual Python source files define where each TODO comment lives; this is the ground truth for file paths. |
| **2** | `readme_snapshot_9818ab44` | `README.md` captured at commit `9818ab44c0f489e1bb41852989d9fcd39cccb650` ("docs: populate TODO checklist with root-relative file:line paths"). The commit message explicitly states the canonical format: "filepath:lineno relative to the monorepo root (no ./ prefix, no absolute paths)". Corroborates the live file scan. |
| **3** | `review_branch_snapshot` | `README.md` on the `review/sync-todo-to-readme` branch. Also carries correct root-relative paths with no `src/nebula/` prefix. Third corroborating source. |
| **4** | `readme_snapshot_main` | `README.md` on `main` at commit `652b69ac35364af9e81d773dacddbde452fc8504` (current HEAD). Introduced `src/nebula/` prefix — a directory that does not exist in the repository. **Lowest authority**: demonstrably wrong; overridden by all other sources. |

---

## Priority Ordering

**For `todo_checklist.item.file_path_qualified`** (the `filepath:lineno` label of every TODO checklist entry):

```
live_file_scan  >  readme_snapshot_9818ab44  >  review_branch_snapshot  >  readme_snapshot_main
```

Rationale: the actual Python files on disk are the only authoritative source for file paths.  The two earlier/parallel snapshots (`9818ab44` and the review branch) agree with the live scan.  `readme_snapshot_main` is the sole conflicting source and its path prefix (`src/nebula/`) is unsupported by the repository's physical file layout.

**For `todo_checklist.item.description`** (the human-readable TODO text):

```
live_file_scan  =  readme_snapshot_9818ab44  =  readme_snapshot_main
```

All sources agree on description text; no conflict exists for this field.

**For `todo_checklist.item.tag_representation`** (parenthetical labels in source, e.g. `(dev)`, `(bug)`, `(warning)`, `(future)`, `(bugfix)`):

```
readme_snapshot_9818ab44  =  review_branch_snapshot  =  readme_snapshot_main  >  live_file_scan (raw)
```

Both README snapshots strip tags from the rendered checklist entry, producing the bare description.  This is the adopted convention.  Raw source tags are preserved as reference information only, not in the rendered checklist.

**For `module_directory_structure`** (whether `src/nebula/` exists):

```
live_file_scan  >  readme_snapshot_main
```

Live scan is definitive; `readme_snapshot_main` implied a non-existent directory.

---

## Tie-Breaking Rules

1. When two sources at the **same priority tier** agree, that value is chosen without further analysis.
2. When a lower-priority source is the *sole* source claiming a value (as with `readme_snapshot_main` and `src/nebula/`), the claim is rejected.
3. Description text conflicts (capitalisation, punctuation) are resolved in favour of the `live_file_scan` verbatim text.
