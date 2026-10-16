"""
RB.AI - Production Master Web Application & Agent Interface
Implements dynamic user profile, JARVIS Arc Reactor HUD button,
5 Sub-Agents Workspace with glowing flow graph, Live Voice with strict turn-taking,
Telegram webhooks, WhatsApp bridge, GitHub integration, and SQLite persistent storage.
"""

WEB_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>RB Agent — Autonomous Operating System</title>
    <meta name="theme-color" content="#F8FAFC">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-primary: #F8FAFC;
            --bg-card: #FFFFFF;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --border-color: #E2E8F0;
            --accent-cyan: #00E5FF;
            --accent-blue: #0077FE;
            --accent-purple: #8B5CF6;
            --accent-green: #10B981;
            --accent-amber: #F59E0B;
            --accent-pink: #EC4899;
            --hud-glow: rgba(0, 229, 255, 0.4);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: var(--bg-primary); color: var(--text-primary); height: 100vh; display: flex; flex-direction: column; overflow: hidden; transition: background 0.3s; }

        /* Top Header */
        header {
            background: var(--bg-card);
            padding: 12px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border-color);
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            z-index: 20;
        }
        .header-left { display: flex; align-items: center; gap: 14px; }
        .menu-btn { background: none; border: none; font-size: 1.25rem; color: var(--text-primary); cursor: pointer; padding: 4px; }
        .logo-box { display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 1.15rem; letter-spacing: 0.5px; }
        .logo-box span { color: var(--accent-blue); }
        .badge { background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; font-size: 0.7rem; font-weight: 600; padding: 3px 8px; border-radius: 12px; }

        /* Dynamic Greeting Banner */
        .greeting-card {
            background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
            color: #FFFFFF;
            padding: 18px 20px;
            margin: 14px 16px 8px 16px;
            border-radius: 18px;
            box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
            position: relative;
            overflow: hidden;
        }
        .greeting-card::after {
            content: ''; position: absolute; right: -20px; top: -20px; width: 100px; height: 100px;
            background: radial-gradient(circle, rgba(0,229,255,0.2) 0%, transparent 70%); border-radius: 50%;
        }
        .greeting-title { font-size: 1.25rem; font-weight: 800; letter-spacing: -0.3px; display: flex; align-items: center; gap: 8px; }
        .greeting-subtitle { font-size: 0.85rem; color: #94A3B8; margin-top: 4px; }

        /* Floating Status Indicator */
        .floating-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255,255,255,0.12);
            backdrop-filter: blur(8px);
            padding: 5px 12px;
            border-radius: 20px;
            margin-top: 10px;
            font-size: 0.75rem;
            color: #E2E8F0;
            border: 1px solid rgba(255,255,255,0.15);
        }
        .status-dot { width: 8px; height: 8px; border-radius: 50%; background: #10B981; box-shadow: 0 0 8px #10B981; }

        /* Central Arc Reactor HUD Section */
        .hud-stage {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 24px 0 16px 0;
            position: relative;
        }
        .reactor-container {
            width: 170px;
            height: 170px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }
        /* Rotating Outer Rings */
        .reactor-outer-ring {
            position: absolute;
            inset: 0;
            border-radius: 50%;
            border: 2px dashed rgba(0, 229, 255, 0.6);
            animation: rotateClockwise 12s linear infinite;
        }
        .reactor-mid-ring {
            position: absolute;
            inset: 12px;
            border-radius: 50%;
            border: 2px solid rgba(0, 119, 254, 0.5);
            border-top-color: #00E5FF;
            border-bottom-color: #8B5CF6;
            animation: rotateAntiClockwise 7s linear infinite;
        }
        .reactor-core {
            width: 104px;
            height: 104px;
            border-radius: 50%;
            background: radial-gradient(circle, #0F172A 0%, #030712 100%);
            border: 3px solid #00E5FF;
            box-shadow: 0 0 25px rgba(0, 229, 255, 0.5), inset 0 0 18px rgba(0, 229, 255, 0.4);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            z-index: 5;
        }
        .reactor-container:active .reactor-core {
            transform: scale(0.94);
            box-shadow: 0 0 40px rgba(0, 229, 255, 0.8);
        }
        .core-title { font-size: 0.95rem; font-weight: 800; color: #FFFFFF; letter-spacing: 0.8px; text-shadow: 0 0 8px rgba(0,229,255,0.8); }
        .core-sub { font-size: 0.55rem; color: #38BDF8; font-weight: 600; text-transform: uppercase; margin-top: 2px; }

        @keyframes rotateClockwise { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes rotateAntiClockwise { 0% { transform: rotate(360deg); } 100% { transform: rotate(0deg); } }

        /* Quick Action Bar */
        .actions-scroll {
            display: flex;
            gap: 8px;
            padding: 8px 16px;
            overflow-x: auto;
            scrollbar-width: none;
        }
        .actions-scroll::-webkit-scrollbar { display: none; }
        .action-chip {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 7px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            white-space: nowrap;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            transition: all 0.2s;
        }
        .action-chip:hover { border-color: var(--accent-blue); color: var(--accent-blue); }

        /* Main Chat Area */
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 12px 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .message-bubble {
            max-width: 85%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 0.92rem;
            line-height: 1.45;
            word-break: break-word;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        }
        .message-bubble.user {
            align-self: flex-end;
            background: #1E3A8A;
            color: #FFFFFF;
            border-bottom-right-radius: 4px;
        }
        .message-bubble.assistant {
            align-self: flex-start;
            background: var(--bg-card);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-bottom-left-radius: 4px;
        }
        .agent-tag {
            display: inline-block;
            font-size: 0.65rem;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 6px;
            margin-bottom: 4px;
            text-transform: uppercase;
        }
        .tag-research { background: #E0F2FE; color: #0284C7; }
        .tag-memory { background: #DCFCE7; color: #16A34A; }
        .tag-preview { background: #FEF3C7; color: #D97706; }
        .tag-automation { background: #EDE9FE; color: #7C3AED; }
        .tag-coding { background: #FCE7F3; color: #DB2777; }

        /* Live Subtitles & Captions Bar */
        .subtitles-bar {
            background: #0F172A;
            color: #38BDF8;
            padding: 8px 16px;
            font-size: 0.8rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
            border-top: 1px solid #1E293B;
        }
        .subtitles-text { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        /* Input Controls Bar */
        .input-bar {
            background: var(--bg-card);
            padding: 10px 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-top: 1px solid var(--border-color);
        }
        .input-bar input {
            flex: 1;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            padding: 10px 14px;
            border-radius: 22px;
            outline: none;
            color: var(--text-primary);
            font-size: 0.92rem;
        }
        .input-bar input:focus { border-color: var(--accent-blue); }
        .icon-btn {
            background: none;
            border: none;
            font-size: 1.25rem;
            color: var(--accent-blue);
            cursor: pointer;
            padding: 6px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .mic-btn.active {
            background: #EF4444;
            color: #FFFFFF;
            animation: pulseRecord 1.2s infinite;
        }
        @keyframes pulseRecord { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } }

        /* Sidebar Navigation Drawer (Left) */
        .drawer-overlay {
            position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px);
            z-index: 50; display: none; opacity: 0; transition: opacity 0.3s;
        }
        .drawer-overlay.active { display: block; opacity: 1; }
        .drawer {
            position: fixed; top: 0; left: 0; bottom: 0; width: 290px;
            background: #FFFFFF; z-index: 55;
            display: flex; flex-direction: column;
            transform: translateX(-100%); transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 4px 0 20px rgba(0,0,0,0.15);
        }
        .drawer.active { transform: translateX(0); }
        .drawer-header {
            padding: 24px 20px 16px 20px;
            border-bottom: 1px solid var(--border-color);
            background: #F8FAFC;
        }
        .user-avatar-row { display: flex; align-items: center; gap: 12px; }
        .avatar-circle {
            width: 48px; height: 48px; border-radius: 50%; background: #1E3A8A; color: #FFFFFF;
            font-weight: 700; font-size: 1.2rem; display: flex; align-items: center; justify-content: center;
        }
        .user-info-name { font-size: 1rem; font-weight: 800; color: #0F172A; }
        .user-info-role { font-size: 0.75rem; color: #64748B; }
        .drawer-nav { flex: 1; overflow-y: auto; padding: 12px 10px; display: flex; flex-direction: column; gap: 4px; }
        .nav-item {
            display: flex; align-items: center; gap: 14px; padding: 12px 14px;
            border-radius: 12px; color: #334155; font-size: 0.92rem; font-weight: 600;
            cursor: pointer; transition: all 0.2s; text-decoration: none;
        }
        .nav-item:hover, .nav-item.active { background: #EEF2F6; color: var(--accent-blue); }
        .nav-item i { font-size: 1.1rem; width: 22px; text-align: center; }

        /* Fullscreen Dark 5 Sub-Agents Workspace Modal */
        .workspace-modal {
            position: fixed; inset: 0; background: #070B12; z-index: 60;
            display: none; flex-direction: column; opacity: 0; transition: opacity 0.3s;
        }
        .workspace-modal.active { display: flex; opacity: 1; }
        .ws-header {
            padding: 14px 20px; display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid #1E293B; background: #0B111E;
        }
        .ws-title { color: #FFFFFF; font-size: 1.1rem; font-weight: 800; display: flex; align-items: center; gap: 10px; }
        .ws-close-btn { background: none; border: none; color: #94A3B8; font-size: 1.4rem; cursor: pointer; }

        /* Dual Nodes Topology Layout */
        .ws-body { flex: 1; display: flex; overflow: hidden; position: relative; }
        
        /* Left Core Node */
        .ws-left-pane {
            width: 38%; border-right: 1px solid #1E293B; background: #080D18;
            padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center;
            text-align: center; position: relative;
        }
        .core-orb-large {
            width: 130px; height: 130px; border-radius: 50%;
            background: radial-gradient(circle, #00E5FF 0%, rgba(0, 119, 254, 0.4) 60%, transparent 80%);
            box-shadow: 0 0 45px rgba(0, 229, 255, 0.6);
            border: 3px solid #00E5FF;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            animation: pulseOrb 2.5s infinite ease-in-out;
        }
        @keyframes pulseOrb { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
        .core-orb-text { color: #FFFFFF; font-weight: 800; font-size: 1.1rem; text-shadow: 0 0 10px #000; }
        .core-orb-sub { font-size: 0.65rem; color: #020617; font-weight: 700; background: #00E5FF; padding: 2px 8px; border-radius: 10px; margin-top: 4px; }

        /* Right 5 Sub-Agents Nodes */
        .ws-right-pane {
            flex: 1; overflow-y: auto; padding: 18px; display: flex; flex-direction: column; gap: 12px;
            background: #070B12;
        }
        .agent-card {
            background: #0E1626; border-radius: 14px; padding: 14px;
            border: 1px solid rgba(255,255,255,0.08); cursor: pointer; transition: all 0.25s;
            position: relative; overflow: hidden;
        }
        .agent-card:hover, .agent-card.active { transform: translateX(4px); }
        .agent-card.research { border-left: 4px solid var(--accent-cyan); }
        .agent-card.memory { border-left: 4px solid var(--accent-green); }
        .agent-card.preview { border-left: 4px solid var(--accent-amber); }
        .agent-card.automation { border-left: 4px solid var(--accent-purple); }
        .agent-card.coding { border-left: 4px solid var(--accent-pink); }

        .agent-card-header { display: flex; align-items: center; justify-content: space-between; }
        .agent-name-row { display: flex; align-items: center; gap: 10px; }
        .agent-icon-box {
            width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center;
            font-size: 0.95rem; font-weight: 700;
        }
        .research .agent-icon-box { background: rgba(0,229,255,0.15); color: var(--accent-cyan); }
        .memory .agent-icon-box { background: rgba(16,185,129,0.15); color: var(--accent-green); }
        .preview .agent-icon-box { background: rgba(245,158,11,0.15); color: var(--accent-amber); }
        .automation .agent-icon-box { background: rgba(139,92,246,0.15); color: var(--accent-purple); }
        .coding .agent-icon-box { background: rgba(236,72,153,0.15); color: var(--accent-pink); }

        .agent-title { color: #FFFFFF; font-size: 0.92rem; font-weight: 700; }
        .agent-desc { color: #94A3B8; font-size: 0.75rem; margin-top: 4px; }
        
        .agent-action-box {
            margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.06);
            display: flex; gap: 8px;
        }
        .agent-action-box input {
            flex: 1; background: #070B12; border: 1px solid rgba(255,255,255,0.15);
            padding: 8px 12px; border-radius: 8px; color: #FFFFFF; font-size: 0.8rem; outline: none;
        }
        .agent-run-btn {
            background: #1E293B; border: 1px solid rgba(255,255,255,0.2); color: #FFFFFF;
            padding: 8px 14px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; cursor: pointer;
        }
        .agent-result-box {
            margin-top: 8px; background: #070B12; border-radius: 8px; padding: 10px;
            font-size: 0.78rem; color: #CBD5E1; max-height: 140px; overflow-y: auto; white-space: pre-wrap;
            border: 1px solid rgba(255,255,255,0.05); display: none;
        }

        /* Generic Modal (Settings, Notes, Integrations) */
        .generic-modal {
            position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
            z-index: 70; display: none; align-items: center; justify-content: center; padding: 16px;
        }
        .generic-modal.active { display: flex; }
        .modal-card {
            background: #FFFFFF; width: 100%; max-width: 480px; border-radius: 20px;
            max-height: 85vh; display: flex; flex-direction: column; overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        .modal-header {
            padding: 16px 20px; border-bottom: 1px solid var(--border-color);
            display: flex; align-items: center; justify-content: space-between;
        }
        .modal-header h3 { font-size: 1.1rem; font-weight: 800; color: #0F172A; }
        .modal-body { padding: 20px; overflow-y: auto; flex: 1; display: flex; flex-direction: column; gap: 14px; }
        .modal-footer {
            padding: 14px 20px; border-top: 1px solid var(--border-color); background: #F8FAFC;
            display: flex; justify-content: flex-end; gap: 10px;
        }
        .form-group { display: flex; flex-direction: column; gap: 6px; }
        .form-group label { font-size: 0.8rem; font-weight: 700; color: #475569; }
        .form-group input, .form-group select {
            background: #F8FAFC; border: 1px solid var(--border-color);
            padding: 10px 14px; border-radius: 10px; font-size: 0.9rem; color: #0F172A; outline: none;
        }
        .btn-primary {
            background: #1E3A8A; color: #FFFFFF; border: none; padding: 10px 20px;
            border-radius: 10px; font-size: 0.9rem; font-weight: 700; cursor: pointer;
        }
        .btn-secondary {
            background: #E2E8F0; color: #334155; border: none; padding: 10px 16px;
            border-radius: 10px; font-size: 0.9rem; font-weight: 600; cursor: pointer;
        }
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="header-left">
            <button class="menu-btn" onclick="toggleDrawer(true)" aria-label="Menu">
                <i class="fa-solid fa-bars"></i>
            </button>
            <div class="logo-box">
                <i class="fa-solid fa-atom" style="color: var(--accent-blue);"></i>
                RB<span>.AGENT</span>
            </div>
        </div>
        <div class="badge" id="connBadge">
            <i class="fa-solid fa-circle" style="font-size: 0.5rem; margin-right: 4px;"></i> LIVE
        </div>
    </header>

    <!-- Dynamic Greeting Card -->
    <div class="greeting-card">
        <div class="greeting-title" id="greetingBanner">
            नमस्ते, Ram Binay kumar Pandit
        </div>
        <div class="greeting-subtitle">आज आपका क्या प्लान है? RB Agent is online.</div>
        <div class="floating-status-pill">
            <div class="status-dot"></div>
            <span id="floatingStatusText">Battery: 85% • Hey RB Wake Active</span>
        </div>
    </div>

    <!-- Central Arc Reactor HUD Button -->
    <div class="hud-stage">
        <div class="reactor-container" onclick="openAgentsWorkspace()" title="Open 5 Sub-Agents Workspace">
            <div class="reactor-outer-ring"></div>
            <div class="reactor-mid-ring"></div>
            <div class="reactor-core">
                <i class="fa-solid fa-bolt" style="color: #00E5FF; font-size: 1.1rem; margin-bottom: 2px;"></i>
                <div class="core-title">RB Agent</div>
                <div class="core-sub">tap to open agents</div>
            </div>
        </div>
    </div>

    <!-- Quick Action Chips -->
    <div class="actions-scroll">
        <button class="action-chip" onclick="triggerHardware('torch')"><i class="fa-solid fa-lightbulb"></i> Torch Toggle</button>
        <button class="action-chip" onclick="triggerHardware('battery')"><i class="fa-solid fa-battery-half"></i> Battery Status</button>
        <button class="action-chip" onclick="triggerHardware('vibrate')"><i class="fa-solid fa-mobile-screen"></i> Haptic Vibrate</button>
        <button class="action-chip" onclick="triggerCallAnnouncement()"><i class="fa-solid fa-phone"></i> Call Announce</button>
        <button class="action-chip" onclick="openNotesModal()"><i class="fa-solid fa-note-sticky"></i> Persistent Notes</button>
    </div>

    <!-- Chat Messages View -->
    <div class="chat-container" id="chatArea">
        <div class="message-bubble assistant">
            <div class="agent-tag tag-automation">RB System</div>
            नमस्ते Ram Binay! I am RB Agent, your autonomous on-device operating system agent. All 5 Sub-Agents, persistent storage, and hardware bridges are active.
        </div>
    </div>

    <!-- Subtitles / Live Captions Bar -->
    <div class="subtitles-bar">
        <i class="fa-solid fa-closed-captioning"></i>
        <div class="subtitles-text" id="subtitlesText">Agent idle • Turn-taking ready</div>
        <button onclick="toggleTtsPause()" style="background:none;border:none;color:#38BDF8;cursor:pointer;"><i id="pauseIcon" class="fa-solid fa-pause"></i></button>
    </div>

    <!-- Input Bar -->
    <div class="input-bar">
        <button class="icon-btn" onclick="captureCameraPhoto()" title="Camera"><i class="fa-solid fa-camera"></i></button>
        <input type="text" id="userInput" placeholder="Ask RB Agent, run command, or say 'यह चीज़ सेव कर लो'..." onkeypress="handleEnter(event)">
        <button class="icon-btn mic-btn" id="micBtn" onclick="toggleVoice()" title="Microphone"><i class="fa-solid fa-microphone"></i></button>
        <button class="icon-btn" onclick="sendMessage()" title="Send"><i class="fa-solid fa-paper-plane"></i></button>
    </div>

    <!-- Sidebar Navigation Drawer -->
    <div class="drawer-overlay" id="drawerOverlay" onclick="toggleDrawer(false)"></div>
    <div class="drawer" id="mainDrawer">
        <div class="drawer-header">
            <div class="user-avatar-row">
                <div class="avatar-circle" id="userAvatar">RB</div>
                <div>
                    <div class="user-info-name" id="drawerUserName">Ram Binay kumar Pandit</div>
                    <div class="user-info-role">Master User • Autonomous OS</div>
                </div>
            </div>
        </div>
        <div class="drawer-nav">
            <div class="nav-item active" onclick="toggleDrawer(false)"><i class="fa-solid fa-house"></i> Home</div>
            <div class="nav-item" onclick="openAgentsWorkspace(); toggleDrawer(false);"><i class="fa-solid fa-network-wired"></i> 5 Sub-Agents Workspace</div>
            <div class="nav-item" onclick="openNotesModal(); toggleDrawer(false);"><i class="fa-solid fa-database"></i> Persistent Storage & Notes</div>
            <div class="nav-item" onclick="openGitHubModal(); toggleDrawer(false);"><i class="fa-brands fa-github"></i> Coding & GitHub Sync</div>
            <div class="nav-item" onclick="openTelegramModal(); toggleDrawer(false);"><i class="fa-brands fa-telegram"></i> Telegram Webhook Bot</div>
            <div class="nav-item" onclick="openWhatsAppModal(); toggleDrawer(false);"><i class="fa-brands fa-whatsapp"></i> WhatsApp Automation</div>
            <div class="nav-item" onclick="openSettingsModal(); toggleDrawer(false);"><i class="fa-solid fa-gear"></i> Settings & Voice Profiles</div>
        </div>
    </div>

    <!-- Fullscreen Dark 5 Sub-Agents Workspace Modal -->
    <div class="workspace-modal" id="workspaceModal">
        <div class="ws-header">
            <div class="ws-title">
                <i class="fa-solid fa-network-wired" style="color: #00E5FF;"></i>
                5 SUB-AGENTS ORCHESTRATION WORKSPACE
            </div>
            <button class="ws-close-btn" onclick="closeAgentsWorkspace()"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="ws-body">
            <!-- Left Core Node -->
            <div class="ws-left-pane">
                <div class="core-orb-large">
                    <div class="core-orb-text">RB AGENT</div>
                    <div class="core-orb-sub">ORCHESTRATOR</div>
                </div>
                <div style="color: #94A3B8; font-size: 0.78rem; margin-top: 18px; line-height: 1.4;">
                    Connected to 5 Autonomous Hardware & Network Sub-Nodes
                </div>
            </div>

            <!-- Right 5 Sub-Agents Nodes -->
            <div class="ws-right-pane">
                <!-- 1. Research & Web Agent -->
                <div class="agent-card research">
                    <div class="agent-card-header">
                        <div class="agent-name-row">
                            <div class="agent-icon-box"><i class="fa-solid fa-globe"></i></div>
                            <div>
                                <div class="agent-title">1. Research & Web Agent</div>
                                <div class="agent-desc">Real-time web search API for live data & Gemini models</div>
                            </div>
                        </div>
                    </div>
                    <div class="agent-action-box">
                        <input type="text" id="researchInput" placeholder="Query: e.g. new Google Gemini 2.5 flash models">
                        <button class="agent-run-btn" onclick="runSubAgent('research')">Search</button>
                    </div>
                    <div class="agent-result-box" id="res_research"></div>
                </div>

                <!-- 2. Memory & Notes Agent -->
                <div class="agent-card memory">
                    <div class="agent-card-header">
                        <div class="agent-name-row">
                            <div class="agent-icon-box"><i class="fa-solid fa-brain"></i></div>
                            <div>
                                <div class="agent-title">2. Memory & Notes Agent</div>
                                <div class="agent-desc">NLP parsing for 'यह चीज़ सेव कर लो' & SQLite persistence</div>
                            </div>
                        </div>
                    </div>
                    <div class="agent-action-box">
                        <input type="text" id="memoryInput" placeholder="Text: e.g. यह चीज़ सेव कर लो: Meeting at 5pm with dev team">
                        <button class="agent-run-btn" onclick="runSubAgent('memory')">Save / Parse</button>
                    </div>
                    <div class="agent-result-box" id="res_memory"></div>
                </div>

                <!-- 3. Preview / View Agent -->
                <div class="agent-card preview">
                    <div class="agent-card-header">
                        <div class="agent-name-row">
                            <div class="agent-icon-box"><i class="fa-solid fa-eye"></i></div>
                            <div>
                                <div class="agent-title">3. Preview / View Agent</div>
                                <div class="agent-desc">Live web URL scraper & Markdown rendering engine</div>
                            </div>
                        </div>
                    </div>
                    <div class="agent-action-box">
                        <input type="text" id="previewInput" placeholder="URL: e.g. https://github.com/flutter/flutter">
                        <button class="agent-run-btn" onclick="runSubAgent('preview')">Inspect Preview</button>
                    </div>
                    <div class="agent-result-box" id="res_preview"></div>
                </div>

                <!-- 4. Automation Agent -->
                <div class="agent-card automation">
                    <div class="agent-card-header">
                        <div class="agent-name-row">
                            <div class="agent-icon-box"><i class="fa-solid fa-microchip"></i></div>
                            <div>
                                <div class="agent-title">4. Automation Agent</div>
                                <div class="agent-desc">Platform channels, phone hardware & Call Announcements</div>
                            </div>
                        </div>
                    </div>
                    <div class="agent-action-box">
                        <input type="text" id="automationCallerInput" placeholder="Caller Name: e.g. Ankit Sharma">
                        <button class="agent-run-btn" onclick="triggerCallAnnouncementFromWorkspace()">Announce Call</button>
                    </div>
                    <div class="agent-result-box" id="res_automation"></div>
                </div>

                <!-- 5. Coding & GitHub Agent -->
                <div class="agent-card coding">
                    <div class="agent-card-header">
                        <div class="agent-name-row">
                            <div class="agent-icon-box"><i class="fa-brands fa-github"></i></div>
                            <div>
                                <div class="agent-title">5. Coding & GitHub Agent</div>
                                <div class="agent-desc">Termux script execution & GitHub REST API repo sync</div>
                            </div>
                        </div>
                    </div>
                    <div class="agent-action-box">
                        <input type="text" id="codingInput" placeholder="GitHub username: e.g. torvalds or your username">
                        <button class="agent-run-btn" onclick="runSubAgent('coding')">Fetch Repos</button>
                    </div>
                    <div class="agent-result-box" id="res_coding"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Notes & Persistent Storage Modal -->
    <div class="generic-modal" id="notesModal">
        <div class="modal-card">
            <div class="modal-header">
                <h3><i class="fa-solid fa-database" style="color: #10B981;"></i> Persistent Notes & Memory</h3>
                <button onclick="closeModal('notesModal')" style="background:none;border:none;font-size:1.2rem;cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>Add New Note (Persists in SQLite)</label>
                    <input type="text" id="newNoteTitle" placeholder="Note Title">
                    <input type="text" id="newNoteContent" placeholder="Note Content / Details" style="margin-top:6px;">
                    <button class="btn-primary" style="margin-top:6px;" onclick="saveNewNote()">Save to Database</button>
                </div>
                <div style="font-weight:700;font-size:0.85rem;color:#475569;margin-top:10px;">Stored Records</div>
                <div id="notesListContainer" style="display:flex;flex-direction:column;gap:8px;max-height:240px;overflow-y:auto;">
                    Loading notes...
                </div>
            </div>
        </div>
    </div>

    <!-- Settings & Voice Profiles Modal -->
    <div class="generic-modal" id="settingsModal">
        <div class="modal-card">
            <div class="modal-header">
                <h3><i class="fa-solid fa-gear" style="color: #0077FE;"></i> Advanced Settings</h3>
                <button onclick="closeModal('settingsModal')" style="background:none;border:none;font-size:1.2rem;cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>Dynamic User Name</label>
                    <input type="text" id="settingUserName" value="Ram Binay kumar Pandit">
                </div>
                <div class="form-group">
                    <label>Voice Accent / Language</label>
                    <select id="settingVoiceAccent">
                        <option value="hi-IN">Hindi (India) - hi-IN</option>
                        <option value="en-IN">English (India) - en-IN</option>
                        <option value="en-US">English (US) - en-US</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Speech Pitch (0.5 to 1.5)</label>
                    <input type="number" id="settingVoicePitch" step="0.1" value="1.0" min="0.5" max="1.5">
                </div>
                <div class="form-group">
                    <label>Speech Rate (0.5 to 1.5)</label>
                    <input type="number" id="settingVoiceRate" step="0.1" value="0.9" min="0.5" max="1.5">
                </div>
                <div class="form-group">
                    <label>Google Gemini API Key</label>
                    <input type="password" id="settingGeminiApiKey" placeholder="AIzaSy...">
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-secondary" onclick="closeModal('settingsModal')">Cancel</button>
                <button class="btn-primary" onclick="saveAllSettings()"><i class="fa-solid fa-floppy-disk"></i> Save Configuration</button>
            </div>
        </div>
    </div>

    <!-- Telegram Bot Modal -->
    <div class="generic-modal" id="telegramModal">
        <div class="modal-card">
            <div class="modal-header">
                <h3><i class="fa-brands fa-telegram" style="color: #0088cc;"></i> Telegram Bot Integration</h3>
                <button onclick="closeModal('telegramModal')" style="background:none;border:none;font-size:1.2rem;cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>Telegram Bot Token (from @BotFather)</label>
                    <input type="text" id="telegramTokenInput" placeholder="123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ">
                </div>
                <div style="display:flex;gap:10px;">
                    <button class="btn-primary" style="flex:1;" onclick="startTelegramBot()"><i class="fa-solid fa-play"></i> Start Bot Runner</button>
                    <button class="btn-secondary" onclick="stopTelegramBot()">Stop</button>
                </div>
                <div id="telegramStatusBox" style="background:#F1F5F9;padding:10px;border-radius:8px;font-size:0.8rem;color:#334155;">
                    Checking Telegram status...
                </div>
            </div>
        </div>
    </div>

    <!-- WhatsApp Modal -->
    <div class="generic-modal" id="whatsappModal">
        <div class="modal-card">
            <div class="modal-header">
                <h3><i class="fa-brands fa-whatsapp" style="color: #25D366;"></i> WhatsApp Automation</h3>
                <button onclick="closeModal('whatsappModal')" style="background:none;border:none;font-size:1.2rem;cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>Phone Number (with Country Code, e.g. 919876543210)</label>
                    <input type="text" id="waPhone" placeholder="91XXXXXXXXXX">
                </div>
                <div class="form-group">
                    <label>Message Content</label>
                    <input type="text" id="waMsg" placeholder="Hello from RB Agent!">
                </div>
                <button class="btn-primary" onclick="sendWhatsApp()"><i class="fa-brands fa-whatsapp"></i> Launch WhatsApp Message</button>
            </div>
        </div>
    </div>

    <!-- GitHub Repos Modal -->
    <div class="generic-modal" id="githubModal">
        <div class="modal-card">
            <div class="modal-header">
                <h3><i class="fa-brands fa-github"></i> GitHub Repositories Sync</h3>
                <button onclick="closeModal('githubModal')" style="background:none;border:none;font-size:1.2rem;cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>GitHub Username or Personal Token</label>
                    <input type="text" id="ghInput" placeholder="GitHub username">
                    <button class="btn-primary" style="margin-top:6px;" onclick="fetchGitHubReposModal()">Sync Repositories</button>
                </div>
                <div id="ghReposList" style="display:flex;flex-direction:column;gap:8px;max-height:240px;overflow-y:auto;">
                    Enter username to fetch repositories.
                </div>
            </div>
        </div>
    </div>

    <script>
        // State
        let currentUser = "Ram Binay kumar Pandit";
        let isSpeaking = false;
        let isVoiceListening = false;
        let recognition = null;
        let ttsPaused = false;

        // Auto Greeting on launch
        window.addEventListener('DOMContentLoaded', () => {
            loadInitialStatus();
            initSpeechRecognition();
        });

        async function loadInitialStatus() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                if (data.user_name) {
                    currentUser = data.user_name;
                    updateUserUI(data.user_name, data.greeting);
                }
                if (data.device && data.device.battery) {
                    const b = data.device.battery;
                    document.getElementById('floatingStatusText').innerText = 
                        `Battery: ${b.percentage || '85'}% • Hey RB Wake Active`;
                }
            } catch (e) {
                console.log("Status fetch:", e);
            }
        }

        function updateUserUI(name, greeting) {
            document.getElementById('greetingBanner').innerText = greeting || `नमस्ते, ${name} आज आपका क्या प्लान है`;
            document.getElementById('drawerUserName').innerText = name;
            document.getElementById('settingUserName').value = name;
            const initials = name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            document.getElementById('userAvatar').innerText = initials || 'RB';
        }

        // Drawer
        function toggleDrawer(open) {
            document.getElementById('drawerOverlay').classList.toggle('active', open);
            document.getElementById('mainDrawer').classList.toggle('active', open);
        }

        // Sub-Agents Workspace
        function openAgentsWorkspace() {
            document.getElementById('workspaceModal').classList.add('active');
        }
        function closeAgentsWorkspace() {
            document.getElementById('workspaceModal').classList.remove('active');
        }

        // Generic Modals
        function closeModal(id) {
            document.getElementById(id).classList.remove('active');
        }
        function openNotesModal() {
            document.getElementById('notesModal').classList.add('active');
            loadNotes();
        }
        function openSettingsModal() {
            document.getElementById('settingsModal').classList.add('active');
        }
        function openTelegramModal() {
            document.getElementById('telegramModal').classList.add('active');
            checkTelegramStatus();
        }
        function openWhatsAppModal() {
            document.getElementById('whatsappModal').classList.add('active');
        }
        function openGitHubModal() {
            document.getElementById('githubModal').classList.add('active');
        }

        // Sub-Agents Runner
        async function runSubAgent(agent) {
            let params = {};
            const resBox = document.getElementById(`res_${agent}`);
            resBox.style.display = 'block';
            resBox.innerText = 'Executing agent request...';

            if (agent === 'research') {
                const q = document.getElementById('researchInput').value.trim() || 'latest Google Gemini 2.5 flash models';
                params = { query: q };
            } else if (agent === 'memory') {
                const t = document.getElementById('memoryInput').value.trim() || 'यह चीज़ सेव कर लो: Buy groceries and test RB Agent';
                params = { text: t };
            } else if (agent === 'preview') {
                const url = document.getElementById('previewInput').value.trim() || 'https://google.com';
                params = { target: url };
            } else if (agent === 'coding') {
                const u = document.getElementById('codingInput').value.trim() || 'torvalds';
                params = { username: u };
                const res = await fetch(`/api/github?username=${encodeURIComponent(u)}`);
                const data = await res.json();
                resBox.innerText = JSON.stringify(data, null, 2);
                return;
            }

            try {
                const resp = await fetch('/api/agents', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ agent, action: 'run', params })
                });
                const data = await resp.json();
                resBox.innerText = JSON.stringify(data.result, null, 2);
            } catch (e) {
                resBox.innerText = 'Error: ' + e.message;
            }
        }

        function triggerCallAnnouncementFromWorkspace() {
            const caller = document.getElementById('automationCallerInput').value.trim() || 'Ram Pandit';
            triggerCallAnnouncement(caller);
            document.getElementById('res_automation').style.display = 'block';
            document.getElementById('res_automation').innerText = `Announced incoming call for '${caller}' in Hindi and English.`;
        }

        // Hardware actions
        async function triggerHardware(action) {
            try {
                const res = await fetch('/api/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ action })
                });
                const data = await res.json();
                appendMessage('assistant', `Executed hardware action [${action}]: ${JSON.stringify(data.result)}`, 'tag-automation');
            } catch (e) {
                console.error(e);
            }
        }

        // Call Announcement
        async function triggerCallAnnouncement(caller = 'Ankit Sharma') {
            try {
                const res = await fetch('/api/call_announcement', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ caller_name: caller, phone: '+91-9876543210' })
                });
                const data = await res.json();
                appendMessage('assistant', `📞 Call Announcement Triggered: "${currentUser}, ${caller} का फोन आया है"`, 'tag-automation');
                speakText(`${currentUser}, ${caller} का फोन आया है`);
            } catch (e) {
                console.error(e);
            }
        }

        // Chat & Strict Turn-Taking
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            if (!text) return;

            appendMessage('user', text);
            input.value = '';
            updateSubtitles(`User: "${text}"`);

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ text, is_voice: isVoiceListening })
                });
                const data = await res.json();
                const reply = data.response || "Task completed.";
                const agentTag = data.agent ? 'tag-memory' : 'tag-automation';
                appendMessage('assistant', reply, agentTag);
                
                // Speak and enter strict turn-taking listening state
                speakText(reply, () => {
                    // Turn-taking rule: agent remains completely silent and listens
                    updateSubtitles("Agent finished speaking. Strict listening mode active.");
                    if (!isVoiceListening) {
                        toggleVoice(true);
                    }
                });
            } catch (e) {
                appendMessage('assistant', 'Error communicating with RB Agent: ' + e.message);
            }
        }

        function handleEnter(e) {
            if (e.key === 'Enter') sendMessage();
        }

        function appendMessage(sender, text, tagClass = 'tag-automation') {
            const chat = document.getElementById('chatArea');
            const div = document.createElement('div');
            div.className = `message-bubble ${sender}`;
            if (sender === 'assistant') {
                div.innerHTML = `<div class="agent-tag ${tagClass}">RB Agent</div><div>${text}</div>`;
            } else {
                div.innerText = text;
            }
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        // Voice TTS with Pause/Resume and Subtitles
        function speakText(text, onComplete) {
            if (!('speechSynthesis' in window)) {
                if (onComplete) onComplete();
                return;
            }
            window.speechSynthesis.cancel();
            
            // Clean text for speech
            const clean = text.replace(/[*#`_\[\]]/g, '');
            const utter = new SpeechSynthesisUtterance(clean);
            utter.lang = document.getElementById('settingVoiceAccent').value || 'hi-IN';
            utter.pitch = parseFloat(document.getElementById('settingVoicePitch').value) || 1.0;
            utter.rate = parseFloat(document.getElementById('settingVoiceRate').value) || 0.95;

            utter.onstart = () => {
                isSpeaking = true;
                updateSubtitles(`RB Agent speaking: "${clean.substring(0, 50)}..."`);
            };
            utter.onend = () => {
                isSpeaking = false;
                if (onComplete) onComplete();
            };
            window.speechSynthesis.speak(utter);
        }

        function toggleTtsPause() {
            if (!('speechSynthesis' in window)) return;
            if (window.speechSynthesis.speaking) {
                if (window.speechSynthesis.paused) {
                    window.speechSynthesis.resume();
                    document.getElementById('pauseIcon').className = 'fa-solid fa-pause';
                } else {
                    window.speechSynthesis.pause();
                    document.getElementById('pauseIcon').className = 'fa-solid fa-play';
                }
            }
        }

        function updateSubtitles(text) {
            document.getElementById('subtitlesText').innerText = text;
        }

        // Speech-to-Text with "Hey RB" Wake-Phrase
        function initSpeechRecognition() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechRecognition) {
                recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'hi-IN';

                recognition.onresult = (event) => {
                    let transcript = '';
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        transcript += event.results[i][0].transcript;
                    }
                    updateSubtitles(`Listening: "${transcript}"`);
                    
                    const lower = transcript.toLowerCase();
                    // Wake-Phrase Detection
                    if (lower.includes("hey rb") || lower.includes("हे आरबी")) {
                        const stripped = transcript.replace(/hey rb|हे आरबी/gi, '').trim();
                        document.getElementById('userInput').value = stripped;
                        if (stripped.length > 2) {
                            sendMessage();
                        }
                    }
                };
            }
        }

        function toggleVoice(forceState) {
            const btn = document.getElementById('micBtn');
            isVoiceListening = forceState !== undefined ? forceState : !isVoiceListening;
            
            if (isVoiceListening) {
                btn.classList.add('active');
                if (recognition) {
                    try { recognition.start(); } catch(e){}
                }
                updateSubtitles("Microphone active • Listening for speech or 'Hey RB'...");
            } else {
                btn.classList.remove('active');
                if (recognition) {
                    try { recognition.stop(); } catch(e){}
                }
                updateSubtitles("Microphone paused.");
            }
        }

        // Persistent Notes CRUD
        async function loadNotes() {
            const c = document.getElementById('notesListContainer');
            c.innerHTML = 'Loading...';
            try {
                const res = await fetch('/api/notes');
                const data = await res.json();
                if (data.notes && data.notes.length > 0) {
                    c.innerHTML = data.notes.map(n => `
                        <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:10px;">
                            <div style="font-weight:700;color:#0F172A;font-size:0.85rem;">${n.title}</div>
                            <div style="color:#64748B;font-size:0.8rem;margin-top:2px;">${n.content}</div>
                            <div style="font-size:0.65rem;color:#94A3B8;margin-top:4px;">${n.created_at}</div>
                        </div>
                    `).join('');
                } else {
                    c.innerHTML = '<div style="color:#94A3B8;font-size:0.85rem;">No notes saved yet. Say "यह चीज़ सेव कर लो" to add!</div>';
                }
            } catch (e) {
                c.innerHTML = 'Error loading notes';
            }
        }

        async function saveNewNote() {
            const t = document.getElementById('newNoteTitle').value.trim();
            const content = document.getElementById('newNoteContent').value.trim();
            if (!t || !content) return;

            await fetch('/api/notes', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ title: t, content })
            });
            document.getElementById('newNoteTitle').value = '';
            document.getElementById('newNoteContent').value = '';
            loadNotes();
        }

        // Settings Save
        async function saveAllSettings() {
            const newName = document.getElementById('settingUserName').value.trim();
            const accent = document.getElementById('settingVoiceAccent').value;
            const pitch = document.getElementById('settingVoicePitch').value;
            const rate = document.getElementById('settingVoiceRate').value;
            const apiKey = document.getElementById('settingGeminiApiKey').value.trim();

            if (newName) {
                currentUser = newName;
                await fetch('/api/user', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ user_name: newName })
                });
                updateUserUI(newName);
            }

            await fetch('/api/settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    voice_accent: accent,
                    voice_pitch: pitch,
                    voice_rate: rate
                })
            });

            if (apiKey) {
                await fetch('/api/config', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ gemini_api_key: apiKey })
                });
            }

            closeModal('settingsModal');
            appendMessage('assistant', `Configuration saved successfully for ${currentUser}.`);
        }

        // Telegram Bot
        async function checkTelegramStatus() {
            const box = document.getElementById('telegramStatusBox');
            try {
                const res = await fetch('/api/telegram');
                const data = await res.json();
                box.innerText = `Status: ${data.is_running ? '🟢 RUNNING' : '⚪ STOPPED'} | Token Set: ${data.has_token}`;
            } catch(e) {
                box.innerText = 'Unable to check status';
            }
        }

        async function startTelegramBot() {
            const token = document.getElementById('telegramTokenInput').value.trim();
            const res = await fetch('/api/telegram', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: 'start', token })
            });
            const data = await res.json();
            alert(data.message || data.error);
            checkTelegramStatus();
        }

        async function stopTelegramBot() {
            await fetch('/api/telegram', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: 'stop' })
            });
            checkTelegramStatus();
        }

        // WhatsApp
        async function sendWhatsApp() {
            const phone = document.getElementById('waPhone').value.trim();
            const msg = document.getElementById('waMsg').value.trim();
            if (!phone || !msg) return alert('Phone and message required');

            const res = await fetch('/api/whatsapp', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ phone, message: msg })
            });
            const data = await res.json();
            if (data.url) {
                window.open(data.url, '_blank');
            }
            closeModal('whatsappModal');
        }

        // GitHub Repos
        async function fetchGitHubReposModal() {
            const u = document.getElementById('ghInput').value.trim();
            const list = document.getElementById('ghReposList');
            list.innerHTML = 'Fetching repositories...';
            try {
                const res = await fetch(`/api/github?username=${encodeURIComponent(u)}`);
                const data = await res.json();
                if (data.repositories) {
                    list.innerHTML = data.repositories.map(r => `
                        <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:8px;">
                            <a href="${r.html_url}" target="_blank" style="color:#0077FE;font-weight:700;text-decoration:none;">${r.name}</a>
                            <div style="font-size:0.75rem;color:#64748B;">${r.description}</div>
                            <div style="font-size:0.7rem;color:#94A3B8;margin-top:2px;">⭐ ${r.stars} | 🍴 ${r.forks} | ${r.language}</div>
                        </div>
                    `).join('');
                } else {
                    list.innerText = data.error || 'No repos found';
                }
            } catch(e) {
                list.innerText = 'Failed to fetch repos';
            }
        }
    </script>
</body>
</html>
"""
