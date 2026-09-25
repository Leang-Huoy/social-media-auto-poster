import os
import sys
import json
import time
import threading
import datetime
import webbrowser
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from dotenv import set_key, load_dotenv
from functools import wraps

from config import BASE_DIR, Config
from poster import SocialMediaAutoPoster
from scheduler import QUEUE_FILE, init_sample_queue
import auth

# កំណត់ UTF-8 Encoding សម្រាប់ Windows Console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

template_folder = os.path.join(BASE_DIR, "templates")
static_folder = os.path.join(BASE_DIR, "static")
uploads_folder = os.path.join(BASE_DIR, "uploads")
os.makedirs(uploads_folder, exist_ok=True)

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.secret_key = "social_poster_pro_secret_key_2026_rbac"
app.config['UPLOAD_FOLDER'] = uploads_folder
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max

LOGS_FILE = os.path.join(BASE_DIR, "activity_logs.json")
ACCOUNTS_FILE = os.path.join(BASE_DIR, "accounts.json")

# Initialize default accounts & default users
auth.init_default_users()

def load_accounts():
    """ទាញយកបញ្ជីគណនីបណ្ដាញសង្គមទាំងអស់"""
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    default_accs = [
        {
            "id": "tg_channel_sum24",
            "platform": "telegram",
            "type": "channel",
            "name": "Sum24 Channel",
            "chat_id": Config.TELEGRAM_CHANNEL_ID or "-1001775565917",
            "bot_token": Config.TELEGRAM_BOT_TOKEN or "8957791647:AAHE6P5dOmlZy7lkrZOwW6glxvFNA5zoJ7o",
            "enabled": True
        }
    ]
    if Config.TELEGRAM_GROUP_ID:
        default_accs.append({
            "id": "tg_group_1",
            "platform": "telegram",
            "type": "group",
            "name": "Telegram Group",
            "chat_id": Config.TELEGRAM_GROUP_ID,
            "bot_token": Config.TELEGRAM_BOT_TOKEN,
            "enabled": True
        })
    save_accounts(default_accs)
    return default_accs

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii=False, indent=4)

def add_log(status: str, platform: str, message: str, details: str = "", username: str = "system"):
    logs = []
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    
    log_entry = {
        "id": int(time.time() * 1000),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "platform": platform,
        "user": username,
        "message": message[:80] + ("..." if len(message) > 80 else ""),
        "details": details
    }
    logs.insert(0, log_entry)
    logs = logs[:100]
    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

# =========================================================================
# AUTH DECORATORS
# =========================================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return jsonify({"success": False, "error": "សូមចូលប្រើប្រាស់គណនី (Login) ជាមុនសិន!"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return jsonify({"success": False, "error": "សូមចូលប្រើប្រាស់គណនី (Login) ជាមុនសិន!"}), 401
        if session["user"].get("role") != "admin":
            return jsonify({"success": False, "error": "សិទ្ធិមិនគ្រប់គ្រាន់! មានតែ Admin ទេដែលអាចប្រើមុខងារនេះបាន"}), 403
        return f(*args, **kwargs)
    return decorated_function

# =========================================================================
# AUTH ENDPOINTS
# =========================================================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manifest.json")
def serve_manifest():
    from flask import send_from_directory
    return send_from_directory(os.path.join(BASE_DIR, "static"), "manifest.json", mimetype="application/manifest+json")

@app.route("/sw.js")
def serve_sw():
    from flask import send_from_directory, make_response
    response = make_response(send_from_directory(os.path.join(BASE_DIR, "static"), "sw.js", mimetype="application/javascript"))
    response.headers['Service-Worker-Allowed'] = '/'
    return response

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    user = auth.verify_user(username, password)
    if user:
        session["user"] = user
        return jsonify({"success": True, "user": user})
    else:
        return jsonify({"success": False, "error": "ឈ្មោះគណនី ឬពាក្យសម្ងាត់មិនត្រឹមត្រូវ!"}), 401

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    name = data.get("name", "").strip()

    if not username or not password:
        return jsonify({"success": False, "error": "សូមបញ្ចូល Username និង Password!"}), 400
    if len(username) < 3:
        return jsonify({"success": False, "error": "Username ត្រូវមានយ៉ាងហោចណាស់ ៣ តួអក្សរ!"}), 400
    if len(password) < 4:
        return jsonify({"success": False, "error": "Password ត្រូវមានយ៉ាងហោចណាស់ ៤ តួអក្សរ!"}), 400

    new_user, err = auth.create_user(username, password, name, role="user")
    if err:
        return jsonify({"success": False, "error": err}), 400

    # Auto-login after successful registration
    session["user"] = {
        "id": new_user["id"],
        "username": new_user["username"],
        "name": new_user["name"],
        "role": new_user["role"]
    }
    return jsonify({"success": True, "user": session["user"]})

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"success": True})

@app.route("/api/me", methods=["GET"])
def get_current_user():
    user = session.get("user")
    if user:
        return jsonify({"logged_in": True, "user": user})
    return jsonify({"logged_in": False, "user": None})

# User management (Admin Only)
@app.route("/api/users", methods=["GET"])
@admin_required
def list_users():
    return jsonify(auth.get_public_users_list())

@app.route("/api/users", methods=["POST"])
@admin_required
def create_new_user():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    name = data.get("name", "").strip()
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"success": False, "error": "សូមបញ្ចូលឈ្មោះ Username និង Password!"}), 400

    new_user, err = auth.create_user(username, password, name, role)
    if err:
        return jsonify({"success": False, "error": err}), 400

    return jsonify({"success": True, "user": new_user})

@app.route("/api/users/<user_id>", methods=["DELETE"])
@admin_required
def remove_user(user_id):
    ok, err = auth.delete_user(user_id)
    if not ok:
        return jsonify({"success": False, "error": err}), 400
    return jsonify({"success": True})

# =========================================================================
# ACCOUNTS MANAGEMENT (ADMIN ONLY FOR ADD/EDIT/DELETE)
# =========================================================================
@app.route("/api/accounts", methods=["GET"])
@login_required
def get_accounts():
    accounts = load_accounts()
    current_role = session.get("user", {}).get("role", "user")

    # If standard user, hide sensitive tokens/secrets and only return active channels
    if current_role != "admin":
        safe_accounts = []
        for a in accounts:
            if a.get("enabled", True):
                safe_accounts.append({
                    "id": a.get("id"),
                    "platform": a.get("platform"),
                    "type": a.get("type"),
                    "name": a.get("name"),
                    "enabled": True
                })
        return jsonify(safe_accounts)

    # Admin gets full account information
    return jsonify(accounts)

@app.route("/api/accounts", methods=["POST"])
@admin_required
def add_account():
    data = request.json or {}
    platform = data.get("platform", "telegram").lower()
    name = data.get("name", "").strip() or f"{platform.title()} Account"

    accounts = load_accounts()
    new_acc = {
        "id": f"{platform}_{int(time.time() * 1000)}",
        "platform": platform,
        "type": data.get("type", "channel"),
        "name": name,
        "enabled": True,
        # Telegram fields
        "chat_id": data.get("chat_id", "").strip(),
        "bot_token": data.get("bot_token", "").strip(),
        # Facebook fields
        "page_id": data.get("page_id", "").strip(),
        "access_token": data.get("access_token", "").strip(),
        # YouTube fields
        "client_id": data.get("client_id", "").strip(),
        "client_secret": data.get("client_secret", "").strip(),
        "refresh_token": data.get("refresh_token", "").strip(),
        # TikTok fields
        "tiktok_access_token": data.get("tiktok_access_token", "").strip()
    }
    accounts.append(new_acc)
    save_accounts(accounts)
    return jsonify({"success": True, "account": new_acc})

@app.route("/api/accounts/<acc_id>", methods=["PUT"])
@admin_required
def update_account(acc_id):
    data = request.json or {}
    accounts = load_accounts()
    found = False
    for a in accounts:
        if a.get("id") == acc_id:
            for k, v in data.items():
                a[k] = v
            found = True
            break
    if not found:
        return jsonify({"success": False, "error": "រកមិនឃើញគណនីនេះទេ"}), 404
    save_accounts(accounts)
    return jsonify({"success": True})

@app.route("/api/accounts/<acc_id>", methods=["DELETE"])
@admin_required
def delete_account(acc_id):
    accounts = load_accounts()
    accounts = [a for a in accounts if a.get("id") != acc_id]
    save_accounts(accounts)
    return jsonify({"success": True})

@app.route("/api/accounts/<acc_id>/test", methods=["POST"])
@admin_required
def test_single_account(acc_id):
    accounts = load_accounts()
    target_acc = next((a for a in accounts if a.get("id") == acc_id), None)
    if not target_acc:
        return jsonify({"connected": False, "error": "រកមិនឃើញគណនី"}), 404
    
    poster = SocialMediaAutoPoster()
    result = poster.test_account_connection(target_acc)
    return jsonify(result)

# =========================================================================
# STATUS & POSTING ENDPOINTS (ACCESSIBLE BY AUTHENTICATED USERS)
# =========================================================================
@app.route("/api/status", methods=["GET"])
@login_required
def get_status():
    accounts = load_accounts()
    summary = {
        "total_accounts": len(accounts),
        "platforms": {
            "telegram": {"count": 0, "active": 0},
            "facebook": {"count": 0, "active": 0},
            "youtube": {"count": 0, "active": 0},
            "tiktok": {"count": 0, "active": 0}
        }
    }
    for a in accounts:
        p = a.get("platform", "").lower()
        if p in summary["platforms"]:
            summary["platforms"][p]["count"] += 1
            if a.get("enabled", True):
                summary["platforms"][p]["active"] += 1

    return jsonify(summary)

@app.route("/api/upload", methods=["POST"])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "គ្មាន file ត្រូវបានជ្រើសរើស"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "គ្មានឈ្មោះ file"}), 400

    filename = secure_filename(file.filename)
    timestamp = int(time.time())
    unique_name = f"{timestamp}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
    file.save(filepath)

    is_video = filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))
    is_image = filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))

    return jsonify({
        "success": True,
        "file_path": filepath,
        "filename": filename,
        "is_video": is_video,
        "is_image": is_image,
        "url": f"/static/uploads/{unique_name}"
    })

@app.route("/static/uploads/<filename>")
def serve_upload(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/api/post", methods=["POST"])
@login_required
def publish_post():
    data = request.json or {}
    message = data.get("message", "").strip()
    photo_path = data.get("photo_path", "").strip()
    video_path = data.get("video_path", "").strip()
    tiktok_url = data.get("tiktok_url", "").strip()
    account_ids = data.get("account_ids", [])

    current_user = session.get("user", {})
    uname = current_user.get("name", "Unknown")

    if not message and not photo_path and not video_path:
        return jsonify({"success": False, "error": "សូមបញ្ចូលសារ អត្ថបទ រូបភាព ឬ វីដេអូ ដើម្បី Post!"}), 400

    if not account_ids:
        return jsonify({"success": False, "error": "សូមជ្រើសរើសគណនីបណ្ដាញសង្គមយ៉ាងហោចមួយ!"}), 400

    accounts = load_accounts()
    account_map = {a["id"]: a for a in accounts}

    poster = SocialMediaAutoPoster()
    results = {}
    any_success = False

    for aid in account_ids:
        acc = account_map.get(aid)
        if not acc:
            continue
        # Non-admin users can only post to accounts that Admin has enabled
        if current_user.get("role") != "admin" and not acc.get("enabled", True):
            continue

        res = poster.post_to_account(
            account=acc,
            message=message,
            photo_path_or_url=photo_path,
            video_path_or_url=video_path,
            tiktok_public_url=tiktok_url
        )
        results[aid] = res
        if res.get("success"):
            any_success = True
            add_log("success", f"{acc.get('name')} ({acc.get('platform').title()})", message, f"Items: {', '.join(res.get('posted_items', []))}", username=uname)
        else:
            add_log("error", f"{acc.get('name')} ({acc.get('platform').title()})", message, res.get("error", "Failed"), username=uname)

    return jsonify({
        "success": any_success,
        "results": results
    })

@app.route("/api/queue", methods=["GET"])
@login_required
def get_queue():
    init_sample_queue()
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []
    return jsonify(data)

@app.route("/api/queue", methods=["POST"])
@login_required
def add_to_queue():
    data = request.json or {}
    init_sample_queue()
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
    except Exception:
        queue = []

    new_item = {
        "id": int(time.time() * 1000),
        "content": data.get("message", ""),
        "photo_path": data.get("photo_path", ""),
        "video_path": data.get("video_path", ""),
        "tiktok_url": data.get("tiktok_url", ""),
        "account_ids": data.get("account_ids", []),
        "status": "pending",
        "created_by": session.get("user", {}).get("name", "User"),
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    queue.append(new_item)
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=4)
    return jsonify({"success": True, "item": new_item})

@app.route("/api/queue/<int:item_id>", methods=["DELETE"])
@login_required
def delete_from_queue(item_id):
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
        queue = [q for q in queue if q.get("id") != item_id]
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(queue, f, ensure_ascii=False, indent=4)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/logs", methods=["GET"])
@login_required
def get_logs():
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
            return jsonify(logs)
        except Exception:
            return jsonify([])
    return jsonify([])

# Cloudflare Tunnel Manager
PUBLIC_TUNNEL_URL = None
TUNNEL_PROCESS = None

def run_tunnel_thread():
    global PUBLIC_TUNNEL_URL, TUNNEL_PROCESS
    cf_path = os.path.join(BASE_DIR, "cloudflared.exe")
    if not os.path.exists(cf_path):
        return

    import subprocess, re
    cmd = [cf_path, "tunnel", "--url", "http://127.0.0.1:5000"]
    try:
        TUNNEL_PROCESS = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in TUNNEL_PROCESS.stdout:
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if match:
                PUBLIC_TUNNEL_URL = match.group(0)
                print(f"🌐 [Cloudflare Tunnel] Public URL: {PUBLIC_TUNNEL_URL}")
                break
    except Exception as e:
        print(f"⚠️ Tunnel Error: {e}")

@app.route("/api/tunnel/start", methods=["POST"])
def start_public_tunnel():
    global PUBLIC_TUNNEL_URL, TUNNEL_PROCESS
    if PUBLIC_TUNNEL_URL:
        return jsonify({"success": True, "public_url": PUBLIC_TUNNEL_URL})

    t = threading.Thread(target=run_tunnel_thread, daemon=True)
    t.start()

    # Wait up to 10 seconds for URL
    start = time.time()
    while time.time() - start < 10:
        if PUBLIC_TUNNEL_URL:
            break
        time.sleep(0.5)

    if PUBLIC_TUNNEL_URL:
        return jsonify({"success": True, "public_url": PUBLIC_TUNNEL_URL})
    return jsonify({"success": False, "error": "កំពុងរៀបចំ Tunnel សូមសាកល្បងម្ដងទៀតក្នុងរយៈពេល ៥ វិនាទី!"})

def get_local_ip():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.1.5"

@app.route("/api/network-info", methods=["GET"])
def get_network_info():
    ip = get_local_ip()
    local_url = f"http://{ip}:5000"
    active_url = PUBLIC_TUNNEL_URL or local_url
    return jsonify({
        "local_ip": ip,
        "local_url": local_url,
        "public_url": PUBLIC_TUNNEL_URL,
        "active_url": active_url,
        "qr_code_url": f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={active_url}"
    })

def start_server():
    # host='0.0.0.0' អនុញ្ញាតឱ្យទូរស័ព្ទដែលភ្ជាប់ Wi-Fi ជាមួយគ្នាបើកប្រើប្រាស់បាន
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

def main():
    local_ip = get_local_ip()
    print("=" * 65)
    print("  🚀 SOCIAL MEDIA AUTO POSTER PRO កំពុងដំណើរការ...")
    print(f"  💻 Link លើកុំព្យូទ័រ (Computer): http://127.0.0.1:5000")
    print(f"  📱 Link លើទូរស័ព្ទ (Mobile Phone): http://{local_ip}:5000")
    print("  ℹ️  ចំណាំ: ទូរស័ព្ទ និងកុំព្យូទ័រត្រូវភ្ជាប់ Wi-Fi តែមួយ")
    print("=" * 65)

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1.2)

    url = f"http://127.0.0.1:5000"
    try:
        import webview
        print(f"🚀 កំពុងបើកផ្ទាំង Desktop UI: {url}")
        webview.create_window(
            title="Social Media Auto Poster Pro",
            url=url,
            width=1320,
            height=880,
            min_size=(960, 680),
            background_color="#07090e"
        )
        webview.start()
    except Exception as e:
        print(f"ℹ️ បើកតាមរយៈ Browser ដោយសារ: {e}")
        webbrowser.open(url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 កម្មវិធីត្រូវបានបិទ។")

if __name__ == "__main__":
    main()
