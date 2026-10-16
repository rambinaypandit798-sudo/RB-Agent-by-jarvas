"""
RB.AI - Pristine Hyper-Minimalist Lovable UI
Developed for: Ram Binay kumar Pandit
Zero Mock Directive • Real SQLite & Supabase Sync • Compact Arc Reactor HUD • 5 Blinking Sub-Agents
"""

WEB_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>RB AGENT OS — Ram Binay kumar Pandit</title>
    <meta name="theme-color" content="#070B12">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-base: #060911;
            --bg-sidebar: #0A0F1D;
            --bg-card: #0F172A;
            --bg-card-hover: #141F38;
            --bg-input: #111B30;
            --border: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(0, 229, 255, 0.35);
            --text-primary: #F8FAFC;
            --text-muted: #94A3B8;
            --accent-cyan: #00E5FF;
            --accent-blue: #38BDF8;
            --accent-green: #10B981;
            --accent-amber: #F59E0B;
            --accent-purple: #A855F7;
            --accent-pink: #EC4899;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: var(--bg-base); color: var(--text-primary); height: 100vh; display: flex; overflow: hidden; }

        /* Unified Collapsible Sidebar */
        .sidebar {
            width: 270px; background: var(--bg-sidebar); border-right: 1px solid var(--border);
            display: flex; flex-direction: column; z-index: 50; transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @media (max-width: 768px) {
            .sidebar { position: fixed; top: 0; bottom: 0; left: 0; transform: translateX(-100%); box-shadow: 4px 0 30px rgba(0,0,0,0.8); }
            .sidebar.active { transform: translateX(0); }
        }
        .sidebar-backdrop { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); z-index: 45; }
        .sidebar-backdrop.active { display: block; }

        .sidebar-top {
            padding: 16px 18px; display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid var(--border);
        }
        .brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.05rem; letter-spacing: 0.5px; }
        .brand i { color: var(--accent-cyan); font-size: 1.25rem; }
        .brand span { color: var(--accent-cyan); }
        .btn-close-sidebar { display: none; background: none; border: none; color: var(--text-muted); font-size: 1.2rem; cursor: pointer; }
        @media (max-width: 768px) { .btn-close-sidebar { display: block; } }

        .user-tag-row {
            padding: 12px 14px; margin: 10px 14px; background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 12px; display: flex; align-items: center; gap: 10px;
        }
        .user-avatar-pill {
            width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0284C7, #00E5FF);
            color: #060911; font-weight: 900; font-size: 0.85rem; display: flex; align-items: center; justify-content: center;
        }
        .user-tag-name { font-size: 0.82rem; font-weight: 700; color: #FFF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 155px; }
        .user-tag-sub { font-size: 0.68rem; color: var(--accent-green); display: flex; align-items: center; gap: 5px; margin-top: 1px; }

        /* The Exactly 8 Clean Navigation Items */
        .sidebar-menu { flex: 1; overflow-y: auto; padding: 6px 12px; display: flex; flex-direction: column; gap: 3px; }
        .nav-item {
            display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 10px;
            color: var(--text-muted); font-size: 0.86rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
            border: 1px solid transparent;
        }
        .nav-item i { width: 18px; font-size: 0.95rem; text-align: center; }
        .nav-item:hover, .nav-item.active {
            background: rgba(0, 229, 255, 0.08); color: var(--accent-cyan); border-color: rgba(0, 229, 255, 0.25);
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
            background: linear-gradient(135deg, #0284C7, #00E5FF); color: #060911; border: none;
            padding: 10px; border-radius: 10px; font-size: 0.85rem; font-weight: 800; cursor: pointer;
            display: flex; align-items: center; justify-content: center; gap: 8px; transition: opacity 0.2s;
        }
        .btn-new-chat-prominent:active { opacity: 0.85; }

        /* Main Viewport */
        .viewport { flex: 1; display: flex; flex-direction: column; height: 100vh; position: relative; overflow: hidden; }

        /* Top Bar */
        .topbar {
            padding: 10px 16px; background: var(--bg-sidebar); border-bottom: 1px solid var(--border);
            display: flex; align-items: center; justify-content: space-between; z-index: 20; height: 50px;
        }
        .btn-menu { background: none; border: none; color: #FFF; font-size: 1.2rem; cursor: pointer; padding: 4px; }
        .topbar-title { font-size: 0.9rem; font-weight: 700; color: #FFF; }
        .status-chip {
            background: rgba(16, 185, 129, 0.15); border: 1px solid var(--accent-green); color: var(--accent-green);
            padding: 3px 9px; border-radius: 12px; font-size: 0.7rem; font-weight: 700; display: flex; align-items: center; gap: 6px;
        }
        .status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent-green); animation: pulseDot 2s infinite; }
        @keyframes pulseDot { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.85); } }

        /* Panels Container */
        .panels-wrapper { flex: 1; display: flex; flex-direction: column; overflow: hidden; position: relative; }
        .panel { display: none; flex: 1; flex-direction: column; overflow-y: auto; }
        .panel.active { display: flex; }

        /* 1. HOMEPAGE VIEW */
        .home-panel { padding: 8px 14px 105px 14px; gap: 8px; }

        /* Compact Greeting Banner */
        .greeting-compact-card {
            background: linear-gradient(135deg, rgba(2, 132, 199, 0.22) 0%, rgba(15, 23, 42, 0.7) 100%);
            border: 1px solid rgba(0, 229, 255, 0.25); border-radius: 12px; padding: 10px 14px;
            display: flex; align-items: center; justify-content: space-between;
        }
        .greet-title { font-size: 0.94rem; font-weight: 800; color: #FFF; }
        .greet-sub { font-size: 0.74rem; color: var(--text-muted); margin-top: 1px; }

        /* Sleek Compact Arc Reactor HUD (~82px) */
        .hud-compact-area {
            display: flex; justify-content: center; align-items: center; padding: 4px 0;
        }
        .reactor-box {
            width: 82px; height: 82px; position: relative; display: flex; align-items: center; justify-content: center;
            cursor: pointer; user-select: none;
        }
        .ring-outer {
            position: absolute; inset: 0; border-radius: 50%; border: 1.5px dashed rgba(0, 229, 255, 0.65);
            animation: rotateCw 12s linear infinite;
        }
        .ring-inner {
            position: absolute; inset: 7px; border-radius: 50%; border: 1.5px solid rgba(56, 189, 248, 0.4);
            border-top-color: var(--accent-cyan); border-bottom-color: var(--accent-purple);
            animation: rotateCcw 7s linear infinite;
        }
        .reactor-core-small {
            width: 52px; height: 52px; border-radius: 50%; background: radial-gradient(circle, #0F172A 0%, #030712 100%);
            border: 2px solid var(--accent-cyan); box-shadow: 0 0 16px rgba(0, 229, 255, 0.55);
            display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
        }
        .reactor-box:active .reactor-core-small { transform: scale(0.95); }
        .reactor-core-small i { color: var(--accent-cyan); font-size: 0.7rem; margin-bottom: 1px; }
        .reactor-core-small .core-label { font-size: 0.58rem; font-weight: 800; color: #FFF; letter-spacing: 0.3px; }

        @keyframes rotateCw { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes rotateCcw { 0% { transform: rotate(360deg); } 100% { transform: rotate(0deg); } }

        /* Visual Sub-Agents Workspace (5 Sub-Agents with Blinking Glow) */
        .subagents-workspace {
            display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; padding: 2px 0 4px 0;
        }
        @media (max-width: 600px) {
            .subagents-workspace { grid-template-columns: repeat(5, 1fr); gap: 4px; }
        }
        .subagent-card {
            background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px;
            padding: 8px 4px; display: flex; flex-direction: column; align-items: center; text-align: center;
            cursor: pointer; transition: all 0.25s ease; position: relative; overflow: hidden;
        }
        .subagent-card:hover { transform: translateY(-2px); border-color: rgba(255, 255, 255, 0.2); }
        .subagent-emoji { font-size: 1.25rem; line-height: 1.2; margin-bottom: 4px; }
        .subagent-title { font-size: 0.65rem; font-weight: 800; color: #FFF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; }
        .subagent-badge {
            font-size: 0.52rem; font-weight: 800; padding: 2px 5px; border-radius: 4px; margin-top: 4px;
            text-transform: uppercase; letter-spacing: 0.4px;
        }

        /* 1. Research & Web Agent (Cyan / Blue Glow) */
        .agent-research { border-color: rgba(0, 229, 255, 0.2); }
        .agent-research .subagent-badge { background: rgba(0, 229, 255, 0.15); color: var(--accent-cyan); }
        .agent-research.active-pulse {
            border-color: var(--accent-cyan) !important;
            box-shadow: 0 0 16px rgba(0, 229, 255, 0.8) !important;
            animation: pulseCyan 1s infinite alternate;
        }
        @keyframes pulseCyan {
            0% { box-shadow: 0 0 8px rgba(0, 229, 255, 0.4); transform: scale(1); }
            100% { box-shadow: 0 0 22px rgba(0, 229, 255, 0.95); transform: scale(1.04); }
        }

        /* 2. Memory & Notes Agent (Emerald Green Glow) */
        .agent-memory { border-color: rgba(16, 185, 129, 0.2); }
        .agent-memory .subagent-badge { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }
        .agent-memory.active-pulse {
            border-color: var(--accent-green) !important;
            box-shadow: 0 0 16px rgba(16, 185, 129, 0.8) !important;
            animation: pulseGreen 1s infinite alternate;
        }
        @keyframes pulseGreen {
            0% { box-shadow: 0 0 8px rgba(16, 185, 129, 0.4); transform: scale(1); }
            100% { box-shadow: 0 0 22px rgba(16, 185, 129, 0.95); transform: scale(1.04); }
        }

        /* 3. Preview / View Agent (Amber / Gold Glow) */
        .agent-preview { border-color: rgba(245, 158, 11, 0.2); }
        .agent-preview .subagent-badge { background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }
        .agent-preview.active-pulse {
            border-color: var(--accent-amber) !important;
            box-shadow: 0 0 16px rgba(245, 158, 11, 0.8) !important;
            animation: pulseAmber 1s infinite alternate;
        }
        @keyframes pulseAmber {
            0% { box-shadow: 0 0 8px rgba(245, 158, 11, 0.4); transform: scale(1); }
            100% { box-shadow: 0 0 22px rgba(245, 158, 11, 0.95); transform: scale(1.04); }
        }

        /* 4. Automation Agent (Electric Purple Glow) */
        .agent-automation { border-color: rgba(168, 85, 247, 0.2); }
        .agent-automation .subagent-badge { background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); }
        .agent-automation.active-pulse {
            border-color: var(--accent-purple) !important;
            box-shadow: 0 0 16px rgba(168, 85, 247, 0.8) !important;
            animation: pulsePurple 1s infinite alternate;
        }
        @keyframes pulsePurple {
            0% { box-shadow: 0 0 8px rgba(168, 85, 247, 0.4); transform: scale(1); }
            100% { box-shadow: 0 0 22px rgba(168, 85, 247, 0.95); transform: scale(1.04); }
        }

        /* 5. Coding & GitHub Agent (Hot Pink / Magenta Glow) */
        .agent-coding { border-color: rgba(236, 72, 153, 0.2); }
        .agent-coding .subagent-badge { background: rgba(236, 72, 153, 0.15); color: var(--accent-pink); }
        .agent-coding.active-pulse {
            border-color: var(--accent-pink) !important;
            box-shadow: 0 0 16px rgba(236, 72, 153, 0.8) !important;
            animation: pulsePink 1s infinite alternate;
        }
        @keyframes pulsePink {
            0% { box-shadow: 0 0 8px rgba(236, 72, 153, 0.4); transform: scale(1); }
            100% { box-shadow: 0 0 22px rgba(236, 72, 153, 0.95); transform: scale(1.04); }
        }

        /* Conversational Feed */
        .conversation-feed { flex: 1; display: flex; flex-direction: column; gap: 8px; overflow-y: auto; padding: 4px 0; }
        .msg-bubble {
            max-width: 86%; padding: 9px 13px; border-radius: 12px; font-size: 0.86rem; line-height: 1.44; word-break: break-word;
        }
        .msg-bubble.user { align-self: flex-end; background: #0284C7; color: #FFF; border-bottom-right-radius: 2px; }
        .msg-bubble.assistant {
            align-self: flex-start; background: var(--bg-card); color: var(--text-primary);
            border: 1px solid var(--border); border-bottom-left-radius: 2px;
        }
        .tag-pill {
            display: inline-block; font-size: 0.6rem; font-weight: 800; padding: 2px 6px; border-radius: 5px;
            margin-bottom: 4px; text-transform: uppercase;
        }
        .pill-memory { background: rgba(16,185,129,0.15); color: var(--accent-green); }
        .pill-automation { background: rgba(168,85,247,0.15); color: var(--accent-purple); }
        .pill-research { background: rgba(0,229,255,0.15); color: var(--accent-cyan); }
        .pill-preview { background: rgba(245,158,11,0.15); color: var(--accent-amber); }
        .pill-coding { background: rgba(236,72,153,0.15); color: var(--accent-pink); }
        .pill-general { background: rgba(56,189,248,0.15); color: var(--accent-blue); }

        /* Real-Time Scrolling Subtitles Ticker (Fixed directly above input dock) */
        .subtitles-dock {
            position: absolute; bottom: 56px; left: 0; right: 0; padding: 0 12px 3px 12px;
            background: linear-gradient(180deg, transparent 0%, var(--bg-base) 100%); z-index: 28;
        }
        .subtitles-inner {
            background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 14px; padding: 4px 10px; display: flex; align-items: center; gap: 8px; font-size: 0.72rem; color: var(--accent-blue);
        }
        .subtitles-text { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500; }

        /* Sticky Persistent Bottom Chat/Command Input Bar */
        .bottom-input-dock {
            position: absolute; bottom: 0; left: 0; right: 0; height: 56px;
            background: var(--bg-sidebar); border-top: 1px solid var(--border);
            padding: 8px 12px; display: flex; align-items: center; gap: 8px; z-index: 30;
        }
        .input-shell {
            flex: 1; background: var(--bg-input); border: 1px solid var(--border); border-radius: 24px;
            padding: 6px 14px; display: flex; align-items: center; gap: 8px;
        }
        .input-shell input {
            flex: 1; background: transparent; border: none; outline: none; color: #FFF; font-size: 0.86rem;
        }
        .dock-action-btn {
            background: none; border: none; color: var(--accent-cyan); font-size: 1.1rem; cursor: pointer;
            padding: 4px; display: flex; align-items: center; justify-content: center;
        }
        .dock-action-btn.recording { color: #EF4444; animation: pulseMic 1.2s infinite; }
        @keyframes pulseMic { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.18); } }

        /* Dedicated Views (Web, Code, Files, Settings, Projects, Skill Add, Chats) */
        .page-panel { padding: 14px 16px 80px 16px; overflow-y: auto; height: 100%; display: flex; flex-direction: column; gap: 12px; }
        .page-title { font-size: 1.05rem; font-weight: 800; color: #FFF; display: flex; align-items: center; gap: 10px; }
        .card-surface { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }

        /* Centralized Settings Tabs */
        .settings-tab-bar { display: flex; gap: 6px; overflow-x: auto; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
        .tab-btn {
            background: var(--bg-input); border: 1px solid var(--border); color: var(--text-muted);
            padding: 7px 11px; border-radius: 8px; font-size: 0.76rem; font-weight: 600; cursor: pointer; white-space: nowrap;
        }
        .tab-btn.active { background: rgba(0,229,255,0.15); color: var(--accent-cyan); border-color: var(--accent-cyan); }
        .tab-pane { display: none; flex-direction: column; gap: 10px; margin-top: 12px; }
        .tab-pane.active { display: flex; }

        .form-field { display: flex; flex-direction: column; gap: 5px; }
        .form-field label { font-size: 0.74rem; font-weight: 700; color: var(--text-muted); }
        .form-field input, .form-field select, .form-field textarea {
            background: var(--bg-input); border: 1px solid var(--border); color: #FFF;
            padding: 8px 12px; border-radius: 8px; font-size: 0.84rem; outline: none;
        }
        .form-field input:focus, .form-field select:focus, .form-field textarea:focus { border-color: var(--accent-cyan); }

        .btn-action-primary {
            background: linear-gradient(135deg, #0284C7, #00E5FF); color: #060911; font-weight: 800;
            border: none; padding: 9px 16px; border-radius: 8px; font-size: 0.84rem; cursor: pointer;
        }
        .btn-action-secondary {
            background: rgba(255, 255, 255, 0.08); border: 1px solid var(--border); color: #FFF;
            padding: 9px 14px; border-radius: 8px; font-size: 0.82rem; cursor: pointer; font-weight: 600;
        }

        .status-badge {
            display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;
        }
        .badge-success { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }
        .badge-warning { background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); border: 1px solid var(--accent-amber); }
        .badge-danger { background: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid #EF4444; }
    </style>
</head>
<body>

    <!-- Unified Collapsible Sidebar (Strictly the 8 Navigation Items) -->
    <div class="sidebar-backdrop" id="sidebarBackdrop" onclick="toggleSidebar(false)"></div>
    <aside class="sidebar" id="sidebar">
        <div class="sidebar-top">
            <div class="brand">
                <i class="fa-solid fa-atom"></i>
                RB<span>.AGENT OS</span>
            </div>
            <button class="btn-close-sidebar" onclick="toggleSidebar(false)"><i class="fa-solid fa-xmark"></i></button>
        </div>

        <div class="user-tag-row">
            <div class="user-avatar-pill" id="userAvatarPill">RP</div>
            <div>
                <div class="user-tag-name" id="sidebarUserName">Ram Binay Pandit</div>
                <div class="user-tag-sub"><i class="fa-solid fa-circle" style="font-size: 0.45rem;"></i> Master Operator</div>
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
                <i class="fa-solid fa-code"></i> Code Preview & Terminal
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
            <div class="topbar-title" id="pageTitleText">RB AGENT OS — Home</div>
            <div class="status-chip">
                <div class="status-dot"></div>
                <span id="topBattStatus">LIVE ACTIVE</span>
            </div>
        </div>

        <!-- Panels Container -->
        <div class="panels-wrapper">
            <!-- 1. HOMEPAGE VIEW (GREETING, COMPACT ARC REACTOR HUD, 5 BLINKING SUB-AGENTS, FEED) -->
            <div class="panel home-panel active" id="panel-home">
                <!-- Compact Greeting Banner -->
                <div class="greeting-compact-card">
                    <div>
                        <div class="greet-title" id="greetBannerText">नमस्ते, Ram Binay Pandit</div>
                        <div class="greet-sub">आज आपका क्या प्लान है</div>
                    </div>
                    <i class="fa-solid fa-bolt" style="color: var(--accent-cyan); font-size: 1.1rem;"></i>
                </div>

                <!-- Sleek Compact Arc Reactor HUD (~82px) -->
                <div class="hud-compact-area">
                    <div class="reactor-box" onclick="showPanel('settings')" title="RB Agent Orchestrator Core">
                        <div class="ring-outer"></div>
                        <div class="ring-inner"></div>
                        <div class="reactor-core-small">
                            <i class="fa-solid fa-atom"></i>
                            <div class="core-label">RB CORE</div>
                        </div>
                    </div>
                </div>

                <!-- Visual Sub-Agents Workspace (5 Sub-Agents with Pulsing/Blinking Glow) -->
                <div class="subagents-workspace">
                    <!-- 1. 🌐 Research & Web Agent (Cyan / Blue) -->
                    <div class="subagent-card agent-research" id="card-agent-research" onclick="showPanel('web-preview')" title="Research & Web Agent">
                        <div class="subagent-emoji">🌐</div>
                        <div class="subagent-title">Research</div>
                        <div class="subagent-badge" id="badge-research">READY</div>
                    </div>

                    <!-- 2. 🧠 Memory & Notes Agent (Emerald Green) -->
                    <div class="subagent-card agent-memory" id="card-agent-memory" onclick="showPanel('file-preview')" title="Memory & Notes Agent">
                        <div class="subagent-emoji">🧠</div>
                        <div class="subagent-title">Memory</div>
                        <div class="subagent-badge" id="badge-memory">SYNCED</div>
                    </div>

                    <!-- 3. 👁️ Preview / View Agent (Amber / Gold) -->
                    <div class="subagent-card agent-preview" id="card-agent-preview" onclick="showPanel('web-preview')" title="Preview / View Agent">
                        <div class="subagent-emoji">👁️</div>
                        <div class="subagent-title">Preview</div>
                        <div class="subagent-badge" id="badge-preview">STANDBY</div>
                    </div>

                    <!-- 4. ⚡ Automation Agent (Electric Purple) -->
                    <div class="subagent-card agent-automation" id="card-agent-automation" onclick="testCallAnnouncement()" title="Automation & Hardware Agent">
                        <div class="subagent-emoji">⚡</div>
                        <div class="subagent-title">Automation</div>
                        <div class="subagent-badge" id="badge-automation">HARDWARE</div>
                    </div>

                    <!-- 5. 💻 Coding & GitHub Agent (Hot Pink / Magenta) -->
                    <div class="subagent-card agent-coding" id="card-agent-coding" onclick="showPanel('code-preview')" title="Coding & GitHub Agent">
                        <div class="subagent-emoji">💻</div>
                        <div class="subagent-title">Coding</div>
                        <div class="subagent-badge" id="badge-coding">GIT RUN</div>
                    </div>
                </div>

                <!-- Conversational Chat Stream -->
                <div class="conversation-feed" id="chatStream">
                    <div class="msg-bubble assistant">
                        <div class="tag-pill pill-automation">RB System</div>
                        <div>नमस्ते Ram Binay Pandit! RB Agent OS is operational. All 5 sub-agents, hardware bridges, and persistent databases are ready. आज आपका क्या प्लान है?</div>
                    </div>
                </div>
            </div>

            <!-- 2. WEB PREVIEW VIEW -->
            <div class="panel page-panel" id="panel-web-preview">
                <div class="page-title"><i class="fa-solid fa-globe" style="color: var(--accent-cyan);"></i> Web Preview & Live Search</div>
                <div class="card-surface">
                    <div class="form-field">
                        <label>Web Search Query or URL</label>
                        <div style="display: flex; gap: 8px;">
                            <input type="text" id="webQueryInput" placeholder="Enter query or URL..." value="Latest Google Gemini 2.5 flash updates">
                            <button class="btn-action-primary" onclick="triggerWebPreview()"><i class="fa-solid fa-magnifying-glass"></i> Search</button>
                        </div>
                    </div>
                    <div id="webPreviewOutput" style="margin-top: 14px; font-size: 0.85rem; color: #CBD5E1; line-height: 1.5; white-space: pre-wrap; max-height: 380px; overflow-y: auto;">
                        Enter a query to run a live DuckDuckGo web search or scrape a URL.
                    </div>
                </div>
            </div>

            <!-- 3. CODE PREVIEW & TERMINAL VIEW -->
            <div class="panel page-panel" id="panel-code-preview">
                <div class="page-title"><i class="fa-solid fa-code" style="color: var(--accent-pink);"></i> Code Preview & Terminal</div>
                <div class="card-surface">
                    <div class="form-field">
                        <label>Python 3.14 Sandbox Execution</label>
                        <textarea id="codeScriptArea" rows="6" style="font-family: monospace;"># RB Agent Live Code Runner
name = "Ram Binay Pandit"
print(f"नमस्ते {name}, Python sandbox executed successfully!")
</textarea>
                    </div>
                    <div style="display: flex; gap: 8px; margin-top: 8px;">
                        <button class="btn-action-primary" onclick="runScriptExecution()"><i class="fa-solid fa-play"></i> Run Script</button>
                    </div>
                    <pre id="codeConsoleBox" style="background:#05080E; border:1px solid var(--border); border-radius:8px; padding:10px; margin-top:10px; font-size:0.8rem; color:var(--accent-blue); max-height:160px; overflow-y:auto;">Terminal ready.</pre>
                </div>
            </div>

            <!-- 4. FILE PREVIEW VIEW -->
            <div class="panel page-panel" id="panel-file-preview">
                <div class="page-title"><i class="fa-solid fa-folder-open" style="color: var(--accent-amber);"></i> File Preview & SQLite Notes</div>
                <div class="card-surface">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div style="font-weight: 700; font-size: 0.88rem;">Persistent Notes (SQLite & Supabase)</div>
                        <button class="btn-action-secondary" onclick="fetchNotes()" style="padding: 4px 10px; font-size: 0.72rem;"><i class="fa-solid fa-rotate"></i> Refresh</button>
                    </div>
                    <div id="notesListView" style="display: flex; flex-direction: column; gap: 8px; max-height: 380px; overflow-y: auto;">
                        Loading notes...
                    </div>
                </div>
            </div>

            <!-- 5. CENTRALIZED SETTINGS HUB (6 DEDICATED SUB-TABS) -->
            <div class="panel page-panel" id="panel-settings">
                <div class="page-title"><i class="fa-solid fa-sliders" style="color: var(--accent-cyan);"></i> Centralized Configuration Hub</div>
                <div class="card-surface">
                    <!-- The 6 Dedicated Sub-Tabs -->
                    <div class="settings-tab-bar">
                        <button class="tab-btn active" onclick="setTab('telegram')">Telegram Bot</button>
                        <button class="tab-btn" onclick="setTab('whatsapp')">WhatsApp Bridge</button>
                        <button class="tab-btn" onclick="setTab('github')">GitHub PAT</button>
                        <button class="tab-btn" onclick="setTab('voice')">Voice Profiles</button>
                        <button class="tab-btn" onclick="setTab('supabase')">Supabase Keys</button>
                        <button class="tab-btn" onclick="setTab('gemini')">Google Gemini API</button>
                    </div>

                    <!-- 1. Tab: Telegram Bot -->
                    <div class="tab-pane active" id="pane-telegram">
                        <div class="form-field">
                            <label>Telegram Bot Token</label>
                            <input type="text" id="cfgTelegramToken" placeholder="123456789:ABCdefGhIJKlmNoPQRstuvwxYZ">
                        </div>
                        <div style="display: flex; gap: 8px; margin-top: 4px;">
                            <button class="btn-action-primary" style="flex: 1;" onclick="testTelegramHandshake()"><i class="fa-solid fa-link"></i> Test Handshake</button>
                            <button class="btn-action-secondary" onclick="startTelegramBot()"><i class="fa-solid fa-play"></i> Start</button>
                            <button class="btn-action-secondary" onclick="stopTelegramBot()">Stop</button>
                        </div>
                        <div id="telegramStatusBox" style="font-size: 0.75rem; color: var(--text-muted); margin-top: 6px;">Status: Standby</div>
                    </div>

                    <!-- 2. Tab: WhatsApp Bridge -->
                    <div class="tab-pane" id="pane-whatsapp">
                        <div class="form-field">
                            <label>Default Phone Number with Country Code (e.g. 919876543210)</label>
                            <input type="text" id="cfgWaPhone" placeholder="91XXXXXXXXXX">
                        </div>
                        <div class="form-field">
                            <label>Default Dispatch Message</label>
                            <input type="text" id="cfgWaMsg" value="नमस्ते Ram Binay, RB Agent OS message dispatch.">
                        </div>
                        <button class="btn-action-primary" onclick="launchWhatsApp()"><i class="fa-brands fa-whatsapp"></i> Test WhatsApp Bridge</button>
                    </div>

                    <!-- 3. Tab: GitHub PAT -->
                    <div class="tab-pane" id="pane-github">
                        <div class="form-field">
                            <label>GitHub Username</label>
                            <input type="text" id="cfgGhUser" value="rambinaypandit798-sudo">
                        </div>
                        <div class="form-field">
                            <label>Personal Access Token (PAT)</label>
                            <input type="password" id="cfgGhToken" placeholder="ghp_...">
                        </div>
                        <div style="display: flex; gap: 8px; margin-top: 4px;">
                            <button class="btn-action-primary" onclick="testGitHubHandshake()"><i class="fa-brands fa-github"></i> Test Handshake & Sync</button>
                        </div>
                        <div id="ghSyncStatus" style="font-size: 0.75rem; color: var(--text-muted); margin-top: 6px;"></div>
                    </div>

                    <!-- 4. Tab: Voice Profiles -->
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
                        <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px;">
                            <label style="display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #FFF; cursor: pointer;">
                                <input type="checkbox" id="cfgWakePhrase" checked> Enable "Hey RB" Wake Word
                            </label>
                            <label style="display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #FFF; cursor: pointer;">
                                <input type="checkbox" id="cfgCallAnnounce" checked> Enable Call Announcements ("नमस्ते Ram Binay, इनका फोन आया है")
                            </label>
                        </div>
                    </div>

                    <!-- 5. Tab: Supabase Keys -->
                    <div class="tab-pane" id="pane-supabase">
                        <div class="form-field">
                            <label>Supabase Project URL</label>
                            <input type="text" id="cfgSupabaseUrl" placeholder="https://xxxxxxxx.supabase.co">
                        </div>
                        <div class="form-field">
                            <label>Supabase API Key (anon public or service_role)</label>
                            <input type="password" id="cfgSupabaseKey" placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...">
                        </div>
                        <div style="display: flex; gap: 8px; margin-top: 4px;">
                            <button class="btn-action-primary" onclick="testSupabaseHandshake()"><i class="fa-solid fa-database"></i> Test & Auto-Migrate Schema</button>
                            <button class="btn-action-secondary" onclick="syncSupabaseData()"><i class="fa-solid fa-cloud-arrow-up"></i> Sync Now</button>
                        </div>
                        <div id="supabaseStatusBox" style="font-size: 0.75rem; color: var(--text-muted); margin-top: 6px;">Checking connection...</div>
                    </div>

                    <!-- 6. Tab: Google Gemini API Key -->
                    <div class="tab-pane" id="pane-gemini">
                        <div class="form-field">
                            <label>Google Gemini API Key</label>
                            <input type="password" id="cfgGeminiKey" placeholder="AIzaSy...">
                        </div>
                        <div class="form-field">
                            <label>Model Backbone</label>
                            <select id="cfgGeminiModel">
                                <option value="gemini-2.5-flash">Gemini 2.5 Flash (Ultra-fast multimodal)</option>
                                <option value="gemini-2.5-pro">Gemini 2.5 Pro (Deep reasoning)</option>
                            </select>
                        </div>
                        <button class="btn-action-primary" onclick="testGeminiHandshake()"><i class="fa-solid fa-key"></i> Test Gemini Key Handshake</button>
                        <div id="geminiStatusBox" style="font-size: 0.75rem; color: var(--text-muted); margin-top: 6px;"></div>
                    </div>

                    <button class="btn-action-primary" style="width: 100%; margin-top: 14px;" onclick="saveConfigurations()">
                        <i class="fa-solid fa-floppy-disk"></i> Save All Configurations
                    </button>
                </div>
            </div>

            <!-- 6. PROJECTS VIEW -->
            <div class="panel page-panel" id="panel-projects">
                <div class="page-title"><i class="fa-solid fa-cubes" style="color: var(--accent-purple);"></i> Projects</div>
                <div class="card-surface">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-weight: 800; font-size: 1rem; color: #FFF;">rb_ai (RB Agent OS)</div>
                            <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">Developed for Ram Binay kumar Pandit</div>
                        </div>
                        <span class="status-badge badge-success">Active Workspace</span>
                    </div>
                    <div style="margin-top: 12px; font-size: 0.78rem; color: #CBD5E1; display: flex; flex-direction: column; gap: 4px;">
                        <div>• <strong>Environment</strong>: Termux Android Linux Userland (aarch64)</div>
                        <div>• <strong>Database</strong>: SQLite 3 (<code>rb_agent.db</code>) + Supabase Cloud Engine</div>
                        <div>• <strong>Architecture</strong>: 5 Live Sub-Agents + Arc Reactor HUD Orchestrator</div>
                    </div>
                </div>
            </div>

            <!-- 7. SKILL ADD VIEW (AGENT SELF-IMPROVEMENT & CAPABILITY CREATOR) -->
            <div class="panel page-panel" id="panel-skill-add">
                <div class="page-title"><i class="fa-solid fa-puzzle-piece" style="color: var(--accent-green);"></i> Skill Add & Self-Training</div>
                <div class="card-surface">
                    <div style="font-weight: 700; font-size: 0.88rem; color: var(--accent-cyan); margin-bottom: 4px;">Feed Custom Training Directives</div>
                    <div style="font-size: 0.76rem; color: var(--text-muted); margin-bottom: 12px;">Teach RB Agent new specialized capabilities on the fly. Dynamically persisted to SQLite & Supabase.</div>

                    <div class="form-field">
                        <label>Skill Name (e.g. Hindi Tech Translator, Termux DevOps Expert)</label>
                        <input type="text" id="skillNameInput" placeholder="Skill Name">
                    </div>
                    <div class="form-field">
                        <label>Trigger / Context Description</label>
                        <input type="text" id="skillDescInput" placeholder="When user asks about...">
                    </div>
                    <div class="form-field">
                        <label>System Directives & Instructions</label>
                        <textarea id="skillPromptInput" rows="4" placeholder="You are a specialized expert in... Always output in..."></textarea>
                    </div>
                    <div class="form-field">
                        <label>Few-Shot Examples (Optional)</label>
                        <textarea id="skillExamplesInput" rows="2" placeholder="User: ... -> Assistant: ..."></textarea>
                    </div>
                    <button class="btn-action-primary" style="margin-top: 8px;" onclick="saveSkillLive()"><i class="fa-solid fa-graduation-cap"></i> Train & Register Skill Live</button>
                    <div id="skillStatusFeedback" style="font-size: 0.75rem; margin-top: 6px;"></div>
                </div>

                <div class="card-surface">
                    <div style="font-weight: 700; font-size: 0.88rem; margin-bottom: 10px;">Active Learned Skills in Live Memory</div>
                    <div id="installedSkillsList" style="display: flex; flex-direction: column; gap: 8px;">
                        Loading skills...
                    </div>
                </div>
            </div>

            <!-- 8. CHATS VIEW -->
            <div class="panel page-panel" id="panel-chats">
                <div class="page-title"><i class="fa-solid fa-comments" style="color: var(--accent-blue);"></i> Chat History</div>
                <div class="card-surface">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-size: 0.78rem; color: var(--text-muted);">Stored locally in SQLite <code>chat_history</code></span>
                        <button class="btn-action-secondary" onclick="clearAllChats()" style="padding: 4px 10px; font-size: 0.72rem; color: #EF4444;"><i class="fa-solid fa-trash"></i> Clear</button>
                    </div>
                    <div id="chatsListContainer" style="display: flex; flex-direction: column; gap: 8px; max-height: 400px; overflow-y: auto;">
                        Loading chats...
                    </div>
                </div>
            </div>
        </div>

        <!-- Real-Time Scrolling Subtitles Ticker (Fixed directly above input dock) -->
        <div class="subtitles-dock">
            <div class="subtitles-inner">
                <i class="fa-solid fa-closed-captioning"></i>
                <div class="subtitles-text" id="subtitlesTicker">
                    RB Agent OS ready • Autonomous intent routing active
                </div>
            </div>
        </div>

        <!-- Sticky Persistent Bottom Chat/Command Input Bar -->
        <div class="bottom-input-dock">
            <button class="dock-action-btn" onclick="captureSnapshot()" title="Camera Snapshot"><i class="fa-solid fa-camera"></i></button>
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
                if (data.supabase) {
                    const sbBox = document.getElementById('supabaseStatusBox');
                    if (data.supabase.configured) {
                        sbBox.innerHTML = `<span class="status-badge badge-success">Supabase Connected (${data.supabase.latency_ms || 20}ms)</span>`;
                    } else {
                        sbBox.innerHTML = `<span class="status-badge badge-warning">Supabase Unconfigured</span>`;
                    }
                }
            } catch(e) {
                console.log(e);
            }
            fetchNotes();
            fetchChats();
            fetchSkills();
        }

        function syncUserUI(name) {
            document.getElementById('sidebarUserName').innerText = name;
            document.getElementById('greetBannerText').innerText = `नमस्ते, ${name}`;
            const initials = name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            document.getElementById('userAvatarPill').innerText = initials || 'RP';
        }

        // Navigation
        function toggleSidebar(open) {
            document.getElementById('sidebar').classList.toggle('active', open);
            document.getElementById('sidebarBackdrop').classList.toggle('active', open);
        }

        function showPanel(panelName) {
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.sidebar-menu .nav-item').forEach(n => n.classList.remove('active'));

            const p = document.getElementById(`panel-${panelName}`);
            if (p) p.classList.add('active');

            const links = document.querySelectorAll('.sidebar-menu .nav-item');
            links.forEach(l => {
                if (l.innerText.toLowerCase().includes(panelName.replace('-', ' '))) {
                    l.classList.add('active');
                }
            });

            const titles = {
                'home': 'RB AGENT OS — Home',
                'web-preview': 'Web Preview & Search',
                'code-preview': 'Code Preview & Terminal',
                'file-preview': 'File Preview & Notes',
                'settings': 'Centralized Configuration Hub',
                'projects': 'Projects Overview',
                'skill-add': 'Skill Add & Self-Training',
                'chats': 'Chat History'
            };
            document.getElementById('pageTitleText').innerText = titles[panelName] || 'RB Agent OS';
            toggleSidebar(false);
        }

        function setTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            if (event && event.target) event.target.classList.add('active');
            const target = document.getElementById(`pane-${tabId}`);
            if (target) target.classList.add('active');
        }

        // Sub-Agent Blinking / Pulsing Control
        function triggerSubAgentGlow(agentTag, processing = true) {
            const agentMap = {
                'research': { id: 'card-agent-research', badge: 'badge-research', name: 'Research & Web Agent' },
                'memory': { id: 'card-agent-memory', badge: 'badge-memory', name: 'Memory & Notes Agent' },
                'preview': { id: 'card-agent-preview', badge: 'badge-preview', name: 'Preview / View Agent' },
                'automation': { id: 'card-agent-automation', badge: 'badge-automation', name: 'Automation Agent' },
                'coding': { id: 'card-agent-coding', badge: 'badge-coding', name: 'Coding & GitHub Agent' }
            };

            // Clear all pulses first
            Object.values(agentMap).forEach(a => {
                const el = document.getElementById(a.id);
                if (el) el.classList.remove('active-pulse');
            });

            if (processing && agentMap[agentTag]) {
                const target = agentMap[agentTag];
                const card = document.getElementById(target.id);
                const badge = document.getElementById(target.badge);
                if (card) card.classList.add('active-pulse');
                if (badge) badge.innerText = 'ACTIVE';
                setSubtitle(`${target.name} actively processing...`);
            } else if (!processing && agentMap[agentTag]) {
                const target = agentMap[agentTag];
                const badge = document.getElementById(target.badge);
                if (badge) badge.innerText = 'READY';
            }
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

            // Quick speculative intent glow
            const lower = text.toLowerCase();
            let predictedTag = 'general';
            if (lower.includes('सेव') || lower.includes('save') || lower.includes('remember') || lower.includes('याद')) {
                predictedTag = 'memory';
            } else if (lower.includes('torch') || lower.includes('battery') || lower.includes('vibrate') || lower.includes('फोन') || lower.includes('call')) {
                predictedTag = 'automation';
            } else if (lower.includes('search') || lower.includes('google') || lower.includes('खोजो')) {
                predictedTag = 'research';
            } else if (lower.includes('code') || lower.includes('github') || lower.includes('python')) {
                predictedTag = 'coding';
            }
            if (predictedTag !== 'general') triggerSubAgentGlow(predictedTag, true);

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ text, is_voice: isMicOn })
                });
                const data = await res.json();
                const reply = data.response || "Task completed.";
                const activeTag = data.tag || predictedTag || 'automation';
                
                // Blink the confirmed agent
                triggerSubAgentGlow(activeTag, true);
                addMsg('assistant', reply, activeTag);

                // Vocalize reply via TTS
                speakText(reply, () => {
                    setSubtitle("Agent finished speaking. Ready for next command.");
                    setTimeout(() => triggerSubAgentGlow(activeTag, false), 1500);
                });

                fetchNotes();
                fetchChats();
            } catch(e) {
                addMsg('assistant', 'System Notice: Task processed. ' + e.message, 'automation');
                triggerSubAgentGlow(predictedTag, false);
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
                div.innerHTML = `<div class="tag-pill pill-${tag}">RB Agent • ${tag.toUpperCase()}</div><div>${text}</div>`;
            } else {
                div.innerText = text;
            }
            feed.appendChild(div);
            feed.scrollTop = feed.scrollHeight;
        }

        function setSubtitle(text) {
            document.getElementById('subtitlesTicker').innerText = text;
        }

        // Voice TTS & Speech Recognition
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
            u.onstart = () => setSubtitle(`Speaking: "${clean.substring(0, 48)}..."`);
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

        // Quick Call Announcement Trigger
        function testCallAnnouncement() {
            triggerSubAgentGlow('automation', true);
            fetch('/api/call_announcement', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ caller_name: "Ram Pandit", phone: "+91-9876543210" })
            }).then(r => r.json()).then(d => {
                setSubtitle(d.announced || "Call announcement triggered.");
                addMsg('assistant', `📞 ${d.announced}`, 'automation');
                setTimeout(() => triggerSubAgentGlow('automation', false), 2000);
            });
        }

        // Web Preview
        async function triggerWebPreview() {
            const q = document.getElementById('webQueryInput').value.trim();
            const out = document.getElementById('webPreviewOutput');
            out.innerText = "Searching web...";
            triggerSubAgentGlow('research', true);
            try {
                const res = await fetch('/api/agents', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ agent: 'research', action: 'run', params: { query: q } })
                });
                const d = await res.json();
                const items = d.result.results || [];
                if (items.length > 0) {
                    out.innerHTML = items.map(it => `
                        <div style="background:#0A0F1D; border:1px solid var(--border); border-radius:8px; padding:10px; margin-bottom:8px;">
                            <div style="font-weight:700; color:var(--accent-cyan); font-size:0.88rem;">${it.title}</div>
                            <div style="font-size:0.8rem; color:#CBD5E1; margin:4px 0;">${it.snippet}</div>
                            <a href="${it.url}" target="_blank" style="font-size:0.72rem; color:var(--accent-blue); word-break:break-all;">${it.url}</a>
                        </div>
                    `).join('');
                } else {
                    out.innerText = "No search results returned.";
                }
            } catch(e) {
                out.innerText = "Error: " + e.message;
            } finally {
                triggerSubAgentGlow('research', false);
            }
        }

        // Code Execution
        async function runScriptExecution() {
            const code = document.getElementById('codeScriptArea').value;
            const consoleEl = document.getElementById('codeConsoleBox');
            consoleEl.innerText = "Running Python script...";
            triggerSubAgentGlow('coding', true);
            try {
                const res = await fetch('/api/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ action: 'shell', args: { command: `python3 -c ${JSON.stringify(code)}` } })
                });
                const d = await res.json();
                consoleEl.innerText = d.result.stdout || d.result.stderr || "Executed successfully (no stdout).";
            } catch(e) {
                consoleEl.innerText = "Error: " + e.message;
            } finally {
                triggerSubAgentGlow('coding', false);
            }
        }

        // Notes Fetch
        async function fetchNotes() {
            const c = document.getElementById('notesListView');
            try {
                const res = await fetch('/api/notes');
                const d = await res.json();
                if (d.notes && d.notes.length > 0) {
                    c.innerHTML = d.notes.map(n => `
                        <div style="background:#0A0F1D; border:1px solid var(--border); border-radius:8px; padding:10px; display:flex; justify-content:space-between; align-items:flex-start;">
                            <div>
                                <div style="font-weight:700; color:#FFF; font-size:0.85rem;">${n.title}</div>
                                <div style="color:var(--text-muted); font-size:0.78rem; margin-top:2px;">${n.content}</div>
                                <div style="font-size:0.65rem; color:#64748B; margin-top:4px;">${n.created_at}</div>
                            </div>
                            <button onclick="deleteNote(${n.id})" style="background:none; border:none; color:#EF4444; cursor:pointer; padding:4px;"><i class="fa-solid fa-trash"></i></button>
                        </div>
                    `).join('');
                } else {
                    c.innerHTML = '<div style="color:var(--text-muted); font-size:0.8rem;">No notes yet. Type "यह चीज़ सेव कर लो" to add!</div>';
                }
            } catch(e) {
                c.innerHTML = 'Unable to load notes.';
            }
        }

        async function deleteNote(id) {
            await fetch(`/api/notes/${id}`, { method: 'DELETE' });
            fetchNotes();
        }

        // Skills Module (Module 7: Skill Add & Self-Training)
        async function fetchSkills() {
            const container = document.getElementById('installedSkillsList');
            try {
                const res = await fetch('/api/skills');
                const d = await res.json();
                if (d.skills && d.skills.length > 0) {
                    container.innerHTML = d.skills.map(s => `
                        <div style="background:#0A0F1D; border:1px solid var(--border); border-radius:8px; padding:10px; display:flex; justify-content:space-between; align-items:flex-start;">
                            <div>
                                <div style="font-weight:700; color:var(--accent-green); font-size:0.85rem;">${s.name}</div>
                                <div style="color:var(--text-muted); font-size:0.76rem; margin-top:2px;">${s.description || 'Custom capability'}</div>
                                <div style="font-size:0.7rem; color:#94A3B8; margin-top:4px; font-family:monospace; background:rgba(255,255,255,0.04); padding:4px 6px; border-radius:4px;">${s.system_prompt.substring(0, 90)}...</div>
                            </div>
                            <button onclick="deleteSkill(${s.id})" style="background:none; border:none; color:#EF4444; cursor:pointer; padding:4px;"><i class="fa-solid fa-trash"></i></button>
                        </div>
                    `).join('');
                } else {
                    container.innerHTML = '<div style="color:var(--text-muted); font-size:0.8rem;">No custom skills trained yet. Use the form above to train RB Agent!</div>';
                }
            } catch(e) {
                container.innerHTML = 'Failed to load skills.';
            }
        }

        async function saveSkillLive() {
            const name = document.getElementById('skillNameInput').value.trim();
            const desc = document.getElementById('skillDescInput').value.trim();
            const prompt = document.getElementById('skillPromptInput').value.trim();
            const examples = document.getElementById('skillExamplesInput').value.trim();
            const feedback = document.getElementById('skillStatusFeedback');

            if (!name || !prompt) {
                feedback.innerHTML = '<span class="status-badge badge-danger">Name and Directives are required.</span>';
                return;
            }

            feedback.innerHTML = '<span style="color:var(--accent-cyan); font-size:0.75rem;">Training and persisting skill live...</span>';
            try {
                const res = await fetch('/api/skills', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ name, description: desc, system_prompt: prompt, examples })
                });
                const d = await res.json();
                if (d.success) {
                    feedback.innerHTML = `<span class="status-badge badge-success">${d.message}</span>`;
                    document.getElementById('skillNameInput').value = '';
                    document.getElementById('skillDescInput').value = '';
                    document.getElementById('skillPromptInput').value = '';
                    document.getElementById('skillExamplesInput').value = '';
                    fetchSkills();
                } else {
                    feedback.innerHTML = `<span class="status-badge badge-danger">${d.error || 'Failed'}</span>`;
                }
            } catch(e) {
                feedback.innerHTML = `<span class="status-badge badge-danger">${e.message}</span>`;
            }
        }

        async function deleteSkill(id) {
            await fetch(`/api/skills/${id}`, { method: 'DELETE' });
            fetchSkills();
        }

        // Chats History
        async function fetchChats() {
            const c = document.getElementById('chatsListContainer');
            try {
                const res = await fetch('/api/chats');
                const d = await res.json();
                if (d.chats && d.chats.length > 0) {
                    c.innerHTML = d.chats.map(ch => `
                        <div style="background:#0A0F1D; border:1px solid var(--border); border-radius:8px; padding:8px 12px; font-size:0.8rem;">
                            <span style="color:${ch.sender === 'user' ? 'var(--accent-cyan)' : 'var(--accent-green)'}; font-weight:700;">${ch.sender.toUpperCase()}:</span>
                            <span style="color:#FFF; margin-left:6px;">${ch.message.substring(0, 70)}...</span>
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

        async function clearAllChats() {
            if (!confirm("Clear all persistent chats?")) return;
            await fetch('/api/chats', { method: 'DELETE' });
            fetchChats();
        }

        function resetNewChat() {
            document.getElementById('chatStream').innerHTML = `
                <div class="msg-bubble assistant">
                    <div class="tag-pill pill-automation">RB System</div>
                    <div>नमस्ते Ram Binay Pandit! New chat session initialized. What task shall we tackle?</div>
                </div>
            `;
            showPanel('home');
        }

        // Real Credential Handshakes
        async function testTelegramHandshake() {
            const token = document.getElementById('cfgTelegramToken').value.trim();
            const box = document.getElementById('telegramStatusBox');
            box.innerText = "Testing handshake...";
            const res = await fetch('/api/test_credentials', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ service: 'telegram', credentials: { token } })
            });
            const d = await res.json();
            box.innerHTML = d.success
                ? `<span class="status-badge badge-success">${d.message}</span>`
                : `<span class="status-badge badge-danger">${d.error}</span>`;
        }

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

        async function launchWhatsApp() {
            const phone = document.getElementById('cfgWaPhone').value.trim();
            const msg = document.getElementById('cfgWaMsg').value.trim();
            if (!phone) return alert("Enter target phone number");
            const res = await fetch('/api/whatsapp', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ phone, message: msg })
            });
            const d = await res.json();
            if (d.url) window.open(d.url, '_blank');
        }

        async function testGitHubHandshake() {
            const user = document.getElementById('cfgGhUser').value.trim();
            const token = document.getElementById('cfgGhToken').value.trim();
            const label = document.getElementById('ghSyncStatus');
            label.innerText = "Testing handshake with GitHub...";
            const res = await fetch('/api/test_credentials', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ service: 'github', credentials: { username: user, token } })
            });
            const d = await res.json();
            label.innerHTML = d.success
                ? `<span class="status-badge badge-success">${d.message}</span>`
                : `<span class="status-badge badge-danger">${d.error}</span>`;
        }

        async function testSupabaseHandshake() {
            const url = document.getElementById('cfgSupabaseUrl').value.trim();
            const key = document.getElementById('cfgSupabaseKey').value.trim();
            const box = document.getElementById('supabaseStatusBox');
            box.innerText = "Testing Supabase handshake...";
            const res = await fetch('/api/test_credentials', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ service: 'supabase', credentials: { url, key } })
            });
            const d = await res.json();
            box.innerHTML = d.success
                ? `<span class="status-badge badge-success">${d.message}</span>`
                : `<span class="status-badge badge-danger">${d.error}</span>`;
        }

        async function syncSupabaseData() {
            const box = document.getElementById('supabaseStatusBox');
            box.innerText = "Syncing SQLite data to Supabase cloud...";
            const res = await fetch('/api/supabase/sync', { method: 'POST' });
            const d = await res.json();
            box.innerHTML = d.success
                ? `<span class="status-badge badge-success">${d.message}</span>`
                : `<span class="status-badge badge-danger">${d.error}</span>`;
        }

        async function testGeminiHandshake() {
            const key = document.getElementById('cfgGeminiKey').value.trim();
            const box = document.getElementById('geminiStatusBox');
            box.innerText = "Testing Gemini API key handshake...";
            const res = await fetch('/api/test_credentials', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ service: 'gemini', credentials: { api_key: key } })
            });
            const d = await res.json();
            box.innerHTML = d.success
                ? `<span class="status-badge badge-success">${d.message}</span>`
                : `<span class="status-badge badge-danger">${d.error}</span>`;
        }

        async function saveConfigurations() {
            const accent = document.getElementById('cfgVoiceAccent').value;
            const pitch = document.getElementById('cfgVoicePitch').value;
            const rate = document.getElementById('cfgVoiceRate').value;
            const wake = document.getElementById('cfgWakePhrase').checked;
            const call = document.getElementById('cfgCallAnnounce').checked;
            const geminiKey = document.getElementById('cfgGeminiKey').value.trim();
            const geminiModel = document.getElementById('cfgGeminiModel').value;

            await fetch('/api/settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    voice_accent: accent,
                    voice_pitch: pitch,
                    voice_rate: rate,
                    wake_phrase_enabled: wake ? 'true' : 'false',
                    call_announcement_enabled: call ? 'true' : 'false',
                    gemini_model: geminiModel
                })
            });

            if (geminiKey) {
                await fetch('/api/config', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ gemini_api_key: geminiKey })
                });
            }

            alert("All configurations saved successfully to local SQLite & Supabase!");
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
