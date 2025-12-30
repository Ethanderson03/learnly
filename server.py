#!/usr/bin/env python3
"""
Learnly Server - Static file server with Anthropic API proxy
Run with: python server.py
"""

import http.server
import json
import os
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 4173
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

class LearnlyHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
        self.end_headers()

    def do_POST(self):
        """Handle POST requests to /api/chat"""
        if self.path == "/api/chat":
            self.handle_chat()
        else:
            self.send_error(404, "Not Found")

    def handle_chat(self):
        """Proxy chat requests to Anthropic API"""
        try:
            # Read request body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Get API key from request header
            api_key = self.headers.get("X-API-Key")
            if not api_key:
                self.send_json_error(400, "Missing API key")
                return

            # Prepare request to Anthropic
            messages = data.get("messages", [])
            system = data.get("system", "You are a helpful learning assistant. Help the user understand concepts deeply by breaking them down, asking clarifying questions, and building on their existing knowledge.")
            model = data.get("model", "claude-sonnet-4-20250514")
            max_tokens = data.get("max_tokens", 1024)

            anthropic_payload = {
                "model": model,
                "max_tokens": max_tokens,
                "system": system,
                "messages": messages
            }

            # Make request to Anthropic
            req = urllib.request.Request(
                ANTHROPIC_API_URL,
                data=json.dumps(anthropic_payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01"
                },
                method="POST"
            )

            try:
                with urllib.request.urlopen(req, timeout=60) as response:
                    result = json.loads(response.read().decode("utf-8"))

                    # Extract the assistant's response
                    assistant_message = ""
                    if result.get("content"):
                        for block in result["content"]:
                            if block.get("type") == "text":
                                assistant_message += block.get("text", "")

                    self.send_json_response({
                        "success": True,
                        "message": assistant_message,
                        "model": result.get("model"),
                        "usage": result.get("usage")
                    })

            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8")
                try:
                    error_data = json.loads(error_body)
                    error_message = error_data.get("error", {}).get("message", str(e))
                except:
                    error_message = error_body or str(e)
                self.send_json_error(e.code, error_message)

            except urllib.error.URLError as e:
                self.send_json_error(500, f"Network error: {str(e)}")

        except json.JSONDecodeError:
            self.send_json_error(400, "Invalid JSON")
        except Exception as e:
            self.send_json_error(500, str(e))

    def send_json_response(self, data):
        """Send a JSON response"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def send_json_error(self, code, message):
        """Send a JSON error response"""
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({
            "success": False,
            "error": message
        }).encode("utf-8"))

    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║                    LEARNLY SERVER                         ║
╠═══════════════════════════════════════════════════════════╣
║  Static files + Anthropic API proxy                       ║
║                                                           ║
║  Open: http://localhost:{PORT}                             ║
║                                                           ║
║  Press Ctrl+C to stop                                     ║
╚═══════════════════════════════════════════════════════════╝
    """)

    server = HTTPServer(("", PORT), LearnlyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()


if __name__ == "__main__":
    main()
