#!/bin/bash
# Initialize workspace for Skill Generalist pipeline
# Usage: bash scripts/init_workspace.sh <task-name>

TASK_NAME=${1:-"task"}
WORKSPACE="./workspace/${TASK_NAME}"

if [ -d "$WORKSPACE" ]; then
    echo "Workspace already exists at $WORKSPACE"
    echo "Use --force to reinitialize"
    if [ "$2" != "--force" ]; then
        exit 0
    fi
    rm -rf "$WORKSPACE"
fi

mkdir -p "$WORKSPACE"/{approaches,final,generated-skill,input,logs}

# Progress tracking
cat > "$WORKSPACE/progress.json" << 'EOF'
{
  "task_name": "TASK_NAME_PLACEHOLDER",
  "status": "initialized",
  "iterations": [],
  "best_score": 0,
  "best_iteration": null,
  "checkpoints": [],
  "started_at": "TIMESTAMP_PLACEHOLDER"
}
EOF

# Replace placeholders (macOS compatible)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/TASK_NAME_PLACEHOLDER/$TASK_NAME/" "$WORKSPACE/progress.json"
    sed -i '' "s/TIMESTAMP_PLACEHOLDER/$(date -Iseconds)/" "$WORKSPACE/progress.json"
else
    sed -i "s/TASK_NAME_PLACEHOLDER/$TASK_NAME/" "$WORKSPACE/progress.json"
    sed -i "s/TIMESTAMP_PLACEHOLDER/$(date -Iseconds)/" "$WORKSPACE/progress.json"
fi

# Evaluation criteria (to be filled by agent in Phase 0)
cat > "$WORKSPACE/eval_criteria.json" << 'EOF'
{
  "criteria": [],
  "target_score": 90,
  "max_iterations": 10,
  "plateau_threshold": 2,
  "notes": "Agent should populate criteria during Phase 0 ASSESS"
}
EOF

# Learnings file (persistent across iterations)
cat > "$WORKSPACE/learnings.md" << 'EOF'
# Accumulated Learnings

> This file grows with every iteration. The agent reads it before each
> attempt to avoid repeating mistakes and build on what works.

EOF

# Research notes
cat > "$WORKSPACE/research.md" << 'EOF'
# Research Notes

> Approaches discovered through research, with pros/cons/insights.

EOF

# Experiment log (append-only timeline)
cat > "$WORKSPACE/experiment_log.md" << 'EOF'
# Experiment Log

> Chronological record of every action, score, and decision.

EOF

echo "✅ Workspace initialized at $WORKSPACE"
echo ""
echo "Structure:"
find "$WORKSPACE" -type f | sort | sed "s|$WORKSPACE/|  |"
