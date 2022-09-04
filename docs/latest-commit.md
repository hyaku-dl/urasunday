<h1 align="center" style="font-weight: bold">
    Latest Commit
</h1>

## **Summary**

Massive documentation overhaul!

## **Changes**

### **Added**

- `dev/raw_docs/faq.ymd` for frequently-asked questions.
- `What's this` and `Further Reading` sections in `dev/raw_docs/README.ymd`.
- Finally added the ability to dynamically modify the contents of `mkdocs.yml` according to the contents of `dev/vars.yml`
- `str_representer` in `dev/scripts/py/cfg.py` for formatting multiline strings in dumped yaml.
- `dev/scripts/sh/source.sh`'s `tb` function to **t**est **b**uild commands. <!-- cspell: disable-line -->
- `author` and `wakatime` entries in `dev/vars.yml`'s `md_vars.global` dictionary.
- `squashfs-root/` entry in `.gitignore`
- `MD004` entry in `.markdownlint.yml`

### **Changed**

- Moved `dev/constants/tpl/` to `dev/constants/tpl/pdoc/`.
- Moved `dev/constants/0/0/` to `dev/constants/tpl/version/0/0/`.
- Added back `mdformat-shfmt` as a Python requirement for developer utilities.
- `.github/workflows/build.yml` .AppImage build commands so that you can run the cli by appending the `cli` subcommand to the command for running the said AppImage. For example, `./ura.AppImage cli [flags]`.
- Renamed `dev/raw_docs/latest bump.mako`, `dev/raw_docs/latest commit.mako`, `dev/raw_docs/latest commit.mmd`, `dev/raw_docs/latest release notes.mako`, `dev/raw_docs/latest release notes.mako`, `dev/raw_docs/notes to self.ymd`, and the files that they generate so that they does not have a space in their filename, as it yields a much elegant URL. Also modified the dependent files.
- Improved documentation. This is the fucking highlight of the commit, y'know.
- `dev/scripts/py/main.py`'s `main` function to pass the argument to `dev/scripts/sh/source.sh` when it does not match to any condition on the former script.
- `dev/scripts/py/md_vars.py`'s way of appending dynamically-generated global variables
- `dev/scripts/sh/source.sh`'s `req` function to download `niet` as a Python dependency for development utilities.

### **Removed**

- `print("fuck")` in `dev/scripts/py/inst_mods/whine_md_fmt/main.py`.
- `source.sh`'s `dev` function.

### **Fixed**

- `dev/raw_docs/README.ymd`'s link embedded on Wakatime's badge to point on the Wakatime website.
