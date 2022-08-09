(
python -m pip install -r dev/constants/req.txt &
rm -rf dist/ tmp/ &
wait
) &&
mkdir tmp/ &&
(
    cp -r ura/** tmp/ &
    wget -O tmp/python.AppImage "$(wget -qSO - "https://api.github.com/repos/niess/python-appimage/releases/tags/python3.10" 2>/dev/null | grep -E "browser_download_url.*x86_64" | cut -d '"' -f4 | tail -1)" >/dev/null &
    python -c "from dev.scripts.py.eb import main;main('linux','tmp/cfg.yml')" &
    wait
) &&
chmod +x ./tmp/python.AppImage &&
./tmp/python.AppImage --appimage-extract >/dev/null &&
mv squashfs-root tmp/python/ &&
(
    rm -f ./tmp/python.AppImage &
    python -c "import re
F='tmp/gui/main.js'
with open(F,'r') as f:i=f.read()
i=re.sub(r'const scriptPath.+',f'const scriptPath = path.join(__dirname, \'../\')',i,count=1)
with open(F,'w') as f:f.write(re.sub(r'const pythonPath.+',f'const pythonPath = path.join(__dirname, \'../python/opt/python3.10/bin/python3.10\')',i))" &
    python -c "import re
F='tmp/src/__init__.py'
with open(F,'r') as f:i=f.read()
with open(F,'w') as f:f.write(re.sub(r'appimage.+',f'appimage = True',i))" &
    ./tmp/python/usr/bin/pip3 install --upgrade pip --no-warn-script-location --no-cache-dir --disable-pip-version-check &
    ./tmp/python/usr/bin/pip3 uninstall wheel -y --no-cache-dir --disable-pip-version-check &
    wait
) &&
./tmp/python/usr/bin/pip3 install --no-warn-script-location --no-cache-dir --disable-pip-version-check -r requirements.txt
yarn electron-builder --config "tmp/cfg.yml"