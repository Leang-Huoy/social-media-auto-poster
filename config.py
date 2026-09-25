import os
import sys
from dotenv import load_dotenv

# កំណត់ UTF-8 Encoding សម្រាប់ Windows Console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# កំណត់ទីតាំង Base Directory (គាំទ្រទាំង Python Script និង File .exe)
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env_file_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file_path):
    load_dotenv(dotenv_path=env_file_path)
else:
    load_dotenv()

class Config:
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "").strip()
    TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID", "").strip()

    # Facebook
    FB_PAGE_ID = os.getenv("FB_PAGE_ID", "").strip()
    FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN", "").strip()

    # TikTok
    TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "").strip()

    @classmethod
    def has_telegram(cls) -> bool:
        return bool(cls.TELEGRAM_BOT_TOKEN and (cls.TELEGRAM_CHANNEL_ID or cls.TELEGRAM_GROUP_ID))

    @classmethod
    def has_facebook(cls) -> bool:
        return bool(cls.FB_PAGE_ID and cls.FB_PAGE_ACCESS_TOKEN)

    @classmethod
    def has_tiktok(cls) -> bool:
        return bool(cls.TIKTOK_ACCESS_TOKEN)
