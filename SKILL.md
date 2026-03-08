---
name: skill-generalist
description: >
  Autonomous problem-solving pipeline. User gives goal + eval command,
  then walks away. Agent researches, implements, evaluates, reflects,
  and iterates autonomously. Proactively notifies user only on plateau
  or completion. Outputs both the solution AND a reusable skill.
  
  Triggers: "/generalist", "figure it out", "make this work", 
  "build me X", "solve this", any task with evaluation criteria.
---

# Skill Generalist

**One command. Walk away. Get results + reusable skill.**

## Invocation

```
/generalist "<goal>" [--eval "<command>"] [--max-iter N] [--target N]
```

**Examples:**
```
/generalist "Extract metadata from these 20 markdown files to JSON" --eval "bash validate.sh"
/generalist "Deploy this app to production" --eval "curl -s localhost:3000 | grep 'OK'"
/generalist "Make all tests pass" --eval "npm test" --max-iter 15
```

**Defaults:** `--max-iter 10`, `--target 90` (score out of 100)

---

## What Happens After You Walk Away

```
USER: /generalist "goal" --eval "bash validate.sh"

AGENT (autonomous, no user input needed):
  │
  ├─ 1. ASSESS: Analyze complexity, init workspace
  │
  ├─ 2. RESEARCH: Find viable approaches
  │
  └─ 3. LOOP (runs silently):
       │
       ├─→ EXECUTE: Implement current approach
       ├─→ EVALUATE: Run eval command, get score
       ├─→ REFLECT: Diagnose failures, write learnings
       ├─→ DECIDE:
       │     ├─ Score improving? → continue (no notification)
       │     ├─ Need research? → research, then continue
       │     ├─ Target met? → NOTIFY user: "Done! Score X"
       │     └─ Plateau? → NOTIFY user: "Stuck at X, options..."
       │
       └─→ (repeat until target, plateau, or max iterations)

USER (only responds to notifications):
  │
  └─ "Continue" / "Deliver" / "Adjust goal"

AGENT:
  │
  └─ 4. DELIVER: Final result + generated skill
```

**Key point:** Agent NOTIFIES user proactively. User doesn't poll.

---

## Live Progress Stream

**Stream status updates. Don't wait for replies.**

每个阶段完成后，立即输出状态行，然后继续：

```
📋 ASSESS — [complexity], 预计[N]轮

🔍 RESEARCH — 找到[N]个方案: [list]

⚡ Iteration 1/10
   Approach: [name]
   Running... ✓
   Score: 48/100
   Reflection: [一句话]

⚡ Iteration 2/10
   Approach: [name]
   Running... ✓
   Score: 80/100 ↑32
   Reflection: [一句话]

🔔 CHECKPOINT — [reason]
   [options]
```

**Rules:**
1. 输出状态后**不要等用户回复**，直接继续下一步
2. 状态是**报告**，不是**提问**
3. 只有 🔔 CHECKPOINT 才需要用户选择
4. 用户全程能看到进度，但不需要动手

**Format per iteration:**
```
⚡ Iteration N/max — [approach] — Score: X/100 [↑delta] — [reflection]
```

---

## The Autonomous Loop (Phase 3)

This is the core. Runs WITHOUT user interaction until checkpoint.

### For each iteration:

**EXECUTE:**
```bash
# Implement approach, save to workspace/approaches/approach-N-vM/
```

**EVALUATE:**
```bash
# Run the user's eval command
bash validate.sh  # or whatever --eval specifies
# Parse output for score (0-100)
```

**REFLECT:**
For each failure, determine:
- **Bug?** → fix directly, continue
- **Method limitation?** → try new approach
- **Knowledge gap?** → research first
- **Ambiguous task?** → checkpoint user

Write to `learnings.md`:
```markdown
- [timestamp] LEARNED: <specific actionable insight>
```

**DECIDE:**
```
Score >= target?           → DELIVER
Score improving?           → continue silently
Plateau (2+ no improve)?   → NOTIFY user
Max iterations?            → NOTIFY user
Need clarification?        → NOTIFY user
```

---

## Checkpoints (Proactive Notifications)

**Only notify when:**
1. ✅ Target met → "Done! Score X/100. Delivering..."
2. 📊 Plateau → "Stuck at X after N attempts. Options: A/B/C"
3. ❓ Ambiguity → "Need clarification: <question>"
4. ⏱️ Max iterations → "Hit limit. Best: X. Continue or deliver?"

**Notification format:**
```
🔔 CHECKPOINT — [reason]

Score: 85/100 after 5 iterations
Progress: 45 → 62 → 78 → 85 → 85 (plateau)

What's working: [summary]
What's failing: [specific issues]

Options:
A) Continue — I'll try [specific new approach]
B) Deliver current result (85%)
C) Adjust goal to [suggestion]
```

User replies → agent resumes or delivers.

---

## Workspace Structure

```bash
bash scripts/init_workspace.sh <task-name>
```

Creates:
```
workspace/<task>/
├── progress.json       # Score history, iteration tracking
├── learnings.md        # Accumulated insights (persistent memory)
├── experiment_log.md   # Full timeline
├── approaches/         # Each attempt versioned
│   ├── approach-1-v1/
│   └── approach-2-v1/
├── final/              # Best result
└── generated-skill/    # Output skill
    └── SKILL.md
```

---

## Evaluation Design

If user provides `--eval`:
- Use directly, parse output for score

If user provides expected outputs:
- Generate comparison script

If neither:
- YOU design eval criteria, confirm with user ONCE, then proceed

**Eval must output a score (0-100).** Either:
- Exit code 0 = pass (100), else fail (0)
- JSON with `{"score": N}`
- Last line is a number

---

## Deliver

When done, **展示一切，不让用户翻文件**:

### Step 1: Show Results
```
✅ DELIVERED — Score: 95/100 after 4 iterations

📈 Progress: 45 → 68 → 85 → 95
📁 Output: workspace/final/ (20 files)
```

### Step 2: Show Learnings (摘要，不是让用户去读文件)
```
📊 What I Learned:
• [insight 1 from learnings.md]
• [insight 2]
• [insight 3]
• [key pitfall avoided]
```

### Step 3: Show Generated Skill (核心步骤，不是全文)
```
🧠 Generated Skill: <skill-name>

When to use: [trigger description]

Key steps:
1. [step 1]
2. [step 2]
3. [step 3]

Pitfalls to avoid:
• [pitfall 1]
• [pitfall 2]
```

### Step 4: Auto-Install Skill
```bash
# Agent自动执行
mkdir -p ~/.openclaw/skills/<skill-name>
cp -r workspace/generated-skill/* ~/.openclaw/skills/<skill-name>/
```

### Step 5: Confirm
```
✅ Skill installed to ~/.openclaw/skills/<skill-name>/
   下次遇到类似问题，我会自动使用这个skill，不需要重新探索。
```

**完整闭环：探索 → 学习 → 固化 → 复用**

---

## Rules

1. **Stream progress, don't ask** — output status after each iteration, don't wait for reply
2. **Status ≠ Question** — user sees progress but doesn't need to respond
3. **Only CHECKPOINT needs input** — that's the only time you wait
4. **Always evaluate** — no blind iteration
5. **Always write learnings** — files > context memory
6. **Plateau = CHECKPOINT** — don't keep doing the same thing silently
7. **Research when stuck** — search, then continue (don't ask)
8. **Deliver shows everything** — learnings摘要 + skill核心步骤，用户不需要打开任何文件
9. **Auto-install skill** — 复制到 ~/.openclaw/skills/，完成闭环

---

## References

See `references/loop-protocol.md` for:
- Theoretical foundation (GEPA, Letta, SkillsBench)
- Reflection quality guidelines
- When to research vs iterate
- Complexity-adaptive behavior
