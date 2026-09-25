# 🤖 Social Media Auto Poster Tool (Python)

កម្មវិធីស្វ័យប្រវត្តិកម្មសម្រាប់ Post មាតិកា (អត្ថបទ រូបភាព និងវីដេអូ) ទៅកាន់បណ្ដាញសង្គមច្រើនក្នុងពេលតែមួយរួមមាន **Telegram (Channel & Group)**, **Facebook Page**, និង **TikTok**។

---

## 🌟 លក្ខណៈពិសេសចម្បងៗ (Key Features)

1. **ប្រព័ន្ធគ្រប់គ្រងសិទ្ធិ និងគណនីចូលប្រើប្រាស់ (RBAC Authentication)**:
   - 👑 **Admin Account**: មានសិទ្ធិពេញលេញលើប្រព័ន្ធ អាចបន្ថែម/កែប្រែ/លុបបណ្ដាញសង្គម, កំណត់ API Keys, និងបង្កើតគណនីបុគ្គលិកថ្មីបាន។
   - 👤 **User Account**: ប្រើប្រាស់បានត្រឹមតែមុខងារ Post តាមបណ្ដាញសង្គមដែល Admin បានកំណត់ជូន (មិនអាចបន្ថែម ឬឃើញ API Keys សម្ងាត់ឡើយ)។
   - 🔐 គណនីដំបូងដែលបានរៀបចំជូនស្រាប់៖
     - **Admin**: Username: `admin` | Password: `admin123`
     - **User (បុគ្គលិក)**: Username: `user` | Password: `user123`
2. **គាំទ្រការ Post គ្រប់ Format ព្រមគ្នា (All-in-One Post)**:
   - អាច Post **អត្ថបទ (Text) + រូបភាព (Photo) + វីដេអូ (Video)** ក្នុងពេលតែមួយបាន!
3. **គាំទ្រពហុបណ្ដាញសង្គម (Multi-Platform)**:
   - ✈️ **Telegram** (Channel & Group)
   - 🌐 **Facebook** (Page Posts)
   - ▶️ **YouTube** (Upload Videos & Shorts តាម YouTube Data API v3)
   - 🎵 **TikTok** (Content Posting API)
4. **អាចបន្ថែមគណនីមិនកំណត់តាមប្រភេទនីមួយៗ (Multi-Account Management)**:
   - អាចបន្ថែម Telegram Channel ច្រើន, Facebook Page ច្រើន, YouTube Channel ច្រើន
   - មានប៊ូតុង **"ជ្រើសរើសទាំងអស់ (Select All)"** សម្រាប់ Post ទៅកាន់គ្រប់គណនីក្នុង ១ Click!
   - គ្រប់គ្រងតាមរយៈឯកសារ [`accounts.json`](file:///c:/Users/Asus/Desktop/Aoto%20Posts/accounts.json) ឬពីលើផ្ទាំង UI ផ្ទាល់


```text
Aoto Posts/
├── .env                  # កន្លែងដាក់ API Keys / Tokens ផ្ទាល់ខ្លួន
├── .env.example          # គំរូទម្រង់ .env
├── requirements.txt      # បណ្ណាល័យចាំបាច់ (requests, python-dotenv, schedule)
├── config.py             # Configuration loader
├── poster.py             # Core Class សម្រាប់ធ្វើការ Post ទៅកាន់ Platforms
├── scheduler.py          # ប្រព័ន្ធ Post តាមកាលវិភាគ និង Queue
├── posts_queue.json      # តារាងរង់ចាំ Post (JSON Queue)
├── example_run.py        # កូដគំរូសម្រាប់រត់តាម Script ផ្ទាល់
├── main.py               # Menu អន្តរកម្ម (Interactive Terminal Menu)
└── README.md             # សេចក្ដីណែនាំ
```

---

## 🚀 ការដំឡើង និងចាប់ផ្ដើម (Quick Start)

### ១. ដំឡើង Dependencies
បើក Terminal (Command Prompt ឬ PowerShell) រួចដំណើរការ៖
```bash
pip install -r requirements.txt
```

### ២. កំណត់ API Keys ក្នុង file `.env`
បើក file `.env` រួចបំពេញព័ត៌មានសម្ងាត់របស់អ្នក៖
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
TELEGRAM_CHANNEL_ID=@mychannel_or_id
TELEGRAM_GROUP_ID=-1001234567890

FB_PAGE_ID=123456789012345
FB_PAGE_ACCESS_TOKEN=EAAB...

TIKTOK_ACCESS_TOKEN=act.example...
```

---

## 🔑 របៀបយក API Keys នីមួយៗ

### ១. Telegram Bot Token & Chat ID
1. **យក Bot Token**៖
   - ចូលទៅកាន់ Telegram ស្វែងរក `@BotFather`
   - ផ្ញើពាក្យបញ្ជា `/newbot` រួចដាក់ឈ្មោះ និង Username ឱ្យ Bot
   - អ្នកនឹងទទួលបាន **Bot Token** (ឧ. `7123456789:AAH...`)
2. **យក Channel / Group ID**៖
   - បន្ថែម Bot របស់អ្នកចូលទៅក្នុង Channel ឬ Group នោះ ហើយផ្ដល់សិទ្ធិជា **Administrator**
   - ផ្ញើសារសាកល្បងមួយនៅក្នុង Channel ឬ Group នោះ
   - បើក Browser ចូលតំណភ្ជាប់៖ `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
   - ស្វែងរកពាក្យ `"chat":{"id": -100xxxxxxxxxx}` នោះហើយជា Chat ID

---

### ២. Facebook Page ID & Access Token
1. **យក Page ID**៖
   - ចូលទៅកាន់ Facebook Page របស់អ្នក -> ចូល **About** -> រំកិលចុះក្រោមនឹងឃើញ **Page ID**
2. **យក Page Access Token (មិនចេះហួសកំណត់ - Never Expiring Token)**៖
   - ចូលទៅកាន់ [Meta for Developers](https://developers.facebook.com/)
   - បង្កើត App ប្រភេទ **Business**
   - ចូលទៅកាន់ **Tools** -> **Graph API Explorer**
   - ជ្រើសរើស App និង User Token រួចជ្រើសរើស Permissions៖
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `pages_show_list`
   - ចុច **Generate Access Token**
   - នៅត្រង់ប្រអប់ **User or Page** សូមជ្រើសរើស Facebook Page របស់អ្នក ដើម្បីទទួលបាន **Page Access Token**

---

### ៣. TikTok Developer Access Token
1. ចុះឈ្មោះគណនី Developer នៅលើ [TikTok for Developers](https://developers.tiktok.com/)
2. បង្កើត App និងស្នើសុំប្រើប្រាស់ **Content Posting API**
3. កំណត់ Scope: `video.publish`, `video.upload`
4. យក Access Token មកដាក់ក្នុង `.env`

---

## 💻 របៀបប្រើប្រាស់ (How to Use)

### 🌟 ជម្រើសទី ១ (ណែនាំខ្លាំងបំផុត)៖ ដំណើរការផ្ទាំងកម្មវិធី UI ដ៏ទំនើប (Desktop GUI)
អ្នកអាចបើកផ្ទាំងកម្មវិធី Graphic Interface (UI) ដ៏ស្រស់ស្អាត (Dark Glassmorphism + Live Preview) ដោយគ្រាន់តែ៖
* ចុចពីរដង (Double-click) លើ file៖
  ```text
  AutoPosterUI.exe
  ```
  *(ឬចុចលើ file `run_ui.bat` ឬដំណើរការ `python app.py`)*

**លក្ខណៈពិសេសនៃផ្ទាំង UI:**
- 🎨 **ការរចនាបែប Glassmorphism & Dark Mode ទំនើប** គាំទ្រពុម្ពអក្សរខ្មែរស្អាត
- 🟢 **Live Status Badges**: បង្ហាញភ្លាមៗថា Telegram, Facebook, TikTok ភ្ជាប់ជោគជ័យឬនៅ
- 📱 **Live Mobile Mockup Preview**: ឃើញទិដ្ឋភាព Post ជាក់ស្ដែងនៅពេលកំពុងវាយអត្ថបទ
- 🖼️ **Media Drag & Drop**: ទម្លាក់រូបភាព ឬវីដេអូដើម្បី Preview ផ្ទាល់
- ⏰ **Queue Manager**: គ្រប់គ្រងតារាងរង់ចាំ និងកំណត់កាលវិភាគ
- ⚙️ **In-App Settings**: កែសម្រួល API Keys ក្នុង file `.env` ពីលើផ្ទាំង UI ដោយផ្ទាល់

---

### ជម្រើសទី ២៖ ដំណើរការ Menu លើ Terminal តាម `.exe` (CLI)
ចុចពីរដងលើ file៖
```text
AutoPoster.exe
```

---

### ជម្រើសទី ៣៖ ដំណើរការតាមរយៈ Python Terminal
```bash
python main.py
```
អ្នកនឹងឃើញផ្ទាំង Menu៖
- `[1]` 📝 ផ្ញើសារអត្ថបទភ្លាមៗ (Telegram + Facebook)
- `[2]` 🖼️ ផុសរូបភាព + Caption (អាចដាក់ File ក្នុងម៉ាស៊ីន ឬ Link URL)
- `[3]` 🎬 ផុសវីដេអូ + Caption (Telegram, Facebook, និង TikTok)
- `[4]` 🔍 ពិនិត្យការតភ្ជាប់ API (Test API Connections)
- `[5]` ⏰ ដំណើរការ Auto Post តាមកាលវិភាគ (Scheduler)
- `[0]` ❌ ចាកចេញ

---

### ជម្រើសទី ២៖ ដំណើរការតាម Python Script ផ្ទាល់
អ្នកអាចដំណើរការ `example_run.py`៖
```bash
python example_run.py
```
ឬសរសេរកូដផ្ទាល់ខ្លួនដូចខាងក្រោម៖
```python
from poster import SocialMediaAutoPoster

poster = SocialMediaAutoPoster()

# ផុសសារទៅកាន់គ្រប់ Platform
poster.broadcast_text("ជំរាបសួរពី Python Auto Poster! 🚀")

# ផុសរូបភាពទៅ Telegram និង Facebook
poster.broadcast_photo("C:/images/banner.jpg", caption="រូបភាពប្រូម៉ូសិនថ្មី")

# ផុសវីដេអូទៅ Telegram, Facebook, និង TikTok
poster.broadcast_video(
    video_path_or_url="https://example.com/promo.mp4",
    caption="វីដេអូថ្មីប្រចាំថ្ងៃ!",
    tiktok_public_url="https://example.com/promo.mp4"
)
```

---

### ជម្រើសទី ៣៖ Auto Post តាមកាលវិភាគ (Scheduler & Queue)
អ្នកអាចដាក់បញ្ជី Post ទុកមុនក្នុង file `posts_queue.json` រួចដំណើរការ៖
```bash
python scheduler.py
```
កម្មវិធីនឹងទាញយកមាតិកាដែលស្ថិតក្នុងស្ថានភាព `"pending"` មក Post ជារៀងរាល់ N នាទីម្ដងដោយស្វ័យប្រវត្តិ។

---

## 🌐 របៀប Hosting និងដំឡើងទៅជា App លើទូរស័ព្ទ (Mobile PWA & Online Hosting)

### ១. Hosting អនឡាញភ្លាមៗ (Instant Public HTTPS via Cloudflare)
អ្នកអាចបើកឱ្យទូរស័ព្ទដៃប្រើអ៊ីនធឺណិត 4G/5G/Wi-Fi ពីទីណា ឬខេត្តណាក៏អាចចូលប្រើប្រព័ន្ធ Post នេះបានដែរ ដោយមិនចាំបាច់មាន Domain ឬបង់ប្រាក់ឡើយ៖
- **វិធីទី ១ (1-Click Batch)**៖ ចុចពីរដងលើឯកសារ `start_online_tunnel.bat`
- **វិធីទី ២ (លើផ្ទាំង UI ផ្ទាល់)**៖ 
  1. បើក `AutoPosterUI.exe`
  2. ចុចលើប៊ូតុង **"📱 ប្រើលើទូរស័ព្ទ / Hosting"** នៅខាងលើផ្នែកស្ដាំ
  3. ចុចប៊ូតុង **"⚡ បង្កើត Public HTTPS Link ថ្មី"**
  4. អ្នកនឹងទទួលបានតំណភ្ជាប់ `https://xxxx.trycloudflare.com` និង **QR Code** សម្រាប់ Scan ភ្លាមៗ!

---

### ២. របៀបដំឡើងទៅជា App (Install as App) លើទូរស័ព្ទ និងកុំព្យូទ័រ
កម្មវិធីនេះត្រូវបានបំពាក់បច្ចេកវិទ្យា **Progressive Web App (PWA)** អាចដំឡើងជា App ផ្លូវការដែលមាន Icon លើអេក្រង់ទូរស័ព្ទ៖

* **លើទូរស័ព្ទ Android (Chrome / Brave / Edge)**៖
  1. បើកតំណភ្ជាប់ HTTPS លើ Browser
  2. ចុចលើប៊ូតុង **"📲 ដំឡើង App"** ពណ៌បៃតងរលោងនៅផ្នែកខាងលើ
  3. ឬចុចសញ្ញាចុចបី `⋮` ជ្រើសរើស **"Install app"** ឬ **"ដំឡើងកម្មវិធី"** -> ចុច **Install**
  4. App នឹងបង្ហាញនៅលើអេក្រង់ទូរស័ព្ទរបស់អ្នកដូចជា App ធម្មតា!

* **លើទូរស័ព្ទ iPhone / iPad (Safari)**៖
  1. បើកតំណភ្ជាប់ HTTPS ក្នុង Safari
  2. ចុចប៊ូតុង **Share (សញ្ញាព្រួញចង្អុលឡើងលើ 📤)** នៅរបារខាងក្រោម
  3. រំកិលចុះក្រោម រួចជ្រើសរើស **"Add to Home Screen" (បន្ថែមទៅអេក្រង់ដើម)**
  4. ចុច **Add** នៅជ្រុងខាងស្ដាំលើ នោះកម្មវិធីនឹងក្លាយជា App មាន Icon លើ Home Screen ភ្លាមៗ!

* **លើកុំព្យូទ័រ PC / Mac (Chrome / Edge)**៖
  - ចុចប៊ូតុង **"📲 ដំឡើង App"** លើ Header ឬចុច Icon Install នៅជ្រុងស្ដាំនៃ Address Bar ដើម្បីដំឡើងជា Desktop App។

---

### ៣. ការ Hosting អនឡាញ ២៤/៧ ដោយមិនបាច់បើកកុំព្យូទ័រ (Free Cloud Hosting)
ប្រសិនបើអ្នកចង់ឱ្យប្រព័ន្ធដំណើរការ ២៤ម៉ោង/២៤ម៉ោង ដោយមិនបាច់បើកកុំព្យូទ័រផ្ទាល់ខ្លួនចោល៖
1. បង្កើតគណនីឥតគិតថ្លៃនៅ [Render.com](https://render.com/) ឬ [Railway.app](https://railway.app/)
2. Upload កូដនេះទៅកាន់ GitHub របស់អ្នក (កុំ Upload `.env` ដែលមាន Key ពិត)
3. ភ្ជាប់ Repository នោះទៅកាន់ Render ដោយជ្រើសរើស **Web Service**
4. ប្រព័ន្ធនឹងដំណើរការដោយស្វ័យប្រវត្តិតាមឯកសារ `render.yaml` និង `Procfile` ដែលបានរៀបចំជូនរួចជាស្រេច!

