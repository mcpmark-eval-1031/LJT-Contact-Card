import json
import os
import sys
import requests
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

WORKSPACE = Path(os.environ.get("GITHUB_WORKSPACE", "."))
FORMAT_JSON = WORKSPACE / "format.json"
OUTPUT_PARQUET = WORKSPACE / "verl_deepscaler.parquet"
GROUNDTRUTH_DIR = WORKSPACE / "groundtruth_workspace"
GT_JSON = GROUNDTRUTH_DIR / "deepscaler.json"
GT_INFO = GROUNDTRUTH_DIR / "expected_dataset_info.json"

PARQUET_SCHEMA = pa.schema([
    pa.field("data_source",  pa.utf8()),
    pa.field("prompt",       pa.list_(pa.struct([
                                pa.field("role",    pa.utf8()),
                                pa.field("content", pa.utf8()),
                              ]))),
    pa.field("ability",      pa.utf8()),
    pa.field("reward_model", pa.struct([
                                pa.field("style",        pa.utf8()),
                                pa.field("ground_truth", pa.utf8()),
                              ])),
    pa.field("extra_info",   pa.struct([
                                pa.field("index",    pa.int64()),
                                pa.field("solution", pa.utf8()),
                              ])),
])


def download_file(url, dest):
    print(f"Downloading {url} -> {dest}")
    resp = requests.get(url, stream=True, timeout=120)
    resp.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"  Downloaded {dest} ({dest.stat().st_size:,} bytes)")


def ensure_groundtruth():
    GROUNDTRUTH_DIR.mkdir(parents=True, exist_ok=True)
    if not GT_JSON.exists() or GT_JSON.stat().st_size < 1000:
        download_file(
            "https://raw.githubusercontent.com/hkust-nlp/Toolathlon/main/"
            "tasks/finalpool/verl-dataset/groundtruth_workspace/deepscaler.json",
            GT_JSON,
        )
    else:
        print(f"  [skip] {GT_JSON} already exists")
    if not GT_INFO.exists():
        download_file(
            "https://raw.githubusercontent.com/hkust-nlp/Toolathlon/main/"
            "tasks/finalpool/verl-dataset/groundtruth_workspace/expected_dataset_info.json",
            GT_INFO,
        )
    else:
        print(f"  [skip] {GT_INFO} already exists")


def load_format_schema():
    with open(FORMAT_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def convert_dataset_to_parquet():
    """
    关键修复：使用 pyarrow 原生 schema，将 prompt / reward_model / extra_info
    以 list<struct> / struct 形式写入 parquet，不再 json.dumps() 序列化为字符串。
    """
    with open(GT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} items from ground truth")

    data_sources  = []
    prompts       = []
    abilities     = []
    reward_models = []
    extra_infos   = []

    for idx, item in enumerate(data):
        problem  = item.get("problem",  "").strip()
        answer   = item.get("answer",   "").strip()
        solution = item.get("solution", "").strip()

        # ★ 核心修复：使用原生 Python 类型（list / dict），而非 JSON 字符串
        data_sources.append("DeepScaleR")
        prompts.append([{"role": "user", "content": problem}])
        abilities.append("math")
        reward_models.append({"style": "rule", "ground_truth": answer})
        extra_infos.append({"index": idx, "solution": solution})

    arr_ds   = pa.array(data_sources,  type=pa.utf8())
    arr_pr   = pa.array(prompts,       type=pa.list_(pa.struct([
                                            pa.field("role",    pa.utf8()),
                                            pa.field("content", pa.utf8()),
                                          ])))
    arr_ab   = pa.array(abilities,     type=pa.utf8())
    arr_rm   = pa.array(reward_models, type=pa.struct([
                                            pa.field("style",        pa.utf8()),
                                            pa.field("ground_truth", pa.utf8()),
                                          ]))
    arr_ei   = pa.array(extra_infos,   type=pa.struct([
                                            pa.field("index",    pa.int64()),
                                            pa.field("solution", pa.utf8()),
                                          ]))

    table = pa.table(
        {
            "data_source":  arr_ds,
            "prompt":       arr_pr,
            "ability":      arr_ab,
            "reward_model": arr_rm,
            "extra_info":   arr_ei,
        },
        schema=PARQUET_SCHEMA,
    )

    pq.write_table(table, OUTPUT_PARQUET)
    print(f"Wrote {table.num_rows:,} rows to {OUTPUT_PARQUET}")
    return table


def validate_against_schema(df, schema):
    errors = []

    for i in range(len(df)):
        row = df.iloc[i]

        ds = row.get("data_source")
        if not isinstance(ds, str) or ds != "DeepScaleR":
            errors.append(f"Row {i}: data_source must be 'DeepScaleR', got {repr(ds)}")

        prompt = row.get("prompt")
        try:
            if isinstance(prompt, str):
                prompt = json.loads(prompt)
            elif hasattr(prompt, "tolist"):
                prompt = prompt.tolist()
        except Exception as e:
            errors.append(f"Row {i}: prompt parse error: {e}")
            continue

        if not isinstance(prompt, list) or len(prompt) == 0:
            errors.append(f"Row {i}: prompt must be non-empty list")
            continue

        first = prompt[0]
        if not isinstance(first, dict):
            errors.append(f"Row {i}: prompt[0] must be dict")
            continue
        if first.get("role") != "user":
            errors.append(f"Row {i}: prompt[0].role must be 'user'")
        if not isinstance(first.get("content"), str) or not first.get("content").strip():
            errors.append(f"Row {i}: prompt[0].content must be non-empty string")

        ability = row.get("ability")
        if not isinstance(ability, str) or ability != "math":
            errors.append(f"Row {i}: ability must be 'math', got {repr(ability)}")

        rm = row.get("reward_model")
        try:
            if isinstance(rm, str):
                rm = json.loads(rm)
        except Exception as e:
            errors.append(f"Row {i}: reward_model parse error: {e}")
            continue
        if not isinstance(rm, dict):
            errors.append(f"Row {i}: reward_model must be dict")
            continue
        if rm.get("style") != "rule":
            errors.append(f"Row {i}: reward_model.style must be 'rule'")
        if "ground_truth" not in rm:
            errors.append(f"Row {i}: reward_model missing 'ground_truth'")
        elif not isinstance(rm["ground_truth"], str):
            errors.append(f"Row {i}: reward_model.ground_truth must be str")

        ei = row.get("extra_info")
        try:
            if isinstance(ei, str):
                ei = json.loads(ei)
        except Exception as e:
            errors.append(f"Row {i}: extra_info parse error: {e}")
            continue
        if not isinstance(ei, dict):
            errors.append(f"Row {i}: extra_info must be dict")
            continue
        if "index" not in ei:
            errors.append(f"Row {i}: extra_info missing 'index'")
        if "solution" not in ei:
            errors.append(f"Row {i}: extra_info missing 'solution'")

    return errors


def verify_schema(table):
    actual   = table.schema
    expected = PARQUET_SCHEMA
    errors   = []
    for field in expected:
        af = actual.field(field.name)
        ef = field
        if af.type != ef.type:
            errors.append(
                f"  FAIL  '{ef.name}': expected {ef.type}, got {af.type}"
            )
    if errors:
        print("SCHEMA MISMATCH:")
        for e in errors:
            print(e)
        return False
    print("SCHEMA OK — all field types match PARQUET_SCHEMA")
    return True


def main():
    print("=== Step 1: Converting dataset to parquet ===")
    table = convert_dataset_to_parquet()

    print("\n=== Step 2: Loading format schema ===")
    schema = load_format_schema()
    print("Schema:", json.dumps(schema, indent=2))

    print("\n=== Step 3: Verifying schema (pyarrow types) ===")
    schema_ok = verify_schema(table)

    print("\n=== Step 4: Validating content against schema ===")
    import pandas as pd
    df = table.to_pandas()
    errors = validate_against_schema(df, schema)

    if errors:
        print(f"\nVALIDATION FAILED: {len(errors)} error(s)")
        for err in errors[:20]:
            print(err)
        sys.exit(1)
    else:
        print("CONTENT OK — all rows conform to format.json")

    if schema_ok:
        print("\nALL CHECKS PASSED")
    else:
        print("\nSCHEMA CHECK FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
