import os
import time
import shutil
import ollama
import socket

INBOX = r"C:\BlenderFarm\inbox"
PROCESSED = r"C:\BlenderFarm\processed"
OUTBOX = r"C:\BlenderFarm\outbox"

def send_to_blender(code):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 9876))
            s.sendall(code.encode('utf-8'))
            print("🚀 Spell teleported directly to Blender!")
    except Exception as e:
        print(f"❌ Connection to Blender failed: {e}")

for folder in [INBOX, PROCESSED, OUTBOX]:
    if not os.path.exists(folder):
        os.makedirs(folder)

print("🧙 The Network Wizard is LIVE. Watching for scrolls...")

while True:
    try:
        files = os.listdir(INBOX)
        for filename in files:
            file_path = os.path.join(INBOX, filename)
            
            # ✨ FIX 1: Ignore directories/folders
            if os.path.isdir(file_path):
                continue

            # ✨ FIX 2: Wait a moment for Windows to release the lock
            time.sleep(0.5)

            with open(file_path, "r") as f:
                user_prompt = f.read()
            
            if not user_prompt.strip():
                continue

            print(f"\n✨ New Request: {user_prompt}")

            response = ollama.generate(
                model='qwen2.5-coder:7b',
                prompt=f"Write only Blender bpy python code to: {user_prompt}. No markdown."
            )
            
            raw_content = response['response']
            script_content = raw_content.replace("```python", "").replace("```", "").strip()

            send_to_blender(script_content)

            # Save backup
            out_path = os.path.join(OUTBOX, filename.replace(".txt", ".py"))
            with open(out_path, "w") as f:
                f.write(script_content)

            shutil.move(file_path, os.path.join(PROCESSED, filename))
            
    except Exception as e:
        print(f"⚠️ Wizard paused: {e}")
            
    time.sleep(2)