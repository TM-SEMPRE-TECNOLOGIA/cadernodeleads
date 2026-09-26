import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Check all classes with bg-white or light backgrounds
classes = re.findall(r'class="([^"]+)"', text)
missing_dark_bg = []
missing_dark_text = []

for c in classes:
    tokens = c.split()
    if 'bg-white' in tokens and not any(t.startswith('dark:bg-') for t in tokens):
        missing_dark_bg.append(c)
    if any(t in ['text-zinc-900', 'text-zinc-950', 'text-black'] for t in tokens) and not any(t.startswith('dark:text-') for t in tokens):
        missing_dark_text.append(c)

print(f"Missing dark:bg for bg-white: {len(missing_dark_bg)}")
for m in missing_dark_bg[:10]:
    print("  BG:", m[:100])

print(f"\nMissing dark:text for dark text: {len(missing_dark_text)}")
for m in missing_dark_text[:10]:
    print("  TXT:", m[:100])
