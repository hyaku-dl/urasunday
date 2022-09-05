<h1 align="center" style="font-weight: bold">
    Latest Commit
</h1>

## **Summary**

Massive documentation overhaul!

## **Changes**

### **Changed**

- `dev/scripts/py/main.py`'s `main` function to also generate scripts.

### **Fixed**

- `dev/raw_docs/changelog.mako` as it cannot parse the version bump's description if it contained a hash (`#`) character.
- `dev/raw_docs/changelog.mako`'s incorrect latest version bump.
- `dev/scripts/py/rn_md.py` to read the correct markdown file for the latest release's notes.
