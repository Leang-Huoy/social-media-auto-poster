import sys
from poster import SocialMediaAutoPoster
from scheduler import run_schedule_loop

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def safe_pause():
    try:
        input("\nចុច Enter ដើម្បីបន្ត...")
    except (EOFError, KeyboardInterrupt):
        pass

def print_banner():
    banner = """
=====================================================
    🤖 SOCIAL MEDIA AUTO POSTER TOOL (PYTHON) 🚀    
=====================================================
  គាំទ្រ: Telegram (Channel & Group), Facebook Page, TikTok
-----------------------------------------------------
"""
    print(banner)

def main_menu():
    poster = SocialMediaAutoPoster()

    while True:
        print_banner()
        print("សូមជ្រើសរើសជម្រើសខាងក្រោម៖")
        print("  [1] 📝 ផ្ញើសារអត្ថបទ (Broadcast Text)")
        print("  [2] 🖼️ ផុសរូបភាព + Caption (Broadcast Photo)")
        print("  [3] 🎬 ផុសវីដេអូ + Caption (Broadcast Video)")
        print("  [4] 🔍 ពិនិត្យការតភ្ជាប់ API (Test Connections)")
        print("  [5] ⏰ ដំណើរការ Auto Post តាមកាលវិភាគ (Scheduler)")
        print("  [0] ❌ ចាកចេញ (Exit)")
        print("-----------------------------------------------------")

        try:
            choice = input("👉 ជ្រើសរើសលេខ (0-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 សូមអរគុណ! កម្មវិធីត្រូវបានបិទ។")
            sys.exit(0)

        if choice == "1":
            msg = input("\n✍️ បញ្ចូលសារដែលអ្នកចង់ Post: ").strip()
            if msg:
                poster.broadcast_text(msg)
            else:
                print("⚠️ សារមិនអាចទទេបានទេ!")
            safe_pause()

        elif choice == "2":
            photo_path = input("\n📁 បញ្ចូល File Path ឬ URL នៃរូបភាព: ").strip().strip('"').strip("'")
            caption = input("✍️ បញ្ចូល Caption (ឬទុកទទេក៏បាន): ").strip()
            if photo_path:
                poster.broadcast_photo(photo_path, caption)
            else:
                print("⚠️ សូមបញ្ចូលទីតាំង File ឬ URL នៃរូបភាព!")
            safe_pause()

        elif choice == "3":
            video_path = input("\n📁 បញ្ចូល File Path ឬ URL នៃវីដេអូ: ").strip().strip('"').strip("'")
            caption = input("✍️ បញ្ចូល Caption: ").strip()
            tiktok_url = ""
            if not video_path.startswith("http"):
                tiktok_url = input("🌐 (ជម្រើសបន្ថែម) បញ្ចូល Public Video URL សម្រាប់ TikTok: ").strip()
            poster.broadcast_video(video_path, caption, tiktok_public_url=tiktok_url or None)
            safe_pause()

        elif choice == "4":
            poster.test_all_connections()
            safe_pause()

        elif choice == "5":
            minutes_str = input("\n⏱️ បញ្ចូលចំនួននាទីចន្លោះពេល Post ម្តងៗ (ឧ. 30 ឬ 60, default 30): ").strip()
            interval = int(minutes_str) if minutes_str.isdigit() else 30
            run_schedule_loop(interval_minutes=interval)
            safe_pause()

        elif choice == "0":
            print("\n👋 សូមអរគុណ! កម្មវិធីត្រូវបានបិទ។")
            sys.exit(0)

        else:
            print("⚠️ ជម្រើសមិនត្រឹមត្រូវ សូមជ្រើសរើសម្ដងទៀត!")
            input("\nចុច Enter ដើម្បីបន្ត...")

if __name__ == "__main__":
    main_menu()
