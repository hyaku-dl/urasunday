<h1 align="center" style="font-weight: bold">
    Config
</h1><%
import yaml
from os import path
with open(path.join('dev/constants/version', '/'.join(cwd.split('/')[-2:]), 'config.yml')) as f:
    yml = yaml.safe_load(f.read())

md_op = ""
for k, v in yml["config"].items():
    md_op += f'\n\n### **{k}**: `{v["type"]}`'
    if v.get("req", False):
        md_op += '<font color="#ED5E5E">*</font>'

    if de:=v.get("default", None):
        md_op += f'\n\nDefaults to {de}.'

    if desc:=v.get("desc", None):
        md_op += '\n\n' + desc
%>
<%text>
## **Configurations**</%text>${md_op}
<%text>
## **Config File**

### **Config File Lookup Order of Precedence (CFLOP)**

Hyaku is a cross-platform project, which means that it could be ran in different OS.
There is however a lack of unity in the standardization on the location of config files in this OSes.
And such, I have devised a precedence order for Hyaku's config file in different platforms.

The following are the CFLOP for different OSes:

```mermaid
flowchart TD
    A([CFLOP]) --> L[--config argument]
        L --> B{OS?}
        B --> |*nix| C[./ura.yml]
            subgraph <br>
                C --> D{"XDG<br>CONFIG<br>HOME<br>(XCH)?"}
                D --> |true| E["${XCH}/ura/config.yml"] --> F
                D --> |false| F["~/.config/ura/config.yml"]
                F --> G["~/.ura"]
            end
        B --> |Windows| J[.\ura.yml]
            subgraph <br><br>
                J --> K["${boot drive}:\\<br>Users\${username}\<br>AppData\Roaming\ura\<br>config.yml"]
            end
```
</%text>