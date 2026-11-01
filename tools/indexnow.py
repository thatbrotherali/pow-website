"""Tell IndexNow search engines (Bing, Yandex, Seznam, Naver and others) which pages changed in the latest push.
A page counts as changed when its content hash in lastmod.json changed. Run by .github/workflows/indexnow.yml."""
import json, subprocess, sys, urllib.request

KEY = "0a0ec9cc60ad544e9cbc3fa0b18619e8"
HOST = "peopleoftheworld.net"

def load(rev):
    try:
        return json.loads(subprocess.run(["git", "show", f"{rev}:lastmod.json"], capture_output=True, text=True, check=True).stdout)
    except Exception:
        return {}

new, old = load("HEAD"), load("HEAD^")
changed = [f for f, v in new.items() if old.get(f, {}).get("h") != v["h"]]
urls = [f"https://{HOST}/" + (f[:-10] if f.endswith("index.html") else f) for f in changed][:10000]
print(f"{len(urls)} changed pages")
if not urls:
    sys.exit(0)
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("IndexNow response:", r.status)
