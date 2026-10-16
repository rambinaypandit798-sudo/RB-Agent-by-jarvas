"""
RB.AI - Production Server & API Gateway
Serves REST endpoints for Flutter client, Sub-Agents, Database,
Telegram, WhatsApp, GitHub, Supabase, Skills Training, and on-device Web UI.
"""

import json
import base64
import urllib.parse
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any
from core.assistant import RBAssistant
from core.automation import automation
from core.database import db
from core.sub_agents import sub_agents
from core.supabase_client import supabase
from core.telegram_bot import telegram_bot
from core.whatsapp_bridge import whatsapp_bridge

class RBServer:
    """Production HTTP API Server for RB Agent."""

    def __init__(self, assistant: RBAssistant, host: str = "0.0.0.0", port: int = 8765):
        self.assistant = assistant
        self.host = host
        self.port = port

    def run(self):
        assistant_ref = self.assistant

        class RequestHandler(BaseHTTPRequestHandler):
            def _send_json(self, data: Dict[str, Any], status: int = 200):
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                self.end_headers()
                self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

            def do_OPTIONS(self):
                self._send_json({"status": "ok"})

            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                path = parsed.path
                query = urllib.parse.parse_qs(parsed.query)

                if path == "/api/status":
                    user_name = db.get_setting("user_name", "Ram Binay Pandit")
                    status = {
                        "assistant_state": assistant_ref.state,
                        "user_name": user_name,
                        "greeting": f"नमस्ते, {user_name} आज आपका क्या प्लान है",
                        "device": automation.get_system_summary(),
                        "model": assistant_ref.config.GEMINI_MODEL,
                        "has_api_key": bool(assistant_ref.config.GEMINI_API_KEY),
                        "telegram": telegram_bot.get_status(),
                        "supabase": supabase.test_connection(),
                        "settings": db.get_all_settings(),
                        "skills_count": len(db.get_skills())
                    }
                    self._send_json(status)

                elif path == "/api/user":
                    user_name = db.get_setting("user_name", "Ram Binay Pandit")
                    self._send_json({
                        "user_name": user_name,
                        "greeting": f"नमस्ते, {user_name} आज आपका क्या प्लान है",
                        "settings": db.get_all_settings()
                    })

                elif path == "/api/battery":
                    self._send_json(automation.get_battery_status())

                elif path == "/api/notes":
                    search = query.get("q", [None])[0]
                    notes = db.get_notes(search=search)
                    self._send_json({"count": len(notes), "notes": notes})

                elif path == "/api/chats":
                    chats = db.get_chats(limit=100)
                    self._send_json({"count": len(chats), "chats": chats})

                elif path == "/api/skills":
                    skills = db.get_skills()
                    self._send_json({"count": len(skills), "skills": skills})

                elif path == "/api/supabase" or path == "/api/supabase/status":
                    self._send_json(supabase.test_connection())

                elif path == "/api/telegram":
                    self._send_json(telegram_bot.get_status())

                elif path == "/api/github":
                    username = query.get("username", [None])[0]
                    token = query.get("token", [None])[0]
                    res = sub_agents.execute_code_or_github("fetch_github_repos", {
                        "username": username or "",
                        "token": token or ""
                    })
                    self._send_json(res)

                elif path == "/manifest.json":
                    manifest = {
                        "name": "RB Agent OS",
                        "short_name": "RB Agent",
                        "start_url": "/",
                        "display": "standalone",
                        "background_color": "#060A13",
                        "theme_color": "#070B14",
                        "description": "Autonomous Operating System Agent for Ram Binay kumar Pandit",
                        "icons": [
                            {
                                "src": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/svgs/solid/atom.svg",
                                "sizes": "192x192 512x512",
                                "type": "image/svg+xml"
                            }
                        ]
                    }
                    self._send_json(manifest)

                elif path == "/" or path == "/app":
                    from core.web_ui import WEB_HTML
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(WEB_HTML.encode("utf-8"))

                else:
                    self._send_json({"error": "Not Found", "path": path}, status=404)

            def do_POST(self):
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)

                try:
                    payload = json.loads(body.decode("utf-8")) if body else {}
                except Exception:
                    self._send_json({"error": "Invalid JSON"}, status=400)
                    return

                path = urllib.parse.urlparse(self.path).path

                # 1. Dynamic User Name & Settings
                if path == "/api/user":
                    name = payload.get("user_name")
                    if name:
                        db.set_setting("user_name", name.strip())
                    self._send_json({
                        "success": True,
                        "user_name": db.get_setting("user_name"),
                        "greeting": f"नमस्ते, {db.get_setting('user_name')} आज आपका क्या प्लान है"
                    })

                elif path == "/api/settings":
                    for k, v in payload.items():
                        db.set_setting(k, str(v))
                    self._send_json({"success": True, "settings": db.get_all_settings()})

                # 2. Chat with Auto-Memory Intent & Autonomous Routing
                elif path == "/api/chat":
                    text = payload.get("text", "")
                    image_b64 = payload.get("image")
                    is_voice = payload.get("is_voice", False)
                    img_bytes = base64.b64decode(image_b64) if image_b64 else None

                    # Autonomous Intent Router (Memory, Automation, Web Research, Coding)
                    routed_result = sub_agents.route_and_process_intent(text)
                    if routed_result and routed_result.get("routed"):
                        reply = routed_result.get("response", "Task completed.")
                        agent_name = routed_result.get("agent", "RB Agent")
                        agent_tag = routed_result.get("tag", "automation")
                        db.add_chat(sender="user", message=text, agent_type=agent_tag)
                        db.add_chat(sender="assistant", message=reply, agent_type=agent_tag)
                        if is_voice and assistant_ref.config.ENABLE_TTS:
                            assistant_ref.audio.speak(reply)
                        self._send_json({
                            "state": "IDLE",
                            "response": reply,
                            "agent": agent_name,
                            "tag": agent_tag,
                            "active_subagent": agent_tag,
                            "tool_calls": []
                        })
                        return

                    # Normal Gemini / Multimodal Processing with active dynamic skills
                    res = assistant_ref.process_input(raw_text=text, image_bytes=img_bytes, is_voice=is_voice)
                    reply_text = res.get("response", "")
                    tool_calls = res.get("tool_calls", [])

                    # Detect if any tool call mapped to a specific sub-agent
                    active_sub = "core"
                    if tool_calls:
                        tname = tool_calls[0].get("tool", "")
                        if "battery" in tname or "torch" in tname or "vibrate" in tname:
                            active_sub = "automation"
                        elif "url" in tname or "search" in tname:
                            active_sub = "research"
                        elif "shell" in tname:
                            active_sub = "coding"
                    
                    # Persist in SQLite & Supabase
                    db.add_chat(sender="user", message=text, agent_type=active_sub, tool_calls=[])
                    db.add_chat(sender="assistant", message=reply_text, agent_type=active_sub, tool_calls=tool_calls)
                    
                    self._send_json({
                        "state": "IDLE",
                        "response": reply_text,
                        "agent": "RB Agent",
                        "tag": active_sub,
                        "active_subagent": active_sub,
                        "tool_calls": tool_calls
                    })

                # 3. Dedicated 5 Sub-Agents Direct Dispatcher
                elif path == "/api/agents":
                    agent_name = payload.get("agent", "")
                    action = payload.get("action", "")
                    params = payload.get("params", {})

                    if agent_name == "research":
                        query = params.get("query", "")
                        result = sub_agents.run_web_search(query)
                    elif agent_name == "memory":
                        text = params.get("text", "")
                        result = sub_agents.process_memory_intent(text)
                    elif agent_name == "preview":
                        target = params.get("target", "")
                        result = sub_agents.preview_url_or_markdown(target)
                    elif agent_name == "automation":
                        result = sub_agents.execute_device_automation(action, params)
                    elif agent_name == "coding":
                        result = sub_agents.execute_code_or_github(action, params)
                    else:
                        result = {"error": f"Unknown agent: {agent_name}"}

                    self._send_json({"agent": agent_name, "result": result})

                # 4. Agent Training & Self-Improvement ("Skill Add")
                elif path == "/api/skills":
                    name = payload.get("name", "").strip()
                    system_prompt = payload.get("system_prompt", "").strip()
                    description = payload.get("description", "").strip()
                    examples = payload.get("examples", "").strip()

                    if not name or not system_prompt:
                        self._send_json({"success": False, "error": "Skill Name and System Directives are required."}, status=400)
                        return

                    skill_id = db.add_skill(
                        name=name,
                        system_prompt=system_prompt,
                        description=description,
                        examples=examples
                    )
                    self._send_json({
                        "success": True,
                        "skill_id": skill_id,
                        "name": name,
                        "message": f"Skill '{name}' successfully compiled and activated in live memory."
                    })

                elif path == "/api/skills/toggle":
                    skill_id = int(payload.get("id", 0))
                    enabled = int(bool(payload.get("enabled", True)))
                    success = db.toggle_skill(skill_id, enabled)
                    self._send_json({"success": success})

                # 5. Notes CRUD
                elif path == "/api/notes":
                    title = payload.get("title", "New Note")
                    content = payload.get("content", "")
                    tags = payload.get("tags", "")
                    note_id = db.add_note(title=title, content=content, tags=tags)
                    self._send_json({"success": True, "note_id": note_id, "title": title})

                # 6. Device Automation Direct Actions
                elif path == "/api/action":
                    action_name = payload.get("action")
                    args = payload.get("args", {})
                    
                    if action_name == "torch":
                        result = automation.set_torch(bool(args.get("enabled", True)))
                    elif action_name == "vibrate":
                        result = automation.vibrate(int(args.get("duration", 300)))
                    elif action_name == "notify":
                        result = automation.send_notification(args.get("title", "RB.AI"), args.get("content", ""))
                    elif action_name == "clipboard_set":
                        result = automation.set_clipboard(args.get("text", ""))
                    elif action_name == "clipboard_get":
                        result = automation.get_clipboard()
                    elif action_name == "shell":
                        result = automation.execute_shell(args.get("command", ""))
                    elif action_name == "call_announcement":
                        result = sub_agents.execute_device_automation("call_announcement", args)
                    else:
                        result = {"error": f"Unknown action: {action_name}"}

                    self._send_json({"action": action_name, "result": result})

                # 7. Telegram Bot Integration
                elif path == "/api/telegram":
                    action = payload.get("action", "start")
                    token = payload.get("token")
                    if action == "start":
                        res = telegram_bot.start(token=token)
                    elif action == "stop":
                        res = telegram_bot.stop()
                    elif action == "send":
                        chat_id = payload.get("chat_id")
                        text = payload.get("text", "")
                        res = telegram_bot.send_message(chat_id, text)
                    else:
                        res = {"error": f"Unknown telegram action: {action}"}
                    self._send_json(res)

                # 8. WhatsApp Integration
                elif path == "/api/whatsapp":
                    phone = payload.get("phone", "")
                    message = payload.get("message", "")
                    res = whatsapp_bridge.send_whatsapp_message(phone, message)
                    self._send_json(res)

                # 9. Call Announcement Trigger
                elif path == "/api/call_announcement":
                    caller_name = payload.get("caller_name", "")
                    phone = payload.get("phone", "")
                    res = sub_agents.execute_device_automation("call_announcement", {
                        "caller_name": caller_name,
                        "phone": phone
                    })
                    self._send_json(res)

                # 10. Supabase Sync & Connection
                elif path == "/api/supabase/sync":
                    res = db.sync_all_to_supabase()
                    self._send_json(res)

                elif path == "/api/supabase/save":
                    url = payload.get("url", "").strip()
                    key = payload.get("key", "").strip()
                    if url and key:
                        db.save_integration("supabase", {"url": url, "key": key})
                        supabase.update_credentials(url, key)
                        res = supabase.test_connection()
                        self._send_json(res)
                    else:
                        self._send_json({"success": False, "error": "URL and Key required"}, status=400)

                # 11. Live Credential Handshake Verifier
                elif path == "/api/test_credentials":
                    service = payload.get("service")
                    creds = payload.get("credentials", {})

                    if service == "telegram":
                        token = creds.get("token", "").strip()
                        if not token:
                            self._send_json({"success": False, "error": "Telegram Token is empty"})
                            return
                        try:
                            req = urllib.request.Request(f"https://api.telegram.org/bot{token}/getMe")
                            with urllib.request.urlopen(req, timeout=8) as r:
                                tdata = json.loads(r.read().decode("utf-8"))
                                if tdata.get("ok"):
                                    bot_info = tdata.get("result", {})
                                    db.save_integration("telegram", {"token": token, "bot_username": bot_info.get("username")})
                                    self._send_json({
                                        "success": True,
                                        "message": f"Connected as @{bot_info.get('username')} ({bot_info.get('first_name')})"
                                    })
                                else:
                                    self._send_json({"success": False, "error": "Invalid Telegram response"})
                        except Exception as e:
                            self._send_json({"success": False, "error": f"Telegram test failed: {str(e)}"})

                    elif service == "github":
                        user = creds.get("username", "").strip()
                        token = creds.get("token", "").strip()
                        headers = {"User-Agent": "RB-Agent-Test", "Accept": "application/vnd.github.v3+json"}
                        if token:
                            headers["Authorization"] = f"token {token}"
                        url = "https://api.github.com/user" if token else f"https://api.github.com/users/{user}"
                        try:
                            req = urllib.request.Request(url, headers=headers)
                            with urllib.request.urlopen(req, timeout=8) as r:
                                gdata = json.loads(r.read().decode("utf-8"))
                                db.save_integration("github", {"token": token, "username": user or gdata.get("login", "")})
                                self._send_json({
                                    "success": True,
                                    "message": f"Verified GitHub account: {gdata.get('login')} (Public repos: {gdata.get('public_repos', 0)})"
                                })
                        except Exception as e:
                            self._send_json({"success": False, "error": f"GitHub test failed: {str(e)}"})

                    elif service == "gemini":
                        key = creds.get("api_key", "").strip()
                        if not key:
                            self._send_json({"success": False, "error": "Gemini API key is empty"})
                            return
                        try:
                            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
                            req = urllib.request.Request(url)
                            with urllib.request.urlopen(req, timeout=10) as r:
                                mdata = json.loads(r.read().decode("utf-8"))
                                models = [m.get("name").replace("models/", "") for m in mdata.get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
                                assistant_ref.update_api_key(key)
                                db.save_integration("gemini", {"api_key": key})
                                self._send_json({
                                    "success": True,
                                    "message": f"Gemini API handshake valid! {len(models)} models available.",
                                    "models": models[:6]
                                })
                        except Exception as e:
                            self._send_json({"success": False, "error": f"Gemini API test failed: {str(e)}"})

                    elif service == "supabase":
                        s_url = creds.get("url", "").strip()
                        s_key = creds.get("key", "").strip()
                        temp_sb = supabase
                        temp_sb.update_credentials(s_url, s_key)
                        res = temp_sb.test_connection()
                        if res.get("success"):
                            db.save_integration("supabase", {"url": s_url, "key": s_key})
                            # Auto-sync
                            sync_res = db.sync_all_to_supabase()
                            res["sync_status"] = sync_res
                        self._send_json(res)

                    else:
                        self._send_json({"success": False, "error": f"Unknown service: {service}"}, status=400)

                # 12. Config Update
                elif path == "/api/config":
                    api_key = payload.get("gemini_api_key")
                    if api_key:
                        assistant_ref.update_api_key(api_key)
                    self._send_json({"status": "updated", "has_key": bool(assistant_ref.config.GEMINI_API_KEY)})

                else:
                    self._send_json({"error": "Not Found", "path": path}, status=404)

            def do_DELETE(self):
                path = urllib.parse.urlparse(self.path).path
                if path.startswith("/api/notes/"):
                    try:
                        note_id = int(path.split("/")[-1])
                        success = db.delete_note(note_id)
                        self._send_json({"success": success, "deleted_id": note_id})
                    except Exception as e:
                        self._send_json({"success": False, "error": str(e)}, status=400)
                elif path.startswith("/api/skills/"):
                    try:
                        skill_id = int(path.split("/")[-1])
                        success = db.delete_skill(skill_id)
                        self._send_json({"success": success, "deleted_id": skill_id})
                    except Exception as e:
                        self._send_json({"success": False, "error": str(e)}, status=400)
                elif path == "/api/chats":
                    db.clear_chats()
                    self._send_json({"success": True, "message": "Chat history cleared"})
                else:
                    self._send_json({"error": "Not Found"}, status=404)

            def log_message(self, format, *args):
                print(f"[RB.AI HTTP] {args[0]} {args[1]}")

        server = HTTPServer((self.host, self.port), RequestHandler)
        print(f"\n========================================================")
        print(f"🚀 RB.AI Gateway is active on http://{self.host}:{self.port}")
        print(f"📡 Connect your Flutter client to http://<Device_IP>:{self.port}")
        print(f"========================================================\n")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down RB.AI server.")
            server.server_close()
