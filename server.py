import urllib.request
import re
import html
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

def fetch_telegram_configs(channel_name="NamazVPN"):
    url = f"https://t.me/s/{channel_name}"
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            content = html.unescape(content)
            pattern = r'(vless://[^\s<"\'`]+|vmess://[^\s<"\'`]+|trojan://[^\s<"\'`]+|ss://[^\s<"\'`]+|hysteria2://[^\s<"\'`]+|hy2://[^\s<"\'`]+|tuic://[^\s<"\'`]+)'
            raw_links = re.findall(pattern, content, re.IGNORECASE)
            # Cleanup & deduplicate
            cleaned = []
            seen = set()
            for l in raw_links:
                l = l.replace('&amp;', '&')
                if l not in seen:
                    seen.add(l)
                    cleaned.append(l)
            return cleaned
    except Exception as e:
        print(f"Error fetching channel: {e}")
        return []

class SubscriptionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        channel = params.get('channel', ['NamazVPN'])[0]

        if parsed.path == '/sub':
            configs = fetch_telegram_configs(channel)
            plain_text = "\n".join(configs)
            b64_content = base64.b64encode(plain_text.encode('utf-8')).decode('utf-8')
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b64_content.encode('utf-8'))
        elif parsed.path == '/raw':
            configs = fetch_telegram_configs(channel)
            plain_text = "\n".join(configs)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(plain_text.encode('utf-8'))
        else:
            configs = fetch_telegram_configs(channel)
            html_doc = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>V2Ray Subscription Generator - {channel}</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; max-width: 900px; margin: 0 auto; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid #334155; }}
        h1 {{ color: #38bdf8; margin-top: 0; }}
        .sub-box {{ background: #090d16; padding: 1rem; border-radius: 8px; font-family: monospace; color: #4ade80; word-break: break-all; margin: 1rem 0; border: 1px solid #1e293b; }}
        button {{ background: #0284c7; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: bold; cursor: pointer; }}
        button:hover {{ background: #0369a1; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ background: #0f172a; margin: 0.5rem 0; padding: 0.75rem; border-radius: 6px; font-family: monospace; font-size: 0.85rem; word-break: break-all; color: #94a3b8; }}
        .badge {{ background: #38bdf822; color: #38bdf8; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; margin-left: 0.5rem; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 لینک سابسکریپشن کانال @{channel}</h1>
        <p>این لینک را کپی کنید و در نرم‌افزارهای V2Ray (مانند v2rayNG, v2rayN, Shadowrocket) وارد کنید:</p>
        <div class="sub-box" id="subUrl">http://localhost:8000/sub?channel={channel}</div>
        <button onclick="navigator.clipboard.writeText(document.getElementById('subUrl').innerText); alert('لینک کپی شد!');">کپی لینک سابسکریپشن</button>
    </div>

    <div class="card">
        <h2>تعداد کانفیگ‌های فعال استخراج شده: <span class="badge">{len(configs)} کانفیگ</span></h2>
        <ul>
            {"".join(f"<li>{c}</li>" for c in configs)}
        </ul>
    </div>
</body>
</html>"""
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_doc.encode('utf-8'))

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SubscriptionHandler)
    print(f"Server running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
