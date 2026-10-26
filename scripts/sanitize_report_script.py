from pathlib import Path

target = Path("scripts/generate_formal_project_report.py")
content = target.read_text(encoding="utf-8")

replacements = [
    ("\u2019", "'"),
    ("\u201c", '"'),
    ("\u201d", '"'),
    ("\u00b2", "<sup>2</sup>"),
    ("\u00b0C", " deg C"),
    ("\u00b0", " deg"),
    ("\u2013", "-"),
    ("\U0001f3c6", ""),
    ("\u2022", "&bull;"),
    ("\u00b1", "+/-"),
]

for old, new in replacements:
    content = content.replace(old, new)

target.write_text(content, encoding="utf-8")
print("Sanitization completed successfully.")
