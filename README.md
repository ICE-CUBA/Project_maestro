# Skill Generalist

An autonomous problem-solving pipeline for AI agents. Given a goal and evaluation criteria, the agent researches, implements, evaluates, and iterates without human intervention until the target is met or a checkpoint is reached.

## Overview

Skill Generalist transforms vague tasks into solved problems and reusable skills. The agent operates in a closed loop:

1. **Assess** - Analyze task complexity, initialize workspace
2. **Research** - Find viable approaches via search or documentation
3. **Execute** - Implement the current approach
4. **Evaluate** - Run evaluation command, obtain score (0-100)
5. **Reflect** - Diagnose failures, extract learnings
6. **Decide** - Continue, pivot, or checkpoint based on progress
7. **Deliver** - Output solution and generate reusable skill

The user is notified only at checkpoints (target met, plateau detected, or clarification needed).

## Usage

```
/generalist "<goal>" --eval "<command>" [--max-iter N] [--target N]
```

### Examples

```bash
# Extract structured data from documents
/generalist "Parse these 50 PDFs into JSON" --eval "python validate.py"

# Fix failing tests
/generalist "Make all tests pass" --eval "npm test" --max-iter 15

# Deploy application
/generalist "Deploy to production" --eval "curl -s https://app.example.com/health"
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--eval` | Required | Command that outputs a score (0-100) |
| `--max-iter` | 10 | Maximum iterations before checkpoint |
| `--target` | 90 | Score threshold for success |

## How It Works

### Evaluation

The evaluation command must output a score. Supported formats:

- Exit code: 0 = pass (100), non-zero = fail (0)
- JSON output: `{"score": N}`
- Numeric last line: `85`

### Checkpoints

The agent notifies the user when:

- Target score is achieved
- Progress plateaus (2+ iterations without improvement)
- Maximum iterations reached
- Clarification is required

### Skill Generation

Upon successful completion, the agent generates a reusable skill containing:

- Step-by-step procedure
- Common pitfalls and solutions
- Evaluation criteria
- Reference commands

Generated skills are installed to `~/.openclaw/skills/` for future use.

## Workspace Structure

```
workspace/<task>/
├── progress.json       # Score history, iteration state
├── learnings.md        # Accumulated insights
├── experiment_log.md   # Full execution timeline
├── approaches/         # Versioned implementation attempts
├── final/              # Best result
└── generated-skill/    # Output skill package
```

## Design Principles

1. **Autonomous by default** - Agent continues without prompting unless blocked
2. **Evaluation-driven** - Every iteration is scored; no blind progress
3. **Learning accumulates** - Insights persist across iterations in files
4. **Fail fast, pivot faster** - Plateau detection triggers strategy change
5. **Skills as artifacts** - Solutions become reusable procedures

## References

- `references/loop-protocol.md` - Theoretical foundation and implementation details
- Based on research from GEPA, Letta, and SkillsBench

## License

MIT
