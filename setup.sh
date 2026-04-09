#!/bin/bash
# Claude Code Starter Pack - Quick Setup
# Run: bash setup.sh

set -e

echo "=== Claude Code Starter Pack ==="
echo ""

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "Installing Claude Code..."
    curl -fsSL https://claude.ai/install.sh | bash
    echo ""
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Create .claude directory if it doesn't exist
mkdir -p ~/.claude/skills

# Back up existing settings
if [ -f ~/.claude/settings.json ]; then
    echo "Backing up existing settings to ~/.claude/settings.json.bak"
    cp ~/.claude/settings.json ~/.claude/settings.json.bak
fi

# Copy settings
cp "$SCRIPT_DIR/settings.json" ~/.claude/settings.json
echo "[OK] Copied settings.json -> ~/.claude/settings.json"

# Copy CLAUDE.md (only if one doesn't exist)
if [ -f ~/.claude/CLAUDE.md ]; then
    echo "[SKIP] ~/.claude/CLAUDE.md already exists (see CLAUDE.md in this repo for reference)"
else
    cp "$SCRIPT_DIR/CLAUDE.md" ~/.claude/CLAUDE.md
    echo "[OK] Copied CLAUDE.md -> ~/.claude/CLAUDE.md"
fi

# Install skills
echo ""
echo "Installing skills..."
SKILL_COUNT=0
for skill_dir in "$SCRIPT_DIR"/skills/*/; do
    skill_name=$(basename "$skill_dir")
    if [ -d ~/.claude/skills/"$skill_name" ]; then
        echo "  [SKIP] $skill_name (already installed)"
    else
        cp -r "$skill_dir" ~/.claude/skills/
        echo "  [OK] $skill_name"
        SKILL_COUNT=$((SKILL_COUNT + 1))
    fi
done
echo "Installed $SKILL_COUNT new skills"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Run 'claude' in any project directory"
echo "  2. Log in when prompted"
echo "  3. Start working!"
echo ""
echo "Recommended: Install these plugins by pasting into Claude Code:"
echo "  /install-plugin obra/superpowers"
echo "  /install-plugin nextlevelbuilder/ui-ux-pro-max-skill"
echo ""
echo "For GSD (project management), paste this into Claude Code:"
echo "  Install GSD for me — it's a Claude Code project management framework"
echo ""
