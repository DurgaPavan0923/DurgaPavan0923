#!/usr/bin/env python3
"""Generate the animated SVG assets used by the profile README (standard library only).

  python scripts/generate_profile_assets.py            # live assets: repos, stats, trophies (GitHub API)
  python scripts/generate_profile_assets.py --static   # static assets: header, titles, cards, buttons...
  python scripts/generate_profile_assets.py --offline  # empty placeholder state (no network)
"""
import datetime as dt, json, os, sys, textwrap
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
USER = os.environ.get("PROFILE_USER", "DurgaPavan0923")
FONT = "'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
BLUE, LIGHT, BG, TEXT, MUTED, EDGE = "#2563EB", "#58A6FF", "#0D1117", "#E6EDF3", "#8B949E", "#30363D"
REDUCE = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
UP = "@keyframes up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}"
PULSE = "@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}"
FLOAT = "@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}"


def svg(w, h, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>text{{font-family:{FONT}}}{UP}{PULSE}{FLOAT}{css}{REDUCE}</style>{body}</svg>')


def save(name, content):
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / name).write_text(content, encoding="utf-8")
    print("wrote", name)


def txt(x, y, s, size=14, weight=400, fill=TEXT, anchor="start", cls="", style=""):
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    return (f'<text{c}{st} x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}">{escape(str(s))}</text>')


def wave(y, amp, h):
    return f"M0 {y} q112.5 -{amp} 225 0" + " t225 0" * 7 + f" V{h} H0 Z"


WAVE_CSS = (".w1{animation:drift 9s linear infinite}.w2{animation:drift 14s linear infinite reverse}"
            "@keyframes drift{from{transform:translateX(0)}to{transform:translateX(-450px)}}")


# ------------------------------------------------------------------ static assets
def header():
    W, H = 900, 240
    layers = [(745, [70, 120, 170]), (805, [50, 95, 145, 190]), (865, [70, 120, 170])]
    lines, nodes, d = [], [], 0
    for (x1, a), (x2, b) in zip(layers, layers[1:]):
        lines += [f'<line class="flow" x1="{x1}" y1="{p}" x2="{x2}" y2="{q}"/>' for p in a for q in b]
    for x, ys in layers:
        for y in ys:
            nodes.append(f'<circle class="node" cx="{x}" cy="{y}" r="5" style="animation-delay:{d * .25:.2f}s"/>')
            d += 1
    css = (".t1{font-size:40px;font-weight:700;fill:#fff;animation:up 1s ease-out .2s both}"
           ".t2{font-size:21px;fill:#BFDBFE;animation:up 1s ease-out .6s both}"
           ".t3{font-size:16px;fill:#93C5FD;letter-spacing:1px;animation:up 1s ease-out 1s both}"
           ".flow{stroke:#93C5FD;stroke-opacity:.55;stroke-width:1;stroke-dasharray:4 6;animation:flow 1.6s linear infinite}"
           ".node{fill:#fff;transform-box:fill-box;transform-origin:center;animation:pl 2.4s ease-in-out infinite}"
           "@keyframes flow{to{stroke-dashoffset:-20}}"
           "@keyframes pl{0%,100%{opacity:.45;transform:scale(1)}50%{opacity:1;transform:scale(1.6)}}" + WAVE_CSS)
    body = (f'<title>Rajana Durga Pavan Kumar, AI/ML engineer in progress</title>'
            f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/>'
            f'<stop offset=".55" stop-color="#1E3A8A"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
            f'<clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>'
            f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'<g>{"".join(lines)}</g><g>{"".join(nodes)}</g>'
            f'<path class="w1" d="{wave(205, 26, H)}" fill="#fff" fill-opacity=".07"/>'
            f'<path class="w2" d="{wave(215, 20, H)}" fill="#fff" fill-opacity=".10"/>'
            f'<text class="t1" x="48" y="100">Rajana Durga Pavan Kumar</text>'
            f'<text class="t2" x="48" y="140">AI/ML engineer in progress · Research-oriented developer</text>'
            f'<text class="t3" x="48" y="176">NLP · DEEP LEARNING · RECOMMENDER SYSTEMS</text></g>')
    save("header.svg", svg(W, H, body, css))


def footer():
    W, H = 900, 90
    body = (f'<defs><linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/>'
            f'<stop offset="1" stop-color="{BLUE}"/></linearGradient><clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>'
            f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'<path class="w1" d="{wave(48, 22, H)}" fill="#fff" fill-opacity=".08"/>'
            f'<path class="w2" d="{wave(60, 16, H)}" fill="#fff" fill-opacity=".12"/></g>')
    save("footer.svg", svg(W, H, body, WAVE_CSS))


def divider():
    body = (f'<defs><linearGradient id="g"><stop offset="0" stop-color="{LIGHT}" stop-opacity="0"/><stop offset=".5" stop-color="{LIGHT}"/>'
            f'<stop offset="1" stop-color="{LIGHT}" stop-opacity="0"/></linearGradient><clipPath id="c"><rect width="900" height="4" rx="2"/></clipPath></defs>'
            f'<g clip-path="url(#c)"><rect width="900" height="4" fill="{BLUE}" fill-opacity=".25"/><rect class="gl" x="-300" width="300" height="4" fill="url(#g)"/></g>')
    css = ".gl{animation:sl 4s linear infinite}@keyframes sl{from{transform:translateX(0)}to{transform:translateX(1200px)}}"
    save("divider.svg", svg(900, 4, body, css))


def title(slug, text):
    w, h = int(len(text) * 15.5 + 74), 48
    body = (f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#1E3A8A"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
            f'<linearGradient id="s"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><clipPath id="c"><rect width="{w}" height="{h}" rx="24"/></clipPath></defs>'
            f'<g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="url(#g)"/><rect class="sh" x="-90" width="80" height="{h}" fill="url(#s)"/></g>'
            f'<circle class="dot" cx="26" cy="24" r="5" fill="#fff"/>'
            + txt(44, 31, text, 22, 700, "#fff", cls="tx"))
    css = (f".sh{{animation:sh 3.5s ease-in-out infinite}}@keyframes sh{{from{{transform:translateX(0)}}to{{transform:translateX({w + 100}px)}}}}"
           ".dot{animation:pulse 1.6s ease-in-out infinite}.tx{animation:up .8s ease-out both}")
    save(f"title-{slug}.svg", svg(w, h, body, css))


def rotator(slug, lines, w=600, size=20, per=3.2):
    n, h = len(lines), 56
    keep = 100 / n
    css = (f".r{{animation:rot {n * per}s linear infinite backwards}}"
           f"@keyframes rot{{0%{{opacity:0;transform:translateY(10px)}}4%{{opacity:1;transform:none}}{keep - 4:.2f}%{{opacity:1;transform:none}}"
           f"{keep:.2f}%{{opacity:0;transform:translateY(-10px)}}100%{{opacity:0}}}}"
           "@media (prefers-reduced-motion:reduce){.r:nth-of-type(n+2){display:none}}")
    body = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="28" fill="{BG}" stroke="{BLUE}" stroke-width="1.5"/><g>'
            + "".join(txt(w / 2, 35, s, size, 600, TEXT, "middle", "r", f"animation-delay:{i * per}s") for i, s in enumerate(lines))
            + "</g>")
    save(f"{slug}.svg", svg(w, h, body, css))


def pills(slug, rows, w=700, size=15, h=40, gap=14):
    pw = lambda s: len(s) * size * .64 + 36
    out, d = [], 0
    for r, row in enumerate(rows):
        total = sum(pw(s) for s in row) + 12 * (len(row) - 1)
        x, y = (w - total) / 2, 6 + r * (h + gap)
        for s in row:
            out.append(f'<g style="animation:up .7s ease-out {d * .12:.2f}s both"><g class="fl" style="animation-delay:{d * .4:.1f}s">'
                       f'<rect x="{x:.1f}" y="{y}" width="{pw(s):.1f}" height="{h}" rx="20" fill="{BG}" stroke="{BLUE}" stroke-width="1.5"/>'
                       + txt(f"{x + pw(s) / 2:.1f}", y + 26, s, size, 600, TEXT, "middle") + "</g></g>")
            x += pw(s) + 12
            d += 1
    save(f"{slug}.svg", svg(w, 12 + len(rows) * (h + gap) - gap, "".join(out), ".fl{animation:float 3.6s ease-in-out infinite}"))


def skills():
    rows = [["Python", "Java", "C", "C++", "TensorFlow", "PyTorch", "scikit-learn"],
            ["NumPy", "Pandas", "Matplotlib", "Flask", "Docker", "Git", "GitHub", "VS Code", "Linux"]]
    W, H, css, body = 600, 108, "", ""
    for i, items in enumerate(rows):
        x, chips = 0, []
        for _ in range(3):
            for s in items:
                cw = len(s) * 9.6 + 34
                chips.append(f'<rect x="{x:.1f}" y="0" width="{cw:.1f}" height="38" rx="19" fill="{BG}" stroke="#1E3A8A" stroke-width="1.5"/>'
                             f'<circle cx="{x + 16:.1f}" cy="19" r="3.5" fill="{LIGHT}"/>' + txt(f"{x + 27:.1f}", 24, s, 15, 600))
                x += cw + 12
        period = x / 3
        css += (f".m{i}{{animation:m{i} {period / 38:.1f}s linear infinite{' reverse' if i else ''}}}"
                f"@keyframes m{i}{{from{{transform:translateX(0)}}to{{transform:translateX(-{period:.1f}px)}}}}")
        body += f'<g transform="translate(0 {8 + i * 52})"><g class="m{i}">{"".join(chips)}</g></g>'
    defs = (f'<defs><linearGradient id="f"><stop offset="0" stop-color="#000"/><stop offset=".08" stop-color="#fff"/>'
            f'<stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
            f'<mask id="m"><rect width="{W}" height="{H}" fill="url(#f)"/></mask></defs>')
    save("skills.svg", svg(W, H, defs + f'<g mask="url(#m)">{body}</g>', css))


def textcard(slug, paras, w=600, size=17):
    y, out, d = 40, [], 0
    for p in paras:
        for line in textwrap.wrap(p, 52):
            out.append(txt(28, y, line, size, 400, TEXT, style=f"animation:up .8s ease-out {d * .35:.2f}s both"))
            y += size + 11
            d += 1
        y += 10
    h = y + 6
    body = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}" stroke="{EDGE}"/>'
            f'<rect x="1" y="14" width="4" height="{h - 28}" rx="2" fill="{BLUE}"/>' + "".join(out))
    save(f"{slug}.svg", svg(w, h, body))


def card(slug, name, tags, sections, delay=0.0, w=600):
    out = [txt(28, 40, name, 22, 700, "#fff", style=f"animation:up .8s ease-out {delay}s both")]
    x = 28
    for t in tags:
        pw = len(t) * 7.4 + 22
        out.append(f'<g style="animation:up .8s ease-out {delay + .15}s both"><rect x="{x:.1f}" y="54" width="{pw:.1f}" height="24" rx="12" fill="#1E3A8A"/>'
                   + txt(f"{x + pw / 2:.1f}", 70, t, 12, 600, "#DBEAFE", "middle") + "</g>")
        x += pw + 8
    y, k = 108, 0
    for label, text in sections:
        out.append(txt(28, y, label.upper(), 11, 700, LIGHT, style=f"letter-spacing:1px;animation:up .8s ease-out {delay + .3 + k * .15}s both"))
        y += 20
        for line in textwrap.wrap(text, 62):
            out.append(txt(28, y, line, 14.5, 400, "#C9D1D9", style=f"animation:up .8s ease-out {delay + .35 + k * .15}s both"))
            y += 20
        y += 14
        k += 1
    h = y - 2
    body = (f'<defs><linearGradient id="g"><stop offset="0" stop-color="{LIGHT}" stop-opacity="0"/><stop offset=".5" stop-color="{LIGHT}"/><stop offset="1" stop-color="{LIGHT}" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="c"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14"/></clipPath></defs>'
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}" stroke="{EDGE}"/>'
            f'<g clip-path="url(#c)"><rect class="gl" x="-260" width="260" height="3" y="1" fill="url(#g)"/></g>'
            f'<circle class="dot" cx="{w - 26}" cy="28" r="5" fill="{LIGHT}"/>' + "".join(out))
    css = (f".gl{{animation:sl 4.5s linear infinite}}@keyframes sl{{from{{transform:translateX(0)}}to{{transform:translateX({w + 260}px)}}}}"
           ".dot{animation:pulse 1.8s ease-in-out infinite}")
    save(f"{slug}.svg", svg(w, h, body, css))


def button(slug, label, w=170):
    body = (f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#1E3A8A"/><stop offset="1" stop-color="{BLUE}"/></linearGradient></defs>'
            f'<rect class="glow" x="1.5" y="1.5" width="{w - 3}" height="41" rx="21" fill="url(#g)" stroke="{LIGHT}" stroke-width="2"/>'
            + txt(w / 2, 28, label, 16, 700, "#fff", "middle"))
    save(f"btn-{slug}.svg", svg(w, 44, body, ".glow{animation:gl 2.4s ease-in-out infinite}@keyframes gl{0%,100%{stroke-opacity:.2}50%{stroke-opacity:1}}"))


def static_assets():
    header(); footer(); divider()
    for slug, t in [("about", "About"), ("focus", "Focus Areas"), ("stack", "Tech Stack"), ("projects", "Featured Projects"),
                    ("repos", "Latest Repositories"), ("trophies", "Trophies"), ("stats", "GitHub Stats"),
                    ("achievements", "Achievements & Certifications"), ("learning", "Currently Learning / Building"),
                    ("vision", "Career Vision"), ("connect", "Connect")]:
        title(slug, t)
    rotator("tagline", ["Deep Learning · NLP · Recommender Systems", "Predictive Modeling & Data Science", "AI Research & System Design"])
    rotator("vision", ["AI/ML Research", "Data Science", "Intelligent Systems Development", "AI-driven Product Innovation"], size=22)
    pills("edu", [["B.Tech · CSE (AI & ML)", "ITER · SOA University"]], size=15)
    textcard("about", ["I build machine learning systems end to end: preprocessing, feature engineering, training and evaluation.",
                       "I treat projects as experiments: build, measure, iterate."])
    pills("focus", [["Machine Learning Algorithms", "Recommendation Systems"], ["Deep Learning: Neural Networks, Seq2Seq, NLP"],
                    ["Data Science & Predictive Modeling", "AI Research & System Design"]])
    skills()
    card("project-news", "News Summarization", ["Seq2Seq", "Encoder-decoder", "NLP"],
         [("Problem", "Condense long news articles into short, readable summaries."),
          ("Approach", "Encoder-decoder Seq2Seq model for abstractive summarization, with preprocessing, tokenization, training and evaluation.")], 0.0)
    card("project-recsys", "Recommendation System", ["Collaborative filtering", "Content-based", "Similarity metrics"],
         [("Problem", "Suggest relevant items to users from their past interactions."),
          ("Approach", "Collaborative and content-based filtering using a user-item matrix and similarity metrics, with optimization.")], 0.2)
    card("project-pipeline", "End-to-End ML Pipeline", ["Feature engineering", "Classification", "Regression"],
         [("Problem", "Turn raw, messy data into reliable predictions."),
          ("Approach", "Data cleaning, feature engineering, classification and regression models, evaluated with metrics.")], 0.4)
    card("project-research", "AI Research Exploration", ["Deep learning", "Neural architectures", "Experimentation"],
         [("Problem", "Understand how different neural architectures behave."),
          ("Approach", "Hands-on experimentation with neural architectures.")], 0.6)
    for slug, label in [("linkedin", "LinkedIn"), ("email", "Email"), ("portfolio", "Portfolio")]:
        button(slug, label)


# ------------------------------------------------------------------ live assets (GitHub API)
def api(path):
    req = Request("https://api.github.com" + path, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-assets"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urlopen(req, timeout=20) as r:
        return json.load(r)


LANG_COLORS = {"Python": "#3572A5", "Jupyter Notebook": "#DA5B0B", "Java": "#B07219", "C": "#555555", "C++": "#F34B7D",
               "JavaScript": "#F1E05A", "HTML": "#E34C26", "CSS": "#563D7C", "Shell": "#89E051", "TypeScript": "#3178C6"}
TROPHIES = [("Repositories", "repos", [1, 5, 10, 20]), ("Stars", "stars", [1, 5, 20, 50]), ("Followers", "followers", [1, 5, 15, 50]),
            ("Forks", "forks", [1, 3, 10, 25]), ("Languages", "langs", [1, 3, 5, 8]), ("Years on GitHub", "years", [1, 2, 4, 6])]
RANKS, RANK_COLORS = ["C", "B", "A", "S"], {"C": "#58A6FF", "B": "#CD7F32", "A": "#C9D1D9", "S": "#F5C542"}


def fetch():
    user = api(f"/users/{USER}")
    repos, page = [], 1
    while True:
        chunk = api(f"/users/{USER}/repos?per_page=100&page={page}&type=owner&sort=pushed")
        repos += chunk
        if len(chunk) < 100 or page >= 5:
            break
        page += 1
    return user, [r for r in repos if not r["fork"] and r["name"].lower() != USER.lower()]


def repos_svg(repos, w=600, pending=False):
    top = repos[:6]
    if not top:
        body = (f'<rect x="1" y="1" width="{w - 2}" height="78" rx="14" fill="{BG}" stroke="{EDGE}"/>'
                + txt(w / 2, 46, "Loads after the first workflow run" if pending else "No public repositories yet", 16, 600, MUTED, "middle"))
        return svg(w, 80, body)
    out = []
    for i, r in enumerate(top):
        y, d = 18 + i * 68, i * .15
        desc = (r.get("description") or "No description yet")
        desc = desc if len(desc) <= 76 else desc[:75].rstrip() + "…"
        lang = r.get("language") or ""
        meta, x = [], 24
        if lang:
            meta += [f'<circle cx="{x}" cy="{y + 52}" r="5" fill="{LANG_COLORS.get(lang, MUTED)}"/>', txt(x + 10, y + 56, lang, 12, 400, MUTED)]
            x += 10 + len(lang) * 6.6 + 18
        meta.append(txt(x, y + 56, f'★ {r["stargazers_count"]}', 12, 400, MUTED)); x += 48
        meta.append(txt(x, y + 56, f'forks {r["forks_count"]}', 12, 400, MUTED)); x += 70
        meta.append(txt(x, y + 56, f'pushed {r["pushed_at"][:10]}', 12, 400, MUTED))
        out.append(f'<g style="animation:up .8s ease-out {d:.2f}s both"><rect class="acc" x="12" y="{y}" width="3" height="48" rx="1.5" fill="{BLUE}" style="animation-delay:{d:.2f}s"/>'
                   + txt(24, y + 16, r["name"], 16, 700, LIGHT) + txt(24, y + 36, desc, 13, 400, "#C9D1D9") + "".join(meta) + "</g>")
    h = 18 + len(top) * 68 + 4
    body = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}" stroke="{EDGE}"/>'
            f'<circle class="dot" cx="{w - 24}" cy="22" r="4.5" fill="{LIGHT}"/>' + "".join(out))
    return svg(w, h, body, ".dot{animation:pulse 1.8s ease-in-out infinite}.acc{transform-box:fill-box;transform-origin:top;animation:gy .9s ease-out both}"
               "@keyframes gy{from{transform:scaleY(0)}to{transform:scaleY(1)}}")


def metrics(user, repos):
    langs = {}
    for r in repos:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    created = dt.datetime.strptime(user["created_at"][:10], "%Y-%m-%d")
    return {"repos": len(repos), "stars": sum(r["stargazers_count"] for r in repos), "followers": user["followers"],
            "forks": sum(r["forks_count"] for r in repos), "langs": len(langs), "years": (dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) - created).days // 365,
            "since": created.year, "lang_counts": sorted(langs.items(), key=lambda kv: -kv[1])}


def stats_svg(m, w=600, h=230):
    cells = [("Public repos", m["repos"]), ("Stars earned", m["stars"]), ("Followers", m["followers"]), ("Forks", m["forks"])]
    out = [txt(24, 36, "OVERVIEW", 11, 700, LIGHT, style="letter-spacing:1px"), txt(340, 36, "TOP LANGUAGES BY REPOSITORY", 11, 700, LIGHT, style="letter-spacing:1px")]
    for i, (lab, val) in enumerate(cells):
        x, y = 24 + (i % 2) * 150, 62 + (i // 2) * 74
        out.append(f'<g style="animation:up .8s ease-out {i * .15:.2f}s both">' + txt(x, y + 30, val, 32, 700, "#fff") + txt(x, y + 52, lab, 12, 400, MUTED) + "</g>")
    total = sum(c for _, c in m["lang_counts"])
    if not total:
        out.append(txt(340, 80, "No language data yet", 13, 400, MUTED))
    for i, (lang, c) in enumerate(m["lang_counts"][:5]):
        y, pct = 62 + i * 30, c / total
        name = lang if len(lang) <= 14 else lang[:13] + "…"
        out.append(txt(340, y + 9, name, 12, 400, "#C9D1D9") + f'<rect x="432" y="{y}" width="120" height="8" rx="4" fill="{EDGE}"/>'
                   f'<rect class="bar" x="432" y="{y}" width="{max(pct * 120, 4):.1f}" height="8" rx="4" fill="{LANG_COLORS.get(lang, LIGHT)}" style="animation-delay:{i * .15:.2f}s"/>'
                   + txt(560, y + 9, f"{pct * 100:.0f}%", 11, 400, MUTED))
    out.append(txt(24, h - 14, f'Member since {m["since"]} · public GitHub data · refreshed {dt.datetime.now(dt.timezone.utc).replace(tzinfo=None):%Y-%m-%d} UTC', 11, 400, MUTED))
    body = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}" stroke="{EDGE}"/>'
            f'<line x1="320" y1="24" x2="320" y2="{h - 34}" stroke="{EDGE}"/>' + "".join(out))
    return svg(w, h, body, ".bar{transform-box:fill-box;transform-origin:left;animation:gx 1s ease-out both}@keyframes gx{from{transform:scaleX(0)}to{transform:scaleX(1)}}")


def trophy_icon(cx, cy, color):
    return (f'<g class="ic" transform="translate({cx} {cy})"><g class="bob" fill="{color}" stroke="{color}">'
            '<path d="M-12 -14h24v10a12 12 0 0 1-24 0z" stroke="none"/><path d="M-12 -10h-7a6 6 0 0 0 7 9M12 -10h7a6 6 0 0 1-7 9" fill="none" stroke-width="2.5"/>'
            '<rect x="-3" y="8" width="6" height="8" stroke="none"/><rect x="-9" y="16" width="18" height="4" rx="2" stroke="none"/></g></g>')


def trophies_svg(m, w=600):
    tw, th, gx, gy = 184, 124, 24, 16
    out = []
    for i, (label, key, th_list) in enumerate(TROPHIES):
        val = m[key]
        lvl = sum(1 for t in th_list if val >= t)
        rank = RANKS[lvl - 1] if lvl else None
        x, y = (i % 3) * (tw + gx), (i // 3) * (th + gy)
        color = RANK_COLORS[rank] if rank else "#484F58"
        stroke = color if rank else EDGE
        out.append(f'<g transform="translate({x} {y})"><g style="animation:up .8s ease-out {i * .12:.2f}s both">'
                   f'<rect x="1" y="1" width="{tw - 2}" height="{th - 2}" rx="12" fill="{BG}" stroke="{stroke}" stroke-width="1.5"/>'
                   + (f'<g clip-path="url(#t{i})"><rect class="sh" x="-60" width="50" height="{th}" fill="url(#s)"/></g>' if rank else "")
                   + trophy_icon(tw / 2, 32, color) + txt(tw / 2, 78, f"{val}", 22, 700, "#fff", "middle")
                   + txt(tw / 2, 96, label.upper(), 10.5, 700, MUTED, "middle", style="letter-spacing:.8px")
                   + txt(tw / 2, 114, f"Rank {rank}" if rank else "Locked", 11, 700, color, "middle") + "</g></g>")
    clips = "".join(f'<clipPath id="t{i}"><rect x="1" y="1" width="{tw - 2}" height="{th - 2}" rx="12"/></clipPath>' for i in range(len(TROPHIES)))
    defs = (f'<defs><linearGradient id="s"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".18"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>{clips}</defs>')
    css = (f".sh{{animation:sh 4s ease-in-out infinite}}@keyframes sh{{from{{transform:translateX(0)}}to{{transform:translateX({tw + 70}px)}}}}"
           ".bob{animation:float 3s ease-in-out infinite}")
    return svg(w, th * 2 + gy, defs + "".join(out), css)


def live_assets(offline=False):
    if offline:  # placeholder state, replaced by the first workflow run
        user, repos = {"followers": 0, "created_at": dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).strftime("%Y-%m-%d")}, []
    else:
        user, repos = fetch()
    m = metrics(user, repos)
    save("repos.svg", repos_svg(repos, pending=offline))
    save("stats.svg", stats_svg(m))
    save("trophies.svg", trophies_svg(m))


if __name__ == "__main__":
    if "--static" in sys.argv:
        static_assets()
    else:
        live_assets(offline="--offline" in sys.argv)
