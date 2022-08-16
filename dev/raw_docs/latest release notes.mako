<%
    import re
    from os import path

    RE_H1 = r"# ([^\n]*)(\n[^#]+)(.*?)(?=\n#\s|$)"
    RE_H2 = r"## ([^\n]*)\s*(.*?)(?=\n##\s|$)"
    RE_LC = r"- (.*?)(?=- |$)"

    PR = ["alpha", "beta", "rc"]

    VERSIONS_NAME = [
        "User",
        "Dev",
        "Minor",
        "Patch",
        "Pre-release identifier",
        "Pre-release version",
    ]

    def compare(x, y):
        for idx, i in enumerate(VERSIONS_NAME):
            if int(y[idx]) == (int(x[idx]) + 1):
                return i + " bump"

        return None

    def rv(vls: list[str | int]):
        pr = ""
        vls = [int(i) for i in vls]
        if vls[4] <= 2:
            pr = f'-{PR[vls[4]]}.{vls[5]}'
        return ".".join([str(i) for i in vls[0:4]]) + pr

    with open(path.join(cwd, "changelog.mmd"), "r") as f:
        CL = f.read()

    changes = {}
    md_op = ""
    comp = ""

    vbls = re.findall(RE_H1, CL, re.DOTALL)
    vb = vbls[0]
    ver, desc, tls = vb
    vls = ver.split(" ")
    ver_str = rv(vls)
    anchor = ver.replace(" ", "-")
    desc = desc.strip()

    for tch in re.findall(RE_H2, tls, re.DOTALL):
        t, chls = tch
        changes[t] = ovt = []
        for ch in re.findall(RE_LC, chls, re.DOTALL):
            ovt.append(ch)

    if len(vbls) != 1:
        comp = f"{compare(vbls[1][0].split(), vls)}. "

    if (desc != "") or (comp != ""):
        md_op += f'## **Description**\n\n{comp}{desc}'
    else:
        md_op += ''
    for t, chls in changes.items():
        href = f'{anchor}-{t.lower()}'
        md_op += f'\n\n## **<a href="#{href}" id="{href}">{t}</a>**\n'
        for ch in chls:
            md_op += f'\n- {ch}'
%><h1 align="center" style="font-weight: bold">
    ${ver_str}
</h1>

${md_op}
