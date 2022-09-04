# **[ura](../index.md).[src](../src.md).[globals](globals.md)**

## **Variables**

`CFLOP`

```mermaid
flowchart LR
    A([Config]) --> B[Grab CFLOP]
    B --> C{Last item}
        C --> |false| D{File exists?}
            D --> |true| E([Read config file])
            D --> |false| C
        C --> |true| F{OS?}
            F --> |Windows| G[Initialize config file<br>at first lookup path] --> E
            F --> |*nix| H{.AppImage?}
                H --> |true| I[Initialize config file<br>at second lookup path] --> E
                H --> |false| G
```

## **Functions**

<h3><b><a href="#func-init" id="func-init">init</a></b></h3>

```python
(idx: int) ‑> None
```
