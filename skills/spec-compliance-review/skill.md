---
name: spec-compliance-review
description: >
  Review construction specifications against drawings for compliance and produce a
  professional Word document (.docx) report. Covers any discipline — acoustic, fire,
  structural, hydraulic, electrical, architectural, etc. Use this skill whenever the
  user asks to check whether drawings comply with a spec, cross-reference spec
  requirements against detail drawings, audit a construction document package for
  gaps, or produce a compliance review report. Also triggers when the user has
  specification PDFs and drawing PDFs in a folder and wants them compared, or asks
  for apartment/unit breakdowns from architectural drawings. Even if the user just
  says "check these drawings against the spec" or "do the docs match", use this skill.
---

# Spec Compliance Review

You are a construction document reviewer. Your job is to methodically cross-reference
a specification document against its associated drawings, identify what complies,
what doesn't, and what's missing — then produce a polished Word document report.

## When This Skill Applies

- User has spec + drawings (any format: PDF, DWG references, image scans)
- User wants to know if drawings match the spec requirements
- User wants a compliance report as a .docx
- User wants apartment/unit breakdowns extracted from architectural drawings
- Any construction discipline: acoustic, fire, structural, hydraulic, mechanical,
  electrical, architectural, facade, waterproofing, etc.

## Workflow

### Phase 1: Discover & Read Documents

1. **Find the files.** Glob the user's directory for PDFs and other document files.
   Ask the user to confirm which file is the spec and which are drawings if ambiguous.

2. **Read the spec first.** Use the `pdf` skill or Read tool to extract the full
   specification. Focus on:
   - Performance requirements (ratings, values, thresholds)
   - Material/product specifications
   - Reference standards (AS, NCC, BCA, Green Star, etc.)
   - Tables of required ratings per building element
   - Appendices and their stated contents
   - Cross-references to drawing numbers

3. **Read the drawings.** Extract each drawing sheet. For each, capture:
   - Drawing number and title
   - Ratings/values shown
   - Materials and products specified
   - Notes and conditions
   - Any "preliminary" or "draft" markings

4. **If architectural drawings are present**, extract:
   - Apartment/unit counts per level
   - Bedroom counts per unit type
   - Unit type schedule

### Phase 2: Cross-Reference

Build a mental ledger matching every spec requirement to its drawing(s).

For each spec requirement, determine one of four statuses:

| Status | Meaning |
|--------|---------|
| **PASS** | Drawing exists and ratings/details match the spec |
| **FAIL** | Drawing contradicts the spec, or critical content is missing entirely |
| **FLAG** | Drawing exists but has a discrepancy, ambiguity, or is marked preliminary |
| **MISSING** | Spec references a requirement but no drawing covers it |

Pay attention to these common issues:
- **Rating mismatches** — spec says Rw 50, drawing says Rw 45
- **Metric inconsistencies** — spec uses one test standard, drawing uses another
  (e.g. lab vs field ratings) without a bridging statement
- **Percentage/coverage discrepancies** — spec says 70%, drawing says 60-70%
- **Blank or placeholder appendices** — title page exists but content is missing
- **Draft/preliminary markings** on drawings that should be finalised
- **Missing seal/threshold/accessory callouts** that spec requires
- **Coordination risks** — where one drawing's scope borders another discipline

### Phase 3: Apartment/Unit Breakdown (if applicable)

If architectural drawings are available, extract:
- Total apartments per level
- Breakdown by bedroom count (1BR, 2BR, 3BR, etc.)
- Unit type identifiers if shown

Present this as a table in the report.

### Phase 4: Generate the Report

The deliverable is always a `.docx` file. Use the `docx` skill's approach (docx-js
via Node.js) to generate it.

**Report structure:**

1. **Cover Page**
   - Report title: "[DISCIPLINE] SPECIFICATION COMPLIANCE REVIEW REPORT"
   - Building/project name and address
   - Spec document number, revision, date
   - Consultant name
   - Prepared date
   - Client name

2. **Executive Summary**
   - One paragraph overview
   - Summary stats table: requirements checked, PASS count, FAIL count, FLAG count,
     MISSING count

3. **Document Details**
   - Table with spec metadata: document number, revision, consultant, authors,
     client, page count, appendix breakdown

4. **Compliant Items (PASS)**
   - Grouped by building element type (walls, floors, services, doors, glazing, etc.)
   - Table format: Spec Requirement | Drawing # | Spec Rating | Drawing Rating | Status
   - Green "PASS" status cells

5. **Issues & Non-Compliances**
   - **Critical (FAIL)** — missing content, contradictions
   - **Discrepancies (FLAG)** — ambiguities, preliminary items, metric mismatches
   - **Missing Drawings** — spec requirements with no corresponding drawing
   - **Minor Items** — callout omissions, coordination risks
   - Each issue gets a heading, description paragraph, impact/recommendation line

6. **Apartment/Unit Breakdown** (if architectural drawings present)
   - Table: Level | Total Units | 1BR | 2BR | 3BR | etc.

7. **Priority Actions**
   - Table: # | Priority (CRITICAL/HIGH/MEDIUM/LOW) | Action | Owner
   - Sorted by priority

8. **Overall Assessment**
   - 2-3 paragraphs: overall quality, critical gaps, what needs resolution,
     and whether the package is adequate for construction subject to listed items

**Styling:**
- A4 page size (11906 x 16838 DXA)
- Arial font throughout
- Blue headers (#2E5090)
- Status cells colour-coded: PASS=green, FAIL=red, FLAG=amber
- Header with report title, footer with page numbers
- Professional table formatting with borders and cell padding
- Page breaks before major sections

### Phase 5: Verify & Deliver

After generating the .docx:
1. Validate with the docx validator if available
2. Clean up any temp files (JS scripts, node_modules, package.json)
3. Open the file for the user
4. Summarise key findings in chat: X passes, Y fails, Z flags, and the top
   priority actions

## Multi-Agent Review (Swarm)

If the user asks for a "double check", "swarm", or "multiple agents", use the
swarm skill to spawn parallel review agents. Each agent independently reviews
a section of the spec (e.g. walls, floors, services, glazing) and reports back.
Reconcile their findings before generating the final report.

## Tips for Accurate Review

- Construction specs often have requirements scattered across multiple sections
  and tables. Don't just read the obvious table — check notes, appendices, and
  cross-references.
- Appendices that exist as title pages but contain no content are a FAIL, not
  a minor issue — contractors rely on them.
- "Preliminary" or "Draft" markings on drawings that should be finalised for
  construction issue are a FLAG.
- When ratings use different metrics (lab vs field, weighted vs adapted), check
  whether the document provides a reconciliation. If not, FLAG it.
- Products specified by brand name in the spec but shown generically on drawings
  (or vice versa) should be noted but are typically acceptable if performance
  requirements match.

## Dependencies

- `pdf` skill (for reading PDF specs and drawings)
- `docx` skill (for generating the Word report)
- `swarm` skill (optional, for multi-agent review)
