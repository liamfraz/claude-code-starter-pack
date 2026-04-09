---
name: drawing-markup
description: Mark up construction GA plan PDFs with color-coded apartment/unit type annotations. Extracts unit IDs and type codes from the PDF text layer, then overlays colored badges showing bedroom counts, underlines unit labels, and adds a legend. Combines all marked-up pages into a single PDF. Use this skill whenever the user asks to mark up, annotate, highlight, or color-code apartments or units on architectural floor plans, GA plans, or construction drawings. Also use when the user says "mark every room", "color code the apartments", "annotate the drawings", "highlight unit types", or wants a visual takeoff overlay on PDF drawings. Works with any residential project using unit ID patterns like BX.LL.UU (Building.Level.Unit). Requires PyMuPDF (fitz).
---

# Drawing Markup Skill

Mark up construction GA plan PDFs with color-coded apartment/unit type annotations. Produces a combined PDF with all pages annotated.

## When to Use

- User has construction GA plan PDFs with apartment/unit labels in the text layer
- User wants visual markup showing apartment types (1B, 2B, 3B, etc.)
- User wants a combined annotated PDF of all floor plans
- User has already done (or wants to do) an apartment takeoff and wants it visualized on the drawings

## Prerequisites

- **PyMuPDF** (`fitz`) must be installed: `pip install PyMuPDF`
- PDF drawings must have a text layer (not scanned images) containing unit ID labels

## Workflow

### Step 1: Extract Unit IDs from PDFs

Use `pdftotext` or PyMuPDF to extract unit IDs from the PDF text layer. Unit IDs typically follow patterns like:
- `BX.LL.UU` — Building X, Level LL, Unit UU (e.g., `B1.04.07`)
- `BX.L.UU` — Shorter level format (e.g., `B2.4.01`)

```bash
# Quick extraction of all unit IDs from a PDF
pdftotext -layout "drawing.pdf" - | grep -oE 'B[1-4]\.\d+\.\d+'
```

### Step 2: Extract Type Codes

Type codes are usually positioned near the unit ID in the drawing. Extract them with:

```bash
# Raw text extraction preserves spatial proximity
pdftotext -raw "drawing.pdf" - | grep -E '(B[1-4]\.\d+\.\d+|[A-Z]*\.?[1-3]B[12]?B)'
```

Common type code formats:
- `1B1B` — 1 Bedroom, 1 Bathroom
- `2B1B` — 2 Bedroom, 1 Bathroom
- `3B1B1P` — 3 Bedroom, 1 Bathroom, 1 Powder Room
- `2B2B` — 2 Bedroom, 2 Bathroom
- `4B2B` — 4 Bedroom, 2 Bathroom

Prefixes: `DDA.` = accessible, `F.` = facade variant, `TH.` = townhouse
Suffixes: `.M` = mirror layout

### Step 3: Build Unit-to-Type Mapping

Create a dictionary mapping each unit ID to its type code. Two approaches:

**A) From PDF proximity matching** — Match unit IDs to the nearest type code below them in the PDF text:
```python
# Type code should be within ~80pt below and ~40pt horizontally of unit ID
if dy > 0 and dy < 80 and dx < 40:
    # This type belongs to this unit
```

**B) From a pre-built register** — If you've already compiled an apartment register (e.g., via the xlsx skill), use that mapping directly. This is more reliable.

For typical floors (where one drawing represents multiple levels), implement fallback matching — if a unit ID's level number doesn't match exactly, try the base level of the typical floor range.

### Step 4: Generate Markup with the Script

Use the bundled `scripts/markup_plans.py` script. It takes a JSON config file:

```bash
python3 ~/.claude/skills/drawing-markup/scripts/markup_plans.py config.json
```

**Config file format:**
```json
{
  "input_dir": "/path/to/pdf/folder",
  "output_path": "/path/to/output/Marked_Up_Plans.pdf",
  "unit_pattern": "B[1-4]\\.\\d+\\.\\d+",
  "type_map": {
    "B1.04.01": "1B1B-01",
    "B1.04.02": "DDA.2B1B-01",
    "B2.04.01": "F.3B1B1P-01"
  },
  "level_names": {
    "LEVEL 04": "Level 04",
    "LEVEL 07": "Levels 07-11 (Typical)"
  },
  "typical_floor_bases": [7, 12, 16, 20],
  "title": "PROJECT NAME"
}
```

If no config file exists, generate one by:
1. Scanning all PDFs in the input directory for unit IDs
2. Extracting type codes via proximity matching
3. Building the type_map automatically
4. Writing the config for the user to review/edit before final markup

### Step 5: Open and Verify

Open the output PDF and verify the markups look correct. Check:
- All units have colored badges (no grey "?" badges)
- Bedroom counts match the type codes
- Legend is visible and not overlapping drawings
- Badges don't obscure the architectural drawing underneath

## Annotation Style

The markup uses minimal, non-destructive annotations:
- **Colored pill badge** above each unit label showing bedroom count (e.g., "1B", "2B", "3B")
- **Colored underline** beneath the unit ID text
- **Legend** in the top-right corner of each page
- **Level title bar** in the top-left showing level name and apartment count
- No large rectangles or opaque overlays that obscure the drawing

## Color Scheme

| Category | Color | RGB |
|----------|-------|-----|
| 1 Bedroom | Blue | (0.2, 0.4, 0.9) |
| 2 Bedroom | Green | (0.0, 0.6, 0.2) |
| 3 Bedroom | Orange | (0.9, 0.4, 0.0) |
| 4 Bedroom | Red | (0.8, 0.1, 0.1) |
| DDA Accessible | Purple | (0.6, 0.1, 0.8) |
| Townhouse | Teal | (0.0, 0.55, 0.55) |

## Adapting to Different Projects

The unit ID pattern (`B[1-4]\.\d+\.\d+`) covers the most common Australian residential convention. For other conventions:
- Update `unit_pattern` in the config to match the project's naming scheme
- The type code classification logic handles any `XB[Y]B[Z]P` format automatically
- Add custom prefixes (DDA, TH, F, etc.) as needed to the classifier
