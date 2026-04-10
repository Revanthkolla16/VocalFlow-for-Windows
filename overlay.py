"""
Floating overlay pill that shows VocalFlow's current status on screen.
Appears near the bottom-center of the screen, auto-hides after going idle.
"""
import tkinter as tk
import threading

_root = None
_label = None
_visible = False
_hide_timer = None
_lock = threading.Lock()

# Status → (bg_color, fg_color, emoji)
_STATUS_STYLES = {
    "Recording...":    ("#e53935", "#ffffff", "\U0001f534"),   # Red circle
    "Processing...":   ("#fb8c00", "#ffffff", "\u23f3"),       # Hourglass
    "Transcribing...": ("#1e88e5", "#ffffff", "\U0001f4ac"),   # Speech bubble
    "AI cleaning...":  ("#8e24aa", "#ffffff", "\u2728"),       # Sparkles
    "Injecting...":    ("#43a047", "#ffffff", "\u2328\ufe0f"), # Keyboard
    "Idle":            ("#333333", "#aaaaaa", ""),
}

_DEFAULT_STYLE = ("#555555", "#ffffff", "\u2699\ufe0f")


def _create_window():
    """Create the overlay Tk window (must be called from the overlay thread)."""
    global _root, _label

    _root = tk.Tk()
    _root.title("VocalFlow Status")
    _root.overrideredirect(True)          # No title bar / border
    _root.attributes("-topmost", True)    # Always on top
    _root.attributes("-alpha", 0.9)       # Slight transparency
    _root.configure(bg="#222222")

    # Try to make the window click-through (Windows-only)
    try:
        _root.attributes("-transparentcolor", "")
    except tk.TclError:
        pass

    _label = tk.Label(
        _root,
        text="",
        font=("Segoe UI", 11, "bold"),
        padx=18,
        pady=6,
        bd=0,
        relief="flat",
    )
    _label.pack()

    # Start hidden
    _root.withdraw()

    # Run the main loop
    _root.mainloop()


def _position_window():
    """Position the pill at bottom-center of the screen."""
    if _root is None:
        return
    _root.update_idletasks()
    sw = _root.winfo_screenwidth()
    sh = _root.winfo_screenheight()
    ww = _root.winfo_width()
    x = (sw - ww) // 2
    y = sh - 120  # 120px from bottom
    _root.geometry(f"+{x}+{y}")


def _show():
    global _visible
    if _root and not _visible:
        _root.deiconify()
        _position_window()
        _visible = True


def _hide():
    global _visible
    if _root and _visible:
        _root.withdraw()
        _visible = False


def _apply_status(status_text):
    """Apply a status update on the Tk thread."""
    global _hide_timer

    if _root is None or _label is None:
        return

    bg, fg, emoji = _STATUS_STYLES.get(status_text, _DEFAULT_STYLE)
    display = f"  {emoji}  {status_text}  " if emoji else f"  {status_text}  "

    _label.config(text=display, bg=bg, fg=fg)
    _root.configure(bg=bg)

    # Cancel any pending hide
    if _hide_timer is not None:
        _root.after_cancel(_hide_timer)
        _hide_timer = None

    if status_text == "Idle":
        # Show "Idle" briefly then hide
        _show()
        _label.config(text="  \u2705  Done  ", bg="#43a047", fg="#ffffff")
        _root.configure(bg="#43a047")
        _hide_timer = _root.after(1500, _hide)
    else:
        _show()


def update_status(status_text):
    """Thread-safe status update. Can be called from any thread."""
    with _lock:
        if _root is not None:
            _root.after(0, lambda: _apply_status(status_text))


def start():
    """Start the overlay in a daemon thread. Call once at app startup."""
    t = threading.Thread(target=_create_window, daemon=True)
    t.start()
