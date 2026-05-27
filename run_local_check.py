import sys
import os

# Add the evaluation script path
sys.path.insert(0, "https://raw.githubusercontent.com/hkust-nlp/Toolathlon/main/tasks/finalpool/verl-dataset/evaluation")

# Download and run check_local
import urllib.request
import tempfile

eval_url = "https://raw.githubusercontent.com/hkust-nlp/Toolathlon/main/tasks/finalpool/verl-dataset/evaluation/check_local.py"
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write(urllib.request.urlopen(eval_url).read().decode('utf-8'))
    eval_file = f.name

# Import the module
import importlib.util
spec = importlib.util.spec_from_file_location("check_local", eval_file)
check_local = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_local)

# Run check
agent_workspace = os.environ.get("GITHUB_WORKSPACE", ".")
groundtruth_workspace = os.path.join(agent_workspace, "groundtruth_workspace")

success, message = check_local.check_local(agent_workspace, groundtruth_workspace)
if success:
    print("LOCAL CHECK PASSED")
    sys.exit(0)
else:
    print(f"LOCAL CHECK FAILED: {message}")
    sys.exit(1)
