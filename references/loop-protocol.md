# Loop Protocol Reference

> Read this for detailed guidance on the autonomous iteration loop.

## Theoretical Foundation

This pipeline is inspired by two research directions:

**GEPA (ICLR 2026 Oral):** Reflective prompt evolution that outperforms RL.
Key insight: natural language reflection on trajectories is more sample-efficient
than scalar reward signals. GEPA achieves large gains with 100-500 evaluations
vs 10,000+ for RL.

**Letta Skill Learning:** Post-trajectory skill generation that improves agent
performance by 21-36%. Key insight: skills generated AFTER attempting a task
(post-trajectory) are effective, while skills generated BEFORE (pre-trajectory)
are not.

**SkillsBench Finding:** Self-generated skills provide -1.3pp average benefit.
BUT this measures pre-trajectory generation. Our pipeline uses post-trajectory
iterative generation with structured reflection, which is fundamentally different.

## Loop Invariants

Every iteration must maintain these invariants:

1. `learnings.md` is read at the start and written at the end
2. `progress.json` has the score recorded
3. `experiment_log.md` has a new entry
4. Each approach version has its own directory

## Reflection Quality

The quality of reflection determines the quality of the next iteration.
Bad reflection: "It didn't work, I'll try harder"
Good reflection: "Criterion X failed because function Y returned Z instead
of W. Root cause: the library doesn't handle edge case Q. I need to either
find a library that handles Q or write a custom handler."

**Reflection template:**
```
1. Score: [X/100]
2. What improved since last iteration: [specific]
3. What still fails: [specific criteria with specific errors]
4. Root cause analysis: [why each failure happens]
5. Hypothesis for next iteration: [specific change that should fix it]
6. Confidence: [high/medium/low] — if low, consider researching before trying
```

## When to Research vs When to Iterate

ITERATE when:
- You know what's wrong and how to fix it
- The fix is a code change (bug, missing handler, wrong parameter)
- Score improved last round (momentum)

RESEARCH when:
- You don't know WHY something fails
- You've hit the same error twice with different approaches
- The fix requires knowledge you don't have (new library, new technique)
- Score hasn't improved in 2+ iterations

## Complexity-Adaptive Behavior

### Simple Tasks (est. 1-3 iterations)
- Skip multi-approach exploration
- Research → implement → evaluate → fix → done
- Don't over-engineer the evaluation

### Medium Tasks (est. 3-7 iterations)
- Quick prototype 2 approaches → pick winner → iterate
- Evaluation should have 3-5 criteria
- Research when stuck, not every iteration

### Complex Tasks (est. 5-10+ iterations)
- Decompose into subtasks FIRST
- Each subtask gets its own mini-loop
- Integration testing after subtasks are individually solved
- May need multiple checkpoints with user

## Scoring Best Practices

- Weighted criteria: core functionality > edge cases > polish
- Score should be monotonically improvable (no "all or nothing" criteria)
- Include partial credit where possible
- If score seems stuck at 0, the evaluation might be wrong — debug eval first

## Anti-Patterns to Avoid

1. **Iterating without evaluating**: "Let me try this..." without measuring
2. **Evaluating without reflecting**: Running the score but not diagnosing WHY
3. **Reflecting without acting**: Writing long analysis but not changing anything
4. **Changing everything at once**: Make one change per iteration to know what helped
5. **Ignoring accumulated learnings**: Not reading learnings.md before each attempt
6. **Over-iterating on diminishing returns**: Going from 95 to 96 isn't worth 5 iterations
