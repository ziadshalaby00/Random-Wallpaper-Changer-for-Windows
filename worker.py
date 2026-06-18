# worker.py
import os
import sys
import json
import random
import ctypes


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
HISTORY_FILE = os.path.join(BASE_DIR, "wallpaper_history.json")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)


def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)


def choose_random_wallpaper(folder):
    images = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".bmp"))
    ]

    if not images:
        return

    history = load_history()

    history = [img for img in history if os.path.exists(img)]
    remaining = [img for img in images if img not in history]

    if not remaining:
        history = []
        remaining = images

    selected = random.choice(remaining)
    set_wallpaper(selected)

    history.append(selected)
    save_history(history)


# ---------------- Execution ----------------
if __name__ == "__main__":
    config = load_config()

    if config and config.get("enabled", False):
        folder = config.get("wallpaper_path", "")

        if folder and os.path.exists(folder):
            choose_random_wallpaper(folder)