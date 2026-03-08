# Project Maestro

**One Command. Walk Away. Work Gets Done.**

Project Maestro is an autonomous execution loop that solves complex goals, learns from every failure, and turns each solution into a reusable skill. It bridges the gap between capable AI agents and reliable, production-grade workflows.

## The Problem

AI agents are powerful, but they still fail at actual work:

- They don't follow deterministic workflows
- They lack tacit knowledge accumulated from experience
- They can't learn from failures and apply lessons to future tasks

The gap isn't capability. It's procedure, memory, and feedback. That's where Project Maestro helps.

## How It Works

```bash
/maestro "goal" --eval "bash validate.sh" --max-iter 10 --target 90
```

You type this once. Then walk away.

The agent executes a closed-loop cycle:

1. **Assess + Research** - Understand the problem, find viable approaches
2. **Execute** - Implement the current approach
3. **Score** - Run evaluation, measure progress (0-100)
4. **Reflect** - Diagnose failures, extract learnings
5. **Decide** - Continue silently, pivot strategy, or checkpoint for input
6. **Deliver** - Output solution and install reusable skill

You are notified only when a decision is needed or the goal is achieved.

## Use Case: Resource Allocation

**Scenario:** Friday 9 AM. 26 engineers, 12 projects, 4 at risk. Needs risk mitigation.

**Without Project Maestro:**  
Project manager manually reviews each project's staffing, compares against deadlines, makes allocation decisions in a spreadsheet. Inconsistent. Slow. Error-prone.

**With Project Maestro:**  
Agent ingests all project states, models resource contention, proposes reallocation ranked by risk-adjusted impact, outputs a decision memo.

**Evaluation criteria:** At-risk projects <= 2, no unplanned fires in next sprint.

**Result:** 3 iterations. Risk mitigated from 4 at-risk to 1 at-risk.

The skill builds a model of your team's actual throughput over time, improving allocation quality with every weekly run.

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--eval` | Required | Command that outputs a score (0-100) |
| `--max-iter` | 10 | Maximum iterations before checkpoint |
| `--target` | 90 | Score threshold for success |

## Evaluation Formats

The evaluation command must output a score. Supported formats:

- Exit code: 0 = pass (100), non-zero = fail (0)
- JSON output: `{"score": N}`
- Numeric last line: `85`

## Workspace Structure

```
workspace/<task>/
├── progress.json       # Score history, iteration state
├── learnings.md        # Accumulated insights
├── experiment_log.md   # Full execution timeline
├── approaches/         # Versioned implementation attempts
├── final/              # Best result
└── generated-skill/    # Reusable skill package
```

## Skill Generation

Upon successful completion, Project Maestro generates a reusable skill containing:

- Step-by-step procedure derived from the successful approach
- Common pitfalls and their solutions
- Evaluation criteria that worked
- Reference commands and configurations

Generated skills are installed for future use. The next time you encounter a similar problem, the agent already knows how to solve it.

## Design Principles

1. **Autonomous by default** - Agent continues without prompting unless blocked
2. **Evaluation-driven** - Every iteration is scored; no blind iteration
3. **Learning accumulates** - Insights persist across iterations in files
4. **Fail fast, pivot faster** - Plateau detection triggers strategy change
5. **Skills as artifacts** - Solutions become reusable organizational knowledge

## Why Project Maestro

Project Maestro closes the gap between a capable agent and a reliable operator. It equips AI with the structure, context, and follow-through to keep work on track and mitigate risks before they escalate.

## References

See `references/loop-protocol.md` for theoretical foundation and implementation details.

## License

MIT
