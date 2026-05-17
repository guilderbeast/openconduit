# Mosquitto MQTT Setup Guide

Mosquitto is the MQTT broker that powers Conduit's live render farm telemetry and AI monitoring.

---

## Install Mosquitto

Download from [mosquitto.org/download](https://mosquitto.org/download) — select the Windows installer.

Run the installer with default settings. Mosquitto installs as a Windows service and starts automatically.

Verify it's running in CMD:
```
sc query mosquitto
```

Should show `STATE: RUNNING`.

---

## Configure for Network Access

By default Mosquitto only listens on localhost. We need it to accept connections from other machines on the network.

Open Notepad as Administrator and navigate to:
```
C:\Program Files\mosquitto\mosquitto.conf
```

Scroll to the very bottom and add these two lines:
```
listener 1883 0.0.0.0
allow_anonymous true
```

Save the file.

Restart Mosquitto:
```
net stop mosquitto
net start mosquitto
```

Verify it's now listening on the network:
```
netstat -ano | findstr 1883
```

Should show `0.0.0.0:1883` — meaning it's accepting connections from any machine.

---

## Enable MQTT in Flamenco

In `C:\BlenderFarm\flamenco-3.9-windows-amd64\flamenco-manager.yaml` find the MQTT section and update:

```yaml
mqtt:
  client:
    enabled: true
    broker: "tcp://[YOUR-MANAGER-IP]:1883"
    clientID: flamenco
    topic_prefix: flamenco
    username: ""
    password: ""
```

Replace `[YOUR-MANAGER-IP]` with your manager machine's IP address (find it with `ipconfig` in CMD).

Restart Flamenco Manager. You should see in the startup log:
```
INF mqtt client: connection established broker=tcp://[IP]:1883
```

---

## Test the Connection

In CMD on the manager machine:
```
cd "C:\Program Files\mosquitto"
mosquitto_sub -h [YOUR-MANAGER-IP] -t "flamenco/#" -v
```

Now submit a render job — you should see live data flowing in the CMD window showing every task update, worker status change and frame completion in real time.

---

## Running the Conduit Monitor

Once MQTT is working, run the AI monitoring script:

```
pip install paho-mqtt anthropic --break-system-packages
python C:\BlenderFarm\monitoring\conduit_monitor.py
```

The monitor will:
- Subscribe to all Flamenco MQTT topics
- Log every frame, task and worker event
- Alert when workers go offline unexpectedly
- Flag tasks that fail repeatedly
- Detect stalled renders
- Send problem data to Claude AI for analysis (if API key is configured)

See `monitoring/conduit_monitor.py` for configuration options.

---

## Auto-Start Mosquitto

Mosquitto installs as a Windows service and starts automatically on boot — no action needed.

To verify auto-start is configured:
```
sc qc mosquitto
```

Should show `START_TYPE: AUTO_START`.
