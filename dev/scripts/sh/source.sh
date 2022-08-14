# shellcheck disable=SC1087,SC1091,SC2025,SC2045,SC2059,SC2119,SC2120,SC2162,SC2148,SC2154,SC2155,SC2195

# Source
. "$XDG_CONFIG_HOME"/bash/source.sh

# commands

fmt() { (
    t " Python Imports Sorted" "Sorting Python Imports Failed." isort -q --gitignore . &
    t "    Markdown Formatted" "Formatting Markdown Failed." mdformat . &
    t "Python Files Formatted" "Formatting Python Files Failed." black -q . &
    wait
); }

req() {
    pip install --upgrade pip
    for i in $(
        for j in $(niet development.venv.requirements dev/vars.yml); do
            niet requirements."$j" dev/vars.yml
        done
    ); do
        python -m pip install -r "$i"
    done
    for i in $(ls -d dev/scripts/py/inst_mods/*/); do
        case $i in
        *"__pycache__"*) ;;
        *)
            pip install -e "${i%%/}"
            ;;
        esac
    done
}

test() {
    python <"dev/scripts/py/test/$1.py"
}

# main

if type "$1" >/dev/null 2>&1; then
    cmd=$1
    shift
    "$cmd" "$@"
else
    echo "dev: $1 is not a valid command."
fi
