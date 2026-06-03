# SysSim Documentation Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the outdated `aisyssim.github.io` Sphinx site from scratch to document the current SysSim LLM performance/memory simulator, with a Getting Started section and a complete hand-written API reference, looking professional.

**Architecture:** Sphinx + Furo theme, indigo/violet accent via custom CSS, `sphinx-design` (cards/tabs) and `sphinx-copybutton` for polish. API reference is hand-written RST using Sphinx domain directives (`.. py:function::`, `.. py:class::`) — no autodoc import, so CI only needs `sphinx furo sphinx-design sphinx-copybutton` (no torch/megatron). Deployed by the existing GitHub Action (`main` → `gh-pages`).

**Tech Stack:** Sphinx, Furo, sphinx-design, sphinx-copybutton, reStructuredText, GitHub Pages.

**Verification model (no pytest):** the "test" for every task is:
```bash
cd /Users/lexu/Projects/aisyssim.github.io
python3 -m venv .docsenv 2>/dev/null; . .docsenv/bin/activate
pip install -q sphinx furo sphinx-design sphinx-copybutton
sphinx-build -b html -n . _build/html 2>&1 | tail -20
```
Expected: `build succeeded` with no `ERROR`/`WARNING` lines (`-n` = nit-picky; warns on broken refs). `.docsenv/` and `_build/` are gitignored.

---

## File Structure

**Create:**
- `_static/custom.css` — indigo/violet accent + polish
- `_static/logo.svg` — SysSim wordmark for the sidebar
- `requirements-docs.txt` — pinned doc build deps (mirrors CI)
- `configuration.rst` — model + hardware YAML config guide
- `concepts.rst` — what the simulator models
- `calibration.rst` — profile + calibrate workflow
- `api/index.rst` — API overview
- `api/highlevel.rst` — high-level training API
- `api/config.rst` — config module API
- `api/operator_graph.rst` — operator-graph API
- `cli.rst` — command-line reference

**Modify:**
- `conf.py` — Furo theme, extensions, metadata, static assets
- `index.rst` — new home page
- `install.rst` — fresh install instructions
- `quickstart.rst` — fresh quickstart
- `.github/workflows/docs.yaml` — add doc extensions to pip install
- `.gitignore` — add `.docsenv/`

**Delete:**
- `auto_sharding.rst`, `cost_model.rst`, `benchmark.rst` (stale TorchCAP-era)
- `img/torchCAP_overview.png`, `img/refine_hardware_with_torchcap.png`, `img/device_mesh_abstraction.png`, `img/linear_regression_for_runtime_cost_estimation.png`, `img/memory_liveness_analysis.png`, `img/scaling.png` (stale; the whole `img/` dir if nothing replaces it)

---

## Task 1: Build foundation (theme, assets, CI)

**Files:**
- Modify: `conf.py`
- Create: `_static/custom.css`, `_static/logo.svg`, `requirements-docs.txt`
- Modify: `.github/workflows/docs.yaml`, `.gitignore`

- [ ] **Step 1: Replace `conf.py` with the new configuration**

```python
# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = "SysSim"
copyright = "2025, SysSim Contributors"
author = "SysSim Contributors"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "docs/superpowers/**", ".docsenv"]

# Treat the highlevel/config modules as the default domain for :func:/:class: refs.
default_role = "py:obj"
primary_domain = "py"
add_module_names = False

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_title = "SysSim"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = "_static/logo.svg"
html_favicon = "_static/logo.svg"

html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#5b4ee5",
        "color-brand-content": "#5b4ee5",
    },
    "dark_css_variables": {
        "color-brand-primary": "#9d92ff",
        "color-brand-content": "#9d92ff",
    },
    "source_repository": "https://github.com/AISysSim/SysSim/",
    "source_branch": "main",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/AISysSim/SysSim",
            "html": "",
            "class": "fa-brands fa-github",
        },
    ],
}

pygments_style = "friendly"
pygments_dark_style = "monokai"
```

- [ ] **Step 2: Create `_static/logo.svg`** (simple wordmark, indigo accent)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 48" width="200" height="48" role="img" aria-label="SysSim">
  <g fill="none" stroke="#5b4ee5" stroke-width="3" stroke-linecap="round">
    <path d="M10 14 h14 a6 6 0 0 1 0 12 h-8 a6 6 0 0 0 0 12 h14"/>
  </g>
  <text x="44" y="32" font-family="-apple-system, Segoe UI, Roboto, sans-serif" font-size="26" font-weight="700" fill="currentColor">Sys<tspan fill="#5b4ee5">Sim</tspan></text>
</svg>
```

- [ ] **Step 3: Create `_static/custom.css`**

```css
/* SysSim docs — polish on top of Furo */
:root {
  --color-brand-primary: #5b4ee5;
  --color-brand-content: #5b4ee5;
}

/* Hero on the landing page */
.syssim-hero {
  padding: 1.5rem 0 0.5rem;
}
.syssim-hero h1 {
  font-size: 2.6rem;
  line-height: 1.1;
  margin-bottom: 0.3rem;
}
.syssim-tagline {
  font-size: 1.15rem;
  color: var(--color-foreground-secondary);
  margin-bottom: 1.5rem;
}

/* sphinx-design cards: subtle lift + brand border on hover */
.sd-card {
  border-radius: 10px;
  transition: border-color .15s ease, box-shadow .15s ease;
}
.sd-card:hover {
  border-color: var(--color-brand-primary);
  box-shadow: 0 4px 18px rgba(91, 78, 229, 0.12);
}

/* Tables: tighter, readable API field tables */
table.docutils {
  width: 100%;
  border-collapse: collapse;
}
table.docutils td, table.docutils th {
  vertical-align: top;
}

/* Inline code accent */
code.literal {
  color: var(--color-brand-content);
}

/* API signature blocks stand out a touch */
dl.py > dt {
  border-left: 3px solid var(--color-brand-primary);
  padding-left: 0.6rem;
}
```

- [ ] **Step 4: Create `requirements-docs.txt`**

```text
sphinx>=7
furo
sphinx-design
sphinx-copybutton
```

- [ ] **Step 5: Update `.github/workflows/docs.yaml`** — change the install line

Replace:
```yaml
          pip install sphinx furo
```
with:
```yaml
          pip install -r requirements-docs.txt
```

- [ ] **Step 6: Update `.gitignore`** — append `.docsenv/`

Resulting file:
```
_build/
.docsenv/
```

- [ ] **Step 7: Build to verify the theme loads**

Run:
```bash
cd /Users/lexu/Projects/aisyssim.github.io
python3 -m venv .docsenv; . .docsenv/bin/activate
pip install -q -r requirements-docs.txt
sphinx-build -b html . _build/html 2>&1 | tail -20
```
Expected: `build succeeded`. (Warnings about toctree entries in `index.rst` pointing at not-yet-rewritten pages are OK at this step.)

- [ ] **Step 8: Commit**

```bash
git add conf.py _static/custom.css _static/logo.svg requirements-docs.txt .github/workflows/docs.yaml .gitignore
git commit -m "Set up Furo theme, brand assets, and doc build deps"
```

---

## Task 2: Home page (`index.rst`)

**Files:**
- Modify: `index.rst`

- [ ] **Step 1: Replace `index.rst`** with the new landing page

```rst
:layout: landing

SysSim
======

.. rst-class:: syssim-tagline

   Estimate the step time and peak memory of LLM training — on hardware you don't have — without running real computation.

**SysSim** models tensor, sequence, data, context, and pipeline parallelism and reports step time,
MFU, and per-GPU memory (including per-pipeline-stage peaks and OOM) for distributed LLM training.

.. grid:: 2
   :gutter: 3
   :margin: 2 0 0 0

   .. grid-item-card:: :octicon:`rocket` Getting Started
      :link: install
      :link-type: doc

      Install SysSim and run your first simulation in a few minutes.

   .. grid-item-card:: :octicon:`book` API Reference
      :link: api/index
      :link-type: doc

      Every public function, class, and CLI command, documented.

   .. grid-item-card:: :octicon:`gear` Configuration
      :link: configuration
      :link-type: doc

      The two-file YAML system for models and hardware.

   .. grid-item-card:: :octicon:`light-bulb` Concepts
      :link: concepts
      :link-type: doc

      What the simulator models and how to read its report.

Why SysSim
----------

- **Estimate training step time and MFU** on accelerators you can't access.
- **Compare parallelism strategies** (TP / SP / DP / CP / PP) before allocating a cluster.
- **Predict peak per-GPU memory** and catch OOM ahead of time.
- **Find the bottleneck** — top ops by time, dominant op type, heaviest pipeline stage.

A 30-second taste
-----------------

.. code-block:: python

   import syssim

   report = syssim.simulate(
       model="examples/configs/models/qwen3-1_7b.yaml",
       hardware="examples/configs/hardware/isambard_gh200_4gpu.yaml",
       parallelism=syssim.ParallelismConfig(tp=2, dp=2),
       training=syssim.TrainingConfig(micro_batch=1, global_batch=8, dtype="bf16"),
   )
   print(report.step_time_ms, report.mfu, report.peak_memory_gb)

.. toctree::
   :hidden:
   :caption: Getting Started

   install
   quickstart
   configuration

.. toctree::
   :hidden:
   :caption: Guides

   concepts
   calibration

.. toctree::
   :hidden:
   :caption: API Reference

   api/index
   api/highlevel
   api/config
   api/operator_graph
   cli
```

- [ ] **Step 2: Build** (toctree refs to unwritten pages will warn — acceptable until later tasks)

Run: `sphinx-build -b html . _build/html 2>&1 | tail -20`
Expected: `build succeeded`. Open `_build/html/index.html` and confirm the hero, cards, and indigo accent render.

- [ ] **Step 3: Commit**

```bash
git add index.rst
git commit -m "Rewrite home page with hero and navigation cards"
```

---

## Task 3: Getting Started pages

**Files:**
- Modify: `install.rst`, `quickstart.rst`
- Create: `configuration.rst`

- [ ] **Step 1: Replace `install.rst`**

```rst
Installation
============

Requirements
------------

- **Python 3.10+**
- A working PyTorch install (``torch >= 2.6``). For *simulation* no GPU is required; a GPU is only
  needed to *profile* real layers when building a calibrated estimator.

SysSim depends on ``torch``, ``megatron-core``, ``megatron-bridge``, ``numpy``, ``pandas``,
``pyarrow``, ``pyyaml``, ``scikit-learn``, ``lightgbm``, and ``transformers`` (installed
automatically).

Install from source
-------------------

.. code-block:: bash

   git clone https://github.com/AISysSim/SysSim.git
   cd SysSim
   pip install -e .

Verify
------

.. code-block:: bash

   syssim --help

You should see the ``run``, ``memory``, ``summary``, ``sweep``, ``profile``, and ``calibrate``
subcommands. Continue to :doc:`quickstart`.
```

- [ ] **Step 2: Replace `quickstart.rst`**

```rst
Quickstart
==========

This walks through a single simulation of **Qwen3-1.7B** on a 4-GPU **GH200** node, using the
example configs shipped in the SysSim repo.

Python API
----------

Three entry points cover the common needs — run a full simulation, check memory only, or sweep a
config axis.

.. tab-set::

   .. tab-item:: simulate

      .. code-block:: python

         import syssim

         MODEL = "examples/configs/models/qwen3-1_7b.yaml"
         HW    = "examples/configs/hardware/isambard_gh200_4gpu.yaml"

         report = syssim.simulate(
             model=MODEL, hardware=HW,
             parallelism=syssim.ParallelismConfig(tp=2, dp=2),
             training=syssim.TrainingConfig(micro_batch=1, global_batch=8, dtype="bf16"),
         )
         print(report.step_time_ms, report.mfu, report.peak_memory_gb)

   .. tab-item:: estimate_memory

      .. code-block:: python

         import syssim

         mem = syssim.estimate_memory(
             model="examples/configs/models/qwen3-1_7b.yaml",
             hardware="examples/configs/hardware/isambard_gh200_4gpu.yaml",
             parallelism=syssim.ParallelismConfig(tp=2, dp=2),
             training=syssim.TrainingConfig(micro_batch=1, global_batch=8, dtype="bf16"),
         )
         print(mem.peak_memory_gb, mem.pp_stage_memory_gb)

   .. tab-item:: sweep

      .. code-block:: python

         import syssim

         result = syssim.sweep(
             model="examples/configs/models/qwen3-1_7b.yaml",
             hardware="examples/configs/hardware/isambard_gh200_4gpu.yaml",
             parallelism=syssim.ParallelismConfig(),
             training=syssim.TrainingConfig(micro_batch=1, global_batch=8, dtype="bf16"),
             over={"parallelism.tp": [1, 2, 4]},
         )
         best = result.best("mfu")
         print(best.inputs, best.metrics)

Command line
------------

The same three workflows are available from the ``syssim`` CLI:

.. code-block:: bash

   # Full report (step time, MFU, memory, bottlenecks)
   syssim run examples/configs/models/qwen3-1_7b.yaml \
       --hardware examples/configs/hardware/isambard_gh200_4gpu.yaml \
       --tp 2 --dp 2 --micro-batch 1 --global-batch 8

   # Memory only
   syssim memory examples/configs/models/qwen3-1_7b.yaml \
       --hardware examples/configs/hardware/isambard_gh200_4gpu.yaml \
       --micro-batch 1 --global-batch 8

   # Sweep an axis, pick the best by a metric
   syssim sweep examples/configs/models/qwen3-1_7b.yaml \
       --hardware examples/configs/hardware/isambard_gh200_4gpu.yaml \
       --micro-batch 1 --global-batch 8 \
       --over parallelism.tp=1,2,4 --metric mfu

Next steps
----------

- :doc:`configuration` — write your own model and hardware YAML.
- :doc:`concepts` — understand the report fields and what the simulator models.
- :doc:`api/highlevel` — the full Python API.
```

- [ ] **Step 3: Create `configuration.rst`**

```rst
Configuration
=============

SysSim uses **two YAML files** — a model architecture and a hardware spec — kept separate so a model
can be simulated across machines and vice versa. Parallelism and training knobs are passed as Python
kwargs (or CLI flags), **not** YAML.

Model YAML
----------

Architecture only. Either provide the Megatron-style fields below, or a single ``huggingface:``
identifier (resolved lazily, no weights downloaded).

.. code-block:: yaml

   # examples/configs/models/qwen3-1_7b.yaml
   num_layers: 28
   hidden_size: 2048
   num_attention_heads: 16
   num_query_groups: 8           # GQA
   ffn_hidden_size: 6144
   seq_length: 4096
   max_position_embeddings: 40960
   vocab_size: 151936
   swiglu: true
   rope: true
   tie_word_embeddings: true
   rms_norm_eps: 1.0e-6

HuggingFace branch:

.. code-block:: yaml

   huggingface: Qwen/Qwen3-8B
   overrides: {}   # optional Megatron provider overrides

See :class:`ModelConfig` for every field.

Hardware YAML
-------------

Accelerator peaks plus a per-dimension ``topology:`` block.

.. code-block:: yaml

   # examples/configs/hardware/isambard_gh200_4gpu.yaml
   peak_tflops_mm: 1979           # tensor-unit peak (TFLOP/s)
   peak_tflops_math: 989          # vector/math peak (TFLOP/s)
   peak_memory_bandwidth_GBps: 3350
   peak_tflops_mm_fp8: 3958

   gpus_per_node: 4
   gpu_memory_GB: 96              # per-GPU HBM; enables OOM detection

   topology:
     dims:      [ fully_connected ]   # fully_connected | switch | ring
     size:      [ 4 ]                 # endpoints in this dimension
     bandwidth: [ 450 ]               # per-GPU uni-directional GB/s
     latency:   [ 12000 ]             # link latency (ns)

A multi-level fabric (e.g. intra-node NVLink + inter-node Slingshot) adds a second entry to each
list. The number of nodes is derived from ``world_size / gpus_per_node``. See
:class:`HardwareConfig` for every field.

Parallelism & training knobs
-----------------------------

Passed in code via :class:`ParallelismConfig` and :class:`TrainingConfig`, or on the CLI:

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Knob
     - Python (kwarg)
     - CLI flag
   * - Tensor parallel
     - ``ParallelismConfig(tp=...)``
     - ``--tp``
   * - Data parallel
     - ``ParallelismConfig(dp=...)``
     - ``--dp``
   * - Context parallel
     - ``ParallelismConfig(cp=...)``
     - ``--cp``
   * - Sequence parallel
     - ``ParallelismConfig(sp=True)``
     - ``--sp``
   * - Pipeline parallel
     - ``ParallelismConfig(pp=...)``
     - *(Python only)*
   * - Micro / global batch
     - ``TrainingConfig(micro_batch=, global_batch=)``
     - ``--micro-batch`` / ``--global-batch``
   * - Precision
     - ``TrainingConfig(dtype="bf16")``
     - ``--dtype {fp16,bf16,fp8}``
   * - Recompute
     - ``TrainingConfig(recompute="selective")``
     - ``--recompute {selective,full}``
```

- [ ] **Step 4: Build & verify cross-refs**

Run: `sphinx-build -b html -n . _build/html 2>&1 | tail -20`
Expected: `build succeeded`. The `:class:` refs to `ModelConfig`/`HardwareConfig`/etc. will warn until Task 5 adds those targets — that is expected here and must be **gone** after Task 5.

- [ ] **Step 5: Commit**

```bash
git add install.rst quickstart.rst configuration.rst
git commit -m "Rewrite Getting Started: install, quickstart, configuration"
```

---

## Task 4: Guide pages

**Files:**
- Create: `concepts.rst`, `calibration.rst`

- [ ] **Step 1: Create `concepts.rst`**

```rst
Concepts
========

What SysSim models
------------------

SysSim traces an LLM training step into an **operator graph**, attributes a time and memory cost to
each operator, and runs a discrete-event simulation over the cluster topology — no real computation
or weights are needed.

Parallelism
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Strategy
     - Status
     - Notes
   * - Tensor parallel (TP)
     - ✅
     - Splits matmuls across GPUs.
   * - Sequence parallel (SP)
     - ✅
     - Shards the sequence dim of norm/dropout regions.
   * - Data parallel (DP)
     - ✅
     - Replicates the model; all-reduces gradients.
   * - Context parallel (CP)
     - ✅
     - Shards the sequence for attention.
   * - Pipeline parallel (PP)
     - ✅
     - 1F1B schedule; per-stage memory reported.
   * - Expert parallel (EP)
     - 🚧
     - Work in progress.

These combine (e.g. TP × DP × PP).

Cost model
----------

The default estimator is the **roofline** bound (compute vs. memory-bandwidth limit per operator).
For higher accuracy you can attach a **calibrated** estimator that multiplies the roofline by a
learned per-operator residual — see :doc:`calibration`.

Reading the report
-------------------

:func:`simulate` returns a :class:`SimulationReport`:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Meaning
   * - ``step_time_ms``
     - Estimated wall-clock step time.
   * - ``forward_ms`` / ``backward_ms`` / ``optimizer_ms``
     - Time attributed per training phase.
   * - ``collective_total_ms`` / ``collective_exposed_ms``
     - Total vs. non-overlapped collective time.
   * - ``achieved_tflops``, ``mfu``, ``hfu``
     - Throughput and model/hardware FLOPs utilization.
   * - ``peak_memory_gb``
     - Peak per-GPU memory (heaviest pipeline stage).
   * - ``pp_stage_memory_gb``
     - Per-pipeline-stage peak memory (one entry per stage).
   * - ``bottlenecks``
     - Top ops by time, dominant op type, longest collective, binding PP stage, and OOM info.

Memory is broken down into parameters, gradients, optimizer state, and activations. When
``gpu_memory_GB`` is set in the hardware YAML, the report flags OOM (capacity / required / excess).
```

- [ ] **Step 2: Create `calibration.rst`**

```rst
Calibrated Estimator
====================

The default estimator is the roofline bound. For higher accuracy on a specific GPU, attach a
**calibrated** estimator (``TreeEstimator``): the roofline times a learned residual — one
regularized LightGBM tree per operator family (GEMM, elementwise, reduction), with the bare roofline
as the fallback for any uncalibrated op.

Using a calibrated model
-------------------------

.. code-block:: python

   from syssim.compute.tree_estimator import TreeEstimator
   from syssim import HardwareConfig

   hw = HardwareConfig(
       peak_tflops_mm=1979, peak_tflops_math=989,
       peak_memory_bandwidth_GBps=3350, gpus_per_node=4,
       calibrated_model="data/gh200",   # directory with fitted trees
   )

Building a calibrated model
---------------------------

Profiling needs the GPU(s); calibration is CPU-only.

.. code-block:: bash

   # 1) Profile real Megatron transformer layers over the committed shape space.
   #    --num-workers N spawns N workers, one pinned per GPU.
   syssim profile   --out data/gh200 --num-workers 4

   # 2) Fit per-family residual trees from <data>/profile.parquet.
   syssim calibrate --data data/gh200 \
       --hardware examples/configs/hardware/isambard_gh200_4gpu.yaml

There is no model-file input to ``profile`` — the shape space is the committed spec
(``syssim/profiling/default_spec.yaml``). Preview the job list (layer configs × tensor-parallel
shapes) without touching the GPU:

.. code-block:: bash

   syssim profile --dry-run

See ``data/gh200/README.md`` in the SysSim repo for the full reproduce recipe.
```

- [ ] **Step 3: Build**

Run: `sphinx-build -b html -n . _build/html 2>&1 | tail -20`
Expected: `build succeeded` (the `:func:`/`:class:` refs still warn until Task 5).

- [ ] **Step 4: Commit**

```bash
git add concepts.rst calibration.rst
git commit -m "Add Concepts and Calibration guide pages"
```

---

## Task 5: API reference — high-level, config, operator graph

Use Sphinx Python-domain directives so every symbol is anchorable and `:func:`/`:class:` refs from
other pages resolve. Content below is the full inventory.

**Files:**
- Create: `api/index.rst`, `api/highlevel.rst`, `api/config.rst`, `api/operator_graph.rst`

- [ ] **Step 1: Create `api/index.rst`**

```rst
API Reference
=============

SysSim's public API has three layers. Most users only need the **high-level** functions.

.. grid:: 1

   .. grid-item-card:: High-level API
      :link: highlevel
      :link-type: doc

      ``simulate``, ``estimate_memory``, ``sweep`` and the config dataclasses
      (``ModelConfig``, ``ParallelismConfig``, ``TrainingConfig``, ``HardwareConfig``).

   .. grid-item-card:: Configuration & Hardware
      :link: config
      :link-type: doc

      Lower-level hardware modeling: ``HardwareInfo``, ``NetworkParams``, ``get_hardware_info``.

   .. grid-item-card:: Operator Graph
      :link: operator_graph
      :link-type: doc

      The traced IR: ``OperatorGraph``, ``OperatorNode``, ``OperatorType``, ``TensorMeta``.

The :doc:`command-line interface <../cli>` wraps the high-level functions.
```

- [ ] **Step 2: Create `api/highlevel.rst`** (full content)

```rst
High-level API
==============

Importable directly from ``syssim``.

Functions
---------

.. py:function:: simulate(*, model, hardware, parallelism=None, training=None, workdir=None)

   Trace a training step and simulate it, returning a full :class:`SimulationReport`
   (step time, MFU, memory, bottlenecks). Thin wrapper over ``trace(...)`` +
   :meth:`Trace.simulate_on`.

   :param model: Path to a model YAML, a :class:`ModelConfig`, or an :class:`HFModel`.
   :param hardware: Path to a hardware YAML or a :class:`HardwareConfig`.
   :param parallelism: :class:`ParallelismConfig` (default: tp=dp=cp=pp=1, sp=False).
   :param training: :class:`TrainingConfig` (default: micro_batch=1, global_batch=1, bf16).
   :param workdir: Optional working directory; auto-created if omitted.
   :returns: :class:`SimulationReport`

.. py:function:: estimate_memory(*, model, hardware, parallelism=None, training=None, workdir=None)

   Per-GPU peak memory only. Runs the memory pass, **skips** the runtime discrete-event
   simulation, and returns a :class:`SimulationReport` with only the memory fields populated
   (runtime fields zero). Same arguments as :func:`simulate`.

   :returns: :class:`SimulationReport` (memory fields populated)

.. py:function:: sweep(*, model, hardware, parallelism=None, training=None, over, workdir=None)

   Run a simulation for every combination on the given config axes and collect the results.

   :param over: Dict of ``{path: [values]}`` where ``path`` is dotted, e.g.
                ``{"parallelism.tp": [1, 2, 4], "training.micro_batch": [1, 2]}``.
   :returns: :class:`Sweep`

   .. code-block:: python

      result = syssim.sweep(model=MODEL, hardware=HW,
                            over={"parallelism.tp": [1, 2, 4]})
      best = result.best("mfu")
      print(best.inputs, best.metrics)

.. py:function:: load_model_yaml(path)

   Load and validate a model YAML into a :class:`ModelConfig`. Raises ``ValueError`` on any
   disallowed top-level key, or if neither/both of the Megatron-fields and ``huggingface`` branches
   are populated.

.. py:function:: load_hardware_yaml(path)

   Load and validate a hardware YAML into a :class:`HardwareConfig`. Raises ``ValueError`` on
   disallowed keys or required-field violations.

Configuration objects
----------------------

.. py:class:: ModelConfig

   Model architecture. Provide **either** the Megatron fields **or** a ``huggingface``
   discriminator (validated in ``from_dict``).

   **Megatron fields:** ``num_layers``, ``hidden_size``, ``num_attention_heads``,
   ``num_query_groups`` (GQA), ``kv_channels`` (head dim; defaults to ``hidden_size // heads``),
   ``ffn_hidden_size``, ``seq_length``, ``max_position_embeddings``, ``vocab_size``,
   ``swiglu`` (default ``True``), ``rope`` (default ``True``), ``rope_theta`` (default ``10000.0``),
   ``tie_word_embeddings`` (default ``False``), ``rms_norm_eps`` (default ``1e-6``).

   **HuggingFace branch:** ``huggingface`` (HF identifier), ``overrides`` (dict, optional).

.. py:class:: ParallelismConfig(*, tp=None, dp=None, sp=None, cp=None, pp=None, vpp=None)

   Parallelism dimensions. Short kwargs map to Megatron names.

   :param tp: Tensor-model-parallel size (default 1).
   :param dp: Data-parallel size (default 1).
   :param sp: Sequence parallel (bool, default False).
   :param cp: Context-parallel size (default 1).
   :param pp: Pipeline-model-parallel size (default 1).
   :param vpp: Virtual pipeline size (default None).

   .. py:property:: world_size

      Computed ``tp * dp * cp * pp`` (read-only).

.. py:class:: TrainingConfig(*, micro_batch=None, global_batch=None, dtype=None, recompute=None, use_distributed_optimizer=False)

   Training hyperparameters. Short kwargs map to Megatron names.

   :param micro_batch: Micro-batch size (>= 1).
   :param global_batch: Global batch size (>= 1).
   :param dtype: One of ``"fp16"``, ``"bf16"`` (default), ``"fp8"``. Exactly one precision must be
                 selected; you may instead pass ``fp16=/bf16=/fp8=`` flags.
   :param recompute: Activation recomputation: ``None``, ``"selective"``, or ``"full"``.
   :param use_distributed_optimizer: Distributed optimizer (default False).

.. py:class:: HardwareConfig

   Self-describing hardware spec — compute peaks + topology.

   **Required:** ``peak_tflops_mm``, ``peak_tflops_math``, ``peak_memory_bandwidth_GBps``,
   ``gpus_per_node``.
   **Optional:** ``peak_tflops_mm_fp8``, ``peak_tflops_mm_fp4``, ``sfu_peak``,
   ``gpu_memory_GB`` (enables OOM detection), ``inter_node_bandwidth_GBps`` (required when derived
   ``num_nodes > 1``), ``inter_node_latency_us`` (default 0.0), ``topology`` (dict),
   ``estimator`` (custom per-op estimator), ``calibrated_model`` (path to fitted trees).

Model sources
-------------

.. py:class:: HFModel(huggingface, overrides=None)

   HuggingFace-source model spec. Architecture is resolved lazily via
   ``megatron.bridge.AutoBridge.from_hf_config`` at trace time — no weights are downloaded.
   ``overrides`` is applied to the resolved Megatron provider before ``finalize()``.

.. py:class:: CustomModel

   Reserved API symbol for a deferred custom ``nn.Module`` source. **v1 raises
   ``NotImplementedError`` at construction.**

Results
-------

.. py:class:: Trace

   The cached operator graph from one trace run, plus provenance (``model``, ``parallelism``,
   ``training``, ``gpus_per_node``, ``per_stage_profiles``).

   .. py:method:: simulate_on(hardware)

      Inject the DP all-reduce + optimizer step (both depend on hardware bandwidth), run the
      discrete-event simulator on a copy of the cached graph, and return a :class:`SimulationReport`.

.. py:class:: SimulationReport

   Result of a simulation. Key fields:

   **Runtime:** ``step_time_ms``, ``forward_ms``, ``backward_ms``, ``optimizer_ms``,
   ``collective_total_ms``, ``collective_exposed_ms``, ``by_op_type_ms``,
   ``model_flops_per_step``, ``achieved_tflops``, ``mfu``, ``hfu``.
   **Memory:** ``param_bytes``, ``grad_bytes``, ``optimizer_state_bytes``, ``activation_bytes``,
   ``peak_memory_gb``.
   **Pipeline:** ``pp_stage_memory_gb`` (list), ``per_pp_rank_step_time_ms`` (list).
   **Provenance / detail:** ``model``, ``parallelism``, ``training``, ``hardware``, ``bottlenecks``.

   .. py:method:: to_dict()

      Serialize to a dict (includes bottleneck detail when present).

   .. py:method:: to_json(path=None)

      Serialize to a JSON string; optionally also write it to ``path``.

   .. py:method:: to_dataframe()

      Convert to a single-row pandas ``DataFrame``.

.. py:class:: Sweep

   Collection of sweep results.

   .. py:method:: best(metric)

      Return the :class:`SweepRow` with the maximum value of ``metric`` (e.g. ``"mfu"``,
      ``"step_time_ms"``, ``"peak_memory_gb"``), or ``None`` if empty.

   .. py:method:: to_dataframe()

      All rows as a pandas ``DataFrame`` (columns = inputs + metrics).

.. py:class:: SweepRow

   One point in a sweep. Fields: ``inputs`` (dict of the swept values), ``report``
   (:class:`SimulationReport`), ``metrics`` (dict: ``step_time_ms``, ``mfu``, ``peak_memory_gb``).
```

- [ ] **Step 3: Create `api/config.rst`** (full content)

```rst
Configuration & Hardware
=========================

Importable from ``syssim``. These back the lower-level cost model; most users use
:doc:`highlevel` instead.

.. py:function:: get_hardware_info()

   Auto-detect the current GPU and return ``(HardwareInfo, name)``. Raises ``RuntimeError`` if CUDA
   is unavailable or the device is unrecognized. Known devices include gh200, h100, a100, v100, a40,
   rtx4090, mi250, mi300, and pro6000.

   .. code-block:: python

      hw_info, hw_name = syssim.get_hardware_info()
      print(hw_name, hw_info.peak_tflops_mm)

.. py:class:: HardwareInfo(peak_tflops_mm, peak_tflops_math, peak_memory_bandwidth_gbps, peak_tflops_mm_conservative=None, peak_tflops_mm_fp8=None, peak_tflops_mm_fp4=None, network=None, estimator=None, sfu_peak=None, calibrated_model=None)

   Hardware specifications for the roofline model. Peak FLOP rates are in **TFLOP/s** (10\ :sup:`12`),
   memory bandwidth in **GB/s** (10\ :sup:`9`). ``peak_tflops_mm_conservative`` is used for small
   GEMM/ATTN ops where launch overhead dominates (defaults to ``peak_tflops_mm``).

   .. py:method:: build_estimator()

      Return the resolved per-op estimator (cached): a ``TreeEstimator`` if ``calibrated_model`` was
      given, else an explicitly attached ``estimator``, else the default ``RooflineEstimator``.

   .. py:method:: get_peak_tflops(op_type, dtype, is_large_op=False)

      Select the peak FLOP/s for an operator type and dtype.

   .. py:method:: get_peak_tflops_mm_for_dtype(dtype)

      Matrix-unit peak for a dtype; FP8 dtypes use ``peak_tflops_mm_fp8``, falling back to
      ``peak_tflops_mm`` when unset.

.. py:class:: NetworkParams

   Network hardware parameters for the communication simulator. Single-node: ``nvlink_bandwidth``
   (bytes/s, default 25e9), ``nvlink_count`` (default 12), ``ib_bandwidth`` (default 25e9).
   Multi-node: ``num_nodes`` (default 1), ``gpus_per_node`` (default 8). LogGP latency/overhead:
   ``loggp_nvlink_L``, ``loggp_nvlink_o``, ``loggp_ib_L``, ``loggp_ib_o`` (seconds).

.. py:class:: SimulatorConfig

   Bundle of ``hw_info`` (:class:`HardwareInfo`) and ``cache_seq_len`` (int, default 0).

.. py:class:: ExecutionMode

   Enum of execution modes: ``TRAINING`` (forward + backward), ``PREFILL`` (forward only, full
   sequence), ``DECODE`` (forward only, seq_len=1, KV-cache read).
```

- [ ] **Step 4: Create `api/operator_graph.rst`** (full content)

```rst
Operator Graph
==============

Importable from ``syssim``. The traced intermediate representation of a model step. Advanced —
needed only when inspecting or building graphs directly.

.. py:class:: OperatorType

   Enum of operator categories: ``GEMM``, ``ATTN``, ``MATH`` (compute); ``COLLECTIVE``
   (communication); ``MEMORY``; ``BARRIER``, ``STREAM_SYNC`` (sync).

.. py:class:: TensorMeta(shape, dtype, device)

   Frozen dataclass describing a tensor: ``shape`` (tuple), ``dtype`` (str), ``device`` (str).

   .. py:method:: to_dict()

      Serialize to ``{"shape": [...], "dtype": ..., "device": ...}``.

.. py:class:: OperatorNode(name, op_type, config=None, predecessors=None, stream_id=0, device_id=0, inputs=None, outputs=None, estimated_time_ms=0.0)

   A single node in the graph. ``predecessors`` lists same-stream FIFO and cross-stream sync
   dependencies; ``inputs``/``outputs`` are lists of :class:`TensorMeta`.

   .. py:method:: to_dict()

      Serialize all fields to a dict.

.. py:class:: OperatorGraph(name="model")

   DAG of :class:`OperatorNode` with multi-stream critical-path analysis. Holds ``operators``
   (dict by name) and ``streams`` (set of stream ids); ``len(graph)`` is the operator count.

   .. py:method:: add_operator(node)

      Add an :class:`OperatorNode` to the graph.

   .. py:method:: validate()

      Validate the DAG: reference integrity and cycle detection (DFS coloring).

   .. py:method:: topological_sort()

      Kahn's algorithm; cached until the graph is modified.

   .. py:method:: to_json()

      Serialize the graph to JSON.

   .. py:method:: to_dot()

      Graphviz DOT representation, color-coded by op type.

   .. py:method:: summary()

      Human-readable summary of op counts and total time.
```

- [ ] **Step 5: Build with nit-picky refs**

Run: `sphinx-build -b html -n . _build/html 2>&1 | tail -30`
Expected: `build succeeded`. The `:class:`/`:func:` warnings from Tasks 3–4 (e.g. `ModelConfig`, `simulate`, `SimulationReport`) must now be **resolved** (no warnings). If any remain, the target name in the directive doesn't match the ref — fix the directive name.

- [ ] **Step 6: Commit**

```bash
git add api/index.rst api/highlevel.rst api/config.rst api/operator_graph.rst
git commit -m "Add hand-written API reference (high-level, config, operator graph)"
```

---

## Task 6: CLI reference (`cli.rst`)

**Files:**
- Create: `cli.rst`

- [ ] **Step 1: Create `cli.rst`** (full content)

```rst
Command-Line Interface
======================

Installing SysSim provides the ``syssim`` command. The compute subcommands
(``run``, ``memory``, ``summary``, ``sweep``) share these flags:

``--hardware PATH`` (required), ``--tp``, ``--dp``, ``--cp``, ``--sp``, ``--micro-batch``,
``--global-batch``, ``--dtype {fp16,bf16,fp8}``, ``--recompute {selective,full}``,
``--format {table,json,yaml}``. Pipeline parallelism (``pp``) is Python-API only.

run
---

Full simulation report (step time, MFU, memory, bottlenecks).

.. code-block:: bash

   syssim run MODEL --hardware HW \
       --tp 2 --dp 2 --micro-batch 1 --global-batch 8

memory
------

Peak per-GPU memory only (skips step-time estimation).

.. code-block:: bash

   syssim memory MODEL --hardware HW --micro-batch 1 --global-batch 8

summary
-------

Print the resolved model / hardware / parallelism / training configuration.

.. code-block:: bash

   syssim summary MODEL --hardware HW --micro-batch 1 --global-batch 8

sweep
-----

Sweep one or more config axes and print the best row by a metric.

.. code-block:: bash

   syssim sweep MODEL --hardware HW --micro-batch 1 --global-batch 8 \
       --over parallelism.tp=1,2,4 --metric mfu

``--over path=v1,v2,...`` may be repeated; ``--metric`` defaults to ``mfu``.

profile
-------

Build the inputs for a calibrated estimator (see :doc:`calibration`). Two modes:

.. code-block:: bash

   # Layer profiling (needs GPUs): writes <out>/profile.parquet
   syssim profile --out data/gh200 --num-workers 4
   syssim profile --dry-run            # preview the job list, no GPU

   # Network profiling: measures NCCL collectives, derives topology
   syssim profile --out data/gh200 --network --gpus-per-node 4

calibrate
---------

Fit per-family residual trees from ``profile.parquet`` (CPU-only).

.. code-block:: bash

   syssim calibrate --data data/gh200 --hardware HW

Writes ``gemm_model.lgb``, ``elementwise_model.lgb``, ``reduction_model.lgb``, and
``manifest.json`` into the data directory, ready to pass as ``calibrated_model=`` in
:class:`HardwareConfig`.
```

- [ ] **Step 2: Build**

Run: `sphinx-build -b html -n . _build/html 2>&1 | tail -20`
Expected: `build succeeded`, no warnings.

- [ ] **Step 3: Commit**

```bash
git add cli.rst
git commit -m "Add CLI reference page"
```

---

## Task 7: Cleanup and final verification

**Files:**
- Delete: `auto_sharding.rst`, `cost_model.rst`, `benchmark.rst`, stale `img/*`

- [ ] **Step 1: Delete stale content**

```bash
cd /Users/lexu/Projects/aisyssim.github.io
git rm auto_sharding.rst cost_model.rst benchmark.rst
git rm -r img
```

- [ ] **Step 2: Confirm nothing references the deleted files**

Run: `grep -rn -E "auto_sharding|cost_model|benchmark|img/" --include=*.rst --include=*.py .`
Expected: no matches (outside `docs/superpowers/`).

- [ ] **Step 3: Clean full build, nit-picky, treat warnings as errors**

Run:
```bash
rm -rf _build
sphinx-build -b html -n -W . _build/html 2>&1 | tail -30
```
Expected: `build succeeded` with **zero** warnings (``-W`` turns any warning into a failure). Fix anything that surfaces.

- [ ] **Step 4: Visual inspection**

Open `_build/html/index.html` in a browser. Confirm: hero + cards render, indigo accent in light **and** dark mode (toggle), sidebar shows the logo and all sections, copy buttons appear on code blocks, the quickstart tabs switch, and API cross-reference links navigate correctly.

- [ ] **Step 5: Commit**

```bash
git commit -m "Remove stale TorchCAP-era pages and images"
```

---

## Self-Review notes

- **Spec coverage:** Furo+extensions (Task 1) ✓; hand-written API for all inventoried symbols (Task 5) ✓; Getting Started install/quickstart/configuration (Task 3) ✓; Concepts+Calibration guides (Task 4) ✓; CLI (Task 6) ✓; cleanup of stale rst+images (Task 7) ✓; indigo accent (Task 1 CSS + theme vars) ✓; CI install line updated (Task 1) ✓.
- **Cross-ref ordering:** Tasks 3–4 intentionally reference `:class:`/`:func:` targets defined in Task 5; each interim build notes these warnings as expected, and Task 5 Step 5 + Task 7 Step 3 (`-W`) enforce they are resolved before completion.
- **Logo question:** plan generates an SVG wordmark; if the user supplies a real logo, drop it in `_static/logo.svg` and skip Step 2 of Task 1.
