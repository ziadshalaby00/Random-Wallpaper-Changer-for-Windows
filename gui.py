# gui.py
import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


# ---------------- Config ----------------
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    return {
        "enabled": False,
        "wallpaper_path": ""
    }


def save_config(enabled, path):
    data = {
        "enabled": enabled,
        "wallpaper_path": path
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)


# ---------------- Registry ----------------
TASK_NAME = "FastWallpaperWorker"

import winreg

REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "FastWallpaperWorker"

def enable_registry_startup():
    worker_path = os.path.join(BASE_DIR, "worker.exe")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{worker_path}"')
        winreg.CloseKey(key)
        
        messagebox.showinfo("Success", "Enabled successfully!")
        update_status_label(True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to enable: {e}")

def disable_registry_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        
        messagebox.showinfo("Success", "Disabled successfully!")
        update_status_label(False)
    except FileNotFoundError:
        update_status_label(False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to disable: {e}")


# ---------------- UI Actions ----------------
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder)


def enable():
    path = path_entry.get()

    if not os.path.exists(path):
        messagebox.showerror("Error", "Invalid folder path. Please select a valid directory.")
        return

    save_config(True, path)
    
    subprocess.Popen(
        os.path.join(BASE_DIR, "worker.exe"),
        creationflags=subprocess.CREATE_NO_WINDOW
    )
        
    enable_registry_startup()


def disable():
    path = path_entry.get()
    save_config(False, path)
    disable_registry_startup()


def update_status_label(is_enabled):
    if is_enabled:
        status_label.config(text="Status: Active (Fast Boot Enabled)", fg="green")
    else:
        status_label.config(text="Status: Inactive", fg="red")


# ---------------- UI Setup ----------------
root = tk.Tk()
root.title("Wallpaper Manager")
root.geometry("450x190")
root.resizable(False, False)

# Label
tk.Label(root, text="Wallpaper Folder Path:", font=("Arial", 10, "bold")).pack(pady=5)

# Entry
path_entry = tk.Entry(root, width=50)
path_entry.pack(pady=2)

# Load Initial Config
config = load_config()
path_entry.insert(0, config.get("wallpaper_path", ""))

# Browse Button
tk.Button(root, text="Browse Folder", command=browse_folder, width=12).pack(pady=5)

# Status Label
status_label = tk.Label(root, text="", font=("Arial", 9, "italic"))
status_label.pack(pady=2)
update_status_label(config.get("enabled", False))

# Action Buttons Frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(
    frame,
    text="Enable",
    width=15,
    bg="#4CAF50",
    fg="white",
    command=enable
).grid(row=0, column=0, padx=10)

tk.Button(
    frame,
    text="Disable",
    width=15,
    bg="#f44336",
    fg="white",
    command=disable
).grid(row=0, column=1, padx=10)

footer = tk.Label(
    root,
    text="Developed by Ziad Shalaby © 2026",
    font=("Arial", 8),
    fg="gray"
)
footer.pack(side="bottom", pady=5)

root.mainloop()