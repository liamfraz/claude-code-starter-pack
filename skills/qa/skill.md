---
name: qa
description: Unified quality gate — verifies work is actually done with fresh evidence. Runs tests, takes screenshots, checks file integrity, kills zombies.
---

# QA Verification Skill

Run a verification battery to PROVE work is done. No claims without evidence.

## When to Use
- After completing any implementation task
- When the quality-gate hook blocks your stop
- Before claiming any work is "done", "complete", or "verified"
- Anytime the user says `/qa`

## Workflow

### Step 1: Detect Project Type
Check the working directory:
- `package.json` exists → Node/web project
- `.xlsx` output files modified → Excel/data project
- `requirements.txt` or `pyproject.toml` → Python project
- Can be multiple types simultaneously

### Step 2: Run Verification Battery (SEQUENTIAL — never parallel)

Run each applicable check. Show the ACTUAL command output, not a summary.

#### 2a. Tests
```bash
# Node
npm test 2>&1 | tail -20

# Python
pytest -v 2>&1 | tail -20
```
If no test command exists, note "No test suite configured" — do NOT skip silently.

#### 2b. Build
```bash
# Node
npm run build 2>&1 | tail -20
```

#### 2c. Lint / Typecheck
```bash
# Node
npx tsc --noEmit 2>&1 | tail -10
npm run lint 2>&1 | tail -10
```

#### 2d. File Integrity (xlsx)
For each `.xlsx` file modified in this session:
```bash
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('FILE_PATH')
print(f'OK: {len(wb.sheetnames)} sheets')
for s in wb.sheetnames:
    ws = wb[s]
    print(f'  {s}: {ws.max_row} rows x {ws.max_column} cols')
wb.close()
"
```

#### 2e. Visual Verification (web projects)
Take a Playwright screenshot of the running app:
```python
# Use webapp-testing or playwright-mcp to:
# 1. Navigate to the relevant page
# 2. Take a full-page screenshot
# 3. Read the screenshot with the Read tool
# 4. Describe what you see — specifically call out anything broken
```
Use `browser_snapshot` MCP tool or run a Playwright script locally.

#### 2f. Process Check
```bash
ps aux | grep -E 'python|node|openpyxl|xlsx' | grep -v grep | grep -v 'Claude' || echo "CLEAN: No zombie processes"
```

### Step 3: Report

Output a verification report in this exact format:

```
## QA Verification Report

| Check | Result | Evidence |
|-------|--------|----------|
| Tests | PASS/FAIL/N/A | [command output summary] |
| Build | PASS/FAIL/N/A | [exit code] |
| Lint | PASS/FAIL/N/A | [error count] |
| File integrity | PASS/FAIL/N/A | [sheet count, file size] |
| Visual | PASS/FAIL/N/A | [screenshot description] |
| Processes | CLEAN/DIRTY | [process list or "none"] |

**Overall: PASS / FAIL**
```

### Step 4: Act on Results

- **All PASS**: You may now claim the work is done
- **Any FAIL**: Fix the failing items. Then re-run `/qa`. Do NOT claim done with failures
- **DIRTY processes**: Kill them immediately with `kill -9`, then re-check

## Rules
- NEVER skip a check silently — if it's N/A, say why
- NEVER summarise command output as "passed" without showing it
- NEVER run checks in parallel — sequential only
- If a check fails, fix it BEFORE moving to the next check
