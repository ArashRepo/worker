// Cloudflare Worker Script for Telegram V2Ray Subscription Generator
// Deploy this script for free on Cloudflare Workers (https://workers.cloudflare.com)

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Get channel name from query param (?channel=NamazVPN) or default to NamazVPN
    const channel = url.searchParams.get("channel") || "NamazVPN";
    const limit = parseInt(url.searchParams.get("limit") || "100");

    // Fetch Telegram channel web page
    const tgUrl = `https://t.me/s/${channel}`;
    try {
      const response = await fetch(tgUrl, {
        headers: {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
      });

      let html = await response.text();
      // Decode HTML entities
      html = html.replace(/&amp;/g, '&');

      // Regex matching standard v2ray protocols
      const pattern = /(vless:\/\/[^\s<"'\`]+|vmess:\/\/[^\s<"'\`]+|trojan:\/\/[^\s<"'\`]+|ss:\/\/[^\s<"'\`]+|hysteria2:\/\/[^\s<"'\`]+|hy2:\/\/[^\s<"'\`]+|tuic:\/\/[^\s<"'\`]+)/gi;
      
      let matches = html.match(pattern) || [];

      // Remove duplicates
      const uniqueLinks = [...new Set(matches)].slice(0, limit);

      // Plain raw list mode if ?raw=true
      if (url.searchParams.get("raw") === "true") {
        return new Response(uniqueLinks.join('\n'), {
          headers: {
            "content-type": "text/plain; charset=utf-8",
            "Access-Control-Allow-Origin": "*"
          }
        });
      }

      // Standard Base64 V2Ray subscription format
      const plainText = uniqueLinks.join('\n');
      const base64Content = btoa(unescape(encodeURIComponent(plainText)));

      return new Response(base64Content, {
        headers: {
          "content-type": "text/plain; charset=utf-8",
          "Access-Control-Allow-Origin": "*",
          "Cache-Control": "public, max-age=300" // Cache for 5 minutes
        }
      });

    } catch (err) {
      return new Response(`Error fetching configs: ${err.message}`, { status: 500 });
    }
  }
};
