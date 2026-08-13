import urllib.request
import re
import html
import base64
import os

def fetch_and_update():
    channel = "NamazVPN"
    url = f"https://t.me/s/{channel}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            content = html.unescape(content)
            
            # Extract configs
            pattern = r'(vless://[^\s<"\'`]+|vmess://[^\s<"\'`]+|trojan://[^\s<"\'`]+|ss://[^\s<"\'`]+|hysteria2://[^\s<"\'`]+|hy2://[^\s<"\'`]+|tuic://[^\s<"\'`]+)'
            raw_links = re.findall(pattern, content, re.IGNORECASE)
            
            # Clean and deduplicate
            cleaned = []
            seen = set()
            for l in raw_links:
                l = l.replace('&amp;', '&')
                if l not in seen:
                    seen.add(l)
                    cleaned.append(l)
            
            plain_text = "\n".join(cleaned)
            b64_content = base64.b64encode(plain_text.encode('utf-8')).decode('utf-8')
            
            # Write Base64 subscription format (for v2ray clients)
            with open("sub.txt", "w", encoding="utf-8") as f:
                f.write(b64_content)
                
            # Write raw plaintext format
            with open("sub_raw.txt", "w", encoding="utf-8") as f:
                f.write(plain_text)
                
            print(f"Successfully updated subscription! Found {len(cleaned)} configs.")
            
    except Exception as e:
        print(f"Error fetching channel: {e}")

if __name__ == "__main__":
    fetch_and_update()
