import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TG_TOKEN", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

# Admin and Group IDs can be loaded as comma-separated strings
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
GROUP_ID = os.getenv("GROUP_ID", "")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID", "")

# Timings and Limits
INVITE_LINK_EXPIRY = int(os.getenv("INVITE_LINK_EXPIRY", 600))
SPAM_MSG_LIMIT = int(os.getenv("SPAM_MSG_LIMIT", 5))
SPAM_WINDOW_SECONDS = int(os.getenv("SPAM_WINDOW_SECONDS", 10))
STRIKE_LIMIT = int(os.getenv("STRIKE_LIMIT", 3))
MUTE_DURATION_SECONDS = int(os.getenv("MUTE_DURATION_SECONDS", 3600))
LEADERBOARD_POST_TIME = os.getenv("LEADERBOARD_POST_TIME", "20:00")

# Regex for instant deletions
BANNED_WORDS_REGEX = os.getenv("BANNED_WORDS_REGEX", r"(?i)\b(crypto|scam|free money)\b")

DATABASE_URL = os.getenv("DATABASE_URL", "")
