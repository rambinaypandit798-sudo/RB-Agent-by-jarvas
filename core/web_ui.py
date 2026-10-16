"""
RB.AI - Standalone Mobile Web UI
Provides an immediate installable PWA / Mobile Web client for on-device testing.
"""

WEB_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>RB.AI Assistant</title>
    <meta name="theme-color" content="#090E17">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: #090E17; color: #fff; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
        header { background: #0E1726; padding: 14px 16px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1E293B; }
        .logo-box { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 1.1rem; letter-spacing: 1px; }
        .badge { background: rgba(16, 185, 129, 0.2); color: #10B981; border: 1px solid #10B981; font-size: 0.65rem; padding: 2px 6px; border-radius: 10px; }
        .orb-container { padding: 20px 0; display: flex; flex-direction: column; align-items: center; background: linear-gradient(180deg, #0E1726 0%, #090E17 100%); }
        .orb {
            width: 120px; height: 120px; border-radius: 50%;
            background: radial-gradient(circle, #0077FE 0%, rgba(0,119,254,0.4) 60%, transparent 80%);
            box-shadow: 0 0 35px rgba(0,119,254,0.6);
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; transition: all 0.3s ease; animation: breathe 3s infinite ease-in-out;
        }
        .orb.listening {
            background: radial-gradient(circle, #00FFCC 0%, rgba(0,255,204,0.5) 60%, transparent 80%);
            box-shadow: 0 0 45px rgba(0,255,204,0.8);
            animation: pulse 1.2s infinite ease-in-out;
        }
        .orb.thinking {
            background: radial-gradient(circle, #BD00FF 0%, rgba(189,0,255,0.5) 60%, transparent 80%);
            box-shadow: 0 0 45px rgba(189,0,255,0.8);
            animation: spin 2s infinite linear;
        }
        .orb-inner { width: 60px; height: 60px; border-radius: 50%; background: #0A0E17; border: 2px solid #00E5FF; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }
        .status-label { margin-top: 10px; font-size: 0.85rem; color: #00E5FF; font-weight: 600; letter-spacing: 0.5px; }
        @keyframes breathe { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.06); } }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } }
        .actions-bar { display: flex; gap: 8px; padding: 8px 16px; overflow-x: auto; scrollbar-width: none; border-bottom: 1px solid rgba(255,255,255,0.06); }
        .action-chip {
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15);
            color: #E2E8F0; padding: 6px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;
            cursor: pointer; white-space: nowrap; display: flex; align-items: center; gap: 4px;
        }
        .action-chip:active { background: rgba(0,229,255,0.2); border-color: #00E5FF; }
        .chat-area { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
        .msg { max-width: 82%; padding: 12px 14px; border-radius: 14px; font-size: 0.9rem; line-height: 1.4; word-break: break-word; }
        .msg.user { align-self: flex-end; background: #1E3A8A; color: #fff; border-bottom-right-radius: 4px; border: 1px solid #3B82F6; }
        .msg.assistant { align-self: flex-start; background: #161F30; color: #E2E8F0; border-bottom-left-radius: 4px; border: 1px solid #2E3E5C; }
        .tool-tag { display: inline-block; background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid #10B981; font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; margin-top: 6px; font-weight: bold; }
        .input-bar { background: #0E1726; padding: 10px 12px; display: flex; align-items: center; gap: 8px; border-top: 1px solid #1E293B; }
        .input-bar input { flex: 1; background: transparent; border: none; outline: none; color: #fff; font-size: 0.95rem; }
        .btn-icon { background: transparent; border: none; color: #00E5FF; font-size: 1.4rem; cursor: pointer; padding: 4px; }
    </style>
</head>
<body>
    <header>
        <div class="logo-box">
            <span style="color:#00E5FF;">✦</span> RB.AI
            <span class="badge" id="backendBadge">TERMUX READY</span>
        </div>
        <div style="font-size:0.8rem; color:#94A3B8;">Port: 8765</div>
    </header>

    <div class="orb-container">
        <div class="orb" id="voiceOrb" onclick="toggleListening()">
            <div class="orb-inner" id="orbIcon">🎙️</div>
        </div>
        <div class="status-label" id="statusLabel">Tap or say "Hey RB"</div>
    </div>

    <div class="actions-bar">
        <div class="action-chip" onclick="triggerAction('torch')">🔦 Torch Toggle</div>
        <div class="action-chip" onclick="askRB('Hey RB, what is my battery percentage and health?')">🔋 Battery</div>
        <div class="action-chip" onclick="triggerAction('notify')">🔔 Notification</div>
        <div class="action-chip" onclick="askRB('Hey RB, give me a system summary of Termux.')">💻 System Info</div>
    </div>

    <div class="chat-area" id="chatArea">
        <div class="msg assistant">
            Hello! I am RB.AI. Tap the orb or say <b>"Hey RB"</b> to control Termux hardware, run shell commands, or ask anything!
        </div>
    </div>

    <div class="input-bar">
        <button class="btn-icon" onclick="triggerCamera()">📷</button>
        <input type="file" id="cameraInput" accept="image/*" capture="camera" style="display:none;" onchange="handleImagePicked(event)">
        <input type="text" id="userInput" placeholder="Ask RB.AI or command Termux..." onkeydown="if(event.key==='Enter') sendText()">
        <button class="btn-icon" onclick="sendText()">➤</button>
    </div>

    <script>
        let isListening = false;
        let recognition = null;

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRec();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                isListening = true;
                setOrbState('listening', 'Listening... (Say "Hey RB")');
            };

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                appendMsg('user', transcript);
                askRB(transcript, true);
            };

            recognition.onerror = (e) => {
                setOrbState('idle', 'Tap or say "Hey RB"');
            };

            recognition.onend = () => {
                isListening = false;
                setOrbState('idle', 'Tap or say "Hey RB"');
            };
        }

        function setOrbState(state, text) {
            const orb = document.getElementById('voiceOrb');
            const label = document.getElementById('statusLabel');
            orb.className = 'orb ' + (state || '');
            label.innerText = text;
        }

        function toggleListening() {
            if (!recognition) {
                alert('Speech recognition is not supported in this browser. You can type commands below.');
                return;
            }
            if (isListening) {
                recognition.stop();
            } else {
                recognition.start();
            }
        }

        function appendMsg(role, text, toolCalls) {
            const chat = document.getElementById('chatArea');
            const div = document.createElement('div');
            div.className = 'msg ' + role;
            div.innerHTML = text;

            if (toolCalls && toolCalls.length > 0) {
                toolCalls.forEach(t => {
                    const tag = document.createElement('div');
                    tag.className = 'tool-tag';
                    tag.innerText = '⚡ Action: ' + t.tool;
                    div.appendChild(tag);
                });
            }

            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        async function askRB(prompt, isVoice = false) {
            setOrbState('thinking', 'RB.AI is thinking...');
            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: prompt, is_voice: isVoice })
                });
                const data = await res.json();
                appendMsg('assistant', data.response || '(Task completed)', data.tool_calls);

                if (isVoice && 'speechSynthesis' in window) {
                    const utterance = new SpeechSynthesisUtterance(data.response);
                    window.speechSynthesis.speak(utterance);
                }
            } catch (e) {
                appendMsg('assistant', 'Error connecting to RB.AI: ' + e.message);
            } finally {
                setOrbState('idle', 'Tap or say "Hey RB"');
            }
        }

        function sendText() {
            const input = document.getElementById('userInput');
            const val = input.value.trim();
            if (!val) return;
            appendMsg('user', val);
            input.value = '';
            askRB(val);
        }

        let torchState = false;
        async function triggerAction(action) {
            if (action === 'torch') {
                torchState = !torchState;
                await fetch('/api/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ action: 'torch', args: { enabled: torchState } })
                });
                appendMsg('assistant', 'Flashlight turned ' + (torchState ? 'ON' : 'OFF'));
            } else if (action === 'notify') {
                await fetch('/api/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ action: 'notify', args: { title: 'RB.AI', content: 'RB.AI notification triggered!' } })
                });
                appendMsg('assistant', 'Sent Android system notification.');
            }
        }

        function triggerCamera() {
            document.getElementById('cameraInput').click();
        }

        function handleImagePicked(e) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = async function() {
                const b64 = reader.result.split(',')[1];
                appendMsg('user', '<img src="' + reader.result + '" style="max-width:100%; border-radius:8px;"><br>Analyze this photo.');
                setOrbState('thinking', 'Analyzing vision...');
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ text: 'Describe and analyze this image.', image: b64 })
                });
                const data = await res.json();
                appendMsg('assistant', data.response);
                setOrbState('idle', 'Tap or say "Hey RB"');
            };
            reader.readAsDataURL(file);
        }
    </script>
</body>
</html>
"""
