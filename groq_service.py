import config
from groq import Groq
import requests

def process_text(text):
    if not text:
        return text
        
    if not getattr(config, "GROQ_ENABLED", True):
        return text
        
    mode = getattr(config, "GROQ_MODE", "none")
    if mode == "none":
        return text
        
    system_prompt = ""
    if mode == "grammar":
        system_prompt = "You are a direct dictation cleaner. Fix spelling and grammar. Output ONLY the corrected text. Do NOT add conversational filler like 'Here is the text'. If it sounds fine, just output it unchanged."
    elif mode == "transliteration":
        system_prompt = "This is code-mixed text (Tanglish, Hinglish, etc). Transliterate and clean it. Return only the result."
    elif mode == "translation":
        target = getattr(config, "GROQ_TARGET_LANGUAGE", "English")
        system_prompt = f"Translate to {target}. Return only the translation."
    else:
        return text

    try:
        client = Groq(api_key=config.GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            model=config.GROQ_MODEL,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq error: {e}")
        return text

def get_balance():
    try:
        # Fallback implementation as Groq doesn't have a public standard API for balance
        # on standard API tokens
        headers = {
            "Authorization": f"Bearer {config.GROQ_API_KEY}"
        }
        res = requests.get("https://api.groq.com/openai/v1/dashboard/billing/credit_grants", headers=headers, timeout=3)
        if res.status_code == 200:
            data = res.json()
            total_granted = data.get("total_granted", 0.0)
            total_used = data.get("total_used", 0.0)
            balance = total_granted - total_used
            return f"${balance:.2f}"
            
        return "Balance info unavailable"
    except Exception as e:
        return "Unable to fetch balance"
