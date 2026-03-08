#!/usr/bin/env python3
"""
Skill Generalist — Progress Checker & Plateau Detection

Reads progress.json, detects plateau, reports status.

Usage:
  python3 scripts/check_progress.py --workspace workspace/my-task
"""

import argparse
import json
import sys
from pathlib import Path


def check_progress(workspace: str, plateau_threshold: int = 2) -> dict:
    """Analyze progress and detect plateau."""
    progress_path = Path(workspace) / "progress.json"

    if not progress_path.exists():
        return {"status": "error", "message": "progress.json not found"}

    with open(progress_path) as f:
        progress = json.load(f)

    iterations = progress.get("iterations", [])

    if len(iterations) == 0:
        return {
            "status": "not_started",
            "total_iterations": 0,
            "message": "No iterations yet"
        }

    if len(iterations) == 1:
        return {
            "status": "running",
            "total_iterations": 1,
            "best_score": iterations[0]["score"],
            "latest_score": iterations[0]["score"],
            "score_history": [iterations[0]["score"]],
            "message": "Only 1 iteration — too early to detect plateau"
        }

    scores = [it["score"] for it in iterations]
    best_score = max(scores)
    latest_score = scores[-1]

    # Plateau detection: last N scores don't improve over previous best
    if len(scores) >= plateau_threshold:
        recent = scores[-plateau_threshold:]
        previous_best = max(scores[:-plateau_threshold]) if len(scores) > plateau_threshold else 0
        is_plateau = max(recent) <= previous_best
    else:
        is_plateau = False

    # Trend: are scores generally going up?
    if len(scores) >= 3:
        recent_avg = sum(scores[-3:]) / 3
        early_avg = sum(scores[:3]) / min(3, len(scores))
        trend = "improving" if recent_avg > early_avg else "flat_or_declining"
    else:
        trend = "too_early"

    # Check if target met
    eval_criteria_path = Path(workspace) / "eval_criteria.json"
    target_score = 90
    max_iterations = 10
    if eval_criteria_path.exists():
        with open(eval_criteria_path) as f:
            config = json.load(f)
            target_score = config.get("target_score", 90)
            max_iterations = config.get("max_iterations", 10)

    target_met = best_score >= target_score
    max_reached = len(iterations) >= max_iterations

    # Determine status
    if target_met:
        status = "target_met"
        message = f"Target score {target_score} achieved! Best: {best_score}"
    elif max_reached:
        status = "max_iterations"
        message = f"Max iterations ({max_iterations}) reached. Best: {best_score}"
    elif is_plateau:
        status = "plateau"
        message = f"Plateau detected — no improvement in last {plateau_threshold} iterations. Best: {best_score}"
    else:
        status = "running"
        message = f"Iteration {len(iterations)}, best score: {best_score}, trend: {trend}"

    return {
        "status": status,
        "total_iterations": len(iterations),
        "best_score": best_score,
        "best_iteration": progress.get("best_iteration"),
        "latest_score": latest_score,
        "target_score": target_score,
        "max_iterations": max_iterations,
        "score_history": scores,
        "trend": trend,
        "is_plateau": is_plateau,
        "target_met": target_met,
        "message": message
    }


def main():
    parser = argparse.ArgumentParser(description="Check progress and detect plateau")
    parser.add_argument("--workspace", required=True, help="Path to workspace")
    parser.add_argument("--plateau-threshold", type=int, default=2,
                        help="Number of non-improving iterations to trigger plateau (default: 2)")
    args = parser.parse_args()

    result = check_progress(args.workspace, args.plateau_threshold)
    print(json.dumps(result, indent=2))

    # Exit code: 0=running, 1=plateau, 2=target_met, 3=max_iterations
    exit_codes = {"running": 0, "not_started": 0, "plateau": 1,
                  "target_met": 2, "max_iterations": 3, "error": 4}
    sys.exit(exit_codes.get(result["status"], 0))


if __name__ == "__main__":
    main()
