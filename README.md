# Automatically click the button

There's `reference-on.png` and `reference-off.png` that are captured using this script.
It's important to use this tool instead of other screenshot tool to make sure pixel is exactly the same.

`psutil` is used to send signal to process before operating the button.

## Requirements

```bash
sudo apt install gnome-screenshot python3-tk python3-dev python3-pip
pip install pyautogui psutil
```
