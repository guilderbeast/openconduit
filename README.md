# 🧠 Guilded Imagination - Conduit Core

Welcome to the central background automation pipeline for **Guilded Imagination**. Our mission is to build open-source assistive technology tools, utilizing automated 3D rendering pipelines to visualize neural data structures, speech-frequency profiles, and interactive training assets.

This repository provides a split-engine daemon system that handles high-speed script execution natively through a background instance of Blender 5.1, perfectly isolated to ensure 100% stability alongside local render farm configurations.

---

## 📁 Repository Structure

* **`blender_farm/`** - Contains core production configs, local SQLite tracking databases, and asset templates.
* **`core/`** - The dual-engine automation controller files.
  * `conduit_server.py` - The background Blender listening daemon loop.
  * `wizard_watcher.py` - The network receiver loop for incoming dataset strings.

---

## 🚀 Local Quickstart Guide

To spin up the dual-engine pipeline on your local workstation for development or testing, follow these steps:

### 1. Initialize the Blender Background Engine
Open a Command Prompt window and execute the background listener:
```cmd
"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --background --python "C:\guilded-conduit-core\core\conduit_server.py"