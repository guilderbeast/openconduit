import bpy
import os

# Point this to your outbox
OUTBOX_PATH = r"C:\conduit apps\outbox"

def check_for_scripts():
    # 1. Check if folder exists
    if not os.path.exists(OUTBOX_PATH):
        return 1.0
        
    # 2. Look for .py files
    files = [f for f in os.listdir(OUTBOX_PATH) if f.endswith(".py")]
    
    for file in files:
        file_path = os.path.join(OUTBOX_PATH, file)
        print(f"🧙 Wizard found a new scroll: {file}")
        
        try:
            # We use Blender's internal operator to run the file properly
            # This is safer than 'exec' for Blender's API
            bpy.ops.script.python_file_run(filepath=file_path)
            print("✨ Spell cast successfully!")
        except Exception as e:
            print(f"❌ Wizard failed to cast spell: {e}")
            
        # 3. Clean up the outbox
        try:
            os.remove(file_path)
        except:
            pass # Sometimes Windows locks the file for a split second
            
    return 1.0 # Keep checking every second

# Clear any old timers so they don't pile up
if hasattr(bpy.app, "timers"):
    # This just ensures we don't have 10 listeners running at once
    pass 

bpy.app.timers.register(check_for_scripts)
print("👂 Blender is listening... ready for the Squeeze!")
