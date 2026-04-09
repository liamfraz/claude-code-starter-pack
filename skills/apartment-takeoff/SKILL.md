---
name: apartment-takeoff
description: Perform apartment type takeoffs from construction GA plan PDFs. Extracts unit IDs and type codes from the PDF text layer, builds a full apartment register spreadsheet (.xlsx), and produces a takeoff summary with counts by type, building, and level. Use this skill whenever the user asks for an apartment takeoff, unit schedule, apartment register, unit count, dwelling mix, accommodation schedule, or wants to know how many apartments are on each level. Also triggers on "how many units", "apartment types", "dwelling schedule", "unit mix", "bedroom mix", "do a takeoff", or any request to count/catalogue apartments from architectural floor plans. Works with any residential project where GA plan PDFs have unit IDs in the text layer (e.g., BX.LL.UU format). Chains into drawing-markup skill for annotated PDF output. Requires PyMuPDF (fitz) and openpyxl.
---

# Apartment Takeoff Skill

Extract apartment data from construction GA plan PDFs, build a full register, and produce a takeoff summary. This skill reads the PDF text layer — not the visual render — which is faster and more accurate.

## When to Use

- User has GA plan PDFs and wants an apartment count / type breakdown
- User asks for an apartment register, unit schedule, or accommodation schedule
- User wants to know the dwelling mix (how many 1B, 2B, 3B, etc.)
- User wants a spreadsheet of all apartments with building, level, type, bedrooms

## Prerequisites

- **PyMuPDF** (`fitz`): `pip install PyMuPDF`
- **openpyxl**: `pip install openpyxl`
- **pdftotext** (from poppler): `brew install poppler` — used for quick text extraction
- PDFs must have a text layer (not scanned images)

## Workflow

### Step 1: Discover PDFs and Understand the Project

List all PDFs in the input folder. Read filenames to understand:
- How many levels (ground to roof)
- Which levels are typical (repeated layouts shown on one drawing)
- Building structure (single tower vs. multiple buildings)
- Which levels are roof/plant (no apartments)

### Step 2: Extract Unit IDs from Text Layer

Use `pdftotext` for quick extraction of all unit IDs:

```bash
for f in /path/to/pdfs/*.pdf; do
  echo "=== $(basename "$f") ==="
  pdftotext -layout "$f" - | grep -oE 'B[1-4]\.\d+\.\d+' | sort -u
  echo
done
```

This gives exact unit IDs per level per building. Adjust the regex pattern if the project uses a different naming convention.

### Step 3: Extract Type Codes

Use `pdftotext -raw` to preserve spatial proximity between unit IDs and their type codes:

```bash
for f in /path/to/pdfs/*.pdf; do
  echo "=== $(basename "$f") ==="
  pdftotext -raw "$f" - | grep -E '(B[1-4]\.\d+\.\d+|[A-Z]*\.?[1-3]B[12]?B)' | paste - -
  echo
done
```

The raw extraction pairs each unit ID with the type code that appears directly after it in the text stream (which is spatially below it on the drawing).

### Step 4: Parse Type Codes

Common type code conventions in Australian residential:

| Code Pattern | Meaning |
|---|---|
| `1B1B` | 1 Bedroom, 1 Bathroom |
| `2B1B` | 2 Bedroom, 1 Bathroom |
| `2B2B` | 2 Bedroom, 2 Bathroom |
| `3B1B1P` | 3 Bedroom, 1 Bathroom, 1 Powder Room |
| `4B2B` | 4 Bedroom, 2 Bathroom |

Prefixes:
- `DDA.` — Accessible / DDA compliant
- `F.` — Facade variant
- `TH.` — Townhouse
- Suffix `.M` — Mirror image layout
- Suffix `-NN` — Variant number

Classification function:
```python
def get_bedrooms(type_code):
    clean = type_code.replace('DDA.','').replace('F.','').replace('TH.','')
    base = clean.split('-')[0]
    if '4B' in base: return 4
    if '3B' in base: return 3
    if '2B' in base: return 2
    if '1B' in base: return 1
    return 0
```

### Step 5: Handle Typical Floors

Many drawings represent multiple identical levels (e.g., "LEVEL 07-11"). The text layer only contains one set of unit IDs (for the base level), but the same apartments repeat on each level in the range.

When building the register, expand typical floors:
- Parse the level range from the filename (e.g., "LEVEL 07-11" → levels 7, 8, 9, 10, 11)
- For each level in the range, create entries with the correct level number
- Use the same type codes from the base level drawing

### Step 6: Build the Register Spreadsheet

Create an xlsx with openpyxl containing:

**Sheet 1: Apartment Register** (every unit, one row each)
| Column | Content |
|---|---|
| # | Sequential number |
| Unit ID | e.g., B1.04.01 |
| Building | B1, B2, B3, B4 |
| Level | 01, 02, GL, etc. |
| Bedrooms | 1, 2, 3, 4 |
| Bathrooms | 1, 2 |
| Powder Room | 0, 1 |
| Type Code | Full type code |
| DDA Accessible | Yes / blank |
| Townhouse | Yes / blank |
| Apartment Class | "1 Bed", "2 Bed", etc. |

- Add auto-filter on all columns
- Freeze header row
- Color-code DDA rows (light green) and Townhouse rows (light orange)
- Use Kane Blue (#003B73) for headers if it's a Kane project

**Sheet 2: Type Summary**
- Overall count by bedroom type with percentages
- Count by building with level ranges
- Count by level with per-building breakdown
- DDA and Townhouse counts

**Sheet 3: Type Codes**
- Legend explaining each type code format

### Step 7: Print Takeoff Summary

Output a text summary to the user showing:
- Total apartment count
- Breakdown by bedroom type (count and %)
- Breakdown by building (count and level range)
- Special unit counts (DDA, Townhouse)

### Step 8: QA Audit

After building the register, run a systematic QA audit. This is not optional — the initial extraction always has errors. The audit catches them before the user sees the output.

**8a. Duplicate check**
```python
# Every unit ID must appear exactly once
duplicates = df[df.duplicated(subset='Unit ID', keep=False)]
```
Flag and remove any duplicates. Prefer the entry with a matched type code over one without.

**8b. Gap check**
For each building/level combination, check that unit numbers are sequential (01, 02, 03...). Missing numbers indicate a unit the text extraction missed. Go back to the PDF and re-extract that specific page with PyMuPDF `get_text('dict')` to find the missing unit.

**8c. Typical floor consistency**
Typical floors (e.g., L07-11) must have identical unit counts and type distributions. If L08 has a different count than L07, something went wrong in the expansion. Fix by using the base level (L07) as the template for all levels in the range.

**8d. Type code validation**
Every unit must have a type code. If any unit has a missing or unrecognised type:
1. Re-extract from the PDF using `pdftotext -raw` for that specific page
2. Try PyMuPDF bbox extraction to find the nearest type label spatially
3. If still unresolved, check if the unit's position on a typical floor matches another level where the type IS known — inherit from there
4. As a last resort, visually read the PDF page to determine bedroom count from the room layout

**8e. Cross-check totals against PDF**
For each unique floor plan drawing, compare:
- Number of unit IDs found in text layer vs. number in register for that level
- If they don't match, re-extract and reconcile

**8f. Building termination check**
Verify that each building's units stop at the correct level:
- Check for the "ROOF" keyword in filenames to identify where each building terminates
- Ensure no units exist above a building's roof level
- Ensure units DO exist on every level below the roof

**8g. Bedroom mix sanity**
Flag unusual distributions for human review:
- More than 70% single bedroom type → unusual, verify
- Any 4B+ apartments → verify these aren't parsing errors (e.g., "B4" building prefix misread as "4B" bedroom count)
- Zero DDA units → suspicious for social/public housing projects

**8h. Podium / non-typical level validation**
CRITICAL: Podium levels (typically L01-L03) often have communal rooms, amenities, retail, or breakout spaces that replace apartment positions. NEVER assume podium levels have the same unit count as typical floors above.

For each non-typical level:
1. Count units found in text extraction independently — do not inherit from typical floors
2. Cross-reference against communal/amenity room labels on the same drawing (e.g., "COMMUNAL ROOM", "BREAKOUT ROOM", "AMENITIES")
3. If a unit position exists on typical floors but NOT on this level, check whether a communal space occupies that position
4. Flag any level where unit count differs from an adjacent typical floor for manual review

**Why this matters:** Flemington 4CD had phantom units B3.3.06 and B3.3.07 on the podium Level 03 because the takeoff assumed 7 B3 units (same as L04+), but communal rooms occupied those positions. This inflated the total by 2.

**8i. Dev Sum cross-reference (if available)**
If a Development Summary (Dev Sum) register exists, cross-reference per-level totals against it. The Dev Sum is the authoritative apartment count — it takes precedence over text extraction when they disagree.

**8j. All-tabs verification**
After building the xlsx, read back EVERY tab (not just the main data tab) and verify:
- Summary totals match the data tab
- Level Breakdown has ALL levels (no gaps)
- Bed mix percentages add up to 100%

**8k. Fix and re-run**
After identifying errors:
1. Fix the type_map or unit list
2. Regenerate the xlsx
3. Re-run the audit to confirm all issues resolved
4. Print a QA summary showing what was found and fixed

```
--- QA AUDIT ---
Duplicates: 0 found
Gaps: 0 found
Typical floor consistency: PASS (all typical floors match)
Missing types: 0 units without type codes
Building termination: PASS
Total units verified: 415
Status: CLEAN
```

### Step 9: Offer Markup (Optional)

After the register passes QA, offer to run the `drawing-markup` skill to produce annotated PDFs with color-coded apartment badges. The type_map from this takeoff feeds directly into the markup config.

## Adapting to Different Projects

### Unit ID Patterns
The default regex `B[1-4]\.\d+\.\d+` covers the most common Australian convention. Adjust for:
- Single-building projects: might use `APT-LL.UU` or `U.LL.UU`
- Numbered buildings: `B[1-9]` or `BLK[A-D]`
- Always check the text layer of one PDF first to identify the actual pattern

### Type Code Formats
If the project uses different type naming:
- Check `pdftotext -raw` output to identify the format
- Common alternatives: `1BR`, `2BR`, `STUDIO`, `1BED`, `2BED`
- Adjust the classification regex accordingly

### Non-Residential Spaces
Filter out non-apartment spaces that might match the unit ID pattern:
- Corridor labels (often have `COR`, `CORR`, or `C` suffix)
- Fire stairs (`FS`, `STAIR`)
- Plant rooms, lobbies, retail
- Look for suffixes like `.C`, `.FS`, `.P` (plant), `.S` (services)

## Quality Standards

The Step 8 QA audit is mandatory — never skip it, never present results as final before it passes. The audit exists because PDF text extraction is imperfect: labels get missed, type codes get mismatched, typical floor expansion can introduce errors. The audit catches these systematically rather than hoping the user spots them.

A clean audit means:
- Zero duplicates, zero gaps, zero missing types
- Typical floors consistent
- Podium/non-typical levels verified independently (not assumed from typical)
- Building termination correct
- Bedroom mix passes sanity check
- Total count matches sum of per-level counts
- Dev Sum cross-referenced (if available)
- ALL xlsx tabs verified (not just main data tab)
