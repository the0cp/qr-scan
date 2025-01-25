# QR Scanner

![icon](https://github.com/user-attachments/assets/c37a5b7e-5b9f-4b0d-a6b4-598ffa494db4)

## Usage

Download: [https://github.com/the0cp/qr-scan/releases](https://github.com/the0cp/qr-scan/releases)

- Press hotkey "Ctrl+Shift+Q" to scan the screen
- The results will be stroed in the main window. (Max 20 records)
- Options to display popups near the qr-codes or display the list window directly
- Easy Copy / Open in browser

## Build

```
pip install -r requirements.txt

# generate ui.py files
pyside6-uic form.ui -o ui_form.py
pyside6-uic codebarwindow.ui -o ui_codebarwindow.py

# generate res.py files
pyside6-rcc res.qrc -o rc_res.py

pyinstaller -D -w .\qrhelper.py --icon=icons/icon.ico --upx-dir /path/to/upx/
```
