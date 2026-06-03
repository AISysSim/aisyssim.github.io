# SysSim Documentation Site — Design

**Date:** 2026-06-03
**Repo:** `aisyssim.github.io` (GitHub Pages, deployed from `main` → `gh-pages`)
**Goal:** Rebuild the outdated docs site from scratch to reflect the current SysSim project. Two
must-have sections: **Getting Started** and a **full API reference**. Look professional.

## Background

- The current site is a Sphinx/reStructuredText site using the `alabaster` theme. Its content
  still references the old project name "TorchCAP" and an outdated architecture — stale and must be
  replaced.
- SysSim today (`/Users/lexu/Projects/SysSim`, GitHub `AISysSim/SysSim`, Apache-2.0) is an
  **LLM Performance & Memory Simulator**: it estimates LLM training step time, MFU, and peak per-GPU
  memory without running real computation. It models TP / SP / DP / CP / PP parallelism.
- The deploy workflow `.github/workflows/docs.yaml` already `pip install sphinx furo` and runs
  `sphinx-build . _build/html`, publishing to `gh-pages`. Furo is therefore already expected; only
  `conf.py` still selects `alabaster`.
- This docs repo is **separate** from the SysSim source repo, and CI does **not** install `syssim`
  or its heavy deps (torch, megatron-core, megatron-bridge, lightgbm).

## Decisions (from brainstorming)

1. **Stack:** Sphinx + **Furo** theme.
2. **API reference:** **hand-written RST** (not autodoc) — keeps CI lightweight and build robust;
   the source repo isn't even present in CI. Content sourced from the real, inventoried
   signatures/docstrings.
3. **Accent color:** Indigo/violet.
4. **Scope:** Include both the **Concepts** and **Calibration** guide pages in addition to the two
   must-haves.

## Stack & Build

- `conf.py`: switch `html_theme` to `furo`; set correct project metadata (`SysSim`, current
  authors/copyright); enable extensions: `sphinx_design`, `sphinx_copybutton`. Remove the leftover
  `autodoc`/`napoleon`/`githubpages` autodoc config (we hand-write the API). Keep
  `sphinx.ext.githubpages` (harmless, ensures `.nojekyll`).
- Add `sphinx-design` and `sphinx-copybutton` to the `pip install` line in
  `.github/workflows/docs.yaml`. Both are pure-Python — CI stays fast and never touches torch.
- `_static/custom.css`: indigo/violet accent via Furo CSS variables (`--color-brand-primary`,
  `--color-brand-content`) for both light and dark mode; minor polish (hero spacing, card styling,
  table tweaks). Registered via `html_css_files` in `conf.py`.
- A simple SVG wordmark logo for the sidebar (`_static/logo.svg`), referenced via Furo's
  `html_theme_options` light/dark logo or `html_logo`.
- Furo `html_theme_options`: source repo link to `https://github.com/AISysSim/SysSim`, footer/edit
  links as appropriate.

## Site Map

```
index.rst                     Home: hero, what-it-is, key use cases, "what you get", card links
Getting Started (toctree)
  ├─ install.rst              Requirements + clone + pip install -e .
  ├─ quickstart.rst           Worked example: Python API + CLI (sphinx-design tabs), qwen3-1.7b on GH200
  └─ configuration.rst        Two-YAML system (model + hardware), parallelism/training kwargs & CLI flags
Guides (toctree)
  ├─ concepts.rst             What it models: TP/SP/DP/CP/PP, roofline vs calibrated estimator,
  │                           OOM detection, the SimulationReport & bottlenecks
  └─ calibration.rst          Advanced: profile + calibrate workflow (TreeEstimator), reproduce recipe
API Reference (toctree)
  ├─ api/index.rst            Overview / map of the API surface
  ├─ api/highlevel.rst        simulate, estimate_memory, sweep, Sweep, SweepRow, Trace,
  │                           ModelConfig, ParallelismConfig, TrainingConfig, HardwareConfig,
  │                           HFModel, CustomModel, SimulationReport, load_model_yaml, load_hardware_yaml
  ├─ api/config.rst           HardwareInfo, NetworkParams, SimulatorConfig, ExecutionMode, get_hardware_info
  ├─ api/operator_graph.rst   OperatorType, TensorMeta, OperatorNode, OperatorGraph
  └─ cli.rst                  run / memory / summary / sweep / profile / calibrate
```

## API Reference Format (hand-written)

Each symbol is documented with Sphinx domain directives so it gets proper anchors,
cross-references (`:func:`, `:class:`), and index entries — looks like autodoc but needs no import:

- Functions → `.. py:function:: simulate(*, model, hardware, parallelism=None, training=None, workdir=None)`
  with summary, a parameter list (`:param:` / `:type:` or a table), return type, and a short usage
  snippet.
- Classes / dataclasses → `.. py:class::` with a fields/attributes table (name, type, default,
  meaning) and key methods (e.g. `SimulationReport.to_json`, `Sweep.best`, `Trace.simulate_on`,
  `ParallelismConfig.world_size`).
- Enums → values listed (`ExecutionMode`, `OperatorType`).

Coverage (full inventory, all top-level exports + key helpers):

- **High-level (training):** `simulate`, `estimate_memory`, `sweep`, `Sweep`, `SweepRow`, `Trace`,
  `ModelConfig`, `ParallelismConfig`, `TrainingConfig`, `HardwareConfig`, `HFModel`, `CustomModel`,
  `SimulationReport`, `load_model_yaml`, `load_hardware_yaml`.
- **Config:** `HardwareInfo`, `NetworkParams`, `SimulatorConfig`, `ExecutionMode`, `get_hardware_info`.
- **Operator graph:** `OperatorType`, `TensorMeta`, `OperatorNode`, `OperatorGraph`.
- **CLI:** `run`, `memory`, `summary`, `sweep`, `profile` (layer + `--network`), `calibrate` with
  their shared flags (`--tp --dp --cp --sp --micro-batch --global-batch --dtype --recompute --format`).

`CustomModel` is documented as a reserved/`NotImplementedError` v1 placeholder. `EP` parallelism
noted as work-in-progress.

## Content Sources

- README.md of SysSim for narrative, quick start, config examples, "what you get" table,
  parallelism support table.
- Inventoried signatures/docstrings for the API pages.
- `examples/configs/models/qwen3-1_7b.yaml` and
  `examples/configs/hardware/isambard_gh200_4gpu.yaml` as the canonical worked example.

## Cleanup

- **Delete** stale RST: `auto_sharding.rst`, `cost_model.rst`, `benchmark.rst`.
- **Delete** stale TorchCAP-branded images in `img/` (`torchCAP_overview.png`,
  `refine_hardware_with_torchcap.png`, and the other old diagrams not reused). Keep `img/` only if a
  current asset is added; otherwise remove.
- **Rewrite:** `index.rst`, `install.rst`, `quickstart.rst`, `conf.py`.
- **Keep:** `Makefile`, `make.bat`, `.gitignore` (`_build/`).

## Verification

- Build locally with `sphinx-build . _build/html` (after `pip install sphinx furo sphinx-design
  sphinx-copybutton`) and confirm zero errors/warnings (or only known-benign ones).
- Visually inspect rendered `_build/html/index.html` and key pages (light + dark).
- Confirm all toctree entries resolve and intra-doc cross-references work (no broken refs).

## Out of Scope (YAGNI)

- Benchmarks/validation page (no current data to present).
- Blog/news/changelog page.
- Versioned docs (single `latest` is fine for now).
- Autodoc / API auto-extraction (explicitly rejected above).
