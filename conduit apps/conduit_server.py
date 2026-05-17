import bpy
import os
import time

# Clean, dedicated directory tracking
OUTBOX_PATH = r"C:\conduit apps\outbox"

def check_for_scripts():
    # Make sure the drop-box directory actually exists
    if not os.path.exists(OUTBOX_PATH):
        try:
            os.makedirs(OUTBOX_PATH)
        except:
            return

    # Scan exclusively for executable python scrolls
    files = [f for f in os.listdir(OUTBOX_PATH) if f.endswith(".py")]
    
    for file in files:
        file_path = os.path.join(OUTBOX_PATH, file)
        print(f"\n🧙 Wizard found a new scroll: {file}")
        
        try:
            # Safely execute the payload inside Blender's context
            bpy.ops.script.python_file_run(filepath=file_path)
            print("✨ Spell cast successfully!")
        except Exception as e:
            print(f"❌ Wizard failed to cast spell: {e}")
            
        # Clean up the outbox immediately so it doesn't loop fire
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"⚠️ Could not clear scroll from parchment: {e}")

# Dedicated background execution engine
if bpy.app.background:
    print("\n🛸 ======================================= 🛸")
    print("🛸 Open Conduit Daemon Mode Active (V5.1) 🛸")
    print("🛸 Watching outbox... ready for the Squeeze!🛸")
    print("🛸 ======================================= 🛸\n")
    try:
        while True:
            check_for_scripts()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the Conduit daemon gracefully...")
else:
    # Fallback to internal app timers if ever loaded via the regular Blender GUI
    if hasattr(bpy.app, "timers"):
        pass
    bpy.app.timers.register(check_for_scripts)
    print("👂 Blender GUI Timer Activated... ready for the Squeeze!")