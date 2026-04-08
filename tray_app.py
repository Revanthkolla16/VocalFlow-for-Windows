import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox
import os
import settings_ui
import balance_checker
import threading

_icon = None

def create_fallback_icon():
    image = Image.new('RGB', (64, 64), color = (0, 120, 215))
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
    return image

def get_icon():
    if os.path.exists("assets/icon.png"):
        try:
            return Image.open("assets/icon.png")
        except:
            pass
    return create_fallback_icon()

def set_status(status_text):
    global _icon
    if _icon is not None:
        _icon.menu = _build_menu(status_text)
        _icon.update_menu()

def on_deepgram_balance(icon, item):
    def callback(res):
        tk_root = tk.Tk()
        tk_root.withdraw()
        messagebox.showinfo("Deepgram Balance", res)
        tk_root.destroy()
    balance_checker.get_deepgram_balance(callback)

def on_groq_balance(icon, item):
    def callback(res):
        tk_root = tk.Tk()
        tk_root.withdraw()
        messagebox.showinfo("Groq Balance", res)
        tk_root.destroy()
    balance_checker.get_groq_balance(callback)

def on_settings(icon, item):
    threading.Thread(target=settings_ui.open_settings, daemon=True).start()

_on_exit = None

def on_quit(icon, item):
    icon.stop()
    if _on_exit:
        _on_exit()

def _build_menu(status_text="Idle"):
    return pystray.Menu(
        pystray.MenuItem("VocalFlow", lambda: None, enabled=False),
        pystray.MenuItem(f"Status: {status_text}", lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Deepgram Balance", on_deepgram_balance),
        pystray.MenuItem("Groq Balance", on_groq_balance),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Settings", on_settings),
        pystray.MenuItem("Quit", on_quit)
    )

def start(on_exit_callback):
    global _icon, _on_exit
    _on_exit = on_exit_callback
    _icon = pystray.Icon("VocalFlow", get_icon(), "VocalFlow", _build_menu())
    _icon.run()
