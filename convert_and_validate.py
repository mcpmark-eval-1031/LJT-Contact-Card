import json
import os
import sys
import pandas as pd
import numpy as np
import requests
from pathlib import Path

# Paths
WORKSPACE = Path("/workspace/agent_workspace")
FORMAT_JSON = WORKSPACE / "format.json"
OUTPUT_PARQUET = WORKSPACE / "verl_deepscaler.parquet"
GROUNDTRUTH_DIR = WORKSPACE / "groundtruth_workspace"
SCHEMA_PATH = WORKSPACE / "format.json"


def download_file(url, dest):
    """Download a file from URL to destination."""
    print(f"Downloading {url} -> {dest}")
    resp = requests.get(url, stream=True, timeout=120)
    resp.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {dest} ({dest.stat().st_size} bytes)")


def ensure_groundtruth():
    """Ensure ground truth files are available."""
    GROUNDTRUTH_DIR.mkdir(parents=True, exist_ok=True)
    gt_json = GROUNDTRUTH_DIR / "deepscaler.json"
    gt_info = GROUNDTRUTH_DIR / "expected_dataset_info.json"

    if not gt_json.exists() or gt_json.stat().st_size < 1000:
        download_file(
            "https://raw.githubusercontent.com/hkust-nlp/Toolathlon/main/tasks/finalpool/verl-dataset/groundtruth_workspace/deepscaler.json",
            gt_json,
        )
    if not gt_info.exists():
        download_file(
            "https://raw.githubusercontent.com/hkust-nlp/Toolathlon/main/tasks/finalpool/verl-dataset/groundtruth_workspace/expected_dataset_info.json",
            gt_info,
        )
    return gt_json, gt_info


def load_format_schema():
    """Load and return the format.json schema."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_against_schema(df, schema):
    """
    Validate each row of the DataFrame against the format.json schema.
    Returns a list of error strings.
    """
    errors = []

    for i in range(len(df)):
        row = df.iloc[i]

        # 1. data_source must be string "DeepScaleR"
        ds = row.get("data_source")
        if not isinstance(ds, str) or ds != "DeepScaleR":
            errors.append(f"Row {i}: data_source must be 'DeepScaleR', got {repr(ds)}")

        # 2. prompt must be a list, first element dict with role=='user' and non-empty content string
        prompt = row.get("prompt")
        try:
            if isinstance(prompt, str):
                prompt = json.loads(prompt)
            elif isinstance(prompt, np.ndarray):
                prompt = prompt.tolist()
        except Exception as e:
            errors.append(f"Row {i}: prompt is not valid JSON: {e}")
            continue

        if not isinstance(prompt, list) or len(prompt) == 0:
            errors.append(f"Row {i}: prompt must be a non-empty list")
            continue

        first = prompt[0]
        if not isinstance(first, dict):
            errors.append(f"Row {i}: prompt[0] must be a dict")
            continue

        if first.get("role") != "user":
            errors.append(f"Row {i}: prompt[0].role must be 'user', got {repr(first.get('role'))}")

        content = first.get("content")
        if not isinstance(content, str) or len(content.strip()) == 0:
            errors.append(f"Row {i}: prompt[0].content must be a non-empty string")

        # 3. ability must be string "math"
        ability = row.get("ability")
        if not isinstance(ability, str) or ability != "math":
            errors.append(f"Row {i}: ability must be 'math', got {repr(ability)}")

        # 4. reward_model must be dict with ground_truth
        rm = row.get("reward_model")
        try:
            if isinstance(rm, str):
                rm = json.loads(rm)
        except Exception as e:
            errors.append(f"Row {i}: reward_model is not valid JSON: {e}")
            continue

        if not isinstance(rm, dict):
            errors.append(f"Row {i}: reward_model must be a dict")
            continue

        if "ground_truth" not in rm:
            errors.append(f"Row {i}: reward_model missing 'ground_truth'")
        elif not isinstance(rm["ground_truth"], str):
            errors.append(f"Row {i}: reward_model.ground_truth must be a string")

        if rm.get("style") != "rule":
            errors.append(f"Row {i}: reward_model.style must be 'rule', got {repr(rm.get('style'))}")

        # 5. extra_info must be dict with index and solution
        ei = row.get("extra_info")
        try:
            if isinstance(ei, str):
                ei = json.loads(ei)
        except Exception as e:
            errors.append(f"Row {i}: extra_info is not valid JSON: {e}")
            continue

        if not isinstance(ei, dict):
            errors.append(f"Row {i}: extra_info must be a dict")
            continue

        if "index" not in ei:
            errors.append(f"Row {i}: extra_info missing 'index'")
        if "solution" not in ei:
            errors.append(f"Row {i}: extra_info missing 'solution'")

    return errors


def convert_dataset_to_parquet():
    """Load ground truth and convert to verl parquet format."""
    gt_json, gt_info = ensure_groundtruth()

    with open(gt_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} items from ground truth")

    records = []
    for idx, item in enumerate(data):
        problem = item.get("problem", "").strip()
        answer = item.get("answer", "").strip()
        solution = item.get("solution", "").strip()

        record = {
            "data_source": "DeepScaleR",
            "prompt": json.dumps([{"role": "user", "content": problem}]),
            "ability": "math",
            "reward_model": json.dumps({"style": "rule", "ground_truth": answer}),
            "extra_info": json.dumps({"index": idx, "solution": solution}),
        }
        records.append(record)

    df = pd.DataFrame(records)
    df.to_parquet(OUTPUT_PARQUET, index=False)
    print(f"Wrote {len(df)} rows to {OUTPUT_PARQUET}")
    return df


def main():
    print("=== Step 1: Converting dataset to parquet ===")
    df = convert_dataset_to_parquet()

    print("\n=== Step 2: Loading format schema ===")
    schema = load_format_schema()
    print("Schema loaded:", json.dumps(schema, indent=2))

    print("\n=== Step 3: Validating against schema ===")
    errors = validate_against_schema(df, schema)

    if errors:
        print(f"\nVALIDATION FAILED: {len(errors)} error(s) found")
        print("=" * 60)
        for err in errors[:50]:  # Show first 50 errors
            print(err)
        if len(errors) > 50:
            print(f"... and {len(errors) - 50} more errors")
        print("=" * 60)
        sys.exit(1)
    else:
        print("\nVALIDATION PASSED: All rows conform to format.json")
        sys.exit(0)


if __name__ == "__main__":
    main()
