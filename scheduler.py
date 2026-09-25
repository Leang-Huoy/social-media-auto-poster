import os
import sys
import json
import time
import datetime
import schedule
from poster import SocialMediaAutoPoster
from config import BASE_DIR

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

QUEUE_FILE = os.path.join(BASE_DIR, "posts_queue.json")

def init_sample_queue():
    """បង្កើត Queue គំរូប្រសិនបើមិនទាន់មាន"""
    if not os.path.exists(QUEUE_FILE):
        sample_data = [
            {
                "id": 1,
                "type": "text", # 'text', 'photo', 'video'
                "content": "ជំរាបសួរពេលព្រឹក! សូមជូនពរថ្ងៃថ្មីមានតែភាពជោគជ័យ។",
                "media_path": "",
                "tiktok_url": "",
                "status": "pending" # 'pending', 'published', 'failed'
            },
            {
                "id": 2,
                "type": "text",
                "content": "នេះជាសារសាកល្បងទីពីរពី Scheduler ប្រចាំថ្ងៃ។",
                "media_path": "",
                "tiktok_url": "",
                "status": "pending"
            }
        ]
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=4)
        print(f"📄 បានបង្កើតឯកសារគំរូ: {QUEUE_FILE}")

def process_pending_post():
    """ទាញយក Post ដែលស្ថិតក្នុងស្ថានភាព 'pending' មួយមក Publish"""
    if not os.path.exists(QUEUE_FILE):
        init_sample_queue()

    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            posts = json.load(f)
    except Exception as e:
        print(f"❌ មិនអាចអាន file {QUEUE_FILE}: {e}")
        return

    poster = SocialMediaAutoPoster()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for post in posts:
        if post.get("status") == "pending":
            p_id = post.get("id")
            p_type = post.get("type", "text")
            content = post.get("content", "")
            media = post.get("media_path", "")
            tk_url = post.get("tiktok_url", "")

            print(f"\n⏰ [{now_str}] កំពុងដំណើរការ Post #{p_id} (ប្រភេទ: {p_type})...")

            if p_type == "text":
                poster.broadcast_text(content)
            elif p_type == "photo":
                poster.broadcast_photo(media, caption=content)
            elif p_type == "video":
                poster.broadcast_video(media, caption=content, tiktok_public_url=tk_url)

            post["status"] = "published"
            post["published_at"] = now_str
            break
    else:
        print(f"ℹ️ [{now_str}] មិនមាន Post ណាដែលស្ថិតក្នុង status 'pending' ទៀតទេ។")
        return

    # រក្សាទុកស្ថានភាពថ្មី
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

def run_schedule_loop(interval_minutes: int = 60):
    """ដំណើរការ auto-post ជារៀងរាល់ N នាទី"""
    init_sample_queue()
    print(f"\n⏳ Scheduler បានចាប់ផ្ដើម! វានឹងពិនិត្យ និង Post ជារៀងរាល់ {interval_minutes} នាទី។")
    print("ចុច Ctrl + C ដើម្បីបញ្ឈប់។\n")

    # ដំណើរការភ្លាមៗមួយលើកដំបូង
    process_pending_post()

    # កំណត់ Schedule
    schedule.every(interval_minutes).minutes.do(process_pending_post)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Scheduler ត្រូវបានបញ្ឈប់ដោយអ្នកប្រើប្រាស់។")

if __name__ == "__main__":
    run_schedule_loop(interval_minutes=30)
