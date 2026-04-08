import config
import requests

def transcribe(audio_bytes):
    if not audio_bytes:
        return ""
        
    try:
        url = "https://api.deepgram.com/v1/listen"
        
        params = {
            "model": config.DEEPGRAM_MODEL,
            "language": config.DEEPGRAM_LANGUAGE,
            "smart_format": "true",
            "channels": 1,
            "sample_rate": 16000,
            "encoding": "linear16"
        }
        
        headers = {
            "Authorization": f"Token {config.DEEPGRAM_API_KEY}",
            "Content-Type": "audio/raw"
        }
        
        response = requests.post(url, headers=headers, params=params, data=audio_bytes, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            try:
                transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
                return transcript
            except (KeyError, IndexError):
                return ""
        else:
            print(f"Deepgram HTTP Error: {response.status_code} - {response.text}")
            return ""
            
    except Exception as e:
        print(f"Deepgram error: {e}")
        return ""

def get_balance():
    try:
        headers = {
            "Authorization": f"Token {config.DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }
        res = requests.get("https://api.deepgram.com/v1/projects", headers=headers, timeout=5)
        if res.status_code != 200:
            return "Unable to fetch balance"
            
        projects = res.json().get("projects", [])
        if not projects:
            return "Unable to fetch balance"
            
        project_id = projects[0]["project_id"]
        
        res2 = requests.get(f"https://api.deepgram.com/v1/projects/{project_id}/balances", headers=headers, timeout=5)
        if res2.status_code != 200:
            return "Unable to fetch balance"
            
        balances = res2.json().get("balances", [])
        if not balances:
            return "Unable to fetch balance"
            
        amount = balances[0].get("amount", 0)
        return f"${amount:.2f}"
    except Exception as e:
        return "Unable to fetch balance"
