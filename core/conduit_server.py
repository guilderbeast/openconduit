import bpy
import os
import time

# Pointing explicitly to the outbox inside your consolidated farm folder
OUTBOX_PATH = r"C:\guilded-conduit-core\blender_farm\outbox"

def check_for_scripts():
    if not os.path.exists(OUTBOX_PATH):
        try:
            os.makedirs(OUTBOX_PATH)
        except:
            return

    # Scan exclusively for python scripts
    files = [f for f in os.listdir(OUTBOX_PATH) if f.endswith(".py")]
    
    for file in files:
        file_path = os.path.join(OUTBOX_PATH, file)
        print(f"\n🧙 Wizard found a new scroll: {file}")
        
        try:
            # Execute the payload safely inside Blender
            bpy.ops.script.python_file_run(filepath=file_path)
            print("✨ Spell cast successfully!")
        except Exception as e:
            print(f"❌ Wizard failed to cast spell: {e}")
            
        # Clean up the file so it doesn't loop fire
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"⚠️ Could not clear scroll from parchment: {e}")

if bpy.app.background:
    print("\n🛸 ======================================= 🛸")
    print("🛸 Guilded Imagination Conduit Active     🛸")
    print("🛸 Listening for dynamic neural inputs... 🛸")
    print("🛸 ======================================= 🛸\n")
    try:
        while True:
            check_for_scripts()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the Conduit daemon gracefully...")