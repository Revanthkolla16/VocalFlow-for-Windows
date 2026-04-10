import tkinter as tk
from tkinter import ttk, messagebox
import config
import os

_is_open = False

def open_settings():
    global _is_open
    if _is_open:
        return
    _is_open = True
    
    root = tk.Tk()
    root.title("VocalFlow Settings")
    root.geometry("450x420")
    root.resizable(False, False)
    
    dg_key_var = tk.StringVar(value=config.DEEPGRAM_API_KEY)
    groq_key_var = tk.StringVar(value=config.GROQ_API_KEY)
    hotkey_var = tk.StringVar(value=config.HOTKEY)
    dg_model_var = tk.StringVar(value=config.DEEPGRAM_MODEL)
    dg_lang_var = tk.StringVar(value=config.DEEPGRAM_LANGUAGE)
    groq_enabled_var = tk.BooleanVar(value=config.GROQ_ENABLED)
    groq_mode_var = tk.StringVar(value=config.GROQ_MODE)
    groq_target_var = tk.StringVar(value=config.GROQ_TARGET_LANGUAGE)

    row = 0
    tk.Label(root, text="Deepgram API Key:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
    tk.Entry(root, textvariable=dg_key_var, show="*", width=35).grid(row=row, column=1, padx=10, pady=10)
    row += 1

    tk.Label(root, text="Groq API Key:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
    tk.Entry(root, textvariable=groq_key_var, show="*", width=35).grid(row=row, column=1, padx=10, pady=10)
    row += 1

    tk.Label(root, text="Hotkey:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
    ttk.Combobox(root, textvariable=hotkey_var, values=["right alt", "left alt", "right ctrl", "caps lock"], state="readonly", width=32).grid(row=row, column=1, padx=10, pady=10)
    row += 1

    tk.Label(root, text="Deepgram Model:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
    tk.Entry(root, textvariable=dg_model_var, width=35).grid(row=row, column=1, padx=10, pady=10)
    row += 1

    tk.Label(root, text="Deepgram Language:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
    tk.Entry(root, textvariable=dg_lang_var, width=35).grid(row=row, column=1, padx=10, pady=10)
    row += 1

    tk.Label(root, text="Groq Enabled:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
    tk.Checkbutton(root, variable=groq_enabled_var).grid(row=row, column=1, sticky="w", padx=10, pady=10)
    row += 1

    tk.Label(root, text="Groq Mode:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
    mode_cb = ttk.Combobox(root, textvariable=groq_mode_var, values=["auto", "grammar", "transliteration", "translation", "none"], state="readonly", width=32)
    mode_cb.grid(row=row, column=1, padx=10, pady=10)
    row += 1

    tgt_label = tk.Label(root, text="Groq Target Language:")
    tgt_label.grid(row=row, column=0, sticky="w", padx=10, pady=10)
    tgt_entry = tk.Entry(root, textvariable=groq_target_var, width=35)
    tgt_entry.grid(row=row, column=1, padx=10, pady=10)
    row += 1

    def update_target_state(*args):
        if groq_mode_var.get() in ("translation", "auto"):
            tgt_entry.config(state="normal")
        else:
            tgt_entry.config(state="disabled")
    
    groq_mode_var.trace_add("write", update_target_state)
    update_target_state()

    def on_closing():
        global _is_open
        _is_open = False
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)

    def save():
        config.DEEPGRAM_API_KEY = dg_key_var.get()
        config.GROQ_API_KEY = groq_key_var.get()
        config.HOTKEY = hotkey_var.get()
        config.DEEPGRAM_MODEL = dg_model_var.get()
        config.DEEPGRAM_LANGUAGE = dg_lang_var.get()
        config.GROQ_ENABLED = groq_enabled_var.get()
        config.GROQ_MODE = groq_mode_var.get()
        config.GROQ_TARGET_LANGUAGE = groq_target_var.get()
        
        try:
            with open("config.py", "r", encoding="utf-8") as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith("DEEPGRAM_API_KEY ="):
                    lines[i] = f'DEEPGRAM_API_KEY = "{config.DEEPGRAM_API_KEY}"\n'
                elif line.startswith("GROQ_API_KEY ="):
                    lines[i] = f'GROQ_API_KEY = "{config.GROQ_API_KEY}"\n'
                elif line.startswith("HOTKEY ="):
                    lines[i] = f'HOTKEY = "{config.HOTKEY}"\n'
                elif line.startswith("DEEPGRAM_MODEL ="):
                    lines[i] = f'DEEPGRAM_MODEL = "{config.DEEPGRAM_MODEL}"\n'
                elif line.startswith("DEEPGRAM_LANGUAGE ="):
                    lines[i] = f'DEEPGRAM_LANGUAGE = "{config.DEEPGRAM_LANGUAGE}"\n'
                elif line.startswith("GROQ_ENABLED ="):
                    lines[i] = f'GROQ_ENABLED = {config.GROQ_ENABLED}\n'
                elif line.startswith("GROQ_MODE ="):
                    lines[i] = f'GROQ_MODE = "{config.GROQ_MODE}"\n'
                elif line.startswith("GROQ_TARGET_LANGUAGE ="):
                    lines[i] = f'GROQ_TARGET_LANGUAGE = "{config.GROQ_TARGET_LANGUAGE}"\n'
            
            with open("config.py", "w", encoding="utf-8") as f:
                f.writelines(lines)
                
            messagebox.showinfo("Success", "Settings saved successfully!\nPlease restart the app to apply Hotkey changes.", parent=root)
            on_closing()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save config: {e}", parent=root)

    btn_frame = tk.Frame(root)
    btn_frame.grid(row=row, column=0, columnspan=2, pady=10)
    
    tk.Button(btn_frame, text="Save", command=save, width=15).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Cancel", command=on_closing, width=15).pack(side="left", padx=10)

    root.mainloop()
