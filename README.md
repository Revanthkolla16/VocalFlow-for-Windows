# VocalFlow Windows

VocalFlow is a system tray dictation app that allows you to cleanly inject dictated text into any application you are currently typing in. It is a Windows port built in Python, originally matching the MacOS menu bar app made by VocalLabs.

## Features
- **Hold-to-Talk**: Just press and hold the configured hotkey, speak, and release.
- **Deepgram Live Streaming**: Instant and highly accurate speech-to-text transcription.
- **Groq LLM Support**: Clean your grammar, transliterate hinglish, or translate on the fly!
- **System Tray Agent**: Lives cleanly out of your way until you need it.
- **Wallet Status**: View your available Deepgram or Groq balances right from the system tray menu.

## Prerequisites
- Python 3.10+
- Windows 10/11

## Setup Instructions
1. Clone this repository to your local machine.
2. Copy `config.example.py` to `config.py` and paste your API keys in before running the app.
3. Once configured, open the repository location in terminal and run `build.bat`. This will automatically install requirements and launch the agent.

## How To Use
1. The App will start and sit in your Windows System Tray (the small arrow area on the bottom right of the taskbar).
2. Click down and hold the Hotkey (by default this is `Right Alt`).
3. Speak your message clearly into your microphone.
4. Release the hotkey. The transcribed (and potentially, AI-cleaned) text will automatically inject right where your cursor is currently located!

## API Keys
To get started you need:
- **Deepgram API Key**: [Get one here](https://console.deepgram.com/) - Gives you the lowest latency voice to text.
- **Groq API Key**: [Get one here](https://console.groq.com/keys) - Allows you to utilize LLM post-processing to fix spelling or grammar instantly!

## Configuration Options
Inside `config.py`, or accessible during runtime via the app's `Settings` menu natively, you have access to:
- `DEEPGRAM_API_KEY`: Required string to use Deepgram API.
- `GROQ_API_KEY`: Required string to use Groq API.
- `HOTKEY`: Your capture trigger string, eg "right alt", "left alt", "right ctrl", "caps lock".
- `DEEPGRAM_MODEL`: Set out of the box to "nova-2".
- `DEEPGRAM_LANGUAGE`: By default set to "en-IN".
- `GROQ_ENABLED`: True/False on whether LLM pipelines process the transcript string.
- `GROQ_MODE`: "grammar", "transliteration", "translation", "none" depending on the LLM capability you want executed.
- `GROQ_TARGET_LANGUAGE`: Only used if mode is "translation".

## Project Structure
- `config.example.py`: Environment variable placeholder file.
- `config.py`: Local hardcoded settings repository (ignored by Git).
- `main.py`: Entry point connecting all flows together.
- `hotkey_manager.py`: Global keyword detection loop execution logic.
- `audio_engine.py`: Captures microphone context into bytestream sequences.
- `deepgram_service.py`: Performs remote connections via WebSocket API for text-matching out of audio streams.
- `groq_service.py`: Takes given sentences and forces instruction following on them via standard models.
- `text_injector.py`: Utility managing clipboard content backing and pasting keybind strokes.
- `tray_app.py`: UI wrapper using Python PIL to establish taskbar interactivity.
- `balance_checker.py`: Module encapsulating checking token balance off API.
- `settings_ui.py`: Custom module invoking window logic configuration editing.

## Known Limitations
- The underlying `keyboard` library implementation can be slightly touchy with conflicting hooks from other running anti-cheats or security tools in Windows environments.
- Attempting to capture in high-latency network conditions may result in some dictation lag.

## License
MIT