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
