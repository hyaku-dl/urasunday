<%
    import re
    from os import path

    RE_H1 = re.compile(r"# ([^\n]*)(.*?)(?=\n#\s|$)", re.DOTALL)
    RE_DESC = re.compile(r'^(?!## )(.+?)\n\n## ', re.DOTALL)
    RE_H2 = re.compile(r"## ([^\n]*)\s*(.*?)(?=\n##\s|$)", re.DOTALL)
    RE_LC = re.compile(r"- (.*?)(?=- |$)", re.DOTALL)

    PR = ["alpha", "beta", "rc"]

    def rv(vls: list[str | int]):
        pr = ""
        vls = [int(i) for i in vls]
        if vls[4] <= 2:
            pr = f'-{PR[vls[4]]}.{vls[5]}'
        return ".".join([str(i) for i in vls[0:4]]) + pr

    with open(path.join(cwd, "changelog.mmd"), "r") as f:
        CL = f.read()

    d_op = {}
    for vb in RE_H1.findall(CL):
        ver, dtls = vb
        vls = ver.split(" ")
        if desc := RE_DESC.match(dtls):
            desc = desc.group(1)
        else:
            desc = ''
        d_op[rv(vls)] = ov = {
            "vls": vls,
            "anchor": ver.replace(" ", "-"),
            "desc": desc.strip(),
            "changes": {}
        }
        for tch in RE_H2.findall(dtls):
            t, chls = tch
            ov["changes"][t] = ovt = []
            for ch in RE_LC.findall(chls):
                ovt.append(ch)

    md_op = ""
    for k, v in d_op.items():
        md_op += f'\n\n<h2 id="{v["anchor"]}">{k}</h2>'
        if desc:=v["desc"]:
            md_op += f'\n\n{desc}\n\n'
        else:
            md_op += ''
        for t, chls in v["changes"].items():
            md_op += f'\n\n<h3 id="{v["anchor"]}-{t.lower()}">{t}</h3>\n'
            for ch in chls:
                md_op += f'\n- {ch}'
%>
<h1 align="center" style="font-weight: bold">
    Changelog
</h1>${md_op}