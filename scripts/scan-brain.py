#!/usr/bin/env python3
"""Quét Bộ Não Thứ 2 → sinh brain.js cho trang chủ METTA EYE.

Cách dùng (chạy ở thư mục gốc repo metta-eye):
    python3 scripts/scan-brain.py ../Nao-thu-2 ../bo-nao-claude-v2

Chỉ xuất TIÊU ĐỀ / tên / tên miền công khai — không xuất nội dung,
không xuất lead, số điện thoại, email, khoá API hay link Drive riêng.
(repo metta-eye đang để public.)
"""
import glob, json, os, re, sys, datetime

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

nao = sys.argv[1] if len(sys.argv) > 1 else "../Nao-thu-2"
extra = sys.argv[2:]  # các repo skill khác (vd bo-nao-claude-v2)


def front(path):
    t = open(path, encoding="utf8", errors="ignore").read()
    m = re.match(r"^---\s*\n([\s\S]*?)\n---", t)
    if not m:
        return {}, t
    if yaml:
        try:
            return (yaml.safe_load(m.group(1)) or {}), t
        except Exception:
            pass
    d = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.strip()
    return d, t


def clean(s, n=170):
    s = re.sub(r"\s+", " ", str(s or "")).strip().strip('"')
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


# ---------- Tri thức (wiki) ----------
# Trang có nhắc người thật ngoài anh Luân (anh/chị/gia đình …) → không xuất ra trang public.
PRIVATE = re.compile(r"\b(anh|chị|gia đình|học viên [A-ZĐ])\b", re.I)
wiki, hidden = [], 0
for p in sorted(glob.glob(os.path.join(nao, "wiki", "*", "*.md"))):
    fm, _ = front(p)
    kind = p.split(os.sep)[-2]
    if PRIVATE.search(str(fm.get("title") or "")):
        hidden += 1
        continue
    wiki.append({
        "title": clean(fm.get("title") or os.path.basename(p)[:-3], 110),
        "kind": kind,
        "tags": [str(x) for x in (fm.get("tags") or [])][:5] if isinstance(fm.get("tags"), list) else [],
        "updated": str(fm.get("updated") or fm.get("created") or ""),
    })

# ---------- Skill ----------
skills, seen = [], set()
roots = [os.path.join(nao, ".claude", "skills"), os.path.join(nao, "Skill marketing")]
for r in extra:
    roots += glob.glob(os.path.join(r, "plugins", "*", "skills"))
for root in roots:
    for p in sorted(glob.glob(os.path.join(root, "*", "SKILL.md"))):
        fm, _ = front(p)
        name = str(fm.get("name") or p.split(os.sep)[-2]).strip()
        if name in seen:
            continue
        seen.add(name)
        skills.append({"name": name, "desc": clean(fm.get("description"), 180)})

# ---------- Trang đang chạy ----------
hosts = set()
for f in glob.glob(os.path.join(nao, "**", "*.*"), recursive=True):
    if f.endswith((".html", ".md", ".json", ".txt")) and "/.git/" not in f:
        try:
            hosts |= set(re.findall(r"([a-z0-9-]+)\.deche1nguoi\.com", open(f, encoding="utf8", errors="ignore").read()))
        except Exception:
            pass
pages, seenp = [], set()
for d in sorted(glob.glob(os.path.join(nao, "DEPLOY CÁC TRANG", "*"))):
    if not os.path.isdir(d):
        continue
    slug = os.path.basename(d).replace("-deploy", "").replace("-cf", "")
    meta = {}
    if os.path.exists(os.path.join(d, "deploy.json")):
        try:
            meta = json.load(open(os.path.join(d, "deploy.json"), encoding="utf8"))
        except Exception:
            meta = {}
    title = ""
    ix = os.path.join(d, "index.html")
    if os.path.exists(ix):
        h = open(ix, encoding="utf8", errors="ignore").read()
        m = re.search(r"<title>(.*?)</title>", h, re.S)
        title = re.sub(r"&amp;", "&", m.group(1)).strip() if m else ""
    if not title or title in seenp:
        continue
    seenp.add(title)
    status = meta.get("status") or "unknown"  # không có deploy.json → chưa ghi trạng thái
    domain = meta.get("domain") or ""
    if not domain and status == "live" and meta.get("slug"):
        domain = meta["slug"] + ".deche1nguoi.com"  # quy ước subdomain của anh Luân
    if not domain and status == "unknown" and slug in hosts:
        domain, status = slug + ".deche1nguoi.com", "linked"  # chưa có deploy.json nhưng đã có link dùng thật
    pages.append({"slug": meta.get("slug") or slug, "title": clean(title.split("|")[0].split(" — ")[0], 70),
                  "sub": clean(" — ".join(title.split(" — ")[1:]).split("|")[0], 90),
                  "domain": domain, "status": status, "updated": meta.get("updatedAt") or ""})

data = {"scannedAt": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).strftime("%Y-%m-%d %H:%M"),
        "wiki": wiki, "hiddenWiki": hidden, "skills": skills, "pages": pages}
out = "window.BRAIN=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
open("brain.js", "w", encoding="utf8").write(out)
print(f"brain.js: {len(wiki)} trang tri thức (ẩn {hidden} trang riêng tư) · {len(skills)} skill · {len(pages)} trang bán hàng")
