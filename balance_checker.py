import threading
import deepgram_service
import groq_service

def get_deepgram_balance(callback):
    def run():
        result = deepgram_service.get_balance()
        if "$" in result and not result.startswith("Deepgram"):
            callback(f"Deepgram Balance: {result}")
        else:
            callback(result)
    threading.Thread(target=run, daemon=True).start()

def get_groq_balance(callback):
    def run():
        result = groq_service.get_balance()
        if result == "Balance info unavailable" or result == "Unable to fetch balance":
            callback(f"Groq: {result}")
        else:
            callback(result)
    threading.Thread(target=run, daemon=True).start()
