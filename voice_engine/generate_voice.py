import os
import sys
import faulthandler

# 1. Enable C-level crash reporting (The Black Box)
faulthandler.enable()

# 2. Prevent the most common Windows/PyTorch silent crash
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 3. Disable HuggingFace's buggy cache migration sequence
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

print("--- Open Conduit Voice Engine: Diagnostic Mode ---")

BASE_DIR = r"C:\guilded-conduit-core\voice_engine"
REF_AUDIO = r"C:\guilded-conduit-core\voice_engine\reference\lorna.wav"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.exists(REF_AUDIO):
    print(f"❌ Error: Reference audio file missing at: {REF_AUDIO}")
    sys.exit(1)

print("✅ Checkpoint 1: Workspace ready.")

try:
    print("📦 Checkpoint 2: Importing F5-TTS libraries...")
    from f5_tts.api import F5TTS
    
    print("🧠 Checkpoint 3: Libraries loaded. Booting up the neural network...")
    f5tts = F5TTS()
    
    print("✅ Checkpoint 4: Model successfully initialized!")
except Exception as e:
    print("\n❌ The real underlying error blocking the library is:")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def generate_speech(text_to_speak):
    try:
        print(f"🎙️ Generating voice output for: \"{text_to_speak}\"")
        output_file = os.path.join(OUTPUT_DIR, "output.wav")
        
        f5tts.infer(
            ref_file=REF_AUDIO,
            ref_text="Welcome back to the channel! Today, we are exploring something completely new.", 
            gen_text=text_to_speak,
            file_wave=output_file
        )
        print(f"🎉 Success! Audio file saved to: {output_file}")
    except Exception as e:
        print(f"❌ Synthesis failed: {str(e)}")

if __name__ == "__main__":
    test_text = "The local voice engine is officially online. Sovereignty achieved. Every asset, framework, and neural weights file is running directly on our own hardware."
    generate_speech(test_text)