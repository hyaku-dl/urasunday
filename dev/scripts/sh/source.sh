# shellcheck disable=SC1087,SC1091,SC2025,SC2059,SC2119,SC2120,SC2162,SC2148,SC2154,SC2155,SC2195

# Source
. "$XDG_CONFIG_HOME"/bash/source.sh

# Constants
PRVA=("alpha" "beta" "rc")

# Dependencies

options() {

    # little helpers for terminal print control and key input
    ESC=$(printf "\033")
    cursor_blink_on() { printf "$ESC[?25h"; }
    cursor_blink_off() { printf "$ESC[?25l"; }
    cursor_to() { printf "$ESC[$1;${2:-1}H"; }
    print_option() { printf "   $1 "; }
    print_selected() { printf "  $ESC[7m $1 $ESC[27m"; }
    get_cursor_row() {
        IFS=';' read -sdR -p $'\E[6n' ROW _
        echo "${ROW#*[}"
    }
    key_input() {
        read -s -n3 key 2>/dev/null >&2
        if [[ $key = $ESC[A ]]; then echo up; fi
        if [[ $key = $ESC[B ]]; then echo down; fi
        if [[ $key = "" ]]; then echo enter; fi
    }

    # initially print empty new lines (scroll down if at bottom of screen)
    for opt; do printf "\n"; done

    # determine current screen position for overwriting the options
    local lastrow="$(get_cursor_row)"
    local startrow="$((lastrow - $#))"

    # ensure cursor and input echoing back on upon a ctrl+c during read -s
    trap "cursor_blink_on; stty echo; printf '\n'; exit" 2
    cursor_blink_off

    local selected=0
    while true; do
        # print options by overwriting the last lines
        local idx=0
        for opt; do
            cursor_to "$((startrow + idx))"
            if [ $idx -eq $selected ]; then
                print_selected "$opt"
            else
                print_option "$opt"
            fi
            ((idx++))
        done

        # user key control
        case $(key_input) in
        enter) break ;;
        up)
            ((selected--))
            if [ $selected -lt 0 ]; then selected=$(($# - 1)); fi
            ;;
        down)
            ((selected++))
            if [ "$selected" -ge $# ]; then selected=0; fi
            ;;
        esac
    done

    # cursor position back to normal
    cursor_to "$lastrow"
    printf "\n"
    cursor_blink_on

    return "$selected"
}

fmt() { (
    t " Python Imports Sorted" "Sorting Python Imports Failed." isort -q --gitignore . &
    t "Python Files Formatted" "Formatting Python Files Failed." black -q . &
    wait
); }

cp() {
    inner() {
        local v bd mj yml fn
        readarray -d ' ' -t v <<<"$(_ver)"
        bd="dev/constants/${v[1]}/${v[2]}"
        mj=$(niet .cp "$bd/_meta.yml" -f json)
        for i in $(echo "$mj" | jq -r 'keys[]'); do
            yml="$bd/$i.yml"
            fn="$(echo "$mj" | jq -r ".$i.dir")"
            case "$(echo "$mj" | jq -r ".$i.fmt // \"mp\"")" in
            yaml | yml)
                cp "$yml" "$fn.yml"
                ;;
            *)
                niet . "$yml" -f json | json2msgpack -o "$fn.mp"
                ;;
            esac
        done
    }
    t "Copying Constants" "Copying Constants Failed." inner
}

req() {
    pip install --upgrade pip
    for i in $(
        for j in $(niet development.venv.requirements dev/vars.yml); do
            niet requirements."$j" dev/vars.yml
        done
    ); do
        python -m pip install -r "$i"
    done
}

push() {
    local msg v vls
    printf "Commit Message: "
    read -r msg
    if [ $# -eq 0 ]; then
        [ -z "$msg" ] && msg="push"
    else
        readarray -d ' ' -t vls <<<"$1"
        v=$(printf "-%s" "${vls[@]}")
        [ -n "$msg" ] && msg="$msg, "
        msg="$msg""https://hyaku.download/changelog#v${v:1}"
    fi
    inner() { git add . && git commit -am "\"$msg\"" && git push; }
    t "Pushing Changes" "Pushing Changes Failed." inner
}

test() {
    python <"dev/scripts/py/test/$1.py"
}

if type "$1" >/dev/null 2>&1; then
    cmd=$1
    shift
    "$cmd" "$@"
else
    echo "dev: $1 is not a valid command."
fi
