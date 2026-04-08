import sounddevice as sd
import numpy as np
import threading
import queue

_audio_queue = queue.Queue()
_recording = False
_stream = None

def callback(indata, frames, time, status):
    if status:
        print(f"Error in audio capture: {status}")
    if _recording:
        _audio_queue.put(indata.copy())

def start_recording():
    global _recording, _stream
    _recording = True
    
    while not _audio_queue.empty():
        try:
            _audio_queue.get_nowait()
        except queue.Empty:
            break

    try:
        _stream = sd.InputStream(samplerate=16000, channels=1, dtype='int16', callback=callback)
        _stream.start()
    except Exception as e:
        print(f"Unable to access microphone: {e}")
        _recording = False

def stop_recording():
    global _recording, _stream
    _recording = False
    
    if _stream is not None:
        _stream.stop()
        _stream.close()
        _stream = None
        
    frames = []
    while not _audio_queue.empty():
        try:
            frames.append(_audio_queue.get_nowait())
        except queue.Empty:
            break
            
    if len(frames) > 0:
        return np.concatenate(frames).tobytes()
    return b""
