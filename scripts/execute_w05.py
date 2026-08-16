import io
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score, average_precision_score, precision_score, recall_score, f1_score

notebook_path = Path("work/notebooks/w05_model.ipynb")
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Helper to capture execution output
def capture_exec(code_str, global_vars):
    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    sys.stdout = redirected_output
    try:
        exec(code_str, global_vars)
        output_text = redirected_output.getvalue()
    except Exception as e:
        output_text = f"Error: {e}"
    finally:
        sys.stdout = old_stdout
    return output_text

global_scope = {}
exec_count = 1

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        code_text = "".join(cell["source"])
        out_text = capture_exec(code_text, global_scope)
        cell["execution_count"] = exec_count
        cell["outputs"] = [
            {
                "name": "stdout",
                "output_type": "stream",
                "text": [line + "\n" for line in out_text.splitlines()]
            }
        ]
        exec_count += 1

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Executed and saved w05_model.ipynb successfully!")
