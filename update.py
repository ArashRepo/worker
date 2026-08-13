import urllib.request
import re
import html
import base64

def fetch_and_update(channel="NamazVPN", target_count=30):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    unique_links = []
    seen = set()
    url = f"https://t.me/s/{channel}"
    
    for page in range(5):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                content = resp.read().decode('utf-8')
                content = html.unescape(content)
                
                pattern = r'(vless://[^\s<"\'`]+|vmess://[^\s<"\'`]+|trojan://[^\s<"\'`]+|ss://[^\s<"\'`]+|hysteria2://[^\s<"\'`]+|hy2://[^\s<"\'`]+|tuic://[^\s<"\'`]+)'
                raw_links = re.findall(pattern, content, re.IGNORECASE)
                
                for l in raw_links:
                    l = l.replace('&amp;', '&')
                    if l not in seen:
                        seen.add(l)
                        unique_links.append(l)
                
                if len(unique_links) >= target_count:
                    break
                    
                before_match = re.search(r'href="(/s/' + channel + r'\?before=\d+)"', content)
                if before_match:
                    url = f"https://t.me{before_match.group(1)}"
                else:
                    break
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
            
    final_configs = unique_links[:target_count]
    
    plain_text = "\n".join(final_configs)
    b64_content = base64.b64encode(plain_text.encode('utf-8')).decode('utf-8')
    
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)
        
    with open("sub_raw.txt", "w", encoding="utf-8") as f:
        f.write(plain_text)
        
    print(f"Successfully updated subscription! Generated {len(final_configs)} configs.")

if __name__ == "__main__":
    fetch_and_update("NamazVPN", 30)
