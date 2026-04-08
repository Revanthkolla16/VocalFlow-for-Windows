import keyboard
import config

_listener = None
_on_press = None
_on_release = None
_is_pressed = False

def start(on_press_callback, on_release_callback):
    global _listener, _on_press, _on_release, _is_pressed
    _on_press = on_press_callback
    _on_release = on_release_callback
    _is_pressed = False
    
    def on_event(e):
        global _is_pressed
        if e.name == config.HOTKEY:
            if e.event_type == keyboard.KEY_DOWN:
                if not _is_pressed:
                    _is_pressed = True
                    if _on_press:
                        _on_press()
            elif e.event_type == keyboard.KEY_UP:
                if _is_pressed:
                    _is_pressed = False
                    if _on_release:
                        _on_release()

    _listener = keyboard.hook(on_event)

def stop():
    global _listener
    if _listener is not None:
        keyboard.unhook(_listener)
        _listener = None
