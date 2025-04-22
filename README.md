# Monitor Brightness Controller

A lightweight Python GUI tool to control external monitor brightness using the `monitorcontrol` library and DDC/CI support.

🔧 Now available as a standalone `.exe` — no need to install Python!

---

## ✨ Features

- 🖥️ Adjust monitor brightness using a clean slider interface
- 🔁 Reset brightness to original level
- ✅ Auto-installs required packages (Python version only)
- 🔐 Requires admin privileges to access DDC/CI
- 🎨 Minimal dark UI with Material-like design (tkinter-based)
- 💡 Works with most DDC/CI-enabled monitors

---

## 🛠️ Requirements

### For Python Script (`brightness_controller.py`):
- Python 3.6+
- Windows OS
- Monitor with **DDC/CI** enabled
- Must be run as **Administrator**
- Internet connection (for one-time auto-install of `monitorcontrol`)

### For EXE File (`brightness_controller.exe`):
- No Python required
- Just double-click the `.exe`
- Tested on Windows 10 / 11
- Must be run as **Administrator**

---

## 📦 Dependencies

Only one external dependency:

```
monitorcontrol
```

To install manually:

```bash
pip install monitorcontrol
```

Or use:

```bash
pip install -r requirements.txt
```

---

## 🏗️ Build the EXE Yourself

Want to compile the `.exe` from source?

```cmd
pip install pyinstaller && ^
pyinstaller --onefile --noconsole --icon="icon.ico" brightness_controller.py
```

✅ The compiled `.exe` will be located in:

```
dist/brightness_controller.exe
```

> 📌 Ensure:
> - `icon.ico` is valid (recommended: 256x256 resolution)
> - You run the final `.exe` as **Administrator**
> - Your monitor supports **DDC/CI**

---

## ⚠️ Notes

- This tool supports only the **first detected monitor**
- Ensure **DDC/CI** is enabled in your monitor’s physical menu/settings
- If no compatible monitor is found, a user-friendly error message will appear

---

## 📄 License

MIT License

---

Made with 💡 for smooth brightness control on Windows.
