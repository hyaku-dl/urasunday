function main
{
    pip install --upgrade pip
    foreach ( $i in (python -m niet development.venv.requirements dev\vars.yml) ) {
    python -m pip install -r $(python -m niet requirements.$i dev\vars.yml)
    }
}
t "Installing Requirements" "Installing Requirements Failed." main