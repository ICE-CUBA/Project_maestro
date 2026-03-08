# Demo: Landing Page Generator

Generate a complete landing page from a product description. Visual output, clear iterations.

## Run the Demo

```bash
/maestro "Create a landing page for 'Maestro AI' - an autonomous agent that solves complex tasks while you sleep" \
  --eval "bash validate.sh" \
  --max-iter 5 \
  --target 85
```

## What Happens

```
Iteration 1: Basic HTML structure
  Score: 40/100 (missing styling)

Iteration 2: Add CSS, hero section
  Score: 60/100 (no responsive, weak CTA)

Iteration 3: Responsive design, animations
  Score: 75/100 (needs testimonials, footer)

Iteration 4: Full sections, polished
  Score: 90/100 ✓ Target met
```

## Output

Opens `output/index.html` in browser — a complete, deployable landing page.

## Evaluation Criteria

- Has hero section with headline + CTA
- Has feature grid (3+ features)
- Has social proof section
- Responsive (mobile + desktop)
- Valid HTML, no console errors
- Loads under 2 seconds
