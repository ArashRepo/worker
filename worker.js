export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const channel = url.searchParams.get("channel") || "NamazVPN";
    const limit = parseInt(url.searchParams.get("limit") || "30");

    const tgUrl = `https://t.me/s/${channel}`;
    try {
      const response = await fetch(tgUrl, {
        headers: {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
      });

      let html = await response.text();
      html = html.replace(/&amp;/g, '&');

      const pattern = /(vless:\/\/[^\s<"'\`]+|vmess:\/\/[^\s<"'\`]+|trojan:\/\/[^\s<"'\`]+|ss:\/\/[^\s<"'\`]+|hysteria2:\/\/[^\s<"'\`]+|hy2:\/\/[^\s<"'\`]+|tuic:\/\/[^\s<"'\`]+)/gi;
      let matches = html.match(pattern) || [];

      const uniqueLinks = [...new Set(matches)].slice(0, limit);

      if (url.searchParams.get("raw") === "true") {
        return new Response(uniqueLinks.join('\n'), {
          headers: {
            "content-type": "text/plain; charset=utf-8",
            "Access-Control-Allow-Origin": "*"
          }
        });
      }

      const plainText = uniqueLinks.join('\n');
      const base64Content = btoa(unescape(encodeURIComponent(plainText)));

      return new Response(base64Content, {
        headers: {
          "content-type": "text/plain; charset=utf-8",
          "Access-Control-Allow-Origin": "*",
          "Cache-Control": "public, max-age=300"
        }
      });

    } catch (err) {
      return new Response(`Error: ${err.message}`, { status: 500 });
    }
  }
};
