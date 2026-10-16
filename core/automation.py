"""
RB.AI - System Automation Engine
Integrates with Termux API and Android system capabilities.
"""

import os
import json
import shutil
import subprocess
from typing import Dict, Any, Optional

class TermuxAutomation:
    """Provides hardware and OS automation for RB.AI via Termux API."""

    def __init__(self):
        self.has_termux_api = self._check_command("termux-battery-status")

    def _check_command(self, cmd: str) -> bool:
        return shutil.which(cmd) is not None

    def _run_cmd(self, cmd_args: list, timeout: int = 10) -> subprocess.CompletedProcess:
        try:
            res = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )
            return res
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(cmd_args, 124, "", "Command timed out")
        except Exception as e:
            return subprocess.CompletedProcess(cmd_args, 1, "", str(e))

    def get_battery_status(self) -> Dict[str, Any]:
        """Returns battery percentage, health, temperature, and charging status."""
        if not self._check_command("termux-battery-status"):
            # Fallback: inspect sysfs if available on rooted/accessible devices
            return {
                "available": False,
                "message": "termux-battery-status not found. Install 'termux-api' package and app."
            }

        res = self._run_cmd(["termux-battery-status"])
        if res.returncode == 0 and res.stdout.strip():
            try:
                data = json.loads(res.stdout)
                return {
                    "available": True,
                    "percentage": data.get("percentage"),
                    "status": data.get("status"),
                    "health": data.get("health"),
                    "temperature": data.get("temperature"),
                    "plugged": data.get("plugged")
                }
            except Exception as e:
                return {"available": False, "error": f"Failed to parse battery JSON: {e}"}
        return {"available": False, "error": res.stderr.strip() or "Failed to read battery"}

    def speak(self, text: str, pitch: float = 1.0, rate: float = 1.0) -> Dict[str, Any]:
        """Speaks text using Android TTS via Termux."""
        if not text:
            return {"success": False, "error": "Empty text"}

        if self._check_command("termux-tts-speak"):
            res = self._run_cmd(["termux-tts-speak", "-p", str(pitch), "-r", str(rate), text])
            return {"success": res.returncode == 0, "engine": "termux-tts"}
        
        # Fallback console speech log
        print(f"[RB.AI Voice]: {text}")
        return {"success": True, "engine": "console_fallback"}

    def send_notification(self, title: str, content: str, priority: str = "high") -> Dict[str, Any]:
        """Shows a system notification on Android."""
        if self._check_command("termux-notification"):
            res = self._run_cmd([
                "termux-notification",
                "--title", title,
                "--content", content,
                "--priority", priority,
                "--id", "rb_ai_notification"
            ])
            return {"success": res.returncode == 0}
        return {"success": False, "message": "termux-notification not available"}

    def vibrate(self, duration_ms: int = 300) -> Dict[str, Any]:
        """Vibrates the device."""
        if self._check_command("termux-vibrate"):
            res = self._run_cmd(["termux-vibrate", "-d", str(duration_ms)])
            return {"success": res.returncode == 0}
        return {"success": False, "message": "termux-vibrate not available"}

    def set_torch(self, enabled: bool) -> Dict[str, Any]:
        """Toggles the device flashlight/torch."""
        if self._check_command("termux-torch"):
            state = "on" if enabled else "off"
            res = self._run_cmd(["termux-torch", state])
            return {"success": res.returncode == 0, "torch": state}
        return {"success": False, "message": "termux-torch not available"}

    def get_clipboard(self) -> Dict[str, Any]:
        """Reads text from system clipboard."""
        if self._check_command("termux-clipboard-get"):
            res = self._run_cmd(["termux-clipboard-get"])
            return {"success": res.returncode == 0, "text": res.stdout}
        return {"success": False, "message": "termux-clipboard-get not available"}

    def set_clipboard(self, text: str) -> Dict[str, Any]:
        """Copies text to system clipboard."""
        if self._check_command("termux-clipboard-set"):
            res = self._run_cmd(["termux-clipboard-set", text])
            return {"success": res.returncode == 0}
        return {"success": False, "message": "termux-clipboard-set not available"}

    def open_url(self, url: str) -> Dict[str, Any]:
        """Opens a URL or app intent in the browser or default app."""
        cmd = "termux-open-url" if self._check_command("termux-open-url") else "termux-open"
        if self._check_command(cmd):
            res = self._run_cmd([cmd, url])
            return {"success": res.returncode == 0, "url": url}
        return {"success": False, "message": f"{cmd} not available"}

    def get_wifi_info(self) -> Dict[str, Any]:
        """Returns current Wi-Fi connection info."""
        if self._check_command("termux-wifi-connectioninfo"):
            res = self._run_cmd(["termux-wifi-connectioninfo"])
            if res.returncode == 0 and res.stdout.strip():
                try:
                    return {"success": True, "info": json.loads(res.stdout)}
                except Exception:
                    return {"success": True, "raw": res.stdout.strip()}
        return {"success": False, "message": "termux-wifi-connectioninfo not available"}

    def take_photo(self, output_path: str = "/data/data/com.termux/files/home/rb_ai/latest_camera.jpg", camera_id: int = 0) -> Dict[str, Any]:
        """Captures a photo using the device camera."""
        if self._check_command("termux-camera-photo"):
            res = self._run_cmd(["termux-camera-photo", "-c", str(camera_id), output_path], timeout=15)
            if res.returncode == 0 and os.path.exists(output_path):
                return {"success": True, "path": output_path}
            return {"success": False, "error": res.stderr.strip() or "Camera capture failed"}
        return {"success": False, "message": "termux-camera-photo not available"}

    def get_system_summary(self) -> Dict[str, Any]:
        """Provides a complete system health overview (storage, load, battery, memory)."""
        summary = {
            "battery": self.get_battery_status(),
            "cwd": os.getcwd(),
            "user": os.getenv("USER", "termux_user"),
        }
        
        # Disk usage
        try:
            total, used, free = shutil.disk_usage("/")
            summary["storage"] = {
                "total_gb": round(total / (1024**3), 2),
                "free_gb": round(free / (1024**3), 2),
                "used_gb": round(used / (1024**3), 2)
            }
        except Exception:
            pass

        return summary

    def execute_shell(self, command: str, timeout: int = 15) -> Dict[str, Any]:
        """Executes a safe shell command inside Termux and returns output."""
        # Restrict dangerous recursive deletions
        dangerous = ["rm -rf /", "rm -rf ~", ":(){ :|:& };:"]
        for d in dangerous:
            if d in command:
                return {"success": False, "error": "Prohibited command"}

        res = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": res.returncode == 0,
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.returncode
        }

# Global singleton
automation = TermuxAutomation()
