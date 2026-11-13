# ZEUS project page

A static research project page for **ZEUS: Accelerating Diffusion Models with Only Second-Order Predictor** (ACM Multimedia 2026). It retains the original website's Bulma layout, fonts, colors, section order, gallery, and curved-arrow method animation.

## Preview before pushing

Open PowerShell in this folder and run:

```powershell
python preview.py
```

Open **http://127.0.0.1:8000** in your browser. Refresh after changes. Stop the server with **Ctrl+C**. If port 8000 is occupied, run `python preview.py --port 8001` and open http://127.0.0.1:8001 instead. No installation or build step is required.

For a phone-sized preview in Chrome or Edge, press **F12**, toggle the device toolbar with **Ctrl+Shift+M**, and select a phone or set the viewport to 390 pixels wide. Check the two comparison figures, the original method animation and Replay control, the gallery rows, scrollable results tables, and the BibTeX. The method diagram and gallery rows scroll horizontally on small screens. The page has no audio. This server accepts connections only from your own computer.

## Content sources

- Camera-ready text, title, author order, affiliations, equations, and result tables: the local `orginal paper/` LaTeX source. That directory is deliberately ignored by Git.
- Main comparison plots: `new_results/FLUX_3.22_faster.png` and `new_results/Wan2.1_2.24_faster.png`.
- Paper-native qualitative and ablation figures: selected exports in `static/media/`, generated with `python scripts/export-paper-figures.py` (requires Poppler and Pillow).
- Public preprint: https://arxiv.org/abs/2604.01552 and https://arxiv.org/pdf/2604.01552. The website follows the camera-ready authors, including Qinsi Wang; the public preprint may lag behind the camera-ready source.

The quantitative HTML is embedded directly in `index.html` so it works without JavaScript. `static/results-tables.html` is its editable source fragment. After editing the fragment, run `python scripts/sync-results.py` to update the marked block in `index.html`. Run `python scripts/check-site.py` for local reference and content checks, and `python scripts/check-results.py` for numeric checks against the local LaTeX tables.

`frontier_animation.html` and `preset_replay.html` are preserved historical experiments and are not embedded or linked. The main page retains its original inline SVG method animation and its 45-image qualitative gallery. At the user's request, gallery playback uses the original speed code and rates (1, 1.92, 2.25, 2.91, 3.64); camera-ready benchmark measurements are reported separately in the results tables. `main_ani.html` and `main_paper.html` retain the original standalone diagrams, with small notation fixes.

The page retains the original website's CC BY-SA 4.0 license and Nerfies attribution. No push or deployment is required to preview locally.
