import pyperclip
import pyautogui
import time

def inject_text(text):
    if not text:
        return
        
    original = ""
    try:
        original = pyperclip.paste()
    except Exception:
        pass
        
    pyperclip.copy(text)
    time.sleep(0.2)
    
    # If using Alt, Windows often focuses the app menu bar upon release.
    # Yielding a quick ESC or relying on user switching fixes this. We will try just Ctrl+V with stronger wait.
    pyautogui.hotkey('ctrl', 'v')
    
    time.sleep(0.5)
    if original:
        pyperclip.copy(original)
