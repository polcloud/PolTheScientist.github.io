# Independent re-extraction of the graph

`extract_graph.py` is a from-scratch re-implementation of Graphify's
extraction step, written to verify `graph.json` / `GRAPH_REPORT.md`
independently rather than trusting the copied output. It parses
`vault-source/**/*.md`, reads YAML frontmatter (`title`, `aliases`) with
PyYAML, resolves every `[[wikilink]]` in the body against those titles/
aliases/filenames, and builds an undirected graph with `networkx`.

Run it with:

```
pip install networkx pyyaml
python3 extract_graph.py
```

It writes `graph_reextracted.json` next to this file.

## Result: matches the original extraction exactly

| Metric | Original (`graph.json`) | Re-extraction |
|---|---|---|
| Nodes | 126 | 126 |
| Edges | 399 | 399 |
| Unresolved `[[links]]` | — | 0 |
| Isolated nodes | 7 (all `03-NanoERT/Collaborators/*`) | same 7, identical names |
| Top god node | NanoERT Hub — 93 edges | NanoERT Hub — 93 edges |
| God-node ranking (all 10) | Content Pillars 74, Calendar 55, About Me Hub 35, IKI-AI Synthesis 26, Pipeline GBA 14, Thesis Hub 9, Platform Mechanism 8, Pipeline Alpha-Gal A 7, Pipeline CTSD 7 | identical, edge-for-edge |

Every node count, edge count, and per-node degree in the god-node table
matches the original to the exact integer. This confirms `graph.json` is a
faithful, reproducible extraction of `vault-source/` — not something that
only the original Graphify run could have produced.

The one place they don't need to match — and honestly don't — is community
detection: this script uses `networkx`'s `greedy_modularity_communities`
(6 communities), while the original used whatever clustering Graphify's own
pipeline runs internally (13 communities, with per-community cohesion
scores in `GRAPH_REPORT.md`). Community/cluster assignment isn't a
deterministic ground truth the way node/edge extraction is — different
algorithms (or the same algorithm at a different resolution) legitimately
disagree. Getting through 0 unresolved links first, then matching the
independently-checkable numbers (nodes, edges, degree, isolated nodes)
exactly, is the meaningful validation here.

## What made resolution hard

Getting from 41 unresolved links down to 0 took three fixes to the naive
first pass, all because the vault's frontmatter uses YAML features a
line-by-line parser mishandles:

1. Post titles with an apostrophe are YAML single-quoted with `''`
   escaping (e.g. `'...Parkinson''s risk'`) — a plain string strip left a
   double apostrophe in the label, so it never matched the same title
   quoted differently inside a wikilink.
2. Long titles get YAML line-folded across two lines — a regex expecting
   one line per key silently truncated them.
3. Fix: parse frontmatter with `yaml.safe_load` instead of hand-rolled
   line parsing, which handles both correctly.
