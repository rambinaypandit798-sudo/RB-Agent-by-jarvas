# RB.AI - Voice & Multimodal Assistant

**RB.AI** is a hybrid voice and multimodal AI assistant running on **Android** powered by **Python**, **Dart/Flutter**, and **Termux**. It features:

- 🎙️ **"Hey RB" Wake Phrase Detection**: Hands-free voice trigger and speech-to-text / text-to-speech feedback.
- ⚡ **Full Termux System Task Automation**: Battery status, flashlight/torch toggle, device vibration, Android notifications, camera photo snapshots, system clipboard, Wi-Fi info, and shell execution.
- 🧠 **Google Gemini Multimodal AI**: Direct function calling for hardware control and vision understanding for captured images.
- 📱 **Futuristic Flutter UI**: Dynamic pulsing Voice Orb visualizer reacting to listening/thinking/speaking states, quick hardware action buttons, and multimodal chat history.

---

## Architecture Overview

```
                      +-----------------------------+
                      |      Flutter / Dart UI      |
                      |   (Voice Orb, Camera, Chat) |
                      +--------------+--------------+
                                     |
                       REST / WS     |  (port 8765)
                                     v
                      +-----------------------------+
                      |     RB.AI Python Server     |
                      |    (core/server.py: 8765)   |
                      +--------------+--------------+
                                     |
           +-------------------------+-------------------------+
           |                                                   |
           v                                                   v
+-------------------------+                         +----------------------+
|   Google Gemini Engine  |                         |  Termux Automation   |
| (core/gemini_engine.py) |                         | (core/automation.py) |
| - Native Function Calling<------------------------> - Battery Status     |
| - Multimodal Vision     |                         | - Flashlight/Torch   |
| - Natural Language Core |                         | - TTS & STT Voice    |
+-------------------------+                         | - Camera & Shell     |
                                                    +----------------------+
```

---

## Directory Structure

```
rb_ai/
├── core/
│   ├── assistant.py       # Central orchestrator connecting AI & Hardware
│   ├── audio_engine.py    # "Hey RB" Wake-phrase detector & voice loop
│   ├── automation.py      # Termux API & Android system automation layer
│   ├── config.py          # Environment & settings configuration
│   ├── gemini_engine.py   # Gemini API client with function/tool calling
│   └── server.py          # HTTP & WebSocket API gateway (port 8765)
├── flutter_client/
│   ├── pubspec.yaml       # Flutter dependencies
│   └── lib/
│       ├── main.dart
│       ├── models/message.dart
│       ├── services/rbai_service.dart
│       ├── widgets/voice_visualizer.dart
│       ├── widgets/chat_view.dart
│       └── screens/home_screen.dart
├── scripts/
│   ├── install_termux_deps.sh
│   └── start_rbai.sh
├── cli.py                 # Interactive CLI & daemon runner
├── requirements.txt
└── .env.example
```

---

## Quick Start Guide

### 1. Configure Gemini API Key
Copy the template and insert your Gemini API Key:
```bash
cd ~/rb_ai
cp .env.example .env
nano .env # Set GEMINI_API_KEY=your_key
```

### 2. Run RB.AI Terminal Assistant
Test RB.AI directly in Termux:
```bash
python3 cli.py
```
Or execute a single voice/text command:
```bash
python3 cli.py --chat "Hey RB, what is my battery percentage?"
```

### 3. Start RB.AI Server for Flutter
Launch the gateway with Termux wake-lock:
```bash
./scripts/start_rbai.sh
```
The server will start on `http://0.0.0.0:8765`.

### 4. Run the Flutter Client
On your development machine or Android device:
```bash
cd flutter_client
flutter pub get
flutter run
```
Inside the app settings, set the Server URL to `http://127.0.0.1:8765` (or your phone's local Wi-Fi IP).

---

## System Task Automation Commands

Gemini can automatically execute the following system tools when prompted naturally:
- `"Hey RB, check my battery health and level"`
- `"Hey RB, turn on the flashlight"`
- `"Hey RB, show a notification saying meeting in 5 minutes"`
- `"Hey RB, what's in my clipboard?"`
- `"Hey RB, take a photo with the camera"`
- `"Hey RB, run 'uptime' and show my storage usage"`
