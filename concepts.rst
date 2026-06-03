Concepts
========

What SysSim models
------------------

SysSim traces an LLM training step into an **operator graph**, attributes a time and memory cost to
each operator, and runs a discrete-event simulation over the cluster topology — no real computation
or weights are needed.

Tracing still requires PyTorch CUDA dispatch: SysSim uses PyTorch fake tensors marked with
``device="cuda"`` so PyTorch builds the same operator graph shape it would use for CUDA tensors,
without running the real kernels.

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

:func:`simulate` returns a :class:`SimulationReport`; the ``syssim run`` CLI prints the same core
fields. A typical report looks like:

.. code-block:: text

   SimulationReport(
     step_time_ms        = 644.6507
       forward_ms        = 184.5179
       backward_ms       = 383.1765
       optimizer_ms      = 39.4327
     collective_total_ms = 53.9978
     collective_exposed  = 37.5235
     achieved_tflops     = 184.55
     mfu                 = 9.33%
     hfu                 = 12.43%
     peak_memory_gb      = 26.133
     Bottlenecks(
       dominant_op_type = math
       top_ops_by_time  = [('optimizer_step_4289', 39.43271286447761), ('op_1181_aten.mm', 4.286653309549106), ('op_1182_aten.mm', 4.21173467212024)]
       peak_module      = Float16Module
     )
   )

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
     - Throughput, Model FLOPs Utilization (MFU), and Hardware FLOPs Utilization (HFU).
   * - ``peak_memory_gb``
     - Peak per-GPU memory (heaviest pipeline stage).
   * - ``pp_stage_memory_gb``
     - Per-pipeline-stage peak memory (one entry per stage).
   * - ``bottlenecks``
     - Top ops by time, dominant op type, longest collective, binding PP stage, and OOM info.

Memory is broken down into parameters, gradients, optimizer state, and activations. When
``gpu_memory_GB`` is set in the hardware YAML, the report flags OOM (capacity / required / excess).
