import os
import json
import time
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import BASE_DIR

USERS_FILE = os.path.join(BASE_DIR, "users.json")

def init_default_users():
    """បង្កើតគណនី Admin និង User គំរូប្រសិនបើមិនទាន់មាន"""
    if not os.path.exists(USERS_FILE):
        default_users = [
            {
                "id": "admin_main",
                "username": "admin",
                "password_hash": generate_password_hash("admin123"),
                "name": "អ្នកគ្រប់គ្រង (Admin)",
                "role": "admin",
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "id": "user_staff_1",
                "username": "user",
                "password_hash": generate_password_hash("user123"),
                "name": "បុគ្គលិក (Staff User)",
                "role": "user",
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        save_users(default_users)
        print("👤 បានបង្កើតគណនីដំបូង: admin (pass: admin123) និង user (pass: user123)")

def load_users():
    if not os.path.exists(USERS_FILE):
        init_default_users()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def verify_user(username: str, password: str):
    users = load_users()
    for u in users:
        if u.get("username").lower() == username.lower().strip():
            if check_password_hash(u.get("password_hash"), password):
                return {
                    "id": u.get("id"),
                    "username": u.get("username"),
                    "name": u.get("name"),
                    "role": u.get("role")
                }
    return None

def create_user(username: str, password: str, name: str = "", role: str = "user"):
    users = load_users()
    u_clean = username.lower().strip()
    if any(u.get("username").lower() == u_clean for u in users):
        return None, "ឈ្មោះ Username នេះមានរួចហើយ!"

    new_user = {
        "id": f"user_{int(time.time() * 1000)}",
        "username": u_clean,
        "password_hash": generate_password_hash(password),
        "name": name or u_clean.title(),
        "role": role if role in ["admin", "user"] else "user",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    users.append(new_user)
    save_users(users)
    return new_user, None

def delete_user(user_id: str):
    users = load_users()
    # Cannot delete the primary admin
    target = next((u for u in users if u.get("id") == user_id), None)
    if not target:
        return False, "រកមិនឃើញគណនីនេះទេ"
    if target.get("username") == "admin":
        return False, "មិនអាចលុបគណនី Admin ចម្បងបានទេ"

    users = [u for u in users if u.get("id") != user_id]
    save_users(users)
    return True, None

def get_public_users_list():
    users = load_users()
    return [{
        "id": u.get("id"),
        "username": u.get("username"),
        "name": u.get("name"),
        "role": u.get("role"),
        "created_at": u.get("created_at")
    } for u in users]
