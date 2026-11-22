#!/usr/bin/env python3
"""Récupère l'identité visuelle d'une chaîne YouTube avant le montage.

    python3 scripts/branding.py https://www.youtube.com/@ta-chaine
    python3 scripts/branding.py https://www.youtube.com/@ta-chaine --site https://ton-site.fr

Écrit dans ./branding/ :
  avatar.jpg, banner.jpg      la photo et la bannière de la chaîne
  thumbs/<id>.jpg             les miniatures des dernières vidéos
  palette.png                 les couleurs trouvées, en bandes
  branding.json               couleurs (principales, accent, neutres), polices du site, sources

Besoin de : python3, yt-dlp (brew install yt-dlp ou pip install yt-dlp) et Pillow (pip install Pillow).
"""
import argparse
import colorsys
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow manque : pip install Pillow")

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131 Safari/537.36"}


def fetch(url, timeout=30):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def save(url, path):
    try:
        path.write_bytes(fetch(url))
        return True
    except Exception as e:
        print(f"  non téléchargé ({e}) : {url}", file=sys.stderr)
        return False


def channel_info(url, count):
    ytdlp = shutil.which("yt-dlp")
    if not ytdlp:
        sys.exit("yt-dlp manque : brew install yt-dlp (ou pip install yt-dlp)")
    base = url.rstrip("/")
    for suffix in ("/videos", "/featured", "/shorts"):
        if base.endswith(suffix):
            base = base[: -len(suffix)]
    r = subprocess.run([ytdlp, "-J", "--flat-playlist", "--playlist-end", str(count), base + "/videos"],
                       capture_output=True, text=True, timeout=180)
    if r.returncode:
        sys.exit(f"yt-dlp n'a pas pu lire la chaîne : {r.stderr.strip()[-300:]}")
    return json.loads(r.stdout)


def pick(thumbnails, wanted):
    for t in thumbnails or []:
        if t.get("id") == wanted:
            return t["url"]
    return None


def colours(path, k=6):
    img = Image.open(path).convert("RGB")
    img.thumbnail((240, 240))
    q = img.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    total = img.width * img.height
    out = []
    for count, idx in sorted(q.getcolors(), reverse=True):
        rgb = tuple(pal[idx * 3: idx * 3 + 3])
        out.append((rgb, count / total))
    return out


def hexa(rgb):
    return "#%02x%02x%02x" % rgb


def kind(rgb):
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in rgb))
    if l > 0.9:
        return "clair"
    if l < 0.12:
        return "sombre"
    if s < 0.18:
        return "gris"
    return "couleur"


def merge(samples):
    """Regroupe les teintes proches (pas de 24 sur chaque canal) et cumule leur part."""
    buckets = Counter()
    rep = {}
    for rgb, share in samples:
        key = tuple(c // 24 for c in rgb)
        buckets[key] += share
        rep.setdefault(key, rgb)
    total = sum(buckets.values()) or 1
    return [(rep[k], v / total) for k, v in buckets.most_common()]


def site_style(url):
    out = {"url": url, "theme_color": None, "colors": [], "fonts": []}
    try:
        html = fetch(url).decode("utf-8", "ignore")
    except Exception as e:
        out["error"] = str(e)
        return out
    m = re.search(r'<meta[^>]+name=["\']theme-color["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if m:
        out["theme_color"] = m.group(1)
    css = [html]
    for href in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']([^"\']+)', html, re.I)[:6]:
        try:
            css.append(fetch(urllib.parse.urljoin(url, href), 20).decode("utf-8", "ignore"))
        except Exception:
            pass
    text = "\n".join(css)
    found = Counter()
    for h in re.findall(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", text):
        h = h.lower()
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        found["#" + h] += 1
    for r_, g_, b_ in re.findall(r"rgba?\(\s*(\d{1,3})[ ,]+(\d{1,3})[ ,]+(\d{1,3})", text):
        found[hexa((int(r_), int(g_), int(b_)))] += 1
    out["colors"] = [{"hex": h, "uses": n, "kind": kind(tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)))}
                     for h, n in found.most_common(12)]
    fonts = Counter()
    for fam in re.findall(r"font-family\s*:\s*([^;}{]+)", text, re.I):
        first = fam.split(",")[0].strip().strip("'\"")
        if first and not first.startswith("var(") and "fallback" not in first.lower() and first.lower() not in ("inherit", "initial", "sans-serif", "serif", "monospace"):
            fonts[first] += 1
    for fam in re.findall(r"fonts\.googleapis\.com/css2?\?family=([^&\"']+)", text):
        fonts[urllib.parse.unquote_plus(fam.split(":")[0])] += 5
    out["fonts"] = [f for f, _ in fonts.most_common(5)]
    return out


def strip(path, colors):
    w, h = 1200, 160
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    x = 0
    for c in colors:
        cw = max(60, int(w * c["share"]))
        d.rectangle([x, 0, x + cw, h], fill=c["hex"])
        d.text((x + 8, h - 22), c["hex"], fill="black" if kind(tuple(int(c["hex"][i:i + 2], 16) for i in (1, 3, 5))) in ("clair", "couleur") else "white")
        x += cw
        if x >= w:
            break
    img.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("channel", help="URL de la chaîne YouTube (https://www.youtube.com/@...)")
    ap.add_argument("--site", help="site du créateur, pour ses couleurs et polices exactes")
    ap.add_argument("--count", type=int, default=10, help="nombre de miniatures récentes (10 par défaut)")
    ap.add_argument("--out", default="branding", help="dossier de sortie (branding/ par défaut)")
    a = ap.parse_args()

    out = Path(a.out)
    (out / "thumbs").mkdir(parents=True, exist_ok=True)
    print("Lecture de la chaîne...")
    info = channel_info(a.channel, a.count)
    avatar = pick(info.get("thumbnails"), "avatar_uncropped")
    banner = pick(info.get("thumbnails"), "banner_uncropped")
    if avatar:
        save(avatar, out / "avatar.jpg")
    if banner:
        save(banner, out / "banner.jpg")

    samples, thumbs = [], []
    for e in info.get("entries") or []:
        vid = e.get("id")
        if not vid:
            continue
        p = out / "thumbs" / f"{vid}.jpg"
        ok = save(f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg", p) or save(f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg", p)
        if not ok:
            continue
        cs = colours(p)
        samples += cs
        thumbs.append({"id": vid, "title": e.get("title"), "file": str(p),
                       "colors": [{"hex": hexa(c), "share": round(s, 3), "kind": kind(c)} for c, s in cs]})
    if banner and (out / "banner.jpg").exists():
        samples += [(c, s * 2) for c, s in colours(out / "banner.jpg")]

    merged = merge(samples)
    palette = [{"hex": hexa(c), "share": round(s, 3), "kind": kind(c)} for c, s in merged[:12]]
    chroma = [c for c in palette if c["kind"] == "couleur"]
    accent = max(chroma, key=lambda c: c["share"] * colorsys.rgb_to_hls(*(int(c["hex"][i:i + 2], 16) / 255 for i in (1, 3, 5)))[2],
                 default=None)
    data = {
        "channel": info.get("channel") or info.get("uploader"),
        "channel_url": info.get("channel_url"),
        "handle": info.get("uploader_id"),
        "palette": palette,
        "accent_guess": accent["hex"] if accent else None,
        "neutrals": [c["hex"] for c in palette if c["kind"] != "couleur"][:4],
        "thumbnails": thumbs,
        "site": site_style(a.site) if a.site else None,
        "to_confirm": [
            "La couleur d'accent et la couleur principale (le créateur valide ou corrige)",
            "La police des titres de ses miniatures (lue à l'oeil sur thumbs/, ou celle de son site)",
            "Son logo, s'il en a un (fichier fourni par le créateur)",
            "Chaîne avec ou sans visage (face caméra ou faceless)",
        ],
    }
    (out / "branding.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    strip(out / "palette.png", palette)
    print(f"OK : {out}/branding.json, {len(thumbs)} miniatures, accent proposé {data['accent_guess']}")
    if data["site"] and data["site"].get("fonts"):
        print(f"Polices du site : {', '.join(data['site']['fonts'])}")


if __name__ == "__main__":
    main()
