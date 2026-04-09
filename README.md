# Claude Code Starter Pack

Get up and running with Claude Code in under 10 minutes. This pack includes sensible permissions, a starter CLAUDE.md, and recommended plugins.

## Step 1: Install Claude Code

**macOS / Linux / WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Homebrew (macOS):**
```bash
brew install --cask claude-code
```

You'll need a Claude Pro, Max, or Team subscription at [claude.ai](https://claude.ai).

## Step 2: First Run & Login

```bash
cd ~/your-project
claude
```

You'll be prompted to log in on first launch. After that, credentials are stored locally.

## Step 3: Apply Starter Settings

Copy the included settings file to set up permissions so Claude doesn't prompt you for every action:

```bash
# Back up existing settings if you have any
cp ~/.claude/settings.json ~/.claude/settings.json.bak 2>/dev/null

# Copy starter settings
cp settings.json ~/.claude/settings.json
```

This allows common tools (file read/write, git, npm, etc.) and blocks dangerous operations (rm -rf, sudo, force push).

See [settings.json](settings.json) for the full list.

## Step 4: Set Up Your CLAUDE.md

Copy the starter CLAUDE.md to your home directory:

```bash
cp CLAUDE.md ~/.claude/CLAUDE.md
```

This gives Claude baseline instructions for how to work. Edit it to match your preferences.

## Step 5: Install Recommended Plugins

Open Claude Code and paste this to install the essential plugins:

```
Install these plugins for me:
1. Superpowers from obra/superpowers (structured workflows for planning, TDD, debugging, code review)
2. UI/UX Pro Max from nextlevelbuilder/ui-ux-pro-max-skill (design intelligence for frontend work)
```

Or install them manually with slash commands inside Claude Code:
```
/install-plugin obra/superpowers
/install-plugin nextlevelbuilder/ui-ux-pro-max-skill
```

### Install GSD (Get Shit Done)

GSD is a project management framework that plans and executes work in phases. Install it by pasting this into Claude Code:

```
Install GSD for me. Search npm for "claude-code-gsd" and install it, or search GitHub for the GSD Claude Code plugin and set it up.
```

Once installed, key commands:
- `/gsd:new-project` — Start a new project with deep planning
- `/gsd:progress` — Check where things stand
- `/gsd:plan-phase` — Plan a phase of work
- `/gsd:execute-phase` — Execute a planned phase

## Step 6: Install Skills (Optional)

Skills are specialized prompts that teach Claude specific workflows. Install any that match your work:

| Skill | What it does | Install |
|-------|-------------|---------|
| `xlsx` | Read, write, format spreadsheets | Included in many skill packs |
| `docx` | Create/edit Word documents | Included in many skill packs |
| `pdf` | Read, merge, split, create PDFs | Included in many skill packs |
| `pptx` | Create/edit PowerPoint decks | Included in many skill packs |
| `qa` | Verify work is actually done | Included in many skill packs |

To find and install more skills:
```
/find-skills spreadsheet automation
```

## Quick Reference

| Command | What it does |
|---------|-------------|
| `claude` | Start interactive mode |
| `claude "do something"` | One-shot task |
| `/help` | Show all commands |
| `/compact` | Compress conversation to save context |
| `/clear` | Clear conversation history |
| `Shift+Tab` | Toggle auto-accept mode (skip permission prompts) |
| `Ctrl+D` or `exit` | Quit |

## Tips for Getting Started

1. **Just talk naturally** — "what does this codebase do?", "fix the login bug", "add tests for the auth module"
2. **Point it at files** — "read package.json and tell me what dependencies we have"
3. **Let it run commands** — "run the tests and fix any failures"
4. **Use it for git** — "commit these changes", "create a PR for this feature"
5. **Ask it to explain** — "explain how the payment flow works"

## Permissions Explained

The included `settings.json` uses three permission levels:

- **allow** — Auto-approved, no prompt. Common safe operations (read files, run tests, git status)
- **deny** — Always blocked. Destructive operations (rm -rf, sudo, force push)
- Everything else prompts you for approval. Hit "Always allow" to permanently approve specific tools

You can always check and modify permissions by editing `~/.claude/settings.json`.
