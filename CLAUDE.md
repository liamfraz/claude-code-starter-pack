# Claude Code Instructions

## How I Work
- **Simplicity first** — minimal changes, minimal code. Don't over-engineer
- **Prove it works** — run tests and show output before claiming something is done
- **No laziness** — find root causes, not temporary fixes
- **Be direct** — short responses, skip the preamble

## Workflow
- For non-trivial tasks (3+ steps), enter plan mode first
- Break work into small, verifiable steps
- Run tests after making changes
- Commit with clear messages explaining *why*, not just *what*

## Rules
- Never hardcode secrets or API keys — use environment variables
- Don't create unnecessary files — prefer editing existing ones
- Keep files under 500 lines — split into modules if needed
- Ask before running destructive operations (deleting files, force pushing, etc.)

## Git
- Create new commits rather than amending existing ones
- Never force push without asking first
- Write concise commit messages (1-2 sentences)

## When Things Break
- Read the actual error message
- Check the logs
- Debug the code
- Don't blame caches, deployment lag, or framework bugs without evidence
