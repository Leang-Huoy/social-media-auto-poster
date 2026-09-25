import os
import sys
import json
import requests
from config import Config, BASE_DIR

# កំណត់ UTF-8 Encoding សម្រាប់ Windows Console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

class SocialMediaAutoPoster:
    def __init__(self):
        # Default credentials from config/.env
        self.tg_bot_token = Config.TELEGRAM_BOT_TOKEN
        self.tg_channel_id = Config.TELEGRAM_CHANNEL_ID
        self.tg_group_id = Config.TELEGRAM_GROUP_ID

        self.fb_page_id = Config.FB_PAGE_ID
        self.fb_access_token = Config.FB_PAGE_ACCESS_TOKEN

        self.tiktok_access_token = Config.TIKTOK_ACCESS_TOKEN

    # =========================================================================
    # TELEGRAM METHODS
    # =========================================================================
    def post_to_telegram(self, message: str, chat_id: str = None, bot_token: str = None) -> bool:
        """ផ្ញើសារអត្ថបទ (Text) ទៅកាន់ Telegram"""
        token = bot_token or self.tg_bot_token
        target_chat = chat_id or self.tg_channel_id
        if not token or not target_chat:
            print("⚠️ Telegram: ខ្វះ Bot Token ឬ Chat ID")
            return False

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": target_chat,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            res = requests.post(url, json=payload, timeout=15)
            data = res.json()
            if res.status_code == 200 and data.get("ok"):
                print(f"✅ Telegram [{target_chat}]: ផ្ញើសារជោគជ័យ!")
                return True
            else:
                desc = data.get("description", res.text)
                print(f"❌ Telegram [{target_chat}] បរាជ័យ: {desc}")
                return False
        except Exception as e:
            print(f"❌ Telegram Error: {e}")
            return False

    def post_photo_to_telegram(self, photo_path_or_url: str, caption: str = "", chat_id: str = None, bot_token: str = None) -> bool:
        """ផុសរូបភាព (Photo) ទៅកាន់ Telegram"""
        token = bot_token or self.tg_bot_token
        target_chat = chat_id or self.tg_channel_id
        if not token or not target_chat:
            print("⚠️ Telegram: ខ្វះ Bot Token ឬ Chat ID")
            return False

        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        try:
            if photo_path_or_url.startswith("http://") or photo_path_or_url.startswith("https://"):
                payload = {
                    "chat_id": target_chat,
                    "photo": photo_path_or_url,
                    "caption": caption,
                    "parse_mode": "HTML"
                }
                res = requests.post(url, json=payload, timeout=20)
            else:
                if not os.path.exists(photo_path_or_url):
                    print(f"❌ រកមិនឃើញ File រូបភាព: {photo_path_or_url}")
                    return False
                with open(photo_path_or_url, "rb") as photo_file:
                    data = {"chat_id": target_chat, "caption": caption, "parse_mode": "HTML"}
                    files = {"photo": photo_file}
                    res = requests.post(url, data=data, files=files, timeout=30)

            data = res.json()
            if res.status_code == 200 and data.get("ok"):
                print(f"✅ Telegram Photo [{target_chat}]: ផុសរូបភាពជោគជ័យ!")
                return True
            else:
                desc = data.get("description", res.text)
                print(f"❌ Telegram Photo [{target_chat}] បរាជ័យ: {desc}")
                return False
        except Exception as e:
            print(f"❌ Telegram Photo Error: {e}")
            return False

    def post_video_to_telegram(self, video_path_or_url: str, caption: str = "", chat_id: str = None, bot_token: str = None) -> bool:
        """ផុសវីដេអូ (Video) ទៅកាន់ Telegram"""
        token = bot_token or self.tg_bot_token
        target_chat = chat_id or self.tg_channel_id
        if not token or not target_chat:
            print("⚠️ Telegram: ខ្វះ Bot Token ឬ Chat ID")
            return False

        url = f"https://api.telegram.org/bot{token}/sendVideo"
        try:
            if video_path_or_url.startswith("http://") or video_path_or_url.startswith("https://"):
                payload = {
                    "chat_id": target_chat,
                    "video": video_path_or_url,
                    "caption": caption,
                    "parse_mode": "HTML"
                }
                res = requests.post(url, json=payload, timeout=30)
            else:
                if not os.path.exists(video_path_or_url):
                    print(f"❌ រកមិនឃើញ File វីដេអូ: {video_path_or_url}")
                    return False
                with open(video_path_or_url, "rb") as video_file:
                    data = {"chat_id": target_chat, "caption": caption, "parse_mode": "HTML"}
                    files = {"video": video_file}
                    res = requests.post(url, data=data, files=files, timeout=60)

            data = res.json()
            if res.status_code == 200 and data.get("ok"):
                print(f"✅ Telegram Video [{target_chat}]: ផុសវីដេអូជោគជ័យ!")
                return True
            else:
                desc = data.get("description", res.text)
                print(f"❌ Telegram Video [{target_chat}] បរាជ័យ: {desc}")
                return False
        except Exception as e:
            print(f"❌ Telegram Video Error: {e}")
            return False

    # =========================================================================
    # FACEBOOK PAGE METHODS
    # =========================================================================
    def post_to_facebook_page(self, message: str, page_id: str = None, access_token: str = None) -> bool:
        """Post សារអត្ថបទទៅកាន់ Facebook Page"""
        pid = page_id or self.fb_page_id
        token = access_token or self.fb_access_token
        if not pid or not token:
            print("⚠️ Facebook: ខ្វះ Page ID ឬ Access Token")
            return False

        url = f"https://graph.facebook.com/v19.0/{pid}/feed"
        payload = {"message": message, "access_token": token}
        try:
            res = requests.post(url, data=payload, timeout=20)
            data = res.json()
            if res.status_code == 200 and "id" in data:
                print(f"✅ Facebook Page [{pid}]: ផុសសារជោគជ័យ! (Post ID: {data['id']})")
                return True
            else:
                error_msg = data.get("error", {}).get("message", res.text)
                print(f"❌ Facebook Page [{pid}] បរាជ័យ: {error_msg}")
                return False
        except Exception as e:
            print(f"❌ Facebook Error: {e}")
            return False

    def post_photo_to_facebook_page(self, photo_path_or_url: str, caption: str = "", page_id: str = None, access_token: str = None) -> bool:
        """ផុសរូបភាពទៅកាន់ Facebook Page"""
        pid = page_id or self.fb_page_id
        token = access_token or self.fb_access_token
        if not pid or not token:
            print("⚠️ Facebook: ខ្វះ Page ID ឬ Access Token")
            return False

        url = f"https://graph.facebook.com/v19.0/{pid}/photos"
        try:
            if photo_path_or_url.startswith("http://") or photo_path_or_url.startswith("https://"):
                payload = {"url": photo_path_or_url, "caption": caption, "access_token": token}
                res = requests.post(url, data=payload, timeout=30)
            else:
                if not os.path.exists(photo_path_or_url):
                    print(f"❌ រកមិនឃើញ File រូបភាព: {photo_path_or_url}")
                    return False
                with open(photo_path_or_url, "rb") as f:
                    data = {"caption": caption, "access_token": token}
                    files = {"source": f}
                    res = requests.post(url, data=data, files=files, timeout=45)

            data = res.json()
            if res.status_code == 200 and ("id" in data or "post_id" in data):
                print(f"✅ Facebook Page Photo [{pid}]: ផុសរូបភាពជោគជ័យ!")
                return True
            else:
                error_msg = data.get("error", {}).get("message", res.text)
                print(f"❌ Facebook Photo [{pid}] បរាជ័យ: {error_msg}")
                return False
        except Exception as e:
            print(f"❌ Facebook Photo Error: {e}")
            return False

    def post_video_to_facebook_page(self, video_path_or_url: str, caption: str = "", title: str = "", page_id: str = None, access_token: str = None) -> bool:
        """ផុសវីដេអូទៅកាន់ Facebook Page"""
        pid = page_id or self.fb_page_id
        token = access_token or self.fb_access_token
        if not pid or not token:
            print("⚠️ Facebook: ខ្វះ Page ID ឬ Access Token")
            return False

        url = f"https://graph.facebook.com/v19.0/{pid}/videos"
        try:
            if video_path_or_url.startswith("http://") or video_path_or_url.startswith("https://"):
                payload = {
                    "file_url": video_path_or_url,
                    "description": caption,
                    "title": title or caption[:50],
                    "access_token": token
                }
                res = requests.post(url, data=payload, timeout=40)
            else:
                if not os.path.exists(video_path_or_url):
                    print(f"❌ រកមិនឃើញ File វីដេអូ: {video_path_or_url}")
                    return False
                with open(video_path_or_url, "rb") as f:
                    data = {
                        "description": caption,
                        "title": title or caption[:50],
                        "access_token": token
                    }
                    files = {"source": f}
                    res = requests.post(url, data=data, files=files, timeout=90)

            data = res.json()
            if res.status_code == 200 and "id" in data:
                print(f"✅ Facebook Video [{pid}]: ផុសវីដេអូជោគជ័យ!")
                return True
            else:
                error_msg = data.get("error", {}).get("message", res.text)
                print(f"❌ Facebook Video [{pid}] បរាជ័យ: {error_msg}")
                return False
        except Exception as e:
            print(f"❌ Facebook Video Error: {e}")
            return False

    # =========================================================================
    # YOUTUBE DATA API v3 METHODS
    # =========================================================================
    def get_youtube_access_token(self, client_id: str, client_secret: str, refresh_token: str) -> str:
        """ទាញយក Access Token ថ្មីពី Google OAuth2 ដោយប្រើ Refresh Token"""
        if not client_id or not client_secret or not refresh_token:
            return ""
        url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        try:
            res = requests.post(url, data=payload, timeout=15)
            data = res.json()
            return data.get("access_token", "")
        except Exception as e:
            print(f"❌ YouTube OAuth2 Token Refresh Error: {e}")
            return ""

    def post_to_youtube(self, video_path: str, title: str, description: str = "", tags: list = None, privacy: str = "public", access_token: str = None, client_id: str = None, client_secret: str = None, refresh_token: str = None) -> bool:
        """
        Upload វីដេអូទៅកាន់ YouTube Channel តាមរយៈ YouTube Data API v3 Resumable Upload
        """
        token = access_token
        if not token and refresh_token:
            token = self.get_youtube_access_token(client_id, client_secret, refresh_token)

        if not token:
            print("⚠️ YouTube: ខ្វះ OAuth2 Access Token ឬ Refresh Token")
            return False

        if not os.path.exists(video_path):
            print(f"❌ រកមិនឃើញ File វីដេអូសម្រាប់ YouTube: {video_path}")
            return False

        # Metadata
        metadata = {
            "snippet": {
                "title": title or "New Video Upload",
                "description": description or "",
                "tags": tags or ["auto-poster"],
                "categoryId": "22"  # People & Blogs
            },
            "status": {
                "privacyStatus": privacy or "public",
                "selfDeclaredMadeForKids": False
            }
        }

        # Step 1: Initiate Resumable Upload Session
        init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/*",
            "X-Upload-Content-Length": str(os.path.getsize(video_path))
        }

        try:
            init_res = requests.post(init_url, json=metadata, headers=headers, timeout=25)
            if init_res.status_code != 200:
                print(f"❌ YouTube Session Error: {init_res.text}")
                return False

            upload_url = init_res.headers.get("Location")
            if not upload_url:
                print("❌ YouTube Error: មិនទទួលបាន Upload Session Location URL")
                return False

            # Step 2: Upload Video File Content
            with open(video_path, "rb") as f:
                upload_res = requests.put(
                    upload_url,
                    data=f,
                    headers={"Content-Type": "video/*"},
                    timeout=300
                )

            if upload_res.status_code in [200, 201]:
                res_data = upload_res.json()
                vid_id = res_data.get("id", "")
                print(f"✅ YouTube: Upload វីដេអូជោគជ័យ! (Video URL: https://youtu.be/{vid_id})")
                return True
            else:
                print(f"❌ YouTube Upload Failed: {upload_res.text}")
                return False
        except Exception as e:
            print(f"❌ YouTube Exception: {e}")
            return False

    # =========================================================================
    # TIKTOK METHODS
    # =========================================================================
    def post_to_tiktok(self, video_url: str, caption: str, access_token: str = None) -> bool:
        """TikTok Content Posting API (PULL_FROM_URL)"""
        token = access_token or self.tiktok_access_token
        if not token:
            print("⚠️ TikTok: ខ្វះ Access Token")
            return False

        url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        payload = {
            "post_info": {
                "title": caption,
                "privacy_level": "PUBLIC_TO_EVERYONE"
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "video_url": video_url
            }
        }
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=25)
            data = res.json()
            if res.status_code == 200 and data.get("error", {}).get("code") == "ok":
                publish_id = data.get("data", {}).get("publish_id", "N/A")
                print(f"✅ TikTok: បានបញ្ជូនវីដេអូទៅ Publish! (Publish ID: {publish_id})")
                return True
            else:
                err = data.get("error", {})
                print(f"❌ TikTok បរាជ័យ: [{err.get('code')}] {err.get('message', res.text)}")
                return False
        except Exception as e:
            print(f"❌ TikTok Error: {e}")
            return False

    # =========================================================================
    # MULTI-ACCOUNT DYNAMIC POSTER (គាំទ្រការ Post អត្ថបទ រូបភាព និងវីដេអូព្រមគ្នា)
    # =========================================================================
    def post_to_account(self, account: dict, message: str = "", photo_path_or_url: str = "", video_path_or_url: str = "", tiktok_public_url: str = "") -> dict:
        """
        ធ្វើការ Post ទៅកាន់គណនីជាក់លាក់មួយ ដោយគាំទ្រ format ទាំង អត្ថបទ រូបភាព និងវីដេអូ ព្រមគ្នា
        """
        platform = account.get("platform", "").lower()
        acc_name = account.get("name", "Account")
        has_photo = bool(photo_path_or_url)
        has_video = bool(video_path_or_url)

        res_details = {"platform": platform, "account_name": acc_name, "success": False, "posted_items": []}

        try:
            # 1. TELEGRAM (Channel or Group)
            if platform == "telegram":
                token = account.get("bot_token") or self.tg_bot_token
                chat_id = account.get("chat_id")

                success_any = False
                # ប្រសិនបើមានរូបភាព
                if has_photo:
                    ok_p = self.post_photo_to_telegram(photo_path_or_url, caption=message, chat_id=chat_id, bot_token=token)
                    if ok_p:
                        res_details["posted_items"].append("photo")
                        success_any = True

                # ប្រសិនបើមានវីដេអូ
                if has_video:
                    ok_v = self.post_video_to_telegram(video_path_or_url, caption=(message if not has_photo else ""), chat_id=chat_id, bot_token=token)
                    if ok_v:
                        res_details["posted_items"].append("video")
                        success_any = True

                # ប្រសិនបើមានតែអត្ថបទសុទ្ធ (គ្មាន photo និង video)
                if not has_photo and not has_video and message:
                    ok_t = self.post_to_telegram(message, chat_id=chat_id, bot_token=token)
                    if ok_t:
                        res_details["posted_items"].append("text")
                        success_any = True

                res_details["success"] = success_any
                return res_details

            # 2. FACEBOOK PAGE
            elif platform == "facebook":
                pid = account.get("page_id") or self.fb_page_id
                token = account.get("access_token") or self.fb_access_token

                success_any = False
                if has_video:
                    ok_v = self.post_video_to_facebook_page(video_path_or_url, caption=message, page_id=pid, access_token=token)
                    if ok_v:
                        res_details["posted_items"].append("video")
                        success_any = True

                if has_photo:
                    ok_p = self.post_photo_to_facebook_page(photo_path_or_url, caption=message, page_id=pid, access_token=token)
                    if ok_p:
                        res_details["posted_items"].append("photo")
                        success_any = True

                if not has_photo and not has_video and message:
                    ok_t = self.post_to_facebook_page(message, page_id=pid, access_token=token)
                    if ok_t:
                        res_details["posted_items"].append("text")
                        success_any = True

                res_details["success"] = success_any
                return res_details

            # 3. YOUTUBE
            elif platform == "youtube":
                if not has_video:
                    res_details["error"] = "YouTube តម្រូវឱ្យមាន File វីដេអូ"
                    return res_details

                cid = account.get("client_id")
                csecret = account.get("client_secret")
                rtoken = account.get("refresh_token")
                atoken = account.get("access_token")

                title_line = message.split("\n")[0] if message else "New Video"
                ok = self.post_to_youtube(
                    video_path=video_path_or_url,
                    title=title_line[:100],
                    description=message,
                    access_token=atoken,
                    client_id=cid,
                    client_secret=csecret,
                    refresh_token=rtoken
                )
                res_details["success"] = ok
                if ok:
                    res_details["posted_items"].append("youtube_video")
                return res_details

            # 4. TIKTOK
            elif platform == "tiktok":
                token = account.get("access_token") or self.tiktok_access_token
                tk_url = tiktok_public_url or (video_path_or_url if video_path_or_url.startswith("http") else "")
                if not tk_url:
                    res_details["error"] = "TikTok តម្រូវឱ្យមាន Public Video URL"
                    return res_details
                ok = self.post_to_tiktok(tk_url, message, access_token=token)
                res_details["success"] = ok
                if ok:
                    res_details["posted_items"].append("tiktok_video")
                return res_details

            else:
                res_details["error"] = f"Platform មិនស្គាល់: {platform}"
                return res_details

        except Exception as e:
            res_details["error"] = str(e)
            return res_details

    # =========================================================================
    # TEST CONNECTION HELPER FOR SINGLE ACCOUNT
    # =========================================================================
    def test_account_connection(self, account: dict) -> dict:
        """តេស្តការតភ្ជាប់សម្រាប់គណនីនីមួយៗ"""
        p = account.get("platform", "").lower()
        if p == "telegram":
            token = account.get("bot_token") or self.tg_bot_token
            if not token:
                return {"connected": False, "error": "គ្មាន Bot Token"}
            try:
                r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=8)
                d = r.json()
                if r.status_code == 200 and d.get("ok"):
                    return {"connected": True, "name": d.get("result", {}).get("first_name", "Bot"), "username": d.get("result", {}).get("username", "")}
                return {"connected": False, "error": d.get("description", r.text)}
            except Exception as e:
                return {"connected": False, "error": str(e)}

        elif p == "facebook":
            pid = account.get("page_id") or self.fb_page_id
            token = account.get("access_token") or self.fb_access_token
            if not pid or not token:
                return {"connected": False, "error": "គ្មាន Page ID ឬ Token"}
            try:
                r = requests.get(f"https://graph.facebook.com/v19.0/{pid}?fields=id,name&access_token={token}", timeout=8)
                d = r.json()
                if r.status_code == 200 and "id" in d:
                    return {"connected": True, "name": d.get("name", "Page")}
                return {"connected": False, "error": d.get("error", {}).get("message", r.text)}
            except Exception as e:
                return {"connected": False, "error": str(e)}

        elif p == "youtube":
            cid = account.get("client_id")
            csec = account.get("client_secret")
            rtok = account.get("refresh_token")
            atok = account.get("access_token")
            if not atok and rtok:
                atok = self.get_youtube_access_token(cid, csec, rtok)
            if not atok:
                return {"connected": False, "error": "គ្មាន Access/Refresh Token"}
            try:
                headers = {"Authorization": f"Bearer {atok}"}
                r = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true", headers=headers, timeout=8)
                d = r.json()
                if r.status_code == 200 and "items" in d and len(d["items"]) > 0:
                    yt_name = d["items"][0].get("snippet", {}).get("title", "YouTube Channel")
                    return {"connected": True, "name": yt_name}
                return {"connected": False, "error": d.get("error", {}).get("message", "Channel not found")}
            except Exception as e:
                return {"connected": False, "error": str(e)}

        elif p == "tiktok":
            token = account.get("access_token") or self.tiktok_access_token
            if not token:
                return {"connected": False, "error": "គ្មាន Token"}
            try:
                headers = {"Authorization": f"Bearer {token}"}
                r = requests.get("https://open.tiktokapis.com/v2/user/info/?fields=open_id,display_name", headers=headers, timeout=8)
                d = r.json()
                if r.status_code == 200 and d.get("error", {}).get("code") == "ok":
                    return {"connected": True, "name": d.get("data", {}).get("user", {}).get("display_name", "User")}
                return {"connected": False, "error": d.get("error", {}).get("message", "Error")}
            except Exception as e:
                return {"connected": False, "error": str(e)}

        return {"connected": False, "error": "Unknown platform"}

    # Backward compatibility helpers
    def broadcast_text(self, message: str):
        if self.tg_bot_token and self.tg_channel_id:
            self.post_to_telegram(message, self.tg_channel_id)
        if self.tg_bot_token and self.tg_group_id:
            self.post_to_telegram(message, self.tg_group_id)
        if self.fb_page_id and self.fb_access_token:
            self.post_to_facebook_page(message)

    def test_all_connections(self):
        print("\n🔍 --- ពិនិត្យការតភ្ជាប់ API (Test Connections) ---")
        if self.tg_bot_token:
            try:
                res = requests.get(f"https://api.telegram.org/bot{self.tg_bot_token}/getMe", timeout=10)
                data = res.json()
                if res.status_code == 200 and data.get("ok"):
                    bot_name = data.get("result", {}).get("first_name", "Bot")
                    bot_user = data.get("result", {}).get("username", "")
                    print(f"✅ Telegram: ភ្ជាប់ជោគជ័យ! (Bot: {bot_name} - @{bot_user})")
                else:
                    print(f"❌ Telegram Token មិនត្រឹមត្រូវ: {data.get('description')}")
            except Exception as e:
                print(f"❌ Telegram Connection Error: {e}")
        else:
            print("⚪ Telegram: មិនទាន់បានកំណត់ TELEGRAM_BOT_TOKEN")

        if self.fb_page_id and self.fb_access_token:
            try:
                res = requests.get(
                    f"https://graph.facebook.com/v19.0/{self.fb_page_id}?fields=id,name&access_token={self.fb_access_token}",
                    timeout=10
                )
                data = res.json()
                if res.status_code == 200 and "id" in data:
                    print(f"✅ Facebook Page: ភ្ជាប់ជោគជ័យ! (Page: {data.get('name')} | ID: {data.get('id')})")
                else:
                    err = data.get("error", {}).get("message", res.text)
                    print(f"❌ Facebook Token/Page ID មិនត្រឹមត្រូវ: {err}")
            except Exception as e:
                print(f"❌ Facebook Connection Error: {e}")
        else:
            print("⚪ Facebook: មិនទាន់បានកំណត់ FB_PAGE_ID ឬ FB_PAGE_ACCESS_TOKEN")

        if self.tiktok_access_token:
            try:
                headers = {"Authorization": f"Bearer {self.tiktok_access_token}"}
                res = requests.get("https://open.tiktokapis.com/v2/user/info/?fields=open_id,display_name", headers=headers, timeout=10)
                data = res.json()
                if res.status_code == 200 and data.get("error", {}).get("code") == "ok":
                    user_info = data.get("data", {}).get("user", {})
                    print(f"✅ TikTok: ភ្ជាប់ជោគជ័យ! (User: {user_info.get('display_name', 'OK')})")
                else:
                    err = data.get("error", {})
                    print(f"❌ TikTok Token មិនត្រឹមត្រូវ: [{err.get('code')}] {err.get('message')}")
            except Exception as e:
                print(f"❌ TikTok Connection Error: {e}")
        else:
            print("⚪ TikTok: មិនទាន់បានកំណត់ TIKTOK_ACCESS_TOKEN")
        print("--------------------------------------------------\n")
