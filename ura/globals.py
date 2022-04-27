import locale
import os
from os import get_terminal_size

TW = get_terminal_size().columns

if os.name != 'posix':
    import ctypes

    POSIX = 0

    CFLOP = [
        fr"{os.getcwd()}\ura.yml",
        fr"{os.getenv('USERPROFILE')}\AppData\Roaming\ura\config.yml"
    ]
    LOCALE = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()][:2]
else:
    POSIX = 1
    CFLOP = [
        f"{os.getcwd()}/ura.yml",
        "~/.config/ura/config.yml",
        "~/.ura",
        "/etc/ura/config.yml"
    ]
    if xch:=os.getenv('XDG_CONFIG_HOME'):
        CFLOP.insert(1, f"{xch}/ura/config.yml")
    LOCALE = locale.getdefaultlocale()[0][:2]