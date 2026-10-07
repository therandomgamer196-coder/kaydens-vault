"""Build the Obsidian "Brain Map" from graphify-out/graph.json.

Run from anywhere after a graphify rebuild of the vault:
    python "C:\\Users\\NCG\\OneDrive\\Desktop\\Kaydens Vault\\graphify-out\\build_brain_map.py"

Writes (all inside  Kaydens Vault\\Brain Map\\ — never touches brain\\):
    Brain Map.md                 index: lobes, hubs, circuits, surprising links
    Lobes\\Lobe - <name>.md       one note per graphify community
    Neurons\\<concept>.md         one note per extracted concept, wired to the real brain notes
    Jarvis Brain Map.canvas      JSON Canvas laid out like a brain (two hemispheres)
    Jarvis Brain 3D.html         glowing 3D brain, open in a browser
Also rewrites the colour groups in .obsidian/graph.json so Graph view shows the lobes.
"""
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
OUT = VAULT / "Brain Map"
GRAPH = VAULT / "graphify-out" / "graph.json"
TODAY = date.today().isoformat()

# Community name -> brain region, colour, blurb. Unknown names fall back to a spare slot.
REGIONS = {
    "Future Integrations & Research": ("Left frontal lobe", "#c084fc", "planning ahead: the roadmap and the reading behind it", (110, 25, -45)),
    "Claude Code Tooling": ("Right frontal lobe", "#e879f9", "the tools used to change Jarvis and the dashboard", (110, 25, 45)),
    "Jarvis Core System": ("Left parietal lobe", "#ff7a18", "the core of Jarvis: bridge, model, interface, and the index that ties it together", (10, 70, -40)),
    "Dashboard UI Widgets": ("Right parietal lobe", "#818cf8", "what the dashboard shows on screen", (10, 70, 40)),
    "Safety & Voice Privacy": ("Left temporal lobe", "#f43f5e", "hearing and judgement: wake word, transcription, routing, and the safety rules", (30, -30, -75)),
    "Kayden & Jobs": ("Right temporal lobe", "#facc15", "long-term memory about Kayden: identity, jobs, pay, money habits", (30, -30, 75)),
    "Dashboard Display Files": ("Left occipital lobe", "#60a5fa", "vision: the wallpaper and artifact files that render the dashboard", (-110, 20, -40)),
    "Dashboard Data Sync": ("Right occipital lobe", "#34d399", "what the dashboard sees: the daily sync and its data format", (-110, 20, 40)),
    "Reliability & Maintenance": ("Brainstem", "#22d3ee", "autonomic functions that keep Jarvis alive: autostart, watchdog, mic self-healing", (-80, -70, -25)),
    "Logs & Change Tracking": ("Cerebellum", "#a3e635", "coordination and recall of past work: change log and work log", (-80, -70, 25)),
}
SPARE = [("Association cortex", c, "extra cluster", (0, 0, 0)) for c in ("#94a3b8", "#fda4af", "#5eead4", "#fde68a")]
HUB_COLOR = "#ffffff"
LOBE_COLOR = "#ffd166"

REL = {
    "calls": "triggers", "implements": "implements", "references": "references", "cites": "cites",
    "conceptually_related_to": "related to", "shares_data_with": "shares data with",
    "semantically_similar_to": "similar to", "rationale_for": "explains why",
}


def safe(name: str) -> str:
    name = re.sub(r"(^|\s)[/\\]", r"\1", name)  # "/health" -> "health"
    name = name.replace("/", "-").replace("\\", "-")  # "calendar/mail" -> "calendar-mail"
    name = re.sub(r'[:*?"<>|#^\[\]]', "", name).strip(" .-")
    return re.sub(r"\s+", " ", name) or "untitled"


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def is_note(n) -> bool:
    """True when the node IS a vault note (id == its file stem), not a doc it mentions."""
    stem = re.sub(r"[^a-z0-9]+", "_", n["source_file"].replace("\\", "/")[:-3].lower()).strip("_")
    return n.get("file_type") == "document" and n["id"] == stem


def conf(e) -> str:
    c = e.get("confidence", "")
    if c == "EXTRACTED":
        return "stated"
    if c == "INFERRED":
        return f"inferred {e.get('confidence_score', '')}"
    return "unsure"


def main():
    g = json.loads(GRAPH.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in g["nodes"]}
    links = g["links"]
    hyper = g.get("hyperedges") or g.get("graph", {}).get("hyperedges", [])

    existing = {p.stem.lower() for p in (VAULT / "brain").rglob("*.md")}

    # --- communities -> lobes
    comm_name = {}
    for n in nodes.values():
        comm_name[n["community"]] = n.get("community_name") or f"Community {n['community']}"
    region = {}
    spare = iter(SPARE)
    for cid, name in comm_name.items():
        region[cid] = REGIONS.get(name) or next(spare)
    lobe_note = {cid: f"Lobe - {safe(name)}" for cid, name in comm_name.items()}

    # --- link target for every node: real brain note for documents, neuron note otherwise
    link = {}
    neuron_file = {}
    used = set(existing)
    for nid, n in nodes.items():
        if is_note(n):
            path = n["source_file"].replace("\\", "/")
            link[nid] = f"[[{path[:-3]}|{Path(path).stem}]]"
        else:
            base = safe(n["label"])
            if base.lower() in used:
                base = f"{base} (neuron)"
            used.add(base.lower())
            neuron_file[nid] = base
            link[nid] = f"[[{base}]]"

    adj = defaultdict(list)
    degree = Counter()
    for e in links:
        s, t = e["source"], e["target"]
        adj[s].append((t, e))
        adj[t].append((s, e))
        degree[s] += 1
        degree[t] += 1

    # --- clean + recreate output (generated folder only)
    for sub in ("Neurons", "Lobes"):
        if (OUT / sub).exists():
            shutil.rmtree(OUT / sub)
        (OUT / sub).mkdir(parents=True)

    # --- neuron notes
    for nid, base in neuron_file.items():
        n = nodes[nid]
        cid = n["community"]
        src = n["source_file"].replace("\\", "/")
        fm = [
            "---",
            "type: neuron",
            f'lobe: "[[{lobe_note[cid]}]]"',
            f'source: "[[{src[:-3]}|{Path(src).stem}]]"',
            f"kind: {n.get('file_type', 'concept')}",
            f"connections: {degree[nid]}",
            f"tags: [brain-map, lobe/{slug(comm_name[cid])}]",
            f"generated: {TODAY}",
            "---",
        ]
        body = [f"# {n['label']}", ""]
        if n.get("summary"):
            body += [f"> {n['summary']}", ""]
        if n.get("rationale"):
            body += [f"**Why:** {n['rationale']}", ""]
        body += ["## Connections", ""]
        for other, e in sorted(adj[nid], key=lambda x: (x[1].get("confidence") != "EXTRACTED", nodes[x[0]]["label"].lower())):
            body.append(f"- {REL.get(e['relation'], e['relation'].replace('_', ' '))} {link[other]} · {conf(e)}")
        body += ["", "## Lives in", "", f"- Lobe: [[{lobe_note[cid]}]]", f"- Source note: [[{src[:-3]}|{Path(src).stem}]]", ""]
        (OUT / "Neurons" / f"{base}.md").write_text("\n".join(fm + body), encoding="utf-8")

    # --- lobe notes
    members = defaultdict(list)
    for nid, n in nodes.items():
        members[n["community"]].append(nid)
    cross = defaultdict(Counter)
    for e in links:
        a, b = nodes[e["source"]]["community"], nodes[e["target"]]["community"]
        if a != b:
            cross[a][b] += 1
            cross[b][a] += 1
    for cid, mids in members.items():
        reg, color, blurb, _ = region[cid]
        internal = sum(1 for e in links if nodes[e["source"]]["community"] == cid and nodes[e["target"]]["community"] == cid)
        possible = max(1, len(mids) * (len(mids) - 1) // 2)
        lines = [
            "---", "type: lobe", f"region: {reg}", f"color: \"{color}\"", f"neurons: {len(mids)}",
            f"cohesion: {internal / possible:.2f}", "tags: [brain-map, lobe]", f"generated: {TODAY}", "---",
            f"# {lobe_note[cid]}", "", f"> **{reg}** — {blurb}.", "",
        ]
        hubs = [m for m in mids if m not in neuron_file]
        if hubs:
            lines += ["## Brain notes in this lobe", ""] + [f"- {link[m]}" for m in sorted(hubs, key=lambda m: -degree[m])] + [""]
        lines += ["## Neurons", ""]
        for m in sorted((m for m in mids if m in neuron_file), key=lambda m: -degree[m]):
            s = nodes[m].get("summary", "")
            lines.append(f"- {link[m]}" + (f" — {s}" if s else ""))
        lines += ["", "## Wired to other lobes", ""]
        for other, cnt in cross[cid].most_common():
            lines.append(f"- [[{lobe_note[other]}]] — {cnt} connection{'s' if cnt != 1 else ''}")
        lines += ["", "Back to [[Brain Map]]", ""]
        (OUT / "Lobes" / f"{lobe_note[cid]}.md").write_text("\n".join(lines), encoding="utf-8")

    # --- index note
    order = sorted(members, key=lambda c: -len(members[c]))
    idx = [
        "---", "type: brain-map", "tags: [brain-map, index]", f"generated: {TODAY}", "---",
        "# Brain Map", "",
        "> [!info] Generated — don't hand-edit",
        "> Built by Graphify from every note in `brain/`, then rewritten into this folder by `graphify-out/build_brain_map.py`. "
        "The real notes stay in `brain/`; this folder only holds the map. Rebuild steps are at the bottom.", "",
        f"Jarvis's memory as a brain: **{len(nodes)} nodes** ({len(neuron_file)} neurons + {len(nodes) - len(neuron_file)} brain notes), "
        f"**{len(links)} connections**, **{len(members)} lobes**. Hub notes ([[Jarvis Brain]], [[Maintenance]], …) are the white nodes; "
        "neurons are coloured by lobe.", "",
        "## Ways to look at it", "",
        "- **Graph view** — `Ctrl+G`. Colours below. Zoom in to read labels, drag a node to see what it pulls with it.",
        "- **Canvas** — [[Brain Map/Jarvis Brain Map.canvas|Jarvis Brain Map]]: the lobes laid out as two hemispheres.",
        "- **3D** — open `Brain Map\\Jarvis Brain 3D.html` in a browser (glowing, rotating, click a node for details).",
        "- **Table** — [[Main brain Base.base|Main brain Base]] lists every note and neuron.", "",
        "## Lobes", "", "| Lobe | Region | Colour | Neurons |", "|---|---|---|---|",
    ]
    for cid in order:
        reg, color, _, _ = region[cid]
        idx.append(f"| [[{lobe_note[cid]}]] | {reg} | `{color}` | {len(members[cid])} |")
    idx += ["", "## Hubs (most connected)", ""]
    for nid, d in degree.most_common(8):
        idx.append(f"- {link[nid]} — {d} connections")
    if hyper:
        idx += ["", "## Circuits", "", "Groups of nodes that work together as one flow:", ""]
        for h in hyper:
            chain = " → ".join(link[m] for m in h.get("nodes", []) if m in link)
            idx.append(f"- **{h.get('label', h.get('id'))}**: {chain}")
    surprises = [e for e in links if e.get("confidence") == "INFERRED"
                 and nodes[e["source"]]["community"] != nodes[e["target"]]["community"]]
    if surprises:
        idx += ["", "## Cross-lobe links worth checking", "",
                "Inferred by the model, not stated in a note — confirm or fix the note if one is wrong:", ""]
        for e in sorted(surprises, key=lambda e: -e.get("confidence_score", 0))[:8]:
            idx.append(f"- {link[e['source']]} {REL.get(e['relation'], e['relation'])} {link[e['target']]} · {conf(e)}")
    idx += [
        "", "## Rebuild", "",
        "After notes in `brain/` change, in Claude Code opened on the vault folder:", "",
        "1. `/graphify . --update` — re-reads only changed notes (`Brain Map/` is excluded by `.graphifyignore`).",
        "2. `python graphify-out\\build_brain_map.py` — regenerates this folder, the canvas, the 3D page, and Graph view colours.", "",
    ]
    (OUT / "Brain Map.md").write_text("\n".join(idx), encoding="utf-8")

    build_canvas(nodes, members, neuron_file, region, lobe_note, cross, comm_name)
    build_3d(nodes, links, region, comm_name, neuron_file, degree)
    set_graph_colors(members, region, comm_name)
    print(f"Brain Map: {len(neuron_file)} neurons, {len(members)} lobes -> {OUT}")


def build_canvas(nodes, members, neuron_file, region, lobe_note, cross, comm_name):
    CW, CH, PAD, HEAD = 300, 70, 30, 60
    # rows front→back, columns = hemispheres (left / right)
    layout = [
        ("Future Integrations & Research", "Claude Code Tooling"),
        ("Jarvis Core System", "Dashboard UI Widgets"),
        ("Safety & Voice Privacy", "Kayden & Jobs"),
        ("Dashboard Display Files", "Dashboard Data Sync"),
        ("Reliability & Maintenance", "Logs & Change Tracking"),
    ]
    by_name = {v: k for k, v in comm_name.items()}
    placed = [c for row in layout for c in row if c in by_name]
    extra = [c for c in comm_name.values() if c not in placed]
    rows = [tuple(c for c in row if c in by_name) for row in layout] + [(c,) for c in extra]

    def size(cid):
        n = len(members[cid])
        cols = 2
        r = (n + cols - 1) // cols
        return cols * CW + (cols + 1) * PAD, HEAD + r * (CH + PAD) + PAD

    cnodes, cedges = [], []
    y = 0
    GAP = 260
    group_id = {}
    for row in rows:
        hmax = 0
        for side, name in enumerate(row):
            cid = by_name[name]
            w, h = size(cid)
            x = -w - GAP // 2 if side == 0 and len(row) > 1 else (GAP // 2 if len(row) > 1 else -w // 2)
            gid = f"lobe-{cid}"
            group_id[cid] = gid
            reg, color, _, _ = region[cid]
            cnodes.append({"id": gid, "type": "group", "x": x, "y": y, "width": w, "height": h,
                           "label": f"{name} · {reg}", "color": color})
            mids = sorted(members[cid], key=lambda m: (m in neuron_file, nodes[m]["label"].lower()))
            for i, m in enumerate(mids):
                cx = x + PAD + (i % 2) * (CW + PAD)
                cy = y + HEAD + (i // 2) * (CH + PAD)
                file = (nodes[m]["source_file"].replace("\\", "/") if m not in neuron_file
                        else f"Brain Map/Neurons/{neuron_file[m]}.md")
                cnodes.append({"id": f"n-{m}", "type": "file", "file": file, "x": cx, "y": cy,
                               "width": CW, "height": CH, **({"color": color} if m in neuron_file else {})})
            hmax = max(hmax, h)
        y += hmax + 160
    # corpus callosum: index cards in the middle column
    mid_y = y // 2 - 200
    cnodes.append({"id": "hub-index", "type": "file", "file": "brain/Jarvis Brain.md",
                   "x": -120, "y": mid_y, "width": 240, "height": 120, "color": "#ffffff"})
    cnodes.append({"id": "hub-map", "type": "file", "file": "Brain Map/Brain Map.md",
                   "x": -120, "y": mid_y + 170, "width": 240, "height": 120, "color": "#ffd166"})
    for cid, gid in group_id.items():
        left = any(comm_name[cid] == row[0] and len(row) > 1 for row in rows)
        cedges.append({"id": f"e-hub-{cid}", "fromNode": "hub-index", "fromSide": "left" if left else "right",
                       "toNode": gid, "toSide": "right" if left else "left", "color": region[cid][1]})
    done = set()
    for a, cnt in cross.items():
        for b, k in cnt.items():
            if k >= 3 and (b, a) not in done and a in group_id and b in group_id:
                done.add((a, b))
                cedges.append({"id": f"e-{a}-{b}", "fromNode": group_id[a], "toNode": group_id[b],
                               "label": f"{k} links", "color": "#94a3b8"})
    canvas = {"nodes": cnodes, "edges": cedges}
    (OUT / "Jarvis Brain Map.canvas").write_text(json.dumps(canvas, indent=1), encoding="utf-8")


def build_3d(nodes, links, region, comm_name, neuron_file, degree):
    data = {
        "nodes": [{
            "id": nid, "label": n["label"], "community": n["community"], "lobe": comm_name[n["community"]],
            "region": region[n["community"]][0], "color": HUB_COLOR if nid not in neuron_file else region[n["community"]][1],
            "hub": nid not in neuron_file, "deg": degree[nid], "summary": n.get("summary", ""),
            "why": n.get("rationale", ""), "source": n["source_file"].replace("\\", "/"),
            "file": (n["source_file"].replace("\\", "/")[:-3] if nid not in neuron_file else f"Brain Map/Neurons/{neuron_file[nid]}"),
        } for nid, n in nodes.items()],
        "links": [{"source": e["source"], "target": e["target"], "rel": REL.get(e["relation"], e["relation"]),
                   "conf": e.get("confidence", "")} for e in links],
        "lobes": [{"id": cid, "name": name, "region": region[cid][0], "color": region[cid][1], "anchor": region[cid][3]}
                  for cid, name in sorted(comm_name.items())],
    }
    tpl = (Path(__file__).parent / "brain_3d_template.html").read_text(encoding="utf-8")
    html = tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    (OUT / "Jarvis Brain 3D.html").write_text(html, encoding="utf-8")


def set_graph_colors(members, region, comm_name):
    p = VAULT / ".obsidian" / "graph.json"
    cfg = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    groups = [
        {"query": 'path:"Brain Map/Lobes" OR file:"Brain Map"', "color": {"a": 1, "rgb": int(LOBE_COLOR[1:], 16)}},
        {"query": "path:brain/", "color": {"a": 1, "rgb": int(HUB_COLOR[1:], 16)}},
    ]
    for cid in sorted(members):
        groups.append({"query": f"tag:#lobe/{slug(comm_name[cid])}",
                       "color": {"a": 1, "rgb": int(region[cid][1][1:], 16)}})
    cfg.update({
        "colorGroups": groups, "showTags": False, "showAttachments": False, "hideUnresolved": True,
        "showOrphans": False, "showArrow": False, "textFadeMultiplier": -1.2,
        "nodeSizeMultiplier": 1.3, "lineSizeMultiplier": 0.6,
        "centerStrength": 0.45, "repelStrength": 14, "linkStrength": 0.9, "linkDistance": 90,
    })
    p.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
