<h1 align="center" style="font-weight: bold">
    Latest Commit
</h1>

## **Summary**

Massive documentation overhaul!

## **Changes**

### **Changed**

- `dev/scripts/sh/source.sh`'s `fmt` function to only format the markdowns located under `docs/`.

### **Fixed**

- `.github/workflows/build.yml`'s `jobs.linux.steps[?name=='Build'].run` script, as the shitty appimagetool.AppImage is exiting with code `1` even though there IS NO FUCKING ERROR! GAAAAAAAHH! <!-- cspell: disable-line -->
