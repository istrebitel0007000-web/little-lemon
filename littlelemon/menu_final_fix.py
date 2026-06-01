
path = r'C:\Users\A\little-lemon\littlelemon\restaurant\templates\menu.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace each problematic line exactly as it appears in the file
replacements = [
    # Remove Google Fonts import (we already have fonts in base.html)
    ("  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&display=swap');",
     ""),
    # Force html/body dark
    ("  body { background: var(--bg) !important; font-family: 'DM Sans', sans-serif; }",
     "  html, body, main { background: #1a1205 !important; color: #f0ece4 !important; }\n  body { font-family: 'Karla', sans-serif; }"),
    # Fix h1
    ("    font-family: 'Playfair Display', serif;",
     "    font-family: 'Markazi Text', serif;"),
    ("    color: var(--text);",
     "    color: #f4ce14;"),
    # Fix h2
    ("    border-bottom: 2px solid var(--red);",
     "    border-bottom: 1px solid #3a2810;"),
    ("    color: var(--red);",
     "    color: #f0ece4;"),
    # Fix menu-item hover shadow
    ("    box-shadow: 0 8px 24px rgba(0,0,0,0.12);",
     "    box-shadow: 0 12px 40px rgba(0,0,0,0.7);\n    border-color: #f4ce14 !important;"),
    # Fix menu-item-img background
    ("    background: #f0ede8;",
     "    background: #2a1e0a !important;"),
    # Fix placeholder background
    ("    background: linear-gradient(135deg, #f5f0eb 0%, #ede8e2 100%);",
     "    background: #2a1e0a !important;"),
    # Fix menu-item-body
    ("  .menu-item-body {",
     "  .menu-item-body {\n    background: #221508 !important;"),
    # Fix h3 color
    ("    color: var(--text);",
     "    color: #f0ece4 !important;"),
    # Fix price color (was red, now gold)
    ("    color: var(--red);",
     "    color: #f4ce14 !important;"),
    # Fix badges
    ("  .badge-veg     { background: #e8f5e9; color: var(--green); }",
     "  .badge-veg     { background: rgba(76,175,125,0.2); color: #4caf7d; }"),
    ("  .badge-popular { background: #fff8e1; color: var(--gold); }",
     "  .badge-popular { background: rgba(244,206,20,0.18); color: #f4ce14; }"),
    # Fix subsection title
    ("  .subsection-title {",
     "  .subsection-title {\n    background: transparent !important;"),
    ("    font-family: 'DM Sans', sans-serif;",
     "    font-family: 'Karla', sans-serif;"),
    ("    color: #555;",
     "    color: #b8a898 !important;"),
    ("    border-left: 3px solid var(--red);",
     "    border-left: 3px solid #f4ce14;"),
    # Fix search form
    ("border:1.5px solid #d1cbc2;",
     "border:1.5px solid #4a3518; background:#211608; color:#f0ece4;"),
    ("background:#f4ce14;",
     "background:#f4ce14;"),
    # Fix search button
    ("background:#c0392b; color:#fff;",
     "background:#f4ce14; color:#1a1205;"),
    # Fix clear link
    ("color:#7a7a6e;",
     "color:#b8a898;"),
    # Fix empty state text
    ("color: #999;",
     "color: #b8a898;"),
    # Fix query text
    ("color:#7a7a6e;margin-bottom:16px;",
     "color:#b8a898;margin-bottom:16px;"),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"SUCCESS! Applied {count}/{len(replacements)} replacements")
