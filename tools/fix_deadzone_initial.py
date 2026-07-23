from pathlib import Path

path = Path("dial2.html")
text = path.read_text(encoding="utf-8")
needle = "  deadZoneEl.setAttribute('fill', 'none');\n"
replacement = (
    "  deadZoneEl.setAttribute('fill', 'none');\n"
    "  // A circle with no dash pattern renders as a full ring. Seed the\n"
    "  // dead zone at zero length so first load matches later replays.\n"
    "  deadZoneEl.setAttribute('stroke-dasharray', `0 ${gCircumference}`);\n"
)
if needle not in text:
    raise SystemExit("Expected dead-zone setup line not found")
path.write_text(text.replace(needle, replacement, 1), encoding="utf-8")
