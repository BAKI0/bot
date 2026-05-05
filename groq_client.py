import json
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

# Initialize Groq client only if key is available
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def analyze_message(text: str, members_list: list) -> dict:
    """Analyze message for karma, sentiment, and topics."""
    if not client:
        return {"sentiment": "neutral", "target": None, "is_self_praise": False, "topic": "general", "religious_sentiment": "neutral"}
    
    prompt = f"""
    Analyze the following Telegram message.
    Known members context: {members_list}
    Message: "{text}"
    Respond ONLY with a raw JSON object matching this schema:
    {{ "sentiment": "positive|negative|neutral", "target": "@username or name or null", "is_self_praise": true|false, "topic": "religion|general", "religious_sentiment": "positive|negative|neutral" }}
    """
    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"[Groq Error] analyze_message: {e}")
        return {"sentiment": "neutral", "target": None, "is_self_praise": False, "topic": "general", "religious_sentiment": "neutral"}

def analyze_group_mood(messages_list: list) -> str:
    """Summarize the overall group mood for /moodreport."""
    if not client: return "AI unconfigured."
    
    prompt = f"Analyze the mood of these recent group messages:\n{messages_list}\nSummarize the overall group mood in one short sentence, categorizing it as Positive, Neutral, or Tense."
    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def summarize_chat(messages_list: list) -> str:
    """Summarize recent chat history for /tldr."""
    if not client: return "AI unconfigured."
    
    prompt = f"Provide a concise summary (TL;DR) of the following chat messages in bullet points:\n{messages_list}"
    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def translate_text(text: str) -> str:
    """Translate text to English if in a foreign language."""
    if not client: return text
    
    prompt = f"If the following text is not in English, translate it to English. If it is in English, just return it exactly as is. Output ONLY the translation/text.\n\n{text}"
    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return completion.choices[0].message.content
    except Exception:
        return text

def generate_daily_quest() -> str:
    """Generate a daily engagement topic/quest."""
    if not client: return "Discuss your favorite tech tool!"
    
    prompt = "Generate a fun, engaging, and professional 'Daily Quest' or topic of discussion for a tech Telegram group. Keep it under 2 sentences."
    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception:
        return "Discuss your favorite tech tool!"