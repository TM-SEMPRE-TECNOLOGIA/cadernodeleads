import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find JS section
script_match = re.findall(r'<script>(.*?)</script>', text, re.DOTALL)
js_code = script_match[-1]

# Find innerHTML assignments with bg-white or text-zinc-900 or bg-zinc-50
template_literals = re.findall(r'`([^`]{50,})`', js_code)
print(f"Total template literals in JS: {len(template_literals)}")

light_only_templates = []
for t in template_literals:
    has_light_bg = 'bg-white' in t or 'bg-zinc-50' in t or 'bg-amber-50' in t
    has_dark_bg = 'dark:bg-' in t
    if has_light_bg and not has_dark_bg:
        light_only_templates.append(t)

print(f"Templates with light background but NO dark:bg: {len(light_only_templates)}")
for idx, t in enumerate(light_only_templates[:10]):
    print(f"\n--- Template {idx+1} ---")
    lines = [l.strip() for l in t.split('\n') if 'bg-' in l or 'text-' in l]
    print("\n".join(lines[:5]))
