"""
RB.AI - Server & WebSocket Gateway
Serves REST and WebSocket endpoints for Flutter client and Termux integration.
"""

import json
import base64
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any
from core.assistant import RBAssistant
from core.automation import automation

class RBServer:
    """Lightweight HTTP & Real-time API Server for RB.AI."""

    def __init__(self, assistant: RBAssistant, host: str = "0.0.0.0", port: int = 8765):
        self.assistant = assistant
        self.host = host
        self.port = port

    def run(self):
        assistant_ref = self.assistant

        class RequestHandler(BaseHTTPRequestHandler):
            def _send_json(self, data: Dict[str, Any], status: int = 200):
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode("utf-8"))

            def do_OPTIONS(self):
                self._send_json({"status": "ok"})

            def do_GET(self):
                if self.path == "/api/status":
                    status = {
                        "assistant_state": assistant_ref.state,
                        "device": automation.get_system_summary(),
                        "model": assistant_ref.config.GEMINI_MODEL,
                        "has_api_key": bool(assistant_ref.config.GEMINI_API_KEY)
                    }
                    self._send_json(status)
                elif self.path == "/api/battery":
                    self._send_json(automation.get_battery_status())
                elif self.path == "/":
                    self._send_json({
                        "name": "RB.AI Voice & Multimodal Assistant Server",
                        "status": "online",
                        "endpoints": ["/api/status", "/api/chat", "/api/action", "/api/battery"]
                    })
                else:
                    self._send_json({"error": "Not Found"}, status=404)

            def do_POST(self):
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)

                try:
                    payload = json.loads(body.decode("utf-8")) if body else {}
                except Exception:
                    self._send_json({"error": "Invalid JSON"}, status=400)
                    return

                if self.path == "/api/chat":
                    text = payload.get("text", "")
                    image_b64 = payload.get("image")
                    is_voice = payload.get("is_voice", False)
                    img_bytes = base64.b64decode(image_b64) if image_b64 else None

                    res = assistant_ref.process_input(raw_text=text, image_bytes=img_bytes, is_voice=is_voice)
                    self._send_json(res)

                elif self.path == "/api/action":
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
                    else:
                        result = {"error": f"Unknown action: {action_name}"}

                    self._send_json({"action": action_name, "result": result})

                elif self.path == "/api/config":
                    api_key = payload.get("gemini_api_key")
                    if api_key:
                        assistant_ref.update_api_key(api_key)
                    self._send_json({"status": "updated", "has_key": bool(assistant_ref.config.GEMINI_API_KEY)})

                else:
                    self._send_json({"error": "Not Found"}, status=404)

            def log_message(self, format, *args):
                # Clean logging
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
