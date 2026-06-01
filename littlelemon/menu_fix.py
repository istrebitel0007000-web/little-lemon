import re

path = r'C:\Users\A\little-lemon\littlelemon\restaurant\templates\menu.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire :root block
old_root = """:root {
    --red: #c0392b;
    --red-light: #fdecea;
    --gold: #f57f17;
    --green: #2e7d32;
    --bg: #faf9f7;
    --card-bg: #ffffff;
    --border: #ece9e4;
    --text: #1a1a1a;
    --muted: #6b6460;
  }"""

new_root = """:root {
    --red: #e05555;
    --red-light: rgba(224,85,85,0.15);
    --gold: #f4ce14;
    --green: #4caf7d;
    --bg: #1a1205;
    --card-bg: #221508;
    --border: #3a2810;
    --text: #f0ece4;
    --muted: #b8a898;
  }"""

# Also fix body background
old_body = "body { background: var(--bg); font-family: 'DM Sans', sans-serif; }"
new_body = "body { background: var(--bg) !important; font-family: 'DM Sans', sans-serif; }"

content = content.replace(old_root, new_root)
content = content.replace(old_body, new_body)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
