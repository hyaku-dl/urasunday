dev() {
    if [[ $# = 0 ]]; then
        python -c "from dev.scripts.py.main import main;main()"
    else
        bash dev/scripts/sh/source.sh "$@"
    fi
}