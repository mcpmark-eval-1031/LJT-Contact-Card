"""
convert_and_validate_fixed.py

修复说明
--------
原脚本 convert_and_validate.py 将 prompt / reward_model / extra_info
全部通过 json.dumps() 序列化为字符串再存入 parquet，导致：

  • pandas 读回后这三列的类型是 string，而非 list / dict
  • check_local.py 虽能兼容字符串（内部 json.loads 兜底），但
    format.json 规范的字段级 schema 要求这些列以原生嵌套类型存储

本脚本改用 pyarrow 显式 schema，确保：
  data_source : utf8 (string)
  prompt      : list<struct<role:utf8, content:utf8>>
  ability     : utf8 (string)
  reward_model: struct<style:utf8, ground_truth:utf8>
  extra_info  : struct<index:int64, solution:utf8>
"""
import json
import os
import sys
import requests
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

WORKSPACE = Path(os.environ.get("GITHUB_WORKSPACE", "."))
OUTPUT_PARQUET = WORKSPACE / "verl_deepscaler.parquet"
GROUNDTRUTH_DIR = WORKSPACE / "groundtruth_workspace"
GT_JSON = GROUNDTRUTH_DIR / "deepscaler.json"
GT_INFO = GROUNDTRUTH_DIR / "expected_dataset_info.json"

# ── pyarrow schema（严格对齐 format.json） ─────────────────────────────────
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


def ensure_groundtruth():
    """下载 ground truth 数据文件（如不存在）"""
    GROUNDTRUTH_DIR.mkdir(parents=True, exist_ok=True)
    if not GT_JSON.exists() or GT_JSON.stat().st_size < 1000:
        print("Downloading deepscaler.json ...")
        r = requests.get(
            "https://raw.githubusercontent.com/hkust-nlp/Toolathlon/main/"
            "tasks/finalpool/verl-dataset/groundtruth_workspace/deepscaler.json",
            timeout=120,
        )
        r.raise_for_status()
        GT_JSON.write_bytes(r.content)
        print(f"  -> {GT_JSON}  ({GT_JSON.stat().st_size:,} bytes)")
    else:
        print(f"  [skip]  {GT_JSON}  already exists")
    if not GT_INFO.exists():
        print("Downloading expected_dataset_info.json ...")
        r = requests.get(
            "https://raw.githubusercontent.com/hkust-nlp/Toolathlon/main/"
            "tasks/finalpool/verl-dataset/groundtruth_workspace/expected_dataset_info.json",
            timeout=120,
        )
        r.raise_for_status()
        GT_INFO.write_bytes(r.content)
        print(f"  -> {GT_INFO}")
    else:
        print(f"  [skip]  {GT_INFO}  already exists")


def load_groundtruth():
    with open(GT_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def convert_to_parquet():
    """
    用 pyarrow 直接构建 Table，保证 prompt / reward_model / extra_info
    以原生嵌套类型（list<struct> / struct）写入 parquet。
    """
    data = load_groundtruth()
    print(f"Loaded {len(data)} items from ground truth")

    # 逐列收集数据
    data_sources   = []
    prompts        = []  # list of list of struct dicts
    abilities      = []
    reward_models  = []  # list of struct dicts
    extra_infos    = []  # list of struct dicts

    for idx, item in enumerate(data):
        problem   = item.get("problem",  "").strip()
        answer    = item.get("answer",   "").strip()
        solution  = item.get("solution", "").strip()

        data_sources.append("DeepScaleR")
        prompts.append([{"role": "user", "content": problem}])
        abilities.append("math")
        reward_models.append({"style": "rule", "ground_truth": answer})
        extra_infos.append({"index": idx, "solution": solution})

    # 构建 pyarrow arrays
    arr_data_source = pa.array(data_sources,  type=pa.utf8())
    arr_prompt      = pa.array(prompts,        type=pa.list_(pa.struct([
                                                    pa.field("role",    pa.utf8()),
                                                    pa.field("content", pa.utf8()),
                                                  ])))
    arr_ability     = pa.array(abilities,      type=pa.utf8())
    arr_reward      = pa.array(reward_models,  type=pa.struct([
                                                    pa.field("style",        pa.utf8()),
                                                    pa.field("ground_truth", pa.utf8()),
                                                  ]))
    arr_extra       = pa.array(extra_infos,    type=pa.struct([
                                                    pa.field("index",    pa.int64()),
                                                    pa.field("solution", pa.utf8()),
                                                  ]))

    table = pa.table(
        {
            "data_source":  arr_data_source,
            "prompt":       arr_prompt,
            "ability":      arr_ability,
            "reward_model": arr_reward,
            "extra_info":   arr_extra,
        },
        schema=PARQUET_SCHEMA,
    )

    pq.write_table(table, OUTPUT_PARQUET)
    print(f"Wrote {table.num_rows:,} rows  ({OUTPUT_PARQUET})")
    return table


def verify_schema(table):
    """逐字段校验 pyarrow schema 与 PARQUET_SCHEMA 是否一致"""
    actual   = table.schema
    expected = PARQUET_SCHEMA
    errors   = []

    for field in expected:
        af = actual.field(field.name)
        ef = field
        if af.type != ef.type:
            errors.append(
                f"  FAIL  field '{ef.name}': expected {ef.type}, got {af.type}"
            )

    if errors:
        print("SCHEMA MISMATCH:")
        for e in errors:
            print(e)
        return False
    else:
        print("SCHEMA OK — all field types match PARQUET_SCHEMA")
        return True


def verify_content(table):
    """抽样验证内容语义（与 check_local.py 逻辑对齐）"""
    import pandas as pd
    df = table.to_pandas()
    n = len(df)
    print(f"Rows: {n}")

    for i in range(min(100, n)):
        row = df.iloc[i]
        if row["data_source"] != "DeepScaleR":
            print(f"  Row {i}: data_source != 'DeepScaleR'")
            return False
        if row["ability"] != "math":
            print(f"  Row {i}: ability != 'math'")
            return False
        prompt = row["prompt"]
        if not isinstance(prompt, list) or not prompt:
            print(f"  Row {i}: prompt is not a non-empty list")
            return False
        if prompt[0].get("role") != "user" or not prompt[0].get("content"):
            print(f"  Row {i}: prompt[0] malformed")
            return False
        rm = row["reward_model"]
        if not isinstance(rm, dict) or rm.get("style") != "rule" or "ground_truth" not in rm:
            print(f"  Row {i}: reward_model malformed")
            return False
        ei = row["extra_info"]
        if not isinstance(ei, dict) or "index" not in ei or "solution" not in ei:
            print(f"  Row {i}: extra_info malformed")
            return False

    print("CONTENT OK — sampled rows match format.json semantics")
    return True


def main():
    print("=" * 60)
    print("Step 1: Ensuring groundtruth files")
    print("=" * 60)
    ensure_groundtruth()

    print()
    print("=" * 60)
    print("Step 2: Converting to parquet (native pyarrow types)")
    print("=" * 60)
    table = convert_to_parquet()

    print()
    print("=" * 60)
    print("Step 3: Verifying schema")
    print("=" * 60)
    schema_ok = verify_schema(table)

    print()
    print("=" * 60)
    print("Step 4: Verifying content (sample)")
    print("=" * 60)
    content_ok = verify_content(table)

    print()
    print("=" * 60)
    if schema_ok and content_ok:
        print("ALL CHECKS PASSED")
    else:
        print("CHECKS FAILED — see errors above")
        sys.exit(1)


if __name__ == "__main__":
    main()
