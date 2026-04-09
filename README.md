# Claude Code Starter Pack

Get up and running with Claude Code in under 10 minutes. Includes sensible permissions, a starter CLAUDE.md, and 12 pre-built skills for construction and document work.

## Quick Start

```bash
git clone https://github.com/liamfraz/claude-code-starter-pack.git
cd claude-code-starter-pack
bash setup.sh
```

That's it. The setup script will:
- Install Claude Code (if not already installed)
- Copy permissions so you're not clicking "allow" on every action
- Set up a starter CLAUDE.md with baseline instructions
- Install 12 skills for documents, construction, and project management

## Prerequisites

- macOS, Linux, or Windows (with Git for Windows)
- A Claude Pro, Max, or Team subscription at [claude.ai](https://claude.ai)

## What's Included

### Permissions (settings.json)

Pre-configured to allow common safe operations and block dangerous ones:

| Allowed | Blocked |
|---------|---------|
| Read/write/edit files | `rm -rf` |
| Git (status, add, commit, checkout, pull) | `sudo` |
| npm/node/python commands | `git push --force` |
| File utilities (ls, cp, mv, find, curl) | `git reset --hard` |

Everything not explicitly allowed or blocked will prompt you for approval.

### Skills (12 included)

Skills are specialized prompts that teach Claude specific workflows. These are installed automatically by `setup.sh`:

**Document Handling:**
| Skill | What it does |
|-------|-------------|
| `xlsx` | Read, write, format, and chart spreadsheets |
| `docx` | Create and edit Word documents with formatting |
| `pdf` | Read, merge, split, watermark, OCR PDFs |
| `pptx` | Create and edit PowerPoint presentations |
| `summarize` | Summarize URLs, PDFs, videos, or any file |

**Construction:**
| Skill | What it does |
|-------|-------------|
| `spec-compliance-review` | Check drawings against specs, produce compliance reports |
| `apartment-takeoff` | Extract unit counts and types from GA plan PDFs |
| `drawing-analyzer` | Extract dimensions, annotations, and metadata from drawings |
| `drawing-markup` | Color-code apartment types on floor plan PDFs |
| `pdf-construction` | Process RFIs, submittals, specs, drawing packages |

**Workflow:**
| Skill | What it does |
|-------|-------------|
| `qa` | Verify work is actually done with fresh evidence |
| `orchestrator-mode` | Delegates complex tasks to sub-agents for parallel work |

### Recommended Plugins (install manually)

After running `setup.sh`, open Claude Code and install these plugins:

```
/install-plugin obra/superpowers
```

**Superpowers** adds structured workflows for planning, test-driven development, debugging, and code review. It's the best general-purpose plugin.

## Using Claude Code

### Basic Commands

| Command | What it does |
|---------|-------------|
| `claude` | Start interactive mode |
| `claude "do something"` | One-shot task |
| `/help` | Show all commands |
| `/compact` | Compress conversation to save context |
| `Shift+Tab` | Toggle auto-accept mode |
| `Ctrl+D` or `exit` | Quit |

### Example Prompts

**General:**
```
What does this project do?
Summarize this PDF for me
Create a spreadsheet from this data
```

**Construction:**
```
Review these drawings against the acoustic spec and produce a compliance report
Do a takeoff of all apartments from these GA plans
Mark up the floor plans with color-coded unit types
```

**Documents:**
```
Create a Word doc report with these findings
Merge these 5 PDFs into one
Read this Excel file and add a summary sheet
```

### Tips

1. **Just talk naturally** — no special syntax needed
2. **Point it at files** — "read the spec PDF in my Downloads folder"
3. **Let it run commands** — it'll ask permission for anything risky
4. **Use skills by name** — "use the apartment-takeoff skill on these plans"
5. **Ask it to explain** — "what does this spreadsheet contain?"

## Customization

### Adjusting Permissions

Edit `~/.claude/settings.json` to add or remove allowed commands:

```json
{
  "permissions": {
    "allow": ["Bash(your-command *)"],
    "deny": ["Bash(dangerous-command *)"]
  }
}
```

### Adding Your Own Instructions

Edit `~/.claude/CLAUDE.md` to add project-specific rules, preferences, or context that Claude should always know about.

### Installing More Skills

Ask Claude Code directly:
```
/find-skills what I need
```

Or browse skill repos and install with:
```
/install-plugin owner/repo-name
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "command not found: claude" | Re-run `curl -fsSL https://claude.ai/install.sh \| bash` |
| Permission prompts won't stop | Run `bash setup.sh` again to reset settings |
| Skill not triggering | Say "use the [skill-name] skill" explicitly |
| Want to undo everything | `cp ~/.claude/settings.json.bak ~/.claude/settings.json` |
