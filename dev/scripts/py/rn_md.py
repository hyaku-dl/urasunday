import re

with open("docs/latest release notes.md", "r") as f:
    op = re.sub(r"<h1 .+>.+<\/h1>", "", f.read(), 0, re.DOTALL).strip()
with open(".md", "w") as f:
    f.write(op)
