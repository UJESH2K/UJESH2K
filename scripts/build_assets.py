#!/usr/bin/env python3
"""Builds every README image into assets/. Python standard library only."""
import base64, json, os, random, urllib.request
from datetime import date
from html import escape as e
from pathlib import Path

OUT = Path("assets")
OUT.mkdir(exist_ok=True)
USER = "UJESH2K"
BG, INK, MUTE, LINE, ORANGE = "#080808", "#f5f1ea", "#8d8a84", "#262626", "#ff5a1f"
FONT = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
FRAMES, FRAME_PX, ROBOT_SECONDS = 24, 320, 2.4  # must match the sprite export

BASE_CSS = (
    "text{font-family:Site," + FONT + ";fill:" + INK + "}"
    ".m{fill:" + MUTE + "}.o{fill:" + ORANGE + "}"
    "@keyframes float{0%{transform:translateY(0);opacity:0}15%{opacity:.85}"
    "85%{opacity:.5}100%{transform:translateY(var(--d));opacity:0}}"
    "@media(prefers-reduced-motion:reduce){*{animation:none!important}}"
)


def b64(path):
    return base64.b64encode(path.read_bytes()).decode()


def write(name, w, h, body, css=""):
    font = OUT / "font.woff2"
    face = ""
    if font.exists():
        face = "@font-face{font-family:Site;src:url(data:font/woff2;base64," + b64(font) + ")}"
    style = face + BASE_CSS + css
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img"><style>{style}</style>'
        f'<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>{body}</svg>'
    )
    (OUT / name).write_text(svg, encoding="utf-8")


def particles(w, h, n=70, seed=7):
    rng = random.Random(seed)  # fixed seed avoids pointless daily commits
    out = []
    for _ in range(n):
        out.append(
            f'<circle cx="{rng.uniform(0, w):.0f}" cy="{rng.uniform(0, h):.0f}" '
            f'r="{rng.uniform(.6, 2.4):.1f}" fill="{ORANGE}" '
            f'style="--d:-{rng.uniform(30, 120):.0f}px;'
            f'animation:float {rng.uniform(6, 16):.1f}s linear -{rng.uniform(0, 16):.1f}s infinite"/>'
        )
    return "".join(out)


def hero():
    w, h, cx, cy = 1200, 520, 915, 260
    lines = [
        "7 hackathon wins, 20 national finals",
        "First author, IMPACT-2027",
        "One model across NVIDIA, Intel and Apple GPUs",
        "Two identical GPUs, a 2.03× throughput gap",
    ]
    rotating = "".join(
        f'<text class="ln" x="70" y="390" font-size="24" '
        f'style="animation-delay:-{(16 - 4 * i) % 16}s">→ {e(t)}</text>'
        for i, t in enumerate(lines)
    )
    sprite = OUT / "robot-sprite.webp"
    robot_css = ""
    if sprite.exists():
        size = FRAME_PX
        sheet = size * FRAMES
        robot = (
            f'<svg x="{cx - size / 2}" y="{cy - size / 2}" width="{size}" height="{size}" '
            f'viewBox="0 0 {size} {size}"><g class="rb"><image width="{sheet}" height="{size}" '
            f'href="data:image/webp;base64,{b64(sprite)}"/></g></svg>'
        )
        robot_css = (
            f".rb{{animation:rb {ROBOT_SECONDS}s steps({FRAMES}) infinite}}"
            f"@keyframes rb{{to{{transform:translateX(-{sheet}px)}}}}"
        )
    else:
        robot = f'<circle cx="{cx}" cy="{cy}" r="9" fill="{ORANGE}"/>'
    body = (
        particles(w, h)
        + f'<text class="m" x="70" y="80" font-size="18" letter-spacing="3">UJESH KUMAR YADAV · BENGALURU</text>'
        + '<text x="70" y="195" font-size="84" font-weight="600">Hello there,</text>'
        + '<text class="o" x="70" y="285" font-size="84" font-weight="600">I\'m Ujesh.</text>'
        + '<text class="m" x="70" y="340" font-size="24">Full-stack products, applied AI, GPU systems.</text>'
        + rotating
        + '<text class="m" x="70" y="465" font-size="18">ujesh.in ↗</text>'
        + f'<circle cx="{cx}" cy="{cy}" r="190" fill="none" stroke="{LINE}"/>'
        + f'<g class="ring"><circle cx="{cx}" cy="{cy}" r="218" fill="none" stroke="{ORANGE}" stroke-dasharray="3 14"/>'
        + f'<circle cx="{cx + 218}" cy="{cy}" r="6" fill="{ORANGE}"/></g>'
        + robot
    )
    css = (
        ".ln{opacity:0;animation:cycle 16s infinite}"
        "@keyframes cycle{0%,22%{opacity:1}25%,100%{opacity:0}}"
        f".ring{{transform-origin:{cx}px {cy}px;animation:spin 18s linear infinite}}"
        "@keyframes spin{to{transform:rotate(360deg)}}" + robot_css
    )
    write("hero.svg", w, h, body, css)


def marquee():
    items = [
        "EaseMed · Internship", "Hitachi · ML internship", "Edactly · Freelance",
        "Inception · Winner", "Denova · Winner", "Cardano · Winner", "Cypher 1 & 3 · Winner ×2",
        "IMPACT-2027 · Paper accepted", "MNNIT Allahabad · Book chapter",
        "LitmusChaos · Open source", "Smart India Hackathon · College rank 1",
        "HackerRank · Bronze", "Google Solution Challenge · Regional qualifier", "ICPC · Prelims ×2",
    ]
    x, row = 30, []
    for item in items * 2:
        row.append(f'<text x="{x}" y="46" font-size="20">{e(item)}</text>')
        x += int(len(item) * 10.5)
        row.append(f'<text class="o" x="{x + 15}" y="46" font-size="20">✳</text>')
        x += 60
    distance = (x - 30) // 2
    css = f".mq{{animation:mq 45s linear infinite}}@keyframes mq{{to{{transform:translateX(-{distance}px)}}}}"
    write("marquee.svg", 1200, 72, f'<g class="mq">{"".join(row)}</g>', css)


def section(number, title):
    body = (
        f'<text class="m" x="36" y="68" font-size="22">( {number} )</text>'
        f'<text x="120" y="72" font-size="46" font-weight="600">{e(title)}</text>'
        f'<text class="o star" x="1140" y="72" font-size="46">✳</text>'
        + particles(1200, 110, n=18, seed=int(number) + 20)
    )
    css = (
        ".star{transform-box:fill-box;transform-origin:center;animation:spin 8s linear infinite}"
        "@keyframes spin{to{transform:rotate(360deg)}}"
    )
    write(f"section-{number}.svg", 1200, 110, body, css)


def proof_band():
    stats = [
        ("7×", "Hackathon wins"), ("20×", "National finals"), ("50+", "Hackathons entered"),
        ("65+", "Public projects"), ("7", "LitmusChaos PRs merged"),
    ]
    body = ""
    for i, (value, label) in enumerate(stats):
        x = 40 + i * 232
        body += (
            f'<text class="o" x="{x}" y="82" font-size="56" font-weight="600">{e(value)}</text>'
            f'<text class="m" x="{x}" y="118" font-size="18">{e(label)}</text>'
        )
    write("proof.svg", 1200, 150, particles(1200, 150, n=28, seed=3) + body)


def gradmesh():
    workers = [("NVIDIA", "CUDA", 110), ("Intel Arc", "XPU", 220), ("Apple Silicon", "Metal", 330)]
    numbers = [
        ("≤8%", "Prediction error on 4 unseen two-GPU setups"),
        ("2.03×", "Real throughput gap between two RTX 5070s"),
        ("3×", "Tighter shards, imbalance CV 0.319 → 0.107"),
        ("<1 s", "Per-round overhead on RTX 3050, was ~9 s"),
    ]
    body = (
        '<text x="50" y="62" font-size="36" font-weight="600">GradMesh</text>'
        '<text class="m" x="225" y="62" font-size="19">Idle household GPUs, one training cluster</text>'
    )
    for name, api, y in workers:
        mid = y + 35
        down = f"M380 245 C310 245 310 {mid - 6} 240 {mid - 6}"
        up = f"M240 {mid + 6} C310 {mid + 6} 310 251 380 251"
        body += (
            f'<path d="{down}" fill="none" stroke="{LINE}"/><path d="{up}" fill="none" stroke="{LINE}"/>'
            f'<rect x="50" y="{y}" width="190" height="70" rx="10" fill="#111" stroke="{LINE}"/>'
            f'<text x="70" y="{y + 31}" font-size="19" font-weight="600">{e(name)}</text>'
            f'<text class="m" x="70" y="{y + 54}" font-size="15">{e(api)}</text>'
        )
        for i in range(3):
            body += (
                f'<circle r="4" fill="{ORANGE}"><animateMotion dur="2.4s" begin="-{i * .8:.1f}s" '
                f'repeatCount="indefinite" path="{down}"/></circle>'
                f'<circle r="3" fill="{INK}"><animateMotion dur="2.4s" begin="-{i * .8 + .4:.1f}s" '
                f'repeatCount="indefinite" path="{up}"/></circle>'
            )
    body += (
        f'<rect x="380" y="190" width="210" height="110" rx="12" fill="#160b06" stroke="{ORANGE}"/>'
        '<text x="400" y="232" font-size="22" font-weight="600">Coordinator</text>'
        '<text class="m" x="400" y="258" font-size="15">Shards by measured speed</text>'
        '<text class="m" x="400" y="279" font-size="15">Reliability-weighted average</text>'
        f'<circle cx="60" cy="418" r="4" fill="{ORANGE}"/><text class="m" x="72" y="423" font-size="14">shards</text>'
        f'<circle cx="140" cy="418" r="3" fill="{INK}"/><text class="m" x="152" y="423" font-size="14">gradients</text>'
    )
    for i, (value, label) in enumerate(numbers):
        y = 118 + i * 84
        body += (
            f'<text class="o" x="680" y="{y}" font-size="38" font-weight="600">{e(value)}</text>'
            f'<text class="m" x="680" y="{y + 28}" font-size="19">{e(label)}</text>'
        )
    write("gradmesh.svg", 1200, 450, body)


def card(slug, tag, name, tagline, metric, label):
    label_x = 36 + len(metric) * 27 + 14
    body = (
        f'<rect class="edge" x="1" y="1" width="588" height="208" rx="15" fill="none" stroke="{ORANGE}" stroke-width="2"/>'
        f'<text class="m" x="36" y="40" font-size="15" letter-spacing="2">{e(tag)}</text>'
        f'<text x="36" y="84" font-size="38" font-weight="600">{e(name)}</text>'
        f'<text class="m" x="36" y="116" font-size="18">{e(tagline)}</text>'
        f'<text class="o" x="36" y="178" font-size="46" font-weight="600">{e(metric)}</text>'
        f'<text x="{label_x}" y="176" font-size="17">{e(label)}</text>'
    )
    css = (
        ".edge{stroke-dasharray:140 1450;animation:edge 7s linear infinite}"
        "@keyframes edge{to{stroke-dashoffset:-1590}}"
    )
    write(f"card-{slug}.svg", 590, 210, particles(590, 210, n=16, seed=len(slug)) + body, css)


def live_stats():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("No GITHUB_TOKEN, skipping live stats")
        return
    query = (
        '{user(login:"%s"){followers{totalCount}'
        "repositories(ownerAffiliations:OWNER,privacy:PUBLIC,first:100){totalCount nodes{stargazerCount}}"
        "contributionsCollection{contributionCalendar{totalContributions "
        "weeks{contributionDays{date contributionCount}}}}}}" % USER
    )
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        user = json.load(response)["data"]["user"]

    calendar = user["contributionsCollection"]["contributionCalendar"]
    weeks = calendar["weeks"]
    counts = [d["contributionCount"] for w in weeks for d in w["contributionDays"]]
    longest = run = 0
    for count in counts:
        run = run + 1 if count else 0
        longest = max(longest, run)
    current = 0
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    for count in reversed(tail):
        if not count:
            break
        current += 1

    def shade(count):
        if count == 0:
            return "#161616"
        if count < 3:
            return "#4a1d0c"
        if count < 6:
            return "#8a3312"
        if count < 10:
            return "#c94516"
        return ORANGE

    cells = ""
    for x, week in enumerate(weeks):
        for day in week["contributionDays"]:
            y = date.fromisoformat(day["date"]).isoweekday() % 7
            cells += (
                f'<rect class="c" x="{43 + x * 21}" y="{75 + y * 21}" width="18" height="18" rx="4" '
                f'fill="{shade(day["contributionCount"])}" style="animation-delay:{x * 25}ms"/>'
            )
    stars = sum(r["stargazerCount"] for r in user["repositories"]["nodes"])
    stats = [
        (current, "Current streak"), (longest, "Longest streak"),
        (user["repositories"]["totalCount"], "Public repos"), (stars, "Stars"),
        (user["followers"]["totalCount"], "Followers"),
    ]
    numbers = ""
    for i, (value, label) in enumerate(stats):
        x = 43 + i * 225
        numbers += (
            f'<text class="o" x="{x}" y="274" font-size="32" font-weight="600">{value}</text>'
            f'<text class="m" x="{x}" y="298" font-size="16">{e(label)}</text>'
        )
    title = f'<text x="43" y="48" font-size="26" font-weight="600">{calendar["totalContributions"]} public contributions this year</text>'
    css = ".c{animation:pop .6s both}@keyframes pop{from{opacity:0}to{opacity:1}}"
    write("activity.svg", 1200, 325, title + cells + numbers, css)


hero()
marquee()
proof_band()
gradmesh()
for number, title in [("01", "Flagship"), ("02", "Selected work"), ("03", "Wins"), ("04", "Experience"), ("05", "Live from GitHub")]:
    section(number, title)
card("worldforge", "HACKATHON WINNER", "WorldForge", "Build a world from a sentence, then train robots in it", "1st", "Inception World Model Hackathon 2026")
card("tidewatch", "AGENTIC FRAUD INVESTIGATION", "Tidewatch", "Fraud alerts, investigated in under a second", "~40 ms", "per case, 590,742 transactions")
card("crashgraph", "HACKATHON BUILD", "CrashGraph", "A rocket lander with no neural network", "94%", "landing rate")
card("edactly", "AI IN PRODUCTION", "Edactly", "An AI tutor that has read the whole syllabus", "~₹7", "for a 3-minute lesson video")
live_stats()
