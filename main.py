import hotkey_manager
import audio_engine
import deepgram_service
import groq_service
import text_injector
import tray_app
import overlay
import tkinter as tk
from tkinter import messagebox
import threading
import os

def show_error(msg):
    def _err():
        r = tk.Tk()
        r.withdraw()
        messagebox.showerror("Error", msg)
        r.destroy()
    threading.Thread(target=_err, daemon=True).start()

def on_press():
    tray_app.set_status("Recording...")
    overlay.update_status("Recording...")
    audio_engine.start_recording()

def on_release():
    tray_app.set_status("Processing...")
    overlay.update_status("Processing...")
    
    def process():
        try:
            audio_bytes = audio_engine.stop_recording()
            if not audio_bytes:
                show_error("Audio block empty. Is your microphone securely connected?")
                tray_app.set_status("Idle")
                overlay.update_status("Idle")
                return
                
            tray_app.set_status("Transcribing...")
            overlay.update_status("Transcribing...")
            transcript = deepgram_service.transcribe(audio_bytes)
            
            if not transcript:
                show_error("Deepgram caught no speech or returned an empty transcript. Spoke too quietly?")
                tray_app.set_status("Idle")
                overlay.update_status("Idle")
                return
                
            tray_app.set_status("AI cleaning...")
            overlay.update_status("AI cleaning...")
            final_text = groq_service.process_text(transcript)
            
            tray_app.set_status("Injecting...")
            overlay.update_status("Injecting...")
            text_injector.inject_text(final_text)
            
        except Exception as e:
            show_error(f"Processing error: {str(e)}")
            
        tray_app.set_status("Idle")
        overlay.update_status("Idle")
        
    threading.Thread(target=process, daemon=True).start()

def on_exit():
    hotkey_manager.stop()
    audio_engine.stop_recording()
    
    # Force exit in case threads are hanging
    os._exit(0)

def main():
    if not os.path.exists("assets"):
        os.makedirs("assets")

    try:
        overlay.start()
        hotkey_manager.start(on_press, on_release)
        tray_app.start(on_exit)
    except Exception as e:
        show_error(f"Startup error: {str(e)}")

if __name__ == "__main__":
    main()
