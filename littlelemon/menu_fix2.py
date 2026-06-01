path = r'C:\Users\A\little-lemon\littlelemon\restaurant\templates\menu.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all remaining light colors in the style block
fixes = [
    # menu-item-img light background
    ('background: #f0ede8;', 'background: #2a1e0a;'),
    # placeholder light gradient
    ('background: linear-gradient(135deg, #f5f0eb 0%, #ede8e2 100%);', 'background: #2a1e0a;'),
    # badge-veg light green
    ('.badge-veg     { background: #e8f5e9; color: var(--green); }',
     '.badge-veg     { background: rgba(76,175,125,0.2); color: var(--green); }'),
    # badge-popular light yellow
    ('.badge-popular { background: #fff8e1; color: var(--gold); }',
     '.badge-popular { background: rgba(244,206,20,0.18); color: var(--gold); }'),
    # subsection-title light grey
    ('color: #555;', 'color: var(--muted);'),
    # search form light border
    ('border:1.5px solid #d1cbc2;', 'border:1.5px solid #4a3518;'),
    # search form background (input)
    ("style=\"flex:1; padding:10px 14px; border:1.5px solid #4a3518; border-radius:6px; font-size:0.95rem;\"",
     "style=\"flex:1; padding:10px 14px; border:1.5px solid #4a3518; border-radius:6px; font-size:0.95rem; background:#211608; color:#f0ece4;\""),
    # search button red
    ('background:#c0392b;', 'background:#f4ce14;'),
    ('color:#fff; border:none; border-radius:6px; cursor:pointer; font-weight:600;"',
     'color:#1a1205; border:none; border-radius:6px; cursor:pointer; font-weight:600;"'),
    # clear link color
    ('color:#7a7a6e;', 'color:#b8a898;'),
    # "no results" text
    ('color: #999;', 'color: var(--muted);'),
    # query result text
    ('color:#7a7a6e;margin-bottom:16px;', 'color:#b8a898;margin-bottom:16px;'),
    # menu-item hover shadow (make it darker)
    ('box-shadow: 0 8px 24px rgba(0,0,0,0.12);', 'box-shadow: 0 8px 32px rgba(0,0,0,0.6);'),
    # price color change from red to gold
    ('color: var(--red);', 'color: var(--gold);'),
]

original = content
for old, new in fixes:
    content = content.replace(old, new)

changed = sum(1 for old, new in fixes if old not in content and old in original)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Done! Applied {changed}/{len(fixes)} fixes")
