#!/usr/bin/env python3
"""
Mark up construction GA plan PDFs with color-coded apartment type annotations.
Reads a JSON config with unit-to-type mapping, annotates each PDF page with
colored badges and underlines, combines into a single output PDF.

Usage: python3 markup_plans.py config.json
"""
import fitz
import json
import re
import os
import sys
import glob

COLORS = {
    '1B': (0.2, 0.4, 0.9),
    '2B': (0.0, 0.6, 0.2),
    '3B': (0.9, 0.4, 0.0),
    '4B': (0.8, 0.1, 0.1),
    '5B': (0.7, 0.0, 0.0),
    'DDA': (0.6, 0.1, 0.8),
    'TH': (0.0, 0.55, 0.55),
    'STUDIO': (0.4, 0.4, 0.4),
}

def classify(tc):
    if not tc: return '1B'
    if 'DDA' in tc: return 'DDA'
    if 'TH.' in tc: return 'TH'
    if 'STUDIO' in tc.upper(): return 'STUDIO'
    clean = tc.replace('DDA.', '').replace('F.', '').replace('TH.', '')
    for n in ['5', '4', '3', '2', '1']:
        if f'{n}B' in clean:
            return f'{n}B'
    return '1B'

def bed_short(tc):
    if not tc: return '?'
    clean = tc.replace('DDA.', '').replace('F.', '').replace('TH.', '')
    prefix = ''
    if 'DDA' in tc: prefix = 'DDA '
    if 'TH.' in tc: prefix = 'TH '
    if 'STUDIO' in tc.upper(): return f'{prefix}ST'
    for n in ['5', '4', '3', '2', '1']:
        if f'{n}B' in clean:
            return f'{prefix}{n}B'
    return f'{prefix}?'

def find_unit_positions(page, unit_pattern):
    pat = re.compile(f'^{unit_pattern}$')
    blocks = page.get_text('dict')['blocks']
    positions = {}
    for b in blocks:
        if 'lines' in b:
            for l in b['lines']:
                for s in l['spans']:
                    txt = s['text'].strip()
                    if pat.match(txt):
                        positions[txt] = s['bbox']
    return positions

def add_legend(page, active_categories):
    pw = page.rect.width
    items = [(k, v) for k, v in [
        ('1B', '1 Bedroom'), ('2B', '2 Bedroom'), ('3B', '3 Bedroom'),
        ('4B', '4 Bedroom'), ('5B', '5 Bedroom'), ('DDA', 'DDA Accessible'),
        ('TH', 'Townhouse'), ('STUDIO', 'Studio'),
    ] if k in active_categories]

    if not items:
        return

    lw, lh = 300, 50 + len(items) * 26
    lx, ly = pw - lw - 20, 50
    rect = fitz.Rect(lx, ly, lx + lw, ly + lh)
    page.draw_rect(rect, color=(0.2, 0.2, 0.2), fill=(1, 1, 1), width=1.5)
    page.insert_text((lx + 12, ly + 24), "APARTMENT TYPE MARKUP",
                      fontsize=14, fontname="helv", color=(0.15, 0.15, 0.15))
    page.draw_line((lx + 12, ly + 30), (lx + lw - 12, ly + 30),
                   color=(0.7, 0.7, 0.7), width=0.8)

    for i, (key, label) in enumerate(items):
        y = ly + 52 + i * 26
        col = COLORS.get(key, (0.5, 0.5, 0.5))
        r = fitz.Rect(lx + 16, y - 8, lx + 50, y + 8)
        page.draw_rect(r, color=col, fill=col, width=0)
        page.insert_text((lx + 21, y + 5), key, fontsize=9, fontname="helv", color=(1, 1, 1))
        page.insert_text((lx + 58, y + 5), label, fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

def markup_page(page, level_name, type_map, unit_pattern, typical_bases):
    positions = find_unit_positions(page, unit_pattern)
    if not positions:
        return 0, set()

    count = 0
    cats = set()
    for uid, bbox in positions.items():
        tc = type_map.get(uid)
        if not tc and typical_bases:
            parts = uid.split('.')
            if len(parts) == 3:
                bldg, _, unit_num = parts
                for try_lvl in typical_bases:
                    test_uid = f'{bldg}.{try_lvl}.{unit_num}'
                    tc = type_map.get(test_uid)
                    if tc:
                        break

        if not tc:
            continue

        cat = classify(tc)
        cats.add(cat)
        color = COLORS.get(cat, (0.5, 0.5, 0.5))
        label = bed_short(tc)

        cx = (bbox[0] + bbox[2]) / 2

        bw = len(label) * 7 + 12
        bh = 14
        badge = fitz.Rect(cx - bw / 2, bbox[1] - bh - 4, cx + bw / 2, bbox[1] - 4)
        page.draw_rect(badge, color=None, fill=color, width=0)
        page.insert_text((cx - len(label) * 3.2, bbox[1] - 7), label,
                         fontsize=9, fontname="helv", color=(1, 1, 1))
        page.draw_line((bbox[0], bbox[3] + 2), (bbox[2], bbox[3] + 2),
                       color=color, width=2)
        count += 1

    add_legend(page, cats)

    title_rect = fitz.Rect(30, 50, 480, 85)
    page.draw_rect(title_rect, color=None, fill=(0, 0.23, 0.45), width=0)
    page.insert_text((42, 76), f"{level_name}  |  {count} apartments",
                      fontsize=17, fontname="helv", color=(1, 1, 1))
    return count, cats

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 markup_plans.py config.json")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        config = json.load(f)

    input_dir = config['input_dir']
    output_path = config['output_path']
    type_map = config.get('type_map', {})
    unit_pattern = config.get('unit_pattern', r'B[1-4]\.\d+\.\d+')
    level_names = config.get('level_names', {})
    typical_bases = config.get('typical_floor_bases', [])
    title = config.get('title', '')

    pdf_files = sorted(glob.glob(os.path.join(input_dir, '*.pdf')))
    if not pdf_files:
        print(f"No PDFs found in {input_dir}")
        sys.exit(1)

    output_doc = fitz.open()
    total = 0

    for pdf_path in pdf_files:
        fname = os.path.basename(pdf_path)
        lname = fname
        for key, val in level_names.items():
            if key in fname:
                lname = val
                break

        doc = fitz.open(pdf_path)
        page = doc[0]
        n, _ = markup_page(page, lname, type_map, unit_pattern, typical_bases)
        total += n
        output_doc.insert_pdf(doc, from_page=0, to_page=0)
        doc.close()
        print(f'{lname}: {n} marked')

    output_doc.save(output_path, deflate=True, garbage=4)
    output_doc.close()
    print(f'\nTotal: {total} apartments marked across {len(pdf_files)} pages')
    print(f'Saved: {output_path}')

if __name__ == '__main__':
    main()
