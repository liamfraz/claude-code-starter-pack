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

# Back up existing settings
if [ -f ~/.claude/settings.json ]; then
    echo "Backing up existing settings to ~/.claude/settings.json.bak"
    cp ~/.claude/settings.json ~/.claude/settings.json.bak
fi

# Create .claude directory if it doesn't exist
mkdir -p ~/.claude

# Copy settings
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "$SCRIPT_DIR/settings.json" ~/.claude/settings.json
echo "Copied settings.json -> ~/.claude/settings.json"

# Copy CLAUDE.md (only if one doesn't exist)
if [ -f ~/.claude/CLAUDE.md ]; then
    echo "~/.claude/CLAUDE.md already exists — skipping (see CLAUDE.md in this repo for reference)"
else
    cp "$SCRIPT_DIR/CLAUDE.md" ~/.claude/CLAUDE.md
    echo "Copied CLAUDE.md -> ~/.claude/CLAUDE.md"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Run 'claude' in any project directory"
echo "  2. Log in when prompted"
echo "  3. Start working!"
echo ""
echo "Optional: Install recommended plugins by pasting this into Claude Code:"
echo "  /install-plugin obra/superpowers"
echo ""
