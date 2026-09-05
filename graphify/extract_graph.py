import re, json, glob, os
import yaml
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

VAULT = "/home/user/PolTheScientist.github.io/graphify/vault-source"
OUT_DIR = "/home/user/PolTheScientist.github.io/graphify"

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?(?:#[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

def norm(s):
    return re.sub(r"[\s_-]+", " ", s.strip().lower())

files = sorted(glob.glob(os.path.join(VAULT, "**", "*.md"), recursive=True))

nodes = {}  # id -> {label, source_file, file_type, aliases}
alias_lookup = {}  # normalized label/alias/filename -> id

for path in files:
    rel = os.path.relpath(path, VAULT)
    node_id = re.sub(r"[\\/]", "_", re.sub(r"\.md$", "", rel)).lower().replace("-", "_").replace(" ", "_")
    text = open(path, encoding="utf-8").read()
    fm_match = FRONTMATTER_RE.match(text)
    frontmatter = {}
    body = text
    if fm_match:
        body = text[fm_match.end():]
        try:
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            frontmatter = {}
    basename = os.path.splitext(os.path.basename(path))[0].replace("-", " ")
    label = str(frontmatter.get("title") or "").strip() or basename
    file_type = frontmatter.get("type", "document").strip('"').strip("'")
    nodes[node_id] = {
        "id": node_id, "label": label, "source_file": rel,
        "file_type": file_type, "body": body,
    }
    for key in (label, basename):
        alias_lookup[norm(key)] = node_id

# second pass: aliases from frontmatter (aliases: list)
for path in files:
    rel = os.path.relpath(path, VAULT)
    text = open(path, encoding="utf-8").read()
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        continue
    try:
        frontmatter = yaml.safe_load(fm_match.group(1)) or {}
    except yaml.YAMLError:
        continue
    aliases = frontmatter.get("aliases") or []
    if aliases:
        node_id = re.sub(r"[\\/]", "_", re.sub(r"\.md$", "", rel)).lower().replace("-", "_").replace(" ", "_")
        for alias in aliases:
            alias = str(alias).strip()
            if alias:
                alias_lookup[norm(alias)] = node_id

edges = []
unresolved = set()
seen_pairs = set()
for node_id, n in nodes.items():
    for m in WIKILINK_RE.finditer(n["body"]):
        target_raw = m.group(1).strip()
        target_id = alias_lookup.get(norm(target_raw))
        if target_id is None:
            unresolved.add((n["source_file"], target_raw))
            continue
        if target_id == node_id:
            continue
        key = frozenset((node_id, target_id))
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        edges.append({
            "source": node_id, "target": target_id,
            "relation": "connects_to", "confidence": "EXTRACTED",
            "source_file": n["source_file"],
        })

G = nx.Graph()
G.add_nodes_from(nodes.keys())
for e in edges:
    G.add_edge(e["source"], e["target"])

degree = dict(G.degree())
communities = list(greedy_modularity_communities(G))
community_of = {}
for i, com in enumerate(communities):
    for nid in com:
        community_of[nid] = i

def cohesion(com):
    com = list(com)
    if len(com) < 2:
        return 0.0
    possible = len(com) * (len(com) - 1) / 2
    internal = sum(1 for u, v in G.edges(com) if u in com and v in com)
    return round(internal / possible, 2) if possible else 0.0

isolated = [nid for nid, d in degree.items() if d <= 1]
god_nodes = sorted(degree.items(), key=lambda x: -x[1])[:10]

report = {
    "node_count": len(nodes),
    "edge_count": len(edges),
    "unresolved_links": len(unresolved),
    "community_count": len(communities),
    "isolated_count": len(isolated),
    "isolated_nodes": [nodes[n]["label"] for n in isolated],
    "god_nodes": [(nodes[n]["label"], d) for n, d in god_nodes],
    "community_sizes": [len(c) for c in communities],
}
print(json.dumps(report, indent=2))
print("\nUNRESOLVED SAMPLE:", list(unresolved)[:15])

graph_json = {
    "directed": False, "multigraph": False, "graph": {},
    "nodes": [
        {
            "id": nid, "label": n["label"], "source_file": n["source_file"],
            "file_type": n["file_type"], "community": community_of.get(nid, -1),
            "degree": degree[nid],
        }
        for nid, n in nodes.items()
    ],
    "links": edges,
}
with open(os.path.join(OUT_DIR, "graph_reextracted.json"), "w", encoding="utf-8") as f:
    json.dump(graph_json, f, indent=2)

with open(os.path.join(OUT_DIR, "unresolved_links.txt"), "w", encoding="utf-8") as f:
    for src, tgt in sorted(unresolved):
        f.write(f"{src} -> [[{tgt}]]\n")
