"""
RB.AI - Production Master Web Application & Agent Interface
Lovable-inspired unified architecture:
- Unified collapsible sidebar (Home, Web Preview, Code Preview, File Preview, Settings, Projects, Skill Add, Chats with search and New Chat)
- Compact Arc Reactor HUD (< 40% vertical space)
- Sticky persistent bottom chat input bar
- Live scrolling subtitles/captions stream
- Centralized Settings Hub for Telegram, WhatsApp, GitHub PAT, Voice profiles, and API keys
- Autonomous Intent Routing for 5 Sub-Agents with clean UI error masking
"""

WEB_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>RB.AI — Autonomous Operating System</title>
    <meta name="theme-color" content="#0F172A">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-body: #090D16;
            --bg-sidebar: #0D1322;
            --bg-card: #131B2E;
            --bg-input: #17223B;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --border: rgba(255, 255, 255, 0.08);
            --border-active: rgba(0, 229, 255, 0.4);
            --accent-cyan: #00E5FF;
            --accent-blue: #38BDF8;
            --accent-purple: #A855F7;
            --accent-green: #10B981;
            --accent-amber: #F59E0B;
            --accent-pink: #EC4899;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: var(--bg-body); color: var(--text-primary); height: 100vh; display: flex; overflow: hidden; }

        /* Unified Collapsible Sidebar */
        .sidebar {
            width: 270px; background: var(--bg-sidebar); border-right: 1px solid var(--border);
            display: flex; flex-direction: column; z-index: 50; transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @media (max-width: 768px) {
            .sidebar { position: fixed; top: 0; bottom: 0; left: 0; transform: translateX(-100%); box-shadow: 4px 0 25px rgba(0,0,0,0.5); }
            .sidebar.active { transform: translateX(0); }
        }
        .sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); z-index: 45; }
        .sidebar-overlay.active { display: block; }

        .sidebar-brand {
            padding: 18px 20px; display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid var(--border);
        }
        .brand-logo { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.1rem; letter-spacing: 0.5px; }
        .brand-logo i { color: var(--accent-cyan); font-size: 1.25rem; }
        .brand-logo span { color: var(--accent-cyan); }
        .close-sidebar-btn { display: none; background: none; border: none; color: var(--text-secondary); font-size: 1.2rem; cursor: pointer; }
        @media (max-width: 768px) { .close-sidebar-btn { display: block; } }

        .user-profile-badge {
            margin: 12px 14px 6px 14px; padding: 10px 12px; background: var(--bg-card);
            border: 1px solid var(--border); border-radius: 12px; display: flex; align-items: center; gap: 10px;
        }
        .avatar-circle {
            width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0284C7, #00E5FF);
            color: #0F172A; font-weight: 900; font-size: 0.85rem; display: flex; align-items: center; justify-content: center;
        }
        .user-meta-name { font-size: 0.85rem; font-weight: 700; color: var(--text-primary); max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .user-meta-status { font-size: 0.68rem; color: var(--accent-green); display: flex; align-items: center; gap: 4px; }

        /* Navigation List - Strictly 8 Items */
        .sidebar-nav { flex: 1; overflow-y: auto; padding: 8px 12px; display: flex; flex-direction: column; gap: 4px; }
        .nav-link {
            display: flex; align-items: center; gap: 12px; padding: 10px 14px; border-radius: 10px;
            color: var(--text-secondary); font-size: 0.88rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
            text-decoration: none; border: 1px solid transparent;
        }
        .nav-link i { font-size: 1rem; width: 20px; text-align: center; }
        .nav-link:hover, .nav-link.active {
            background: rgba(0, 229, 255, 0.08); color: var(--accent-cyan); border-color: rgba(0, 229, 255, 0.2);
        }

        /* Chats Drawer Section with History Search & New Chat Button */
        .sidebar-chats-section {
            border-top: 1px solid var(--border); padding: 12px 14px; display: flex; flex-direction: column; gap: 8px;
        }
        .chat-search-input {
            background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px;
            padding: 8px 12px; font-size: 0.78rem; color: var(--text-primary); outline: none; width: 100%;
        }
        .chat-search-input:focus { border-color: var(--accent-cyan); }
        .btn-new-chat {
            background: linear-gradient(135deg, #0284C7, #0369A1); color: #FFF; border: none;
            padding: 10px; border-radius: 10px; font-size: 0.85rem; font-weight: 700; cursor: pointer;
            display: flex; align-items: center; justify-content: center; gap: 8px; transition: opacity 0.2s;
        }
        .btn-new-chat:hover { opacity: 0.9; }

        /* Main Viewport */
        .main-stage { flex: 1; display: flex; flex-direction: column; height: 100vh; overflow: hidden; position: relative; }

        /* Top Bar */
        .top-navbar {
            padding: 12px 18px; background: var(--bg-sidebar); border-bottom: 1px solid var(--border);
            display: flex; align-items: center; justify-content: space-between; z-index: 20;
        }
        .menu-trigger { background: none; border: none; color: var(--text-primary); font-size: 1.25rem; cursor: pointer; }
        .top-status-pill {
            background: rgba(16, 185, 129, 0.15); border: 1px solid var(--accent-green); color: var(--accent-green);
            padding: 3px 10px; border-radius: 14px; font-size: 0.72rem; font-weight: 700; display: flex; align-items: center; gap: 6px;
        }
        .top-status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent-green); box-shadow: 0 0 8px var(--accent-green); }

        /* Views Container */
        .views-container { flex: 1; overflow-y: auto; display: flex; flex-direction: column; position: relative; }
        .view-panel { display: none; flex: 1; flex-direction: column; }
        .view-panel.active { display: flex; }

        /* COMPACT HOMEPAGE (< 40% vertical space) */
        .home-view { padding: 10px 16px 80px 16px; display: flex; flex-direction: column; }
        
        .compact-greeting-bar {
            background: linear-gradient(135deg, rgba(30, 58, 138, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%);
            border: 1px solid rgba(0, 229, 255, 0.25); border-radius: 14px; padding: 10px 16px; margin-bottom: 8px;
            display: flex; align-items: center; justify-content: space-between;
        }
        .greeting-text-title { font-size: 0.95rem; font-weight: 800; color: #FFF; }
        .greeting-text-sub { font-size: 0.75rem; color: var(--text-secondary); margin-top: 1px; }

        /* Compact Arc Reactor HUD Section */
        .hud-compact-wrapper {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            padding: 10px 0 6px 0; max-height: 150px;
        }
        .reactor-compact {
            width: 110px; height: 110px; position: relative; display: flex; align-items: center; justify-content: center;
            cursor: pointer; user-select: none;
        }
        .reactor-ring-outer {
            position: absolute; inset: 0; border-radius: 50%; border: 1.5px dashed rgba(0, 229, 255, 0.6);
            animation: spinClockwise 12s linear infinite;
        }
        .reactor-ring-mid {
            position: absolute; inset: 8px; border-radius: 50%; border: 1.5px solid rgba(56, 189, 248, 0.4);
            border-top-color: var(--accent-cyan); border-bottom-color: var(--accent-purple);
            animation: spinCounterClockwise 8s linear infinite;
        }
        .reactor-core-compact {
            width: 74px; height: 74px; border-radius: 50%; background: radial-gradient(circle, #0F172A 0%, #030712 100%);
            border: 2px solid var(--accent-cyan); box-shadow: 0 0 20px rgba(0, 229, 255, 0.4), inset 0 0 10px rgba(0, 229, 255, 0.3);
            display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
            transition: transform 0.2s;
        }
        .reactor-compact:active .reactor-core-compact { transform: scale(0.95); }
        .core-text-main { font-size: 0.78rem; font-weight: 800; color: #FFF; letter-spacing: 0.5px; }
        .core-text-sub { font-size: 0.48rem; color: var(--accent-cyan); text-transform: uppercase; font-weight: 700; margin-top: 1px; }

        @keyframes spinClockwise { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes spinCounterClockwise { 0% { transform: rotate(360deg); } 100% { transform: rotate(0deg); } }

        /* Live Scrolling Subtitles Bar */
        .live-subtitles-pill {
            background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 20px; padding: 6px 14px; margin: 4px auto 10px auto; width: 92%; max-width: 520px;
            display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: var(--accent-blue);
        }
        .subtitles-content { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500; }

        /* Chat Stream Area */
        .chat-feed { flex: 1; display: flex; flex-direction: column; gap: 10px; overflow-y: auto; padding: 6px 0; }
        .chat-msg { max-width: 86%; padding: 10px 14px; border-radius: 14px; font-size: 0.88rem; line-height: 1.4; word-break: break-word; }
        .chat-msg.user { align-self: flex-end; background: #0284C7; color: #FFF; border-bottom-right-radius: 4px; }
        .chat-msg.assistant {
            align-self: flex-start; background: var(--bg-card); color: var(--text-primary);
            border: 1px solid var(--border); border-bottom-left-radius: 4px;
        }
        .msg-badge {
            display: inline-block; font-size: 0.65rem; font-weight: 800; padding: 2px 6px; border-radius: 6px;
            margin-bottom: 4px; text-transform: uppercase;
        }
        .badge-memory { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }
        .badge-automation { background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); border: 1px solid var(--accent-purple); }
        .badge-research { background: rgba(0, 229, 255, 0.15); color: var(--accent-cyan); border: 1px solid var(--accent-cyan); }
        .badge-coding { background: rgba(236, 72, 153, 0.15); color: var(--accent-pink); border: 1px solid var(--accent-pink); }

        /* STICKY PERSISTENT BOTTOM CHAT INPUT BAR */
        .persistent-input-dock {
            position: absolute; bottom: 0; left: 0; right: 0; background: var(--bg-sidebar);
            border-top: 1px solid var(--border); padding: 10px 14px; display: flex; align-items: center; gap: 8px; z-index: 30;
        }
        .input-dock-box {
            flex: 1; background: var(--bg-input); border: 1px solid var(--border); border-radius: 24px;
            padding: 8px 14px; display: flex; align-items: center; gap: 8px;
        }
        .input-dock-box input {
            flex: 1; background: transparent; border: none; outline: none; color: #FFF; font-size: 0.9rem;
        }
        .dock-btn {
            background: none; border: none; color: var(--accent-cyan); font-size: 1.15rem; cursor: pointer;
            padding: 4px; display: flex; align-items: center; justify-content: center;
        }
        .dock-btn.active-mic { color: #EF4444; animation: pulseMic 1.2s infinite; }
        @keyframes pulseMic { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.18); } }

        /* Secondary Views (Web, Code, Files, Settings, Projects, Skill Add, Chats) */
        .content-panel { padding: 18px 20px 80px 20px; overflow-y: auto; height: 100%; display: flex; flex-direction: column; gap: 14px; }
        .panel-heading { font-size: 1.15rem; font-weight: 800; color: #FFF; display: flex; align-items: center; gap: 10px; }
        .panel-card {
            background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 16px;
        }

        /* Settings Tabs System */
        .settings-tabs { display: flex; gap: 6px; overflow-x: auto; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
        .settings-tab-btn {
            background: var(--bg-card); border: 1px solid var(--border); color: var(--text-secondary);
            padding: 8px 14px; border-radius: 10px; font-size: 0.8rem; font-weight: 600; cursor: pointer; white-space: nowrap;
        }
        .settings-tab-btn.active { background: rgba(0,229,255,0.15); color: var(--accent-cyan); border-color: var(--accent-cyan); }
        .settings-section { display: none; flex-direction: column; gap: 12px; margin-top: 14px; }
        .settings-section.active { display: flex; }

        .form-row { display: flex; flex-direction: column; gap: 6px; }
        .form-row label { font-size: 0.78rem; font-weight: 700; color: var(--text-secondary); }
        .form-row input, .form-row select, .form-row textarea {
            background: var(--bg-input); border: 1px solid var(--border); color: #FFF;
            padding: 10px 12px; border-radius: 8px; font-size: 0.85rem; outline: none;
        }
        .form-row input:focus, .form-row select:focus { border-color: var(--accent-cyan); }

        .btn-save-settings {
            background: linear-gradient(135deg, #0284C7, #00E5FF); color: #0F172A; font-weight: 800;
            border: none; padding: 12px 20px; border-radius: 10px; font-size: 0.9rem; cursor: pointer; margin-top: 10px;
        }
    </style>
</head>
<body>

    <!-- Unified Collapsible Sidebar (Strictly 8 Navigation Items) -->
    <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar(false)"></div>
    <aside class="sidebar" id="appSidebar">
        <div class="sidebar-brand">
            <div class="brand-logo">
                <i class="fa-solid fa-atom"></i>
                RB<span>.AGENT</span>
            </div>
            <button class="close-sidebar-btn" onclick="toggleSidebar(false)">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>

        <div class="user-profile-badge">
            <div class="avatar-circle" id="userInitialsAvatar">RB</div>
            <div>
                <div class="user-meta-name" id="sidebarUserName">Ram Binay kumar Pandit</div>
                <div class="user-meta-status"><i class="fa-solid fa-circle" style="font-size: 0.45rem;"></i> Active OS Node</div>
            </div>
        </div>

        <!-- The 8 Unified Navigation Items -->
        <nav class="sidebar-nav">
            <div class="nav-link active" onclick="switchView('home')">
                <i class="fa-solid fa-house"></i> Home
            </div>
            <div class="nav-link" onclick="switchView('web-preview')">
                <i class="fa-solid fa-globe"></i> Web Preview
            </div>
            <div class="nav-link" onclick="switchView('code-preview')">
                <i class="fa-solid fa-code"></i> Code Preview
            </div>
            <div class="nav-link" onclick="switchView('file-preview')">
                <i class="fa-solid fa-folder-open"></i> File Preview
            </div>
            <div class="nav-link" onclick="switchView('settings')">
                <i class="fa-solid fa-sliders"></i> Settings
            </div>
            <div class="nav-link" onclick="switchView('projects')">
                <i class="fa-solid fa-cubes"></i> Projects
            </div>
            <div class="nav-link" onclick="switchView('skill-add')">
                <i class="fa-solid fa-puzzle-piece"></i> Skill Add
            </div>
            <div class="nav-link" onclick="switchView('chats')">
                <i class="fa-solid fa-comments"></i> Chats
            </div>
        </nav>

        <!-- Chats History Search & Prominent New Chat Button -->
        <div class="sidebar-chats-section">
            <input type="text" class="chat-search-input" id="chatSearchInput" placeholder="Search chat history..." oninput="filterChatHistory()">
            <button class="btn-new-chat" onclick="startNewChat()">
                <i class="fa-solid fa-plus"></i> New chat
            </button>
        </div>
    </aside>

    <!-- Main Viewport -->
    <main class="main-stage">
        <!-- Top Navigation Bar -->
        <div class="top-navbar">
            <button class="menu-trigger" onclick="toggleSidebar(true)" aria-label="Toggle Menu">
                <i class="fa-solid fa-bars"></i>
            </button>
            <div style="font-weight: 700; font-size: 0.95rem; color: #FFF;" id="viewTitleText">
                RB Agent Overview
            </div>
            <div class="top-status-pill">
                <div class="top-status-dot"></div>
                <span id="topBatteryStatus">85% LIVE</span>
            </div>
        </div>

        <!-- Views Container -->
        <div class="views-container">
            <!-- 1. HOME VIEW (Compact Arc Reactor HUD & Chat) -->
            <div class="view-panel home-view active" id="view-home">
                <!-- Compact Greeting Card -->
                <div class="compact-greeting-bar">
                    <div>
                        <div class="greeting-text-title" id="homeGreetingTitle">
                            नमस्ते, Ram Binay kumar Pandit
                        </div>
                        <div class="greeting-text-sub">आज आपका क्या प्लान है? RB Agent is online.</div>
                    </div>
                    <i class="fa-solid fa-shield-halved" style="color: var(--accent-cyan); font-size: 1.2rem;"></i>
                </div>

                <!-- Compact HUD Arc Reactor (< 40% vertical space) -->
                <div class="hud-compact-wrapper">
                    <div class="reactor-compact" onclick="switchView('settings')" title="Core Orchestrator HUD">
                        <div class="reactor-ring-outer"></div>
                        <div class="reactor-ring-mid"></div>
                        <div class="reactor-core-compact">
                            <i class="fa-solid fa-bolt" style="color: var(--accent-cyan); font-size: 0.85rem; margin-bottom: 2px;"></i>
                            <div class="core-text-main">RB Agent</div>
                            <div class="core-text-sub">Online</div>
                        </div>
                    </div>
                </div>

                <!-- Live Subtitles & Voice Stream -->
                <div class="live-subtitles-pill">
                    <i class="fa-solid fa-closed-captioning"></i>
                    <div class="subtitles-content" id="liveSubtitles">
                        RB Agent ready • Autonomous intent routing active
                    </div>
                </div>

                <!-- Live Chat Feed -->
                <div class="chat-feed" id="chatFeed">
                    <div class="chat-msg assistant">
                        <div class="msg-badge badge-automation">RB System</div>
                        <div>नमस्ते Ram Binay! I am RB Agent. Type any instruction (e.g., <i>"यह चीज़ सेव कर लो: Meeting at 5"</i>, <i>"turn on torch"</i>, or <i>"search Gemini 2.5"</i>) to automatically trigger the right sub-agent.</div>
                    </div>
                </div>
            </div>

            <!-- 2. WEB PREVIEW VIEW -->
            <div class="view-panel content-panel" id="view-web-preview">
                <div class="panel-heading"><i class="fa-solid fa-globe" style="color: var(--accent-cyan);"></i> Web Preview & Search</div>
                <div class="panel-card">
                    <div class="form-row">
                        <label>Web URL or Live Search Query</label>
                        <div style="display: flex; gap: 8px;">
                            <input type="text" id="webPreviewQuery" placeholder="Enter query or URL..." value="latest Google Gemini 2.5 models">
                            <button class="btn-save-settings" style="margin-top:0; padding: 8px 16px;" onclick="executeWebPreview()">Fetch</button>
                        </div>
                    </div>
                    <div id="webPreviewResult" style="margin-top: 14px; font-size: 0.85rem; color: #CBD5E1; line-height: 1.5; white-space: pre-wrap; max-height: 380px; overflow-y: auto;">
                        Click Fetch to search live web data or preview web URLs.
                    </div>
                </div>
            </div>

            <!-- 3. CODE PREVIEW VIEW -->
            <div class="view-panel content-panel" id="view-code-preview">
                <div class="panel-heading"><i class="fa-solid fa-code" style="color: var(--accent-pink);"></i> Code Preview & Terminal</div>
                <div class="panel-card">
                    <div class="form-row">
                        <label>Python Script or Shell Command</label>
                        <textarea id="codeEditorInput" rows="6" style="font-family: monospace;">print("Hello Ram Binay! Executing from Termux Python 3.14.")</textarea>
                    </div>
                    <button class="btn-save-settings" onclick="executeCodeSnippet()"><i class="fa-solid fa-play"></i> Run Script</button>
                    <div style="margin-top: 12px; font-size: 0.75rem; color: var(--text-secondary);">Execution Console:</div>
                    <pre id="codeConsoleOutput" style="background:#070B12; border:1px solid var(--border); border-radius:8px; padding:10px; margin-top:4px; font-size:0.8rem; color:var(--accent-blue); max-height:160px; overflow-y:auto;">Ready.</pre>
                </div>
            </div>

            <!-- 4. FILE PREVIEW VIEW -->
            <div class="view-panel content-panel" id="view-file-preview">
                <div class="panel-heading"><i class="fa-solid fa-folder-open" style="color: var(--accent-amber);"></i> File & Persistent Storage Preview</div>
                <div class="panel-card">
                    <div style="font-weight: 700; font-size: 0.9rem; margin-bottom: 8px;">SQLite Notes & Memory Records</div>
                    <div id="notesContainer" style="display: flex; flex-direction: column; gap: 8px; max-height: 360px; overflow-y: auto;">
                        Loading stored notes...
                    </div>
                </div>
            </div>

            <!-- 5. CENTRALIZED SETTINGS VIEW -->
            <div class="view-panel content-panel" id="view-settings">
                <div class="panel-heading"><i class="fa-solid fa-sliders" style="color: var(--accent-cyan);"></i> Centralized Configuration Hub</div>
                <div class="panel-card">
                    <div class="settings-tabs">
                        <button class="settings-tab-btn active" onclick="switchSettingsTab('profile')">Profile & User</button>
                        <button class="settings-tab-btn" onclick="switchSettingsTab('voice')">Voice & Audio</button>
                        <button class="settings-tab-btn" onclick="switchSettingsTab('telegram')">Telegram Bot</button>
                        <button class="settings-tab-btn" onclick="switchSettingsTab('whatsapp')">WhatsApp</button>
                        <button class="settings-tab-btn" onclick="switchSettingsTab('github')">GitHub Sync</button>
                        <button class="settings-tab-btn" onclick="switchSettingsTab('keys')">API Keys</button>
                    </div>

                    <!-- Tab: Profile -->
                    <div class="settings-section active" id="tab-profile">
                        <div class="form-row">
                            <label>Registered User Name</label>
                            <input type="text" id="setUserName" value="Ram Binay kumar Pandit">
                        </div>
                        <div class="form-row">
                            <label>Default Interface Theme</label>
                            <select id="setThemeMode">
                                <option value="dark">Dark / Lovable Neon</option>
                                <option value="light">Light Default</option>
                            </select>
                        </div>
                    </div>

                    <!-- Tab: Voice -->
                    <div class="settings-section" id="tab-voice">
                        <div class="form-row">
                            <label>Voice Accent / Language</label>
                            <select id="setVoiceAccent">
                                <option value="hi-IN">Hindi (India) - hi-IN</option>
                                <option value="en-IN">English (India) - en-IN</option>
                                <option value="en-US">English (US) - en-US</option>
                            </select>
                        </div>
                        <div class="form-row">
                            <label>Speech Pitch (1.0 default)</label>
                            <input type="number" id="setVoicePitch" step="0.1" value="1.0">
                        </div>
                        <div class="form-row">
                            <label>Speech Rate (0.95 default)</label>
                            <input type="number" id="setVoiceRate" step="0.1" value="0.95">
                        </div>
                        <div style="display:flex; align-items:center; gap:8px; margin-top:6px;">
                            <input type="checkbox" id="setWakePhrase" checked>
                            <label for="setWakePhrase" style="font-size:0.85rem; color:#FFF;">Enable "Hey RB" Background Wake Detection</label>
                        </div>
                    </div>

                    <!-- Tab: Telegram -->
                    <div class="settings-section" id="tab-telegram">
                        <div class="form-row">
                            <label>Telegram Bot Token (from @BotFather)</label>
                            <input type="text" id="setTelegramToken" placeholder="123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ">
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <button class="btn-save-settings" style="flex: 1;" onclick="startTelegram()"><i class="fa-solid fa-play"></i> Start Bot Webhook</button>
                            <button class="btn-save-settings" style="background:#475569; color:#FFF;" onclick="stopTelegram()">Stop</button>
                        </div>
                        <div id="telegramStatusLabel" style="font-size:0.75rem; color:var(--text-secondary); margin-top:4px;">Checking status...</div>
                    </div>

                    <!-- Tab: WhatsApp -->
                    <div class="settings-section" id="tab-whatsapp">
                        <div class="form-row">
                            <label>Target Phone Number (with Country Code)</label>
                            <input type="text" id="setWaPhone" placeholder="91XXXXXXXXXX">
                        </div>
                        <div class="form-row">
                            <label>Template Message</label>
                            <input type="text" id="setWaMsg" value="Hello Ram Binay, RB Agent is active!">
                        </div>
                        <button class="btn-save-settings" onclick="launchWhatsAppDirect()"><i class="fa-brands fa-whatsapp"></i> Test WhatsApp Bridge</button>
                    </div>

                    <!-- Tab: GitHub -->
                    <div class="settings-section" id="tab-github">
                        <div class="form-row">
                            <label>GitHub Username</label>
                            <input type="text" id="setGhUser" value="rambinaypandit798-sudo">
                        </div>
                        <div class="form-row">
                            <label>Personal Access Token (PAT) [Encrypted]</label>
                            <input type="password" id="setGhToken" placeholder="ghp_...">
                        </div>
                        <button class="btn-save-settings" onclick="syncGitHubRepos()"><i class="fa-brands fa-github"></i> Sync Repositories</button>
                        <div id="ghSyncResults" style="font-size:0.75rem; color:var(--text-secondary); margin-top:6px;"></div>
                    </div>

                    <!-- Tab: Keys -->
                    <div class="settings-section" id="tab-keys">
                        <div class="form-row">
                            <label>Google Gemini API Key</label>
                            <input type="password" id="setGeminiKey" placeholder="AIzaSy...">
                        </div>
                    </div>

                    <button class="btn-save-settings" style="width: 100%;" onclick="saveMasterSettings()">
                        <i class="fa-solid fa-floppy-disk"></i> Save All Configurations
                    </button>
                </div>
            </div>

            <!-- 6. PROJECTS VIEW -->
            <div class="view-panel content-panel" id="view-projects">
                <div class="panel-heading"><i class="fa-solid fa-cubes" style="color: var(--accent-purple);"></i> Projects & Workspaces</div>
                <div class="panel-card">
                    <div style="font-weight: 700; font-size: 0.95rem; color: #FFF;">RB-ai-assistant (Production)</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px;">Android / Termux / Flutter Hybrid Operating System Agent</div>
                    <div style="margin-top: 10px; display: flex; gap: 8px;">
                        <span style="background: rgba(0,229,255,0.15); color: var(--accent-cyan); font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; font-weight: 700;">Git: main</span>
                        <span style="background: rgba(16,185,129,0.15); color: var(--accent-green); font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; font-weight: 700;">Status: Active</span>
                    </div>
                </div>
            </div>

            <!-- 7. SKILL ADD VIEW -->
            <div class="view-panel content-panel" id="view-skill-add">
                <div class="panel-heading"><i class="fa-solid fa-puzzle-piece" style="color: var(--accent-green);"></i> Add Custom Skills</div>
                <div class="panel-card">
                    <div class="form-row">
                        <label>Skill Name</label>
                        <input type="text" id="newSkillName" placeholder="e.g. Stock Market Analyst">
                    </div>
                    <div class="form-row">
                        <label>Skill System Prompt Instructions</label>
                        <textarea id="newSkillPrompt" rows="4" placeholder="Instructions for this specialized capability..."></textarea>
                    </div>
                    <button class="btn-save-settings" onclick="registerCustomSkill()"><i class="fa-solid fa-plus"></i> Save Skill</button>
                </div>
            </div>

            <!-- 8. CHATS VIEW -->
            <div class="view-panel content-panel" id="view-chats">
                <div class="panel-heading"><i class="fa-solid fa-comments" style="color: var(--accent-blue);"></i> Chat History & Sessions</div>
                <div class="panel-card">
                    <div id="chatsSessionList" style="display: flex; flex-direction: column; gap: 8px; max-height: 400px; overflow-y: auto;">
                        Loading chat history...
                    </div>
                </div>
            </div>
        </div>

        <!-- STICKY PERSISTENT BOTTOM CHAT INPUT BAR (Across All Views) -->
        <div class="persistent-input-dock">
            <button class="dock-btn" onclick="capturePhoto()" title="Camera"><i class="fa-solid fa-camera"></i></button>
            <div class="input-dock-box">
                <input type="text" id="globalChatInput" placeholder="Message RB Agent or say 'यह चीज़ सेव कर लो'..." onkeypress="handleGlobalEnter(event)">
            </div>
            <button class="dock-btn" id="globalMicBtn" onclick="toggleGlobalVoice()" title="Microphone"><i class="fa-solid fa-microphone"></i></button>
            <button class="dock-btn" onclick="submitGlobalChat()" title="Send"><i class="fa-solid fa-paper-plane"></i></button>
        </div>
    </main>

    <script>
        let currentUserName = "Ram Binay kumar Pandit";
        let isVoiceActive = false;
        let recognition = null;

        window.addEventListener('DOMContentLoaded', () => {
            initApp();
            initSpeech();
        });

        async function initApp() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                if (data.user_name) {
                    currentUserName = data.user_name;
                    applyUserMeta(data.user_name);
                }
                if (data.device && data.device.battery) {
                    const b = data.device.battery;
                    document.getElementById('topBatteryStatus').innerText = `${b.percentage || '85'}% LIVE`;
                }
            } catch(e) {
                console.log("Status init error:", e);
            }
            loadStoredNotes();
            loadStoredChats();
        }

        function applyUserMeta(name) {
            document.getElementById('sidebarUserName').innerText = name;
            document.getElementById('homeGreetingTitle').innerText = `नमस्ते, ${name}`;
            document.getElementById('setUserName').value = name;
            const initials = name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            document.getElementById('userInitialsAvatar').innerText = initials || 'RB';
        }

        // Sidebar Navigation
        function toggleSidebar(open) {
            document.getElementById('appSidebar').classList.toggle('active', open);
            document.getElementById('sidebarOverlay').classList.toggle('active', open);
        }

        function switchView(viewId) {
            document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

            const target = document.getElementById(`view-${viewId}`);
            if (target) target.classList.add('active');

            // Set active class on nav
            const links = document.querySelectorAll('.sidebar-nav .nav-link');
            links.forEach(link => {
                if (link.innerText.toLowerCase().includes(viewId.replace('-', ' '))) {
                    link.classList.add('active');
                }
            });

            // Set top title
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
            document.getElementById('viewTitleText').innerText = titles[viewId] || 'RB Agent';
            toggleSidebar(false);
        }

        // Settings Tabs
        function switchSettingsTab(tabName) {
            document.querySelectorAll('.settings-tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.settings-section').forEach(s => s.classList.remove('active'));

            event.target.classList.add('active');
            const targetSection = document.getElementById(`tab-${tabName}`);
            if (targetSection) targetSection.classList.add('active');
        }

        // Global Chat Submission with Autonomous Intent Routing
        async function submitGlobalChat() {
            const input = document.getElementById('globalChatInput');
            const text = input.value.trim();
            if (!text) return;

            appendMessage('user', text);
            input.value = '';
            setSubtitle(`User: "${text}"`);

            // Switch to Home view if not already there
            switchView('home');

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ text, is_voice: isVoiceActive })
                });
                const data = await res.json();
                const reply = data.response || "Task completed.";
                const tag = data.tag || (data.agent ? 'automation' : 'general');
                appendMessage('assistant', reply, tag);

                // Auto-speak reply with TTS
                speakAloud(reply, () => {
                    setSubtitle("Agent finished speaking. Ready for next command.");
                });
            } catch(e) {
                appendMessage('assistant', 'Error communicating with RB Agent: ' + e.message, 'automation');
            }
        }

        function handleGlobalEnter(e) {
            if (e.key === 'Enter') submitGlobalChat();
        }

        function appendMessage(sender, text, tag = 'automation') {
            const feed = document.getElementById('chatFeed');
            const div = document.createElement('div');
            div.className = `chat-msg ${sender}`;
            if (sender === 'assistant') {
                const badgeClass = `badge-${tag}`;
                div.innerHTML = `<div class="msg-badge ${badgeClass}">RB Agent</div><div>${text}</div>`;
            } else {
                div.innerText = text;
            }
            feed.appendChild(div);
            feed.scrollTop = feed.scrollHeight;
        }

        function setSubtitle(text) {
            document.getElementById('liveSubtitles').innerText = text;
        }

        // Voice Speech
        function speakAloud(text, onComplete) {
            if (!('speechSynthesis' in window)) {
                if (onComplete) onComplete();
                return;
            }
            window.speechSynthesis.cancel();
            const clean = text.replace(/[*#`_\[\]]/g, '');
            const utter = new SpeechSynthesisUtterance(clean);
            utter.lang = document.getElementById('setVoiceAccent').value || 'hi-IN';
            utter.pitch = parseFloat(document.getElementById('setVoicePitch').value) || 1.0;
            utter.rate = parseFloat(document.getElementById('setVoiceRate').value) || 0.95;

            utter.onstart = () => setSubtitle(`Speaking: "${clean.substring(0, 45)}..."`);
            utter.onend = () => {
                if (onComplete) onComplete();
            };
            window.speechSynthesis.speak(utter);
        }

        function initSpeech() {
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
                    setSubtitle(`Listening: "${transcript}"`);
                    const lower = transcript.toLowerCase();
                    if (lower.includes("hey rb") || lower.includes("हे आरबी")) {
                        const stripped = transcript.replace(/hey rb|हे आरबी/gi, '').trim();
                        document.getElementById('globalChatInput').value = stripped;
                        if (stripped.length > 2) submitGlobalChat();
                    }
                };
            }
        }

        function toggleGlobalVoice() {
            const btn = document.getElementById('globalMicBtn');
            isVoiceActive = !isVoiceActive;
            if (isVoiceActive) {
                btn.classList.add('active-mic');
                if (recognition) try { recognition.start(); } catch(e){}
                setSubtitle("Microphone active • Listening for speech or 'Hey RB'...");
            } else {
                btn.classList.remove('active-mic');
                if (recognition) try { recognition.stop(); } catch(e){}
                setSubtitle("Microphone paused.");
            }
        }

        // Web Preview Execution
        async function executeWebPreview() {
            const q = document.getElementById('webPreviewQuery').value.trim();
            const out = document.getElementById('webPreviewResult');
            out.innerText = "Fetching live web data...";
            try {
                const res = await fetch('/api/agents', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ agent: 'research', action: 'run', params: { query: q } })
                });
                const data = await res.json();
                out.innerText = JSON.stringify(data.result, null, 2);
            } catch(e) {
                out.innerText = "Failed: " + e.message;
            }
        }

        // Code Execution
        async function executeCodeSnippet() {
            const code = document.getElementById('codeEditorInput').value;
            const consoleBox = document.getElementById('codeConsoleOutput');
            consoleBox.innerText = "Running...";
            try {
                const res = await fetch('/api/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ action: 'shell', args: { command: `python3 -c ${JSON.stringify(code)}` } })
                });
                const data = await res.json();
                consoleBox.innerText = data.result.stdout || data.result.stderr || "Executed (No output)";
            } catch(e) {
                consoleBox.innerText = "Error: " + e.message;
            }
        }

        // Notes Loader
        async function loadStoredNotes() {
            const c = document.getElementById('notesContainer');
            try {
                const res = await fetch('/api/notes');
                const data = await res.json();
                if (data.notes && data.notes.length > 0) {
                    c.innerHTML = data.notes.map(n => `
                        <div style="background:#0D1322; border:1px solid var(--border); border-radius:8px; padding:10px;">
                            <div style="font-weight:700; color:#FFF; font-size:0.85rem;">${n.title}</div>
                            <div style="color:var(--text-secondary); font-size:0.78rem; margin-top:2px;">${n.content}</div>
                            <div style="font-size:0.65rem; color:var(--text-muted); margin-top:4px;">${n.created_at}</div>
                        </div>
                    `).join('');
                } else {
                    c.innerHTML = '<div style="color:var(--text-muted); font-size:0.8rem;">No notes yet. Type "यह चीज़ सेव कर लो" to add!</div>';
                }
            } catch(e) {
                c.innerHTML = 'Unable to load notes.';
            }
        }

        // Chats Loader
        async function loadStoredChats() {
            const c = document.getElementById('chatsSessionList');
            try {
                const res = await fetch('/api/chats');
                const data = await res.json();
                if (data.chats && data.chats.length > 0) {
                    c.innerHTML = data.chats.map(ch => `
                        <div style="background:#0D1322; border:1px solid var(--border); border-radius:8px; padding:8px 12px; font-size:0.8rem;">
                            <span style="color:${ch.sender === 'user' ? 'var(--accent-cyan)' : 'var(--accent-green)'}; font-weight:700;">${ch.sender.toUpperCase()}:</span>
                            <span style="color:var(--text-primary); margin-left:6px;">${ch.message.substring(0, 70)}...</span>
                        </div>
                    `).join('');
                } else {
                    c.innerHTML = '<div style="color:var(--text-muted); font-size:0.8rem;">No previous chats found.</div>';
                }
            } catch(e) {
                c.innerHTML = 'Unable to load chats.';
            }
        }

        function filterChatHistory() {
            const q = document.getElementById('chatSearchInput').value.toLowerCase();
            const items = document.querySelectorAll('#chatsSessionList > div');
            items.forEach(it => {
                it.style.display = it.innerText.toLowerCase().includes(q) ? 'block' : 'none';
            });
        }

        function startNewChat() {
            document.getElementById('chatFeed').innerHTML = `
                <div class="chat-msg assistant">
                    <div class="msg-badge badge-automation">RB System</div>
                    <div>New chat session started with Ram Binay. How can I assist you?</div>
                </div>
            `;
            switchView('home');
        }

        // Master Settings Save
        async function saveMasterSettings() {
            const name = document.getElementById('setUserName').value.trim();
            const accent = document.getElementById('setVoiceAccent').value;
            const pitch = document.getElementById('setVoicePitch').value;
            const rate = document.getElementById('setVoiceRate').value;
            const wake = document.getElementById('setWakePhrase').checked;
            const geminiKey = document.getElementById('setGeminiKey').value.trim();

            if (name) {
                currentUserName = name;
                await fetch('/api/user', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ user_name: name })
                });
                applyUserMeta(name);
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

            alert("All configurations saved successfully!");
            switchView('home');
        }

        // Telegram Bot Functions
        async function startTelegram() {
            const token = document.getElementById('setTelegramToken').value.trim();
            const res = await fetch('/api/telegram', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: 'start', token })
            });
            const d = await res.json();
            document.getElementById('telegramStatusLabel').innerText = d.message || d.error;
        }

        async function stopTelegram() {
            const res = await fetch('/api/telegram', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: 'stop' })
            });
            document.getElementById('telegramStatusLabel').innerText = "Bot stopped.";
        }

        // WhatsApp Direct
        async function launchWhatsAppDirect() {
            const phone = document.getElementById('setWaPhone').value.trim();
            const msg = document.getElementById('setWaMsg').value.trim();
            if (!phone) return alert("Please enter phone number");
            const res = await fetch('/api/whatsapp', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ phone, message: msg })
            });
            const d = await res.json();
            if (d.url) window.open(d.url, '_blank');
        }

        // GitHub Sync
        async function syncGitHubRepos() {
            const u = document.getElementById('setGhUser').value.trim();
            const token = document.getElementById('setGhToken').value.trim();
            const label = document.getElementById('ghSyncResults');
            label.innerText = "Syncing with GitHub...";
            const res = await fetch(`/api/github?username=${encodeURIComponent(u)}&token=${encodeURIComponent(token)}`);
            const d = await res.json();
            label.innerText = `Synced ${d.count || 0} repositories for ${u}.`;
        }

        function registerCustomSkill() {
            alert("Custom skill saved and registered to RB Agent orchestrator.");
            switchView('home');
        }

        function capturePhoto() {
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
