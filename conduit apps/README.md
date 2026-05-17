# Conduit — Open Source AI Render Farm
### everyone. by everyone. for everyone.

> Built from a bedroom. During a mental health crisis. By a 48-year-old self-taught developer with no computer science degree.
> And it works.

**openconduit.art** | Free at point of authorship. Always. No exceptions.

---

## What is Conduit?

Conduit is an open source platform connecting AI, Blender and distributed rendering to do two things:

1. **Story → Animation** — A child types a story. Conduit builds and renders it. No money. No technical knowledge. Just imagination.
2. **Thought → Speech** — Real-time AI communication for people who are deaf, mute or non-verbal. Not a phrase board. A voice.

This repository contains **Phase 1** — a fully working, self-monitoring AI render farm running on Windows 11 Pro with Blender 5.1. Everything documented. Everything free.

---

## The Complete Stack

```
┌─────────────────────────────────────────────────────────┐
│                    CONDUIT STACK                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Claude AI (via MCP) ──→ Blender 5.1                   │
│         │                    │                           │
│         │              Flamenco 3.9                      │
│         │            (Render Manager)                    │
│         │                    │                           │
│         │         ┌──────────┴──────────┐               │
│         │         │                     │               │
│         │    Worker 1              Worker 2             │
│         │   (Machine 1)           (Machine 2)           │
│         │         │                     │               │
│         │         └──────────┬──────────┘               │
│         │                    │                           │
│         │              MQTT (Mosquitto)                  │
│         │                    │                           │
│         └────→ Conduit Monitor (AI self-healing)        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

| Component | Purpose | Link |
|---|---|---|
| **Blender 5.1** | 3D creation suite | [blender.org](https://blender.org) |
| **Flamenco 3.9** | Render farm manager | [flamenco.blender.org](https://flamenco.blender.org) |
| **Blender MCP** | AI controls Blender via conversation | [github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) |
| **Mosquitto** | MQTT broker for live telemetry | [mosquitto.org](https://mosquitto.org) |
| **Ollama** | Run AI locally, no API costs | [ollama.com](https://ollama.com) |
| **Claude** | AI assistant (or use local LLM) | [claude.ai](https://claude.ai) |

---

## Quick Start (15 minutes)

### Requirements
- Two machines running Windows 11 Pro on the same network
- Blender 5.1 installed on both (must match exactly)
- Python 3.x installed (tick "Add to PATH" during install)
- Git (optional)

### Step 1 — Download Flamenco
Go to [flamenco.blender.org/download](https://flamenco.blender.org/download) and download Flamenco 3.9 for Windows.

Extract to `C:\BlenderFarm\flamenco-3.9-windows-amd64\` on both machines.

### Step 2 — Copy the pre-configured yaml
Copy `config/flamenco-manager.yaml` from this repo to:
```
C:\BlenderFarm\flamenco-3.9-windows-amd64\flamenco-manager.yaml
```
Edit the Blender path to match your installation. This file fixes:
- Port 80 instead of 8080 (bypasses Windows 11 Pro GPO firewall)
- 120 minute task timeouts (essential for complex scenes)
- Correct absolute storage paths

### Step 3 — Fix the Blender 5.1 addon
Blender 5.1 requires a manifest file the Flamenco addon doesn't include. 

Copy `config/blender_manifest.toml` to:
```
C:\Users\[USERNAME]\AppData\Roaming\Blender Foundation\Blender\5.1\extensions\user_default\flamenco\
```

See `docs/addon-installation.md` for full instructions.

### Step 4 — Create and share the BlenderFarm folder
On your manager machine:
- Create `C:\BlenderFarm\`
- Right-click → Properties → Sharing → Advanced Sharing → Share as `BlenderFarm`
- Give your user Full Control permissions

On your worker machine:
- File Explorer → right-click This PC → Map network drive
- Path: `\\[MANAGER-IP]\BlenderFarm`

### Step 5 — Start everything
Edit `scripts/start-worker.bat` and set your manager IP address.

**On manager machine** (run first):
```
scripts\start-manager.bat
```

**On both machines:**
```
scripts\start-worker.bat
```

Open `http://[MANAGER-IP]` in a browser — both workers should show as Awake.

### Step 6 — Set up auto-start
Press Win+R → type `shell:startup` → place shortcuts to the startup scripts there.

Both machines will now automatically start Flamenco on every boot.

---

## The Self-Monitoring AI Farm

Conduit includes an AI monitoring system that watches the render farm in real time and automatically detects and responds to problems.

### How it works

```
Flamenco → MQTT → Mosquitto → conduit_monitor.py → Claude API → Action
```

When a worker goes offline, a task fails repeatedly, or a render stalls — the monitor sends the data to Claude, which recommends and logs the appropriate action.

### Setup

**Install Mosquitto:**
Download from [mosquitto.org/download](https://mosquitto.org/download) and install on your manager machine.

Add these lines to `C:\Program Files\mosquitto\mosquitto.conf`:
```
listener 1883 0.0.0.0
allow_anonymous true
```

Restart Mosquitto:
```
net stop mosquitto
net start mosquitto
```

**Enable MQTT in Flamenco:**
In `flamenco-manager.yaml` update the MQTT section:
```yaml
mqtt:
  client:
    enabled: true
    broker: "tcp://[MANAGER-IP]:1883"
    clientID: flamenco
    topic_prefix: flamenco
    username: ""
    password: ""
```

**Install Python dependencies:**
```
pip install paho-mqtt anthropic
```

**Run the monitor:**
```
python monitoring/conduit_monitor.py
```

Add your Anthropic API key to the CONFIG section of the script, or leave it blank to run in monitor-only mode (logs everything without AI intervention).

---

## Blender MCP Setup

Blender MCP connects Claude AI directly to Blender so you can control your scenes through conversation.

### Requirements
- Claude Desktop installed ([claude.ai/download](https://claude.ai/download))
- uv package manager installed

### Install uv
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Configure Claude Desktop
Go to Claude Desktop → Settings → Developer → Edit Config and add:
```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    }
  }
}
```

### Install the Blender addon
Download `addon.py` from [github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp)

In Blender: Edit → Preferences → Add-ons → Install → select addon.py

In Blender's N panel → BlenderMCP tab → click **Start Server**

Restart Claude Desktop — look for the hammer icon 🔨 in the chat interface.

---

## Repository Structure

```
conduit/
├── README.md                    ← You are here
├── config/
│   ├── flamenco-manager.yaml    ← Pre-configured manager settings
│   └── blender_manifest.toml   ← Fixes Blender 5.1 missing manifest
├── scripts/
│   ├── start-manager.bat        ← One-click manager startup
│   └── start-worker.bat         ← One-click worker startup (edit IP first)
├── monitoring/
│   ├── conduit_monitor.py       ← AI self-monitoring script
│   └── requirements.txt         ← Python dependencies
└── docs/
    ├── addon-installation.md    ← Blender 5.1 addon fix guide
    ├── blender-mcp-setup.md     ← Blender MCP Windows setup
    ├── mosquitto-setup.md       ← MQTT broker configuration
    └── performance.md           ← GPU, ethernet and optimisation tips
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Missing manifest error | Blender 5.1 extension system | Add `blender_manifest.toml` from config/ |
| Port 8080 blocked | Windows 11 Pro GPO | Change to port 80 in yaml |
| File not found error | Wrong working directory | Run manager from its own subfolder |
| yaml changes not saved | Setup wizard overwrites yaml | Edit yaml after wizard completes |
| Workers can't connect | Manager not running | Start manager before workers |
| Task timeout | Default 10min too short | Set task_timeout: 120m0s in yaml |
| LocalFirewallRules: N/A | GPO override active | Switch to port 80 to bypass |
| Blender MCP no hammer icon | Claude Desktop config wrong | Check claude_desktop_config.json |
| uvx not recognised | uv not in PATH | Reinstall uv, tick Add to PATH |
| MQTT not connecting | Mosquitto config | Add listener 1883 0.0.0.0 to conf |

---

## What We Proved

- ✅ 300 frame WWII animation rendered across two consumer machines
- ✅ 16 hour single-machine render → 7 hours across two machines
- ✅ RTX 4050 + RTX 3060 both running OptiX
- ✅ Live MQTT telemetry streaming from Flamenco
- ✅ Claude AI connected directly to Blender via MCP
- ✅ Self-monitoring script detecting and responding to farm issues
- ✅ Auto-start on boot — zero manual intervention needed

---

## The Vision

This repository is Phase 1 of Conduit. Phase 2 and 3 are in development:

**Phase 2 — Story to Animation**
A child types a story. AI writes the script, builds the scene via Blender MCP, renders across the farm, returns a finished animation. No money. No skills. Just imagination.

**Phase 3 — Thought to Speech**
Real-time AI communication for people who are deaf, mute or non-verbal. Not preset phrases — genuine individual expression, learned for each person, on any device, free.

**The founding principle:** Free at point of authorship. Always. No exceptions.

---

## Contributing

We need:
- Developers (Python, Blender scripting, MCP)
- Accessibility researchers and speech therapists
- Educators and animators
- Writers and translators
- People who believe every human being deserves a voice

No experience necessary. No contribution too small.

Star the repo. Share it. Open an issue. Submit a PR.

---

## Links

- 🌐 Website: [openconduit.art](https://openconduit.art)
- 💬 Discussions: [GitHub Discussions](https://github.com/guilderbeast/openconduit/discussions)
- 🐦 Twitter: [@openconduit](https://twitter.com/openconduit)

---

## Mental Health Support

Conduit was born from depression, anxiety and ADHD. If you are struggling:

| Country | Service | Number |
|---|---|---|
| 🇬🇧 UK | Samaritans | 116 123 |
| 🇬🇧 UK | Mind | 0300 123 3393 |
| 🇬🇧 UK | Crisis Text | Text SHOUT to 85258 |
| 🇺🇸 US | 988 Lifeline | 988 |
| 🌍 International | IASP | [iasp.info/resources](https://www.iasp.info/resources/Crisis_Centres/) |
| 🧠 ADHD | ADHD UK | [adhduk.co.uk](https://adhduk.co.uk) |

---

## License

**GNU General Public License v3.0**

This software is free: you can use it, modify it, and distribute it — but any modified versions must also be open source under GPL v3. Nobody can take Conduit, close it up, and sell it. Ever.

This is a stronger protection than MIT — chosen deliberately because Conduit is being registered as a charity and its open nature must be legally protected permanently.

Full license text: [LICENSE](LICENSE) | [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0.txt)

**FOUNDING PRINCIPLE (non-legal, but foundational):**
Free at point of authorship. Always. No exceptions.

*Born from struggle. Built for everyone. © 2026 Richard Guilder / Conduit Foundation.*
*With love from Willow, Brandy, Bailey, Mercedes, Teddy and Herschey.*
