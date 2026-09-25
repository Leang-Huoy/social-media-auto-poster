"""
ឧទាហរណ៍នៃការប្រើប្រាស់ SocialMediaAutoPoster ក្នុង Script
"""
import sys
from poster import SocialMediaAutoPoster

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

if __name__ == "__main__":
    poster = SocialMediaAutoPoster()

    # 1. ពិនិត្យការតភ្ជាប់ API ទាំងអស់ជាមុន
    poster.test_all_connections()

    # 2. សារសាកល្បង
    test_caption = "ជំរាបសួរ! នេះជាសារតេស្តដោយស្វ័យប្រវត្តិពី Python Auto Poster Tool 🚀"

    # 3. ផ្ញើសារអត្ថបទទៅកាន់ Telegram និង Facebook Page ព្រមគ្នា
    print("--- ចាប់ផ្ដើម Publish សារអត្ថបទ ---")
    poster.broadcast_text(test_caption)

    # 4. ឧទាហរណ៍ផុសរូបភាព (ដោះ Comment # ប្រសិនបើចង់សាកល្បង)
    # image_url = "https://picsum.photos/800/600"
    # poster.broadcast_photo(image_url, caption="រូបភាពសាកល្បងពី Auto Poster")

    # 5. ឧទាហរណ៍ផុសវីដេអូទៅ TikTok និង Facebook/Telegram (ដោះ Comment # ប្រសិនបើចង់សាកល្បង)
    # video_url = "https://example.com/sample_video.mp4"
    # poster.broadcast_video(video_url, caption="វីដេអូសាកល្បងពី Auto Poster", tiktok_public_url=video_url)
