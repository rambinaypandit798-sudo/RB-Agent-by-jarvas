"""
RB.AI - Google Gemini Multimodal Engine
Handles prompt generation, vision, audio input, and automatic tool/function calling.
"""

import json
import urllib.request
import urllib.error
import base64
import os
from typing import List, Dict, Any, Optional
from core.automation import automation
from core.master_prompt import RB_MASTER_SYSTEM_PROMPT

GEMINI_TOOLS = [
    {
        "name": "get_battery_status",
        "description": "Get current battery level percentage, health, status (charging/discharging), and temperature.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "speak_text",
        "description": "Speak text aloud using the device's voice/TTS.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "text": {"type": "STRING", "description": "The message to speak"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "send_notification",
        "description": "Display a notification on the Android device.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "title": {"type": "STRING", "description": "Notification title"},
                "content": {"type": "STRING", "description": "Notification message"}
            },
            "required": ["title", "content"]
        }
    },
    {
        "name": "vibrate_device",
        "description": "Vibrate the device for haptic feedback.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "duration_ms": {"type": "INTEGER", "description": "Vibration duration in milliseconds"}
            },
            "required": []
        }
    },
    {
        "name": "set_torch",
        "description": "Turn the device flashlight / torch on or off.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "enabled": {"type": "BOOLEAN", "description": "True to turn torch on, False to turn torch off"}
            },
            "required": ["enabled"]
        }
    },
    {
        "name": "get_clipboard",
        "description": "Read the text currently copied in the device clipboard.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "set_clipboard",
        "description": "Copy text to the device clipboard.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "text": {"type": "STRING", "description": "Text to copy to clipboard"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "open_url",
        "description": "Open a web URL or deep link in the browser or app on Android.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "url": {"type": "STRING", "description": "The URL to open"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "take_photo",
        "description": "Capture a photo using the phone camera and return path.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "camera_id": {"type": "INTEGER", "description": "0 for back camera, 1 for front camera"}
            },
            "required": []
        }
    },
    {
        "name": "get_system_summary",
        "description": "Get device storage, battery status, and operating system metrics.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "execute_shell_command",
        "description": "Run a bash/shell command inside the Termux environment.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "command": {"type": "STRING", "description": "The shell command to run"}
            },
            "required": ["command"]
        }
    }
]

class GeminiEngine:
    """Multimodal Gemini Engine with native Function Calling."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model = model
        self.system_instruction = RB_MASTER_SYSTEM_PROMPT
        self.history: List[Dict[str, Any]] = []

    def set_api_key(self, api_key: str):
        self.api_key = api_key

    def _execute_tool(self, name: str, args: Dict[str, Any]) -> Any:
        """Dispatches Gemini tool calls to the automation layer."""
        if name == "get_battery_status":
            return automation.get_battery_status()
        elif name == "speak_text":
            return automation.speak(args.get("text", ""))
        elif name == "send_notification":
            return automation.send_notification(args.get("title", "RB.AI"), args.get("content", ""))
        elif name == "vibrate_device":
            return automation.vibrate(args.get("duration_ms", 300))
        elif name == "set_torch":
            return automation.set_torch(bool(args.get("enabled", False)))
        elif name == "get_clipboard":
            return automation.get_clipboard()
        elif name == "set_clipboard":
            return automation.set_clipboard(args.get("text", ""))
        elif name == "open_url":
            return automation.open_url(args.get("url", ""))
        elif name == "take_photo":
            return automation.take_photo(camera_id=args.get("camera_id", 0))
        elif name == "get_system_summary":
            return automation.get_system_summary()
        elif name == "execute_shell_command":
            return automation.execute_shell(args.get("command", ""))
        return {"error": f"Unknown tool: {name}"}

    def chat(self, user_text: str, image_bytes: Optional[bytes] = None, image_mime: str = "image/jpeg") -> Dict[str, Any]:
        """Sends a query to Gemini with full multimodal and tool calling support."""
        if not self.api_key:
            return {
                "text": "Gemini API key is not configured. Please set GEMINI_API_KEY in .env or via config.",
                "tool_calls": []
            }

        # Build user parts
        user_parts = []
        if image_bytes:
            b64_data = base64.b64encode(image_bytes).decode("utf-8")
            user_parts.append({
                "inline_data": {
                    "mime_type": image_mime,
                    "data": b64_data
                }
            })
        if user_text:
            user_parts.append({"text": user_text})

        # Append to history
        self.history.append({"role": "user", "parts": user_parts})

        # Keep history manageable (last 12 turns)
        if len(self.history) > 24:
            self.history = self.history[-24:]

        return self._run_model_turn()

    def _run_model_turn(self, depth: int = 0) -> Dict[str, Any]:
        if depth > 4:
            return {"text": "Tool call depth limit reached.", "tool_calls": []}

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        payload = {
            "contents": self.history,
            "system_instruction": {
                "parts": [{"text": self.system_instruction}]
            },
            "tools": [{"function_declarations": GEMINI_TOOLS}],
            "generation_config": {
                "temperature": 0.7,
                "max_output_tokens": 1024
            }
        }

        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            return {"text": f"Gemini API Error ({e.code}): {err_body}", "tool_calls": []}
        except Exception as e:
            return {"text": f"Network Error contacting Gemini: {str(e)}", "tool_calls": []}

        candidates = data.get("candidates", [])
        if not candidates:
            return {"text": "No response returned from Gemini.", "tool_calls": []}

        first_cand = candidates[0]
        content = first_cand.get("content", {})
        parts = content.get("parts", [])

        # Store model response in history
        self.history.append({"role": "model", "parts": parts})

        executed_tools = []
        function_responses = []
        text_responses = []

        for part in parts:
            if "text" in part:
                text_responses.append(part["text"])
            if "functionCall" in part:
                fc = part["functionCall"]
                name = fc.get("name")
                args = fc.get("args", {})
                
                # Execute tool
                tool_result = self._execute_tool(name, args)
                executed_tools.append({"tool": name, "args": args, "result": tool_result})

                # Prepare functionResponse part
                function_responses.append({
                    "functionResponse": {
                        "name": name,
                        "response": {"output": tool_result}
                    }
                })

        # If any functions were called, feed their results back to the model
        if function_responses:
            self.history.append({"role": "user", "parts": function_responses})
            next_turn = self._run_model_turn(depth=depth + 1)
            # Combine tools
            next_turn["tool_calls"] = executed_tools + next_turn.get("tool_calls", [])
            return next_turn

        final_text = "\n".join(text_responses).strip()
        return {
            "text": final_text or "(Task completed successfully)",
            "tool_calls": executed_tools
        }
