
import urllib.request
import re
import html
import base64
import urllib.parse
import json


def rename_config(config, name="VIP"):
    try:
        if config.lower().startswith("vmess://"):
            raw = config[len("vmess://"):]
            raw += "=" * (-len(raw) % 4)

            data = json.loads(
                base64.b64decode(raw).decode("utf-8")
            )

            data["ps"] = name

            encoded = base64.b64encode(
                json.dumps(
                    data,
                    separators=(",", ":"),
                    ensure_ascii=False
                ).encode("utf-8")
            ).decode("utf-8")

            return "vmess://" + encoded

        # Replace the display name for other supported protocols
        config = config.split("#", 1)[0]
        return config + "#" + urllib.parse.quote(name)

    except Exception:
        return config


def fetch_and_update(channel="NamazVPN", target_count=30):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    unique_links = []
    seen = set()
    url = f"https://t.me/s/{channel}"

    pattern = (
        r'(vless://[^\s<"\'`]+|'
        r'vmess://[^\s<"\'`]+|'
        r'trojan://[^\s<"\'`]+|'
        r'ss://[^\s<"\'`]+|'
        r'hysteria2://[^\s<"\'`]+|'
        r'hy2://[^\s<"\'`]+|'
        r'tuic://[^\s<"\'`]+)'
    )

    for page in range(5):
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                content = resp.read().decode("utf-8")
                content = html.unescape(content)

                raw_links = re.findall(
                    pattern,
                    content,
                    re.IGNORECASE
                )

                for link in raw_links:
                    link = link.replace("&amp;", "&")

                    if link not in seen:
                        seen.add(link)
                        unique_links.append(link)

                if len(unique_links) >= target_count:
                    break

                before_match = re.search(
                    r'href="(/s/' + re.escape(channel) +
                    r'\?before=\d+)"',
                    content
                )

                if before_match:
                    url = "https://t.me" + before_match.group(1)
                else:
                    break

        except Exception as e:
            print(f"Error fetching page {page + 1}: {e}")
            break

    # Rename the display name of each selected configuration
    final_configs = [
        rename_config(config, "VIP")
        for config in unique_links[:target_count]
    ]

    # Plain-text subscription content
    plain_text = "\n".join(final_configs)

    # Base64-encoded subscription content
    b64_content = base64.b64encode(
        plain_text.encode("utf-8")
    ).decode("utf-8")

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)

    with open("sub_raw.txt", "w", encoding="utf-8") as f:
        f.write(plain_text)

    print(
        f"Successfully updated subscription! "
        f"Generated {len(final_configs)} configs."
    )


if __name__ == "__main__":
    fetch_and_update("NamazVPN", 30)

