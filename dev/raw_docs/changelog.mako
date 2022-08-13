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

    d_op = {}
    vls_ls = []
    for vb in re.findall(RE_H1, CL, re.DOTALL):
        ver, desc, tls = vb
        vls = ver.split(" ")
        vls_ls.append(vls)
        d_op[rv(vls)] = ov = {
            "vls": vls,
            "anchor": ver.replace(" ", "-"),
            "desc": desc.strip(),
            "changes": {}
        }
        for tch in re.findall(RE_H2, tls, re.DOTALL):
            t, chls = tch
            ov["changes"][t] = ovt = []
            for ch in re.findall(RE_LC, chls, re.DOTALL):
                ovt.append(ch)

    md_op = ""
    for idx, (k, v) in enumerate(d_op.items()):
        href = v["anchor"]
        comp = ""
        if (idx + 1) != len(vls_ls):
            comp = f" ({compare(vls_ls[idx+1], vls_ls[idx])})"
        md_op += f'\n\n## <a href="#{href}" id="{href}">{k}{comp}</a>'
        if desc:=v["desc"]:
            md_op += f'\n\n{desc}\n\n'
        else:
            md_op += ''
        for t, chls in v["changes"].items():
            href = f'{v["anchor"]}-{t.lower()}'
            md_op += f'\n\n### <a href="#{href}" id="{href}">{t}</a>\n'
            for ch in chls:
                md_op += f'\n- {ch}'
%>
<h1 align="center" style="font-weight: bold">
    Changelog
</h1>${md_op}