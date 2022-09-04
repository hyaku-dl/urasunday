menu() {
    if [[ $# != 0 ]]; then
        python -c "from dev.scripts.py.main import main;main('$1')"
    else
        python -c "from dev.scripts.py.main import main;main()"
    fi
}