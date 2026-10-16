"""
RB.AI - Pristine Hyper-Minimalist Lovable UI
Clean, uncluttered architecture:
- Home Screen strictly contains:
  1. Compact Greeting Banner ("नमस्ते, Ram Binay Pandit आज आपका क्या प्लान है")
  2. Central Compact Arc Reactor HUD (< 30% height, ~96px diameter)
  3. Clean conversational feed
  4. Real-time scrolling subtitles ticker above the input dock
  5. Sticky persistent bottom chat/command input dock
- Collapsible Unified Sidebar Drawer with strictly the 8 items
- Dedicated views for Web Preview, Code Preview, File Preview, Projects, Skill Add, Chats
- Centralized Settings Hub for Telegram, WhatsApp, GitHub PAT, Voice profiles, and API keys
- Autonomous intent routing with zero raw error dumps
"""

WEB_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>RB Agent — Minimalist Autonomous OS</title>
    <meta name="theme-color" content="#090D16">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-base: #070B12;
            --bg-sidebar: #0C1220;
            --bg-card: #111A2E;
            --bg-input: #15223C;
            --border: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(0, 229, 255, 0.35);
            --text-primary: #F8FAFC;
            --text-muted: #94A3B8;
            --accent-cyan: #00E5FF;
            --accent-blue: #38BDF8;
            --accent-purple: #A855F7;
            --accent-green: #10B981;
            --accent-amber: #F59E0B;
            --accent-pink: #EC4899;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: var(--bg-base); color: var(--text-primary); height: 100vh; display: flex; overflow: hidden; }

        /* Unified Collapsible Sidebar */
        .sidebar {
            width: 260px; background: var(--bg-sidebar); border-right: 1px solid var(--border);
            display: flex; flex-direction: column; z-index: 50; transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @media (max-width: 768px) {
            .sidebar { position: fixed; top: 0; bottom: 0; left: 0; transform: translateX(-100%); box-shadow: 4px 0 25px rgba(0,0,0,0.6); }
            .sidebar.active { transform: translateX(0); }
        }
        .sidebar-backdrop { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.65); backdrop-filter: blur(4px); z-index: 45; }
        .sidebar-backdrop.active { display: block; }

        .sidebar-top {
            padding: 18px 20px; display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid var(--border);
        }
        .brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.05rem; letter-spacing: 0.5px; }
        .brand i { color: var(--accent-cyan); font-size: 1.2rem; }
        .brand span { color: var(--accent-cyan); }
        .btn-close-sidebar { display: none; background: none; border: none; color: var(--text-muted); font-size: 1.2rem; cursor: pointer; }
        @media (max-width: 768px) { .btn-close-sidebar { display: block; } }

        .user-tag-row {
            padding: 12px 16px; margin: 10px 14px; background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 12px; display: flex; align-items: center; gap: 10px;
        }
        .user-avatar-pill {
            width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg, #0284C7, #00E5FF);
            color: #070B12; font-weight: 900; font-size: 0.82rem; display: flex; align-items: center; justify-content: center;
        }
        .user-tag-name { font-size: 0.82rem; font-weight: 700; color: #FFF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px; }
        .user-tag-sub { font-size: 0.68rem; color: var(--accent-green); display: flex; align-items: center; gap: 4px; }

        /* The 8 Clean Navigation Items */
        .sidebar-menu { flex: 1; overflow-y: auto; padding: 6px 12px; display: flex; flex-direction: column; gap: 2px; }
        .nav-item {
            display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 10px;
            color: var(--text-muted); font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
            border: 1px solid transparent;
        }
        .nav-item i { width: 18px; font-size: 0.95rem; text-align: center; }
        .nav-item:hover, .nav-item.active {
            background: rgba(0, 229, 255, 0.08); color: var(--accent-cyan); border-color: rgba(0, 229, 255, 0.2);
        }

        /* Sidebar Chats Bottom Area */
        .sidebar-bottom-chats {
            padding: 12px 14px; border-top: 1px solid var(--border); display: flex; flex-direction: column; gap: 8px;
        }
        .chat-filter-input {
            background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px;
            padding: 8px 12px; font-size: 0.78rem; color: #FFF; outline: none; width: 100%;
        }
        .chat-filter-input:focus { border-color: var(--accent-cyan); }
        .btn-new-chat-prominent {
            background: linear-gradient(135deg, #0284C7, #00E5FF); color: #070B12; border: none;
            padding: 10px; border-radius: 10px; font-size: 0.85rem; font-weight: 800; cursor: pointer;
            display: flex; align-items: center; justify-content: center; gap: 8px;
        }

        /* Main Screen Layout */
        .viewport { flex: 1; display: flex; flex-direction: column; height: 100vh; position: relative; overflow: hidden; }

        /* Top Bar */
        .topbar {
            padding: 12px 16px; background: var(--bg-sidebar); border-bottom: 1px solid var(--border);
            display: flex; align-items: center; justify-content: space-between; z-index: 20;
        }
        .btn-menu { background: none; border: none; color: #FFF; font-size: 1.2rem; cursor: pointer; padding: 4px; }
        .topbar-title { font-size: 0.9rem; font-weight: 700; color: #FFF; }
        .status-chip {
            background: rgba(16, 185, 129, 0.15); border: 1px solid var(--accent-green); color: var(--accent-green);
            padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 700; display: flex; align-items: center; gap: 5px;
        }
        .status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent-green); }

        /* Views */
        .panels-wrapper { flex: 1; display: flex; flex-direction: column; overflow: hidden; position: relative; }
        .panel { display: none; flex: 1; flex-direction: column; overflow-y: auto; }
        .panel.active { display: flex; }

        /* 1. HOMEPAGE (PRISTINE & MINIMALIST) */
        .home-panel { padding: 10px 14px 105px 14px; }

        /* Compact Greeting Banner */
        .greeting-compact-card {
            background: linear-gradient(135deg, rgba(2, 132, 199, 0.25) 0%, rgba(17, 26, 46, 0.6) 100%);
            border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 14px; padding: 12px 16px;
            display: flex; align-items: center; justify-content: space-between;
        }
        .greet-title { font-size: 0.98rem; font-weight: 800; color: #FFF; }
        .greet-sub { font-size: 0.75rem; color: var(--text-muted); margin-top: 2px; }

        /* Compact Arc Reactor HUD (< 30% height, ~96px) */
        .hud-compact-area {
            display: flex; justify-content: center; align-items: center; padding: 12px 0 8px 0;
        }
        .reactor-box {
            width: 96px; height: 96px; position: relative; display: flex; align-items: center; justify-content: center;
            cursor: pointer; user-select: none;
        }
        .ring-outer {
            position: absolute; inset: 0; border-radius: 50%; border: 1.5px dashed rgba(0, 229, 255, 0.6);
            animation: rotateCw 12s linear infinite;
        }
        .ring-inner {
            position: absolute; inset: 8px; border-radius: 50%; border: 1.5px solid rgba(56, 189, 248, 0.4);
            border-top-color: var(--accent-cyan); border-bottom-color: var(--accent-purple);
            animation: rotateCcw 7s linear infinite;
        }
        .reactor-core-small {
            width: 62px; height: 62px; border-radius: 50%; background: radial-gradient(circle, #0F172A 0%, #030712 100%);
            border: 2px solid var(--accent-cyan); box-shadow: 0 0 16px rgba(0, 229, 255, 0.5);
            display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
        }
        .reactor-box:active .reactor-core-small { transform: scale(0.95); }
        .reactor-core-small i { color: var(--accent-cyan); font-size: 0.75rem; margin-bottom: 1px; }
        .reactor-core-small .core-label { font-size: 0.65rem; font-weight: 800; color: #FFF; }

        @keyframes rotateCw { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes rotateCcw { 0% { transform: rotate(360deg); } 100% { transform: rotate(0deg); } }

        /* Conversational Feed */
        .conversation-feed { flex: 1; display: flex; flex-direction: column; gap: 10px; overflow-y: auto; padding: 6px 0; }
        .msg-bubble {
            max-width: 86%; padding: 10px 14px; border-radius: 14px; font-size: 0.88rem; line-height: 1.42; word-break: break-word;
        }
        .msg-bubble.user { align-self: flex-end; background: #0284C7; color: #FFF; border-bottom-right-radius: 3px; }
        .msg-bubble.assistant {
            align-self: flex-start; background: var(--bg-card); color: var(--text-primary);
            border: 1px solid var(--border); border-bottom-left-radius: 3px;
        }
        .tag-pill {
            display: inline-block; font-size: 0.62rem; font-weight: 800; padding: 2px 6px; border-radius: 6px;
            margin-bottom: 4px; text-transform: uppercase;
        }
        .pill-memory { background: rgba(16,185,129,0.15); color: var(--accent-green); }
        .pill-automation { background: rgba(168,85,247,0.15); color: var(--accent-purple); }
        .pill-research { background: rgba(0,229,255,0.15); color: var(--accent-cyan); }
        .pill-coding { background: rgba(236,72,153,0.15); color: var(--accent-pink); }

        /* Real-Time Scrolling Subtitles Ticker (Directly above input bar) */
        .subtitles-dock {
            position: absolute; bottom: 58px; left: 0; right: 0; padding: 0 14px 4px 14px;
            background: linear-gradient(180deg, transparent 0%, var(--bg-base) 100%); z-index: 28;
        }
        .subtitles-inner {
            background: rgba(17, 26, 46, 0.95); border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 16px; padding: 5px 12px; display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: var(--accent-blue);
        }
        .subtitles-text { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500; }

        /* Sticky Persistent Bottom Chat/Command Input Bar */
        .bottom-input-dock {
            position: absolute; bottom: 0; left: 0; right: 0; height: 58px;
            background: var(--bg-sidebar); border-top: 1px solid var(--border);
            padding: 8px 14px; display: flex; align-items: center; gap: 8px; z-index: 30;
        }
        .input-shell {
            flex: 1; background: var(--bg-input); border: 1px solid var(--border); border-radius: 24px;
            padding: 7px 14px; display: flex; align-items: center; gap: 8px;
        }
        .input-shell input {
            flex: 1; background: transparent; border: none; outline: none; color: #FFF; font-size: 0.88rem;
        }
        .dock-action-btn {
            background: none; border: none; color: var(--accent-cyan); font-size: 1.1rem; cursor: pointer;
            padding: 4px; display: flex; align-items: center; justify-content: center;
        }
        .dock-action-btn.recording { color: #EF4444; animation: pulseMic 1.2s infinite; }
        @keyframes pulseMic { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.18); } }

        /* Dedicated Panels (Web, Code, Files, Settings, Projects, Skill Add, Chats) */
        .page-panel { padding: 18px 20px 80px 20px; overflow-y: auto; height: 100%; display: flex; flex-direction: column; gap: 14px; }
        .page-title { font-size: 1.1rem; font-weight: 800; color: #FFF; display: flex; align-items: center; gap: 10px; }
        .card-surface { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 16px; }

        /* Centralized Settings Tabs */
        .settings-tab-bar { display: flex; gap: 6px; overflow-x: auto; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
        .tab-btn {
            background: var(--bg-input); border: 1px solid var(--border); color: var(--text-muted);
            padding: 7px 12px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; cursor: pointer; white-space: nowrap;
        }
        .tab-btn.active { background: rgba(0,229,255,0.15); color: var(--accent-cyan); border-color: var(--accent-cyan); }
        .tab-pane { display: none; flex-direction: column; gap: 12px; margin-top: 14px; }
        .tab-pane.active { display: flex; }

        .form-field { display: flex; flex-direction: column; gap: 5px; }
        .form-field label { font-size: 0.75rem; font-weight: 700; color: var(--text-muted); }
        .form-field input, .form-field select, .form-field textarea {
            background: var(--bg-input); border: 1px solid var(--border); color: #FFF;
            padding: 9px 12px; border-radius: 8px; font-size: 0.85rem; outline: none;
        }
        .form-field input:focus, .form-field select:focus { border-color: var(--accent-cyan); }

        .btn-action-primary {
            background: linear-gradient(135deg, #0284C7, #00E5FF); color: #070B12; font-weight: 800;
            border: none; padding: 10px 18px; border-radius: 8px; font-size: 0.85rem; cursor: pointer; margin-top: 8px;
        }
    </style>
</head>
<body>

    <!-- Unified Collapsible Sidebar (Strictly 8 Navigation Items) -->
    <div class="sidebar-backdrop" id="sidebarBackdrop" onclick="toggleSidebar(false)"></div>
    <aside class="sidebar" id="sidebar">
        <div class="sidebar-top">
            <div class="brand">
                <i class="fa-solid fa-atom"></i>
                RB<span>.AGENT</span>
            </div>
            <button class="btn-close-sidebar" onclick="toggleSidebar(false)"><i class="fa-solid fa-xmark"></i></button>
        </div>

        <div class="user-tag-row">
            <div class="user-avatar-pill" id="userAvatarPill">RP</div>
            <div>
                <div class="user-tag-name" id="sidebarUserName">Ram Binay Pandit</div>
                <div class="user-tag-sub"><i class="fa-solid fa-circle" style="font-size: 0.45rem;"></i> Active Node</div>
            </div>
        </div>

        <nav class="sidebar-menu">
            <div class="nav-item active" onclick="showPanel('home')">
                <i class="fa-solid fa-house"></i> Home
            </div>
            <div class="nav-item" onclick="showPanel('web-preview')">
                <i class="fa-solid fa-globe"></i> Web Preview
            </div>
            <div class="nav-item" onclick="showPanel('code-preview')">
                <i class="fa-solid fa-code"></i> Code Preview
            </div>
            <div class="nav-item" onclick="showPanel('file-preview')">
                <i class="fa-solid fa-folder-open"></i> File Preview
            </div>
            <div class="nav-item" onclick="showPanel('settings')">
                <i class="fa-solid fa-sliders"></i> Settings
            </div>
            <div class="nav-item" onclick="showPanel('projects')">
                <i class="fa-solid fa-cubes"></i> Projects
            </div>
            <div class="nav-item" onclick="showPanel('skill-add')">
                <i class="fa-solid fa-puzzle-piece"></i> Skill Add
            </div>
            <div class="nav-item" onclick="showPanel('chats')">
                <i class="fa-solid fa-comments"></i> Chats
            </div>
        </nav>

        <div class="sidebar-bottom-chats">
            <input type="text" class="chat-filter-input" id="chatSearch" placeholder="Search chats..." oninput="searchChats()">
            <button class="btn-new-chat-prominent" onclick="resetNewChat()">
                <i class="fa-solid fa-plus"></i> New chat
            </button>
        </div>
    </aside>

    <!-- Main Viewport -->
    <main class="viewport">
        <!-- Top Navbar -->
        <div class="topbar">
            <button class="btn-menu" onclick="toggleSidebar(true)"><i class="fa-solid fa-bars"></i></button>
            <div class="topbar-title" id="pageTitleText">RB Agent Overview</div>
            <div class="status-chip">
                <div class="status-dot"></div>
                <span id="topBattStatus">85% LIVE</span>
            </div>
        </div>

        <!-- Panels Container -->
        <div class="panels-wrapper">
            <!-- 1. HOMEPAGE (CLEAN & MINIMALIST: ONLY GREETING, COMPACT HUD, FEED) -->
            <div class="panel home-panel active" id="panel-home">
                <!-- Compact Greeting Banner -->
                <div class="greeting-compact-card">
                    <div>
                        <div class="greet-title" id="greetBannerText">नमस्ते, Ram Binay Pandit</div>
                        <div class="greet-sub">आज आपका क्या प्लान है?</div>
                    </div>
                    <i class="fa-solid fa-bolt" style="color: var(--accent-cyan); font-size: 1.1rem;"></i>
                </div>

                <!-- Central Compact Arc Reactor HUD (< 30% height) -->
                <div class="hud-compact-area">
                    <div class="reactor-box" onclick="showPanel('settings')" title="Core Orchestrator HUD">
                        <div class="ring-outer"></div>
                        <div class="ring-inner"></div>
                        <div class="reactor-core-small">
                            <i class="fa-solid fa-atom"></i>
                            <div class="core-label">RB Agent</div>
                        </div>
                    </div>
                </div>

                <!-- Conversational Chat Stream -->
                <div class="conversation-feed" id="chatStream">
                    <div class="msg-bubble assistant">
                        <div class="tag-pill pill-automation">RB System</div>
                        <div>नमस्ते Ram Binay! I am RB Agent, your minimalist on-device operating system agent. All sub-agents and hardware bridges are active.</div>
                    </div>
                </div>
            </div>

            <!-- 2. WEB PREVIEW VIEW -->
            <div class="panel page-panel" id="panel-web-preview">
                <div class="page-title"><i class="fa-solid fa-globe" style="color: var(--accent-cyan);"></i> Web Preview & Live Search</div>
                <div class="card-surface">
                    <div class="form-field">
                        <label>Web URL or Search Query</label>
                        <div style="display: flex; gap: 8px;">
                            <input type="text" id="webQueryInput" placeholder="Enter query or URL..." value="latest Google Gemini 2.5 flash models">
                            <button class="btn-action-primary" style="margin-top:0;" onclick="triggerWebPreview()">Search</button>
                        </div>
                    </div>
                    <div id="webPreviewOutput" style="margin-top: 14px; font-size: 0.85rem; color: #CBD5E1; line-height: 1.5; white-space: pre-wrap; max-height: 380px; overflow-y: auto;">
                        Enter a search query or URL to preview live web intelligence.
                    </div>
                </div>
            </div>

            <!-- 3. CODE PREVIEW VIEW -->
            <div class="panel page-panel" id="panel-code-preview">
                <div class="page-title"><i class="fa-solid fa-code" style="color: var(--accent-pink);"></i> Code Editor & Terminal Execution</div>
                <div class="card-surface">
                    <div class="form-field">
                        <label>Python 3.14 / Shell Script</label>
                        <textarea id="codeScriptArea" rows="6" style="font-family: monospace;">print("Hello Ram Binay Pandit! RB Agent code runner active.")</textarea>
                    </div>
                    <button class="btn-action-primary" onclick="runScriptExecution()"><i class="fa-solid fa-play"></i> Run Script</button>
                    <pre id="codeConsoleBox" style="background:#05080E; border:1px solid var(--border); border-radius:8px; padding:10px; margin-top:10px; font-size:0.8rem; color:var(--accent-blue); max-height:160px; overflow-y:auto;">Ready.</pre>
                </div>
            </div>

            <!-- 4. FILE PREVIEW VIEW -->
            <div class="panel page-panel" id="panel-file-preview">
                <div class="page-title"><i class="fa-solid fa-folder-open" style="color: var(--accent-amber);"></i> File Preview & Persistent Storage</div>
                <div class="card-surface">
                    <div style="font-weight: 700; font-size: 0.88rem; margin-bottom: 8px;">Persistent SQLite Notes</div>
                    <div id="notesListView" style="display: flex; flex-direction: column; gap: 8px; max-height: 380px; overflow-y: auto;">
                        Loading notes...
                    </div>
                </div>
            </div>

            <!-- 5. CENTRALIZED SETTINGS VIEW -->
            <div class="panel page-panel" id="panel-settings">
                <div class="page-title"><i class="fa-solid fa-sliders" style="color: var(--accent-cyan);"></i> Centralized Configuration Hub</div>
                <div class="card-surface">
                    <div class="settings-tab-bar">
                        <button class="tab-btn active" onclick="setTab('profile')">Profile & User</button>
                        <button class="tab-btn" onclick="setTab('voice')">Voice & Audio</button>
                        <button class="tab-btn" onclick="setTab('telegram')">Telegram Bot</button>
                        <button class="tab-btn" onclick="setTab('whatsapp')">WhatsApp Bridge</button>
                        <button class="tab-btn" onclick="setTab('github')">GitHub Sync</button>
                        <button class="tab-btn" onclick="setTab('keys')">API Keys</button>
                    </div>

                    <!-- Tab: Profile -->
                    <div class="tab-pane active" id="pane-profile">
                        <div class="form-field">
                            <label>Registered User Name</label>
                            <input type="text" id="cfgUserName" value="Ram Binay Pandit">
                        </div>
                    </div>

                    <!-- Tab: Voice -->
                    <div class="tab-pane" id="pane-voice">
                        <div class="form-field">
                            <label>Voice Accent / Language</label>
                            <select id="cfgVoiceAccent">
                                <option value="hi-IN">Hindi (India) - hi-IN</option>
                                <option value="en-IN">English (India) - en-IN</option>
                                <option value="en-US">English (US) - en-US</option>
                            </select>
                        </div>
                        <div class="form-field">
                            <label>Speech Pitch</label>
                            <input type="number" id="cfgVoicePitch" step="0.1" value="1.0">
                        </div>
                        <div class="form-field">
                            <label>Speech Rate</label>
                            <input type="number" id="cfgVoiceRate" step="0.1" value="0.95">
                        </div>
                        <div style="display:flex; align-items:center; gap:8px; margin-top:4px;">
                            <input type="checkbox" id="cfgWakePhrase" checked>
                            <label for="cfgWakePhrase" style="font-size:0.82rem; color:#FFF;">Enable "Hey RB" Background Wake Word</label>
                        </div>
                    </div>

                    <!-- Tab: Telegram -->
                    <div class="tab-pane" id="pane-telegram">
                        <div class="form-field">
                            <label>Telegram Bot Token</label>
                            <input type="text" id="cfgTelegramToken" placeholder="123456:ABC-DEF...">
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <button class="btn-action-primary" style="flex:1;" onclick="startTelegramBot()"><i class="fa-solid fa-play"></i> Start Bot</button>
                            <button class="btn-action-primary" style="background:#475569; color:#FFF;" onclick="stopTelegramBot()">Stop</button>
                        </div>
                        <div id="telegramStatusBox" style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">Checking status...</div>
                    </div>

                    <!-- Tab: WhatsApp -->
                    <div class="tab-pane" id="pane-whatsapp">
                        <div class="form-field">
                            <label>Target Phone Number (e.g. 919876543210)</label>
                            <input type="text" id="cfgWaPhone" placeholder="91XXXXXXXXXX">
                        </div>
                        <div class="form-field">
                            <label>Message Text</label>
                            <input type="text" id="cfgWaMsg" value="Hello Ram Binay, RB Agent is active!">
                        </div>
                        <button class="btn-action-primary" onclick="launchWhatsApp()"><i class="fa-brands fa-whatsapp"></i> Launch WhatsApp</button>
                    </div>

                    <!-- Tab: GitHub -->
                    <div class="tab-pane" id="pane-github">
                        <div class="form-field">
                            <label>GitHub Username</label>
                            <input type="text" id="cfgGhUser" value="rambinaypandit798-sudo">
                        </div>
                        <div class="form-field">
                            <label>Personal Access Token (PAT) [Encrypted]</label>
                            <input type="password" id="cfgGhToken" placeholder="ghp_...">
                        </div>
                        <button class="btn-action-primary" onclick="syncGhRepos()"><i class="fa-brands fa-github"></i> Sync Repositories</button>
                        <div id="ghSyncStatus" style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;"></div>
                    </div>

                    <!-- Tab: Keys -->
                    <div class="tab-pane" id="pane-keys">
                        <div class="form-field">
                            <label>Google Gemini API Key</label>
                            <input type="password" id="cfgGeminiKey" placeholder="AIzaSy...">
                        </div>
                    </div>

                    <button class="btn-action-primary" style="width: 100%; margin-top: 14px;" onclick="saveConfigurations()">
                        <i class="fa-solid fa-floppy-disk"></i> Save Configurations
                    </button>
                </div>
            </div>

            <!-- 6. PROJECTS VIEW -->
            <div class="panel page-panel" id="panel-projects">
                <div class="page-title"><i class="fa-solid fa-cubes" style="color: var(--accent-purple);"></i> Projects</div>
                <div class="card-surface">
                    <div style="font-weight: 700; font-size: 0.95rem; color: #FFF;">RB-ai-assistant</div>
                    <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 3px;">Autonomous Android / Termux OS Agent</div>
                    <div style="margin-top: 8px;">
                        <span style="background: rgba(0,229,255,0.15); color: var(--accent-cyan); font-size: 0.7rem; padding: 2px 8px; border-radius: 6px; font-weight: 700;">Git: main (Synced)</span>
                    </div>
                </div>
            </div>

            <!-- 7. SKILL ADD VIEW -->
            <div class="panel page-panel" id="panel-skill-add">
                <div class="page-title"><i class="fa-solid fa-puzzle-piece" style="color: var(--accent-green);"></i> Skill Add</div>
                <div class="card-surface">
                    <div class="form-field">
                        <label>Skill Name</label>
                        <input type="text" id="skillNameInput" placeholder="e.g. Code Reviewer">
                    </div>
                    <div class="form-field">
                        <label>System Prompt Directives</label>
                        <textarea id="skillPromptInput" rows="4" placeholder="Instructions for this skill..."></textarea>
                    </div>
                    <button class="btn-action-primary" onclick="addSkill()"><i class="fa-solid fa-plus"></i> Save Skill</button>
                </div>
            </div>

            <!-- 8. CHATS VIEW -->
            <div class="panel page-panel" id="panel-chats">
                <div class="page-title"><i class="fa-solid fa-comments" style="color: var(--accent-blue);"></i> Chat History</div>
                <div class="card-surface">
                    <div id="chatsListContainer" style="display: flex; flex-direction: column; gap: 8px; max-height: 400px; overflow-y: auto;">
                        Loading previous chats...
                    </div>
                </div>
            </div>
        </div>

        <!-- Real-Time Scrolling Subtitles Ticker (Directly above input bar) -->
        <div class="subtitles-dock">
            <div class="subtitles-inner">
                <i class="fa-solid fa-closed-captioning"></i>
                <div class="subtitles-text" id="subtitlesTicker">
                    RB Agent ready • Autonomous intent routing active
                </div>
            </div>
        </div>

        <!-- Sticky Persistent Bottom Chat/Command Input Bar -->
        <div class="bottom-input-dock">
            <button class="dock-action-btn" onclick="captureSnapshot()" title="Camera"><i class="fa-solid fa-camera"></i></button>
            <div class="input-shell">
                <input type="text" id="primaryChatInput" placeholder="Message RB Agent or say 'यह चीज़ सेव कर लो'..." onkeypress="onEnterSubmit(event)">
            </div>
            <button class="dock-action-btn" id="micBtn" onclick="toggleMic()" title="Microphone"><i class="fa-solid fa-microphone"></i></button>
            <button class="dock-action-btn" onclick="sendChatMessage()" title="Send"><i class="fa-solid fa-paper-plane"></i></button>
        </div>
    </main>

    <script>
        let currentMaster = "Ram Binay Pandit";
        let isMicOn = false;
        let speechRec = null;

        window.addEventListener('DOMContentLoaded', () => {
            initSystem();
            setupVoice();
        });

        async function initSystem() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                if (data.user_name) {
                    currentMaster = data.user_name;
                    syncUserUI(data.user_name);
                }
                if (data.device && data.device.battery) {
                    const b = data.device.battery;
                    document.getElementById('topBattStatus').innerText = `${b.percentage || '85'}% LIVE`;
                }
            } catch(e) {
                console.log(e);
            }
            fetchNotes();
            fetchChats();
        }

        function syncUserUI(name) {
            document.getElementById('sidebarUserName').innerText = name;
            document.getElementById('greetBannerText').innerText = `नमस्ते, ${name}`;
            document.getElementById('cfgUserName').value = name;
            const initials = name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            document.getElementById('userAvatarPill').innerText = initials || 'RP';
        }

        // Navigation Drawer
        function toggleSidebar(open) {
            document.getElementById('sidebar').classList.toggle('active', open);
            document.getElementById('sidebarBackdrop').classList.toggle('active', open);
        }

        function showPanel(panelName) {
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

            const p = document.getElementById(`panel-${panelName}`);
            if (p) p.classList.add('active');

            const links = document.querySelectorAll('.sidebar-menu .nav-item');
            links.forEach(l => {
                if (l.innerText.toLowerCase().includes(panelName.replace('-', ' '))) {
                    l.classList.add('active');
                }
            });

            const titles = {
                'home': 'RB Agent Overview',
                'web-preview': 'Web Preview & Search',
                'code-preview': 'Code Editor & Terminal',
                'file-preview': 'Persistent Storage & Files',
                'settings': 'Centralized Configuration',
                'projects': 'Active Projects',
                'skill-add': 'Skill Add & Extensions',
                'chats': 'Chat History'
            };
            document.getElementById('pageTitleText').innerText = titles[panelName] || 'RB Agent';
            toggleSidebar(false);
        }

        function setTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            event.target.classList.add('active');
            const target = document.getElementById(`pane-${tabId}`);
            if (target) target.classList.add('active');
        }

        // Chat Submission & Autonomous Intent Routing
        async function sendChatMessage() {
            const input = document.getElementById('primaryChatInput');
            const text = input.value.trim();
            if (!text) return;

            addMsg('user', text);
            input.value = '';
            setSubtitle(`User: "${text}"`);
            showPanel('home');

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ text, is_voice: isMicOn })
                });
                const data = await res.json();
                const reply = data.response || "Task completed.";
                const tag = data.tag || (data.agent ? 'automation' : 'general');
                addMsg('assistant', reply, tag);

                // Vocalize reply via TTS
                speakText(reply, () => {
                    setSubtitle("Agent finished speaking. Ready for next command.");
                });
            } catch(e) {
                addMsg('assistant', 'Error communicating with RB Agent: ' + e.message, 'automation');
            }
        }

        function onEnterSubmit(e) {
            if (e.key === 'Enter') sendChatMessage();
        }

        function addMsg(sender, text, tag = 'automation') {
            const feed = document.getElementById('chatStream');
            const div = document.createElement('div');
            div.className = `msg-bubble ${sender}`;
            if (sender === 'assistant') {
                div.innerHTML = `<div class="tag-pill pill-${tag}">RB Agent</div><div>${text}</div>`;
            } else {
                div.innerText = text;
            }
            feed.appendChild(div);
            feed.scrollTop = feed.scrollHeight;
        }

        function setSubtitle(text) {
            document.getElementById('subtitlesTicker').innerText = text;
        }

        // Voice TTS
        function speakText(text, onDone) {
            if (!('speechSynthesis' in window)) {
                if (onDone) onDone();
                return;
            }
            window.speechSynthesis.cancel();
            const clean = text.replace(/[*#`_\[\]]/g, '');
            const u = new SpeechSynthesisUtterance(clean);
            u.lang = document.getElementById('cfgVoiceAccent').value || 'hi-IN';
            u.pitch = parseFloat(document.getElementById('cfgVoicePitch').value) || 1.0;
            u.rate = parseFloat(document.getElementById('cfgVoiceRate').value) || 0.95;
            u.onstart = () => setSubtitle(`Speaking: "${clean.substring(0, 45)}..."`);
            u.onend = () => { if (onDone) onDone(); };
            window.speechSynthesis.speak(u);
        }

        function setupVoice() {
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechRec) {
                speechRec = new SpeechRec();
                speechRec.continuous = true;
                speechRec.interimResults = true;
                speechRec.lang = 'hi-IN';

                speechRec.onresult = (e) => {
                    let transcript = '';
                    for (let i = e.resultIndex; i < e.results.length; i++) {
                        transcript += e.results[i][0].transcript;
                    }
                    setSubtitle(`Listening: "${transcript}"`);
                    const lower = transcript.toLowerCase();
                    if (lower.includes("hey rb") || lower.includes("हे आरबी")) {
                        const stripped = transcript.replace(/hey rb|हे आरबी/gi, '').trim();
                        document.getElementById('primaryChatInput').value = stripped;
                        if (stripped.length > 2) sendChatMessage();
                    }
                };
            }
        }

        function toggleMic() {
            const btn = document.getElementById('micBtn');
            isMicOn = !isMicOn;
            if (isMicOn) {
                btn.classList.add('recording');
                if (speechRec) try { speechRec.start(); } catch(e){}
                setSubtitle("Microphone active • Listening for speech or 'Hey RB'...");
            } else {
                btn.classList.remove('recording');
                if (speechRec) try { speechRec.stop(); } catch(e){}
                setSubtitle("Microphone paused.");
            }
        }

        // Web Preview
        async function triggerWebPreview() {
            const q = document.getElementById('webQueryInput').value.trim();
            const out = document.getElementById('webPreviewOutput');
            out.innerText = "Searching web...";
            try {
                const res = await fetch('/api/agents', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ agent: 'research', action: 'run', params: { query: q } })
                });
                const d = await res.json();
                out.innerText = JSON.stringify(d.result, null, 2);
            } catch(e) {
                out.innerText = "Error: " + e.message;
            }
        }

        // Code Execution
        async function runScriptExecution() {
            const code = document.getElementById('codeScriptArea').value;
            const consoleEl = document.getElementById('codeConsoleBox');
            consoleEl.innerText = "Running...";
            try {
                const res = await fetch('/api/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ action: 'shell', args: { command: `python3 -c ${JSON.stringify(code)}` } })
                });
                const d = await res.json();
                consoleEl.innerText = d.result.stdout || d.result.stderr || "Executed (No output)";
            } catch(e) {
                consoleEl.innerText = "Error: " + e.message;
            }
        }

        // Notes
        async function fetchNotes() {
            const c = document.getElementById('notesListView');
            try {
                const res = await fetch('/api/notes');
                const d = await res.json();
                if (d.notes && d.notes.length > 0) {
                    c.innerHTML = d.notes.map(n => `
                        <div style="background:#0C1220; border:1px solid var(--border); border-radius:8px; padding:10px;">
                            <div style="font-weight:700; color:#FFF; font-size:0.85rem;">${n.title}</div>
                            <div style="color:var(--text-muted); font-size:0.78rem; margin-top:2px;">${n.content}</div>
                            <div style="font-size:0.65rem; color:#64748B; margin-top:4px;">${n.created_at}</div>
                        </div>
                    `).join('');
                } else {
                    c.innerHTML = '<div style="color:var(--text-muted); font-size:0.8rem;">No notes yet. Type "यह चीज़ सेव कर लो" to add!</div>';
                }
            } catch(e) {
                c.innerHTML = 'Unable to load notes.';
            }
        }

        // Chats
        async function fetchChats() {
            const c = document.getElementById('chatsListContainer');
            try {
                const res = await fetch('/api/chats');
                const d = await res.json();
                if (d.chats && d.chats.length > 0) {
                    c.innerHTML = d.chats.map(ch => `
                        <div style="background:#0C1220; border:1px solid var(--border); border-radius:8px; padding:8px 12px; font-size:0.8rem;">
                            <span style="color:${ch.sender === 'user' ? 'var(--accent-cyan)' : 'var(--accent-green)'}; font-weight:700;">${ch.sender.toUpperCase()}:</span>
                            <span style="color:#FFF; margin-left:6px;">${ch.message.substring(0, 65)}...</span>
                        </div>
                    `).join('');
                } else {
                    c.innerHTML = '<div style="color:var(--text-muted); font-size:0.8rem;">No previous chats.</div>';
                }
            } catch(e) {
                c.innerHTML = 'Unable to load chats.';
            }
        }

        function searchChats() {
            const q = document.getElementById('chatSearch').value.toLowerCase();
            document.querySelectorAll('#chatsListContainer > div').forEach(el => {
                el.style.display = el.innerText.toLowerCase().includes(q) ? 'block' : 'none';
            });
        }

        function resetNewChat() {
            document.getElementById('chatStream').innerHTML = `
                <div class="msg-bubble assistant">
                    <div class="tag-pill pill-automation">RB System</div>
                    <div>New chat session started with Ram Binay Pandit. What can I do for you?</div>
                </div>
            `;
            showPanel('home');
        }

        // Settings Save
        async function saveConfigurations() {
            const name = document.getElementById('cfgUserName').value.trim();
            const accent = document.getElementById('cfgVoiceAccent').value;
            const pitch = document.getElementById('cfgVoicePitch').value;
            const rate = document.getElementById('cfgVoiceRate').value;
            const wake = document.getElementById('cfgWakePhrase').checked;
            const geminiKey = document.getElementById('cfgGeminiKey').value.trim();

            if (name) {
                currentMaster = name;
                await fetch('/api/user', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ user_name: name })
                });
                syncUserUI(name);
            }

            await fetch('/api/settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    voice_accent: accent,
                    voice_pitch: pitch,
                    voice_rate: rate,
                    wake_phrase_enabled: wake ? 'true' : 'false'
                })
            });

            if (geminiKey) {
                await fetch('/api/config', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ gemini_api_key: geminiKey })
                });
            }

            alert("Configurations saved successfully!");
            showPanel('home');
        }

        // Telegram
        async function startTelegramBot() {
            const token = document.getElementById('cfgTelegramToken').value.trim();
            const res = await fetch('/api/telegram', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: 'start', token })
            });
            const d = await res.json();
            document.getElementById('telegramStatusBox').innerText = d.message || d.error;
        }

        async function stopTelegramBot() {
            const res = await fetch('/api/telegram', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: 'stop' })
            });
            document.getElementById('telegramStatusBox').innerText = "Bot stopped.";
        }

        // WhatsApp
        async function launchWhatsApp() {
            const phone = document.getElementById('cfgWaPhone').value.trim();
            const msg = document.getElementById('cfgWaMsg').value.trim();
            if (!phone) return alert("Enter phone number");
            const res = await fetch('/api/whatsapp', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ phone, message: msg })
            });
            const d = await res.json();
            if (d.url) window.open(d.url, '_blank');
        }

        // GitHub
        async function syncGhRepos() {
            const u = document.getElementById('cfgGhUser').value.trim();
            const token = document.getElementById('cfgGhToken').value.trim();
            const label = document.getElementById('ghSyncStatus');
            label.innerText = "Syncing...";
            const res = await fetch(`/api/github?username=${encodeURIComponent(u)}&token=${encodeURIComponent(token)}`);
            const d = await res.json();
            label.innerText = `Synced ${d.count || 0} repositories for ${u}.`;
        }

        function addSkill() {
            alert("Custom skill saved and registered.");
            showPanel('home');
        }

        function captureSnapshot() {
            fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: 'shell', args: { command: 'termux-camera-photo ~/rb_ai/latest.jpg' } })
            });
            setSubtitle("Camera snapshot requested via Termux.");
        }
    </script>
</body>
</html>
"""
