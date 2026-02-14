# utils.py
import os
import uuid

def generate_user_id():
    return str(uuid.uuid4())

def ensure_user_folders(base_path, user_id):
    user_path = os.path.join(base_path, user_id)
    folders = ["files", "text", "metadata"]

    for folder in folders:
        os.makedirs(os.path.join(user_path, folder), exist_ok=True)

    return user_path
