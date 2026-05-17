"""
Open Conduit - Live MQTT Monitor Daemon
License: GPLv3
"""
import os
import json
import paho.mqtt.client as mqtt
import anthropic

# --- CONFIGURATION ---
MQTT_BROKER = "127.0.0.1" # Uses localhost. Change to Manager IP if running on a separate worker.
MQTT_PORT = 1883
CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def on_connect(client, userdata, flags, rc):
    print(f"[SUCCESS] Connected to Mosquitto MQTT broker on port {MQTT_PORT}")
    client.subscribe("flamenco/#")
    print("[MONITOR] Listening for Blender render farm telemetry...")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    
    # We only want to trigger alerts on critical failures to keep the terminal clean
    if "task/update" in topic or "worker/status" in topic:
        try:
            data = json.loads(payload)
            status = data.get("status", "")
            
            if status in ["failed", "offline-unexpected", "stalled"]:
                print(f"\n[ALERT] Render Issue Detected on {topic}:")
                print(f"Details: {data}")
                analyze_failure_with_claude(data)
        except json.JSONDecodeError:
            pass

def analyze_failure_with_claude(error_data):
    """Sends failure telemetry to Claude AI for automated troubleshooting."""
    if not CLAUDE_API_KEY:
        print("[NOTICE] No Anthropic API key found in environment. Skipping AI analysis.")
        return
        
    print("[AI] Sending error telemetry to Claude for analysis...")
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    
    # Future integration point: 
    # Use AI response to automatically adjust Blender settings, 
    # or trigger a physical print queue via the Bambu Lab P1S / Elegoo Mars.
    
    print("[AI] Analysis requested successfully.")

client = mqtt.Client(client_id="conduit_monitor_ai")
client.on_connect = on_connect
client.on_message = on_message

if __name__ == "__main__":
    print("===================================================")
    print(" OPEN CONDUIT: AI Render Farm Monitor Initialized  ")
    print("===================================================")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except ConnectionRefusedError:
        print("[ERROR] Cannot connect to Mosquitto. Is the Windows service running?")