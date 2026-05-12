# Blender MCP — Windows 11 Setup Guide

Connect Claude AI directly to Blender so you can control your 3D scenes through conversation.

---

## What You Need

- Windows 11 (Pro or Home)
- Blender 5.1+ installed
- Claude Desktop installed ([claude.ai/download](https://claude.ai/download))
- uv package manager (instructions below)

---

## Step 1 — Install uv

Open PowerShell as Administrator and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close PowerShell and open a fresh CMD window. Verify it worked:

```
uvx --version
```

Should return a version number. If not, restart your machine and try again.

---

## Step 2 — Install the Blender Addon

Download `addon.py` from [github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp)

In Blender:
1. Edit → Preferences → Add-ons
2. Click **Install**
3. Navigate to the downloaded `addon.py`
4. Click **Install Add-on**
5. Tick the checkbox to enable it

In Blender's viewport, press **N** to open the side panel. You should see a **BlenderMCP** tab.

Click **Start Server** in that tab. It should say "Server running on port 9876".

---

## Step 3 — Configure Claude Desktop

Open Claude Desktop → Settings → Developer → Edit Config

This opens `claude_desktop_config.json`. Add:

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

Save the file.

**Completely quit Claude Desktop** — right-click taskbar icon → Quit. Not just close the window.

Reopen Claude Desktop.

---

## Step 4 — Verify Connection

In Claude Desktop, look for a **hammer icon 🔨** in the bottom left of the chat input box.

If you see it — Blender MCP is connected and ready.

Type something like: *"What objects are in my current Blender scene?"*

Claude will query Blender and tell you exactly what's there.

---

## Troubleshooting

**No hammer icon:**
- Make sure Blender is open and the MCP server is running (N panel → BlenderMCP → Start Server)
- Make sure you fully quit and restarted Claude Desktop after editing the config
- Check the config file has valid JSON (no missing brackets or commas)

**uvx not recognised:**
- uv is not in PATH — reinstall uv using the PowerShell command above
- Restart your machine after installing

**Connection refused:**
- Check port 9876 is not blocked by firewall
- In CMD: `netstat -ano | findstr 9876` — should show something listening
- Try: Windows Security → Firewall → Allow an app → add uvx and Blender

**Config file location:**
```
C:\Users\[USERNAME]\AppData\Roaming\Claude\claude_desktop_config.json
```

---

## What Claude Can Do in Blender

Once connected, Claude can:

- Create, modify and delete 3D objects
- Apply materials and textures
- Set up lighting and cameras
- Inspect the current scene
- Execute arbitrary Python code in Blender
- Download assets from Poly Haven
- Generate 3D models via Hyper3D Rodin

Example prompts:
- *"Create a simple WWII airfield with a runway and some buildings"*
- *"Add three point lighting to the scene"*
- *"What is the current render engine and sample count?"*
- *"Delete all objects and start fresh"*
- *"Set the sky to a sunset atmosphere"*

---

## Important Notes

- Only run **one** MCP server instance at a time
- Start Blender and click Start Server **before** opening Claude Desktop
- The first command sometimes doesn't go through — try again if it fails
- Blender MCP works with Blender 3.0 and newer
