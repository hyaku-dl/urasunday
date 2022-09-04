<h1 align="center" style="font-weight: bold">
    Config
</h1>

## **Configurations**

### **download_dir**: `str`

Directory to download the chapter at.

### **overwrite**: `bool`

Defaults to True.

Determines if the program overwrites the chapter if it is already downloaded.

### **overwrite_prompt**: `bool`

Determines if the program prompts the user to overwrite the chapter if it is already downloaded.

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
