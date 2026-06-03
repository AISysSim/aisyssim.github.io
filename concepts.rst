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
