<%
    import re
    from os import path

    RE_SUM = "(## \*\*Summary\*\*)\s*(.*?)(?=\n##\s|$)"
    RE_H3 = r"(### [^\n]*)\s*(?:<!--.+?-->)*(.*?)(?=\n###\s|$)"

    changes = ""

    with open(path.join(cwd, "latest commit.mmd"), "r") as f:
        TXT = f.read()

    x, y = re.search(RE_SUM, TXT, re.DOTALL).span()
    sum = f"{TXT[x:y]}\n".strip()

    for tc in re.findall(RE_H3, TXT, re.DOTALL):
        t, c = tc
        c = c.strip()
        if c != "":
            changes += f"{t}\n\n{c}\n\n"

    changes = changes.strip() + '\n'
%>
<h1 align="center" style="font-weight: bold">
    Latest Commit
</h1>

${sum}
<%text>
## **Changes**
</%text>
${changes}