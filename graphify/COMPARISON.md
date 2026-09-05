# Graphify vs. hand-built vault — comparison

This folder holds the personal knowledge graph built from the "Building a
personal knowledge graph with Obsidian" chat (project `M7_IKIGai_Founderz`).
Two deliverables came out of that chat and were compared here:

- **`vault-source/`** — the *handcrafted* vault: 126 markdown files, hand-organized
  by Pol into `00-Index.md` + four hub trees (`01-About-Me`, `02-Thesis`,
  `03-NanoERT`, `04-Viral-Content`), with sub-folders for Skills, Talents,
  Passions, Loops, Gaps, Strengths, Collaborators, Competitors, and the
  2026-2027 posts calendar.
- **`obsidian-vault-export/`**, **`graph.json`**, **`GRAPH_REPORT.md`**,
  **`graphify_analysis.json`** — the *native* output: what the Graphify tool
  produced when it ran its extraction/analysis pass directly on the
  handcrafted vault above.

## Do they agree?

Yes — the native run is a faithful, verified derivative of the handcrafted
source, not a competing version:

- **File coverage**: `graph.json` has exactly 126 nodes, one per file in
  `vault-source/`. Every `source_file` path in the graph (e.g.
  `03-NanoERT/Collaborators/Sebastian-Tanco.md`) matches a real file in the
  handcrafted vault 1:1.
- **Extraction confidence**: `GRAPH_REPORT.md` reports 399 edges at
  **100% EXTRACTED, 0% INFERRED, 0% AMBIGUOUS** — every edge came from an
  explicit `[[wikilink]]` Pol wrote, nothing was guessed or hallucinated.
- **Obsidian export**: `obsidian-vault-export/` is the same 126 files
  flattened (folders removed, dashes replaced with spaces for readable
  titles) plus a handful of auto-generated files: one graph-navigation index
  (`Pol Rodriguez Carreras Knowledge Graph.md`) and per-community hub notes
  (`_COMMUNITY_Community 0.md` … `_COMMUNITY_Community 12.md`), for a total
  of 131 files — ready to open directly in Obsidian with `.obsidian/graph.json`
  and `graph.canvas` pre-configured.

## What the analysis surfaced

- **126 nodes · 399 edges · 13 communities**, cohesion scores ranging from
  0.12 (Community 2, the collaborators/competitors cluster — weakly
  interlinked) to 0.67 (Community 12: LinkedIn Content Strategy, Explanatory
  Writing, LinkedIn Voice Style Guide — tightly bound).
- **God nodes** (structural hubs): `NanoERT Hub` (93 edges), `Content
  Pillars` (74), `NanoERT LinkedIn Calendar 2026-2027` (55), `About Me Hub`
  (35), `IKI-AI Synthesis` (26).
- **The only real gap**: 7 isolated/near-isolated nodes, and they are
  exactly the 7 files in `vault-source/03-NanoERT/Collaborators/` (Sebastian
  Tanco, Julia Lorenzo Rivera, Pablo Castillo, Mercedes Arrue, Eddie Pradas
  Gracia, Nerea Ruiz, Pau Sarle). Their profile notes exist but aren't
  wikilinked back from the pipeline/content notes that mention them — an
  easy, low-risk fix in the handcrafted vault if a denser graph is wanted
  (add `[[Collaborator Name]]` links from the pages describing their
  contributions).

## Preview

`graph.html` is the native Graphify visualization (vis-network, dark theme,
searchable, filterable by community), lightly wrapped with a banner linking
back to the portfolio. It is **not** linked from the site's nav yet — open it
directly to preview: `graphify/graph.html`.

## Publishing note

This graph and vault contain real collaborator names and NanoERT
platform/pipeline details, plus an unpublished 2026-2027 LinkedIn content
calendar. None of this is wired into the live site navigation. Before
merging any of it into `main` (which auto-publishes via GitHub Pages),
decide what should stay private vs. public — see the options discussed when
this was built.
