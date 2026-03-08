#!/usr/bin/env python3
"""
Skill Generalist — Evaluation Engine

Runs all criteria from eval_criteria.json against current outputs.
Supports three modes:
  1. Script-based: runs user-provided validation script
  2. Criteria-based: runs each criterion check command
  3. Comparison-based: compares output vs expected files

Usage:
  python3 scripts/evaluate.py --workspace workspace/my-task
  python3 scripts/evaluate.py --workspace workspace/my-task --validator validate.sh
  python3 scripts/evaluate.py --workspace workspace/my-task --iteration 3
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_check(check_cmd: str, workspace: str, timeout: int = 30) -> dict:
    """Run a single check command, return result."""
    try:
        result = subprocess.run(
            check_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=workspace
        )
        passed = result.returncode == 0
        return {
            "passed": passed,
            "stdout": result.stdout.strip()[-500:],  # truncate
            "stderr": result.stderr.strip()[-500:],
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"passed": False, "stdout": "", "stderr": "TIMEOUT", "exit_code": -1}
    except Exception as e:
        return {"passed": False, "stdout": "", "stderr": str(e), "exit_code": -1}


def evaluate_with_criteria(workspace: str) -> dict:
    """Evaluate using criteria from eval_criteria.json."""
    criteria_path = os.path.join(workspace, "eval_criteria.json")
    if not os.path.exists(criteria_path):
        return {
            "score": 0,
            "max_score": 0,
            "details": "No eval_criteria.json found",
            "criteria_results": [],
            "errors": ["eval_criteria.json not found — agent must create it in Phase 0"]
        }

    with open(criteria_path) as f:
        config = json.load(f)

    criteria = config.get("criteria", [])
    if not criteria:
        return {
            "score": 0,
            "max_score": 0,
            "details": "No criteria defined yet",
            "criteria_results": [],
            "errors": ["criteria list is empty — agent must populate it"]
        }

    results = []
    total_weight = 0
    earned_weight = 0

    for c in criteria:
        name = c.get("name", "unnamed")
        check = c.get("check", "")
        weight = c.get("weight", 1)
        total_weight += weight

        if not check:
            results.append({"name": name, "passed": False, "error": "no check command"})
            continue

        result = run_check(check, workspace)
        result["name"] = name
        result["weight"] = weight
        results.append(result)

        if result["passed"]:
            earned_weight += weight

    score = int(100 * earned_weight / total_weight) if total_weight > 0 else 0

    errors = []
    for r in results:
        if not r["passed"]:
            error_msg = r.get("stderr", "") or r.get("error", "unknown")
            errors.append(f"[{r['name']}] {error_msg}")

    return {
        "score": score,
        "max_score": 100,
        "passed_criteria": sum(1 for r in results if r["passed"]),
        "total_criteria": len(results),
        "criteria_results": results,
        "errors": errors
    }


def evaluate_with_validator(workspace: str, validator: str) -> dict:
    """Evaluate using a user-provided validation script."""
    result = run_check(f"bash {validator}", workspace, timeout=60)

    # Try to parse output as JSON
    try:
        score_data = json.loads(result["stdout"])
        if "score" in score_data:
            return score_data
    except (json.JSONDecodeError, TypeError):
        pass

    # Try to parse as plain number
    try:
        score = float(result["stdout"].strip().split('\n')[-1])
        return {
            "score": int(score),
            "max_score": 100,
            "details": result["stderr"],
            "errors": [] if result["passed"] else [result["stderr"]]
        }
    except (ValueError, IndexError):
        pass

    # Fallback: binary pass/fail
    return {
        "score": 100 if result["passed"] else 0,
        "max_score": 100,
        "details": result["stdout"],
        "errors": [] if result["passed"] else [result["stderr"] or "validator failed"]
    }


def main():
    parser = argparse.ArgumentParser(description="Skill Generalist Evaluator")
    parser.add_argument("--workspace", required=True, help="Path to workspace")
    parser.add_argument("--validator", default=None, help="Path to custom validation script")
    parser.add_argument("--iteration", type=int, default=None, help="Current iteration number")
    args = parser.parse_args()

    workspace = args.workspace

    # Run evaluation
    if args.validator and os.path.exists(args.validator):
        eval_result = evaluate_with_validator(workspace, args.validator)
    else:
        eval_result = evaluate_with_criteria(workspace)

    eval_result["timestamp"] = datetime.now().isoformat()
    eval_result["iteration"] = args.iteration

    # Update progress.json
    progress_path = os.path.join(workspace, "progress.json")
    if os.path.exists(progress_path):
        with open(progress_path) as f:
            progress = json.load(f)

        iteration_record = {
            "iteration": args.iteration or len(progress["iterations"]) + 1,
            "score": eval_result["score"],
            "timestamp": eval_result["timestamp"],
            "errors_count": len(eval_result.get("errors", []))
        }
        progress["iterations"].append(iteration_record)

        if eval_result["score"] > progress["best_score"]:
            progress["best_score"] = eval_result["score"]
            progress["best_iteration"] = iteration_record["iteration"]

        progress["status"] = "running"

        with open(progress_path, "w") as f:
            json.dump(progress, f, indent=2)

    # Append to experiment log
    log_path = os.path.join(workspace, "experiment_log.md")
    with open(log_path, "a") as f:
        f.write(f"\n## Iteration {args.iteration or '?'} — Score: {eval_result['score']}/100\n")
        f.write(f"- Time: {eval_result['timestamp']}\n")
        if eval_result.get("passed_criteria") is not None:
            f.write(f"- Criteria: {eval_result['passed_criteria']}/{eval_result['total_criteria']} passed\n")
        if eval_result.get("errors"):
            f.write(f"- Errors ({len(eval_result['errors'])}):\n")
            for err in eval_result["errors"][:5]:  # limit to 5
                f.write(f"  - {err[:200]}\n")
        f.write("\n")

    # Output
    print(json.dumps(eval_result, indent=2))


if __name__ == "__main__":
    main()
