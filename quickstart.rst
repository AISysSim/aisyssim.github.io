Quickstart
==========

This walks through **Qwen3-1.7B** on a 4-GPU **GH200** node, using the example configs shipped in
the SysSim repo.

Choose a mode
-------------

.. list-table::
   :header-rows: 1

   * - Mode
     - Use it when you want to
     - Output to inspect
   * - ``simulate``
     - Run the full training-step simulator.
     - Step time, MFU, memory, OOM status, and bottlenecks.
   * - ``estimate_memory``
     - Check whether a configuration fits in GPU memory without running the runtime simulator.
     - Peak per-GPU memory and per-pipeline-stage memory.
   * - ``sweep``
     - Try several values for one or more config axes.
     - One report per candidate plus ``best(metric)``. The best row is the one with the largest
       selected metric, so the quickstart uses ``mfu`` to select the highest-MFU candidate.

Python API
----------

The Python API exposes the same three modes.

.. tab-set::

   .. tab-item:: simulate

      .. code-block:: python

         import syssim

         MODEL = "examples/configs/models/qwen3-1_7b.yaml"
         HW = "examples/configs/hardware/isambard_gh200_4gpu.yaml"

         report = syssim.simulate(
             model=MODEL, hardware=HW,
             parallelism=syssim.ParallelismConfig(tp=2, dp=2),
             training=syssim.TrainingConfig(micro_batch=1, global_batch=8, dtype="bf16"),
         )
         print(report.step_time_ms, report.mfu, report.peak_memory_gb)

   .. tab-item:: estimate_memory

      .. code-block:: python

         import syssim

         MODEL = "examples/configs/models/qwen3-1_7b.yaml"
         HW = "examples/configs/hardware/isambard_gh200_4gpu.yaml"

         mem = syssim.estimate_memory(
             model=MODEL, hardware=HW,
             parallelism=syssim.ParallelismConfig(tp=2, dp=2),
             training=syssim.TrainingConfig(micro_batch=1, global_batch=8, dtype="bf16"),
         )
         print(mem.peak_memory_gb, mem.pp_stage_memory_gb)

   .. tab-item:: sweep

      .. code-block:: python

         import syssim

         MODEL = "examples/configs/models/qwen3-1_7b.yaml"
         HW = "examples/configs/hardware/isambard_gh200_4gpu.yaml"

         result = syssim.sweep(
             model=MODEL, hardware=HW,
             parallelism=syssim.ParallelismConfig(),
             training=syssim.TrainingConfig(micro_batch=1, global_batch=8, dtype="bf16"),
             over={"parallelism.tp": [1, 2, 4]},
         )
         best = result.best("mfu")
         print(best.inputs, best.metrics)

Command line
------------

The same three workflows are available from the ``syssim`` CLI.

For CLI commands, the first positional argument is the model YAML and ``--hardware`` points to the
hardware YAML.

.. tab-set::

   .. tab-item:: simulate

      Full simulation report: step time, MFU, memory, OOM status, and bottlenecks. The CLI
      subcommand for this mode is ``run``.

      .. code-block:: bash

         syssim run examples/configs/models/qwen3-1_7b.yaml \
             --hardware examples/configs/hardware/isambard_gh200_4gpu.yaml \
             --tp 2 --dp 2 --micro-batch 1 --global-batch 8

   .. tab-item:: memory

      Memory-only report. This skips runtime simulation and is useful for fit checks.

      .. code-block:: bash

         syssim memory examples/configs/models/qwen3-1_7b.yaml \
             --hardware examples/configs/hardware/isambard_gh200_4gpu.yaml \
             --tp 2 --dp 2 --micro-batch 1 --global-batch 8

   .. tab-item:: sweep

      Sweep tensor parallelism values and select the candidate with the highest ``mfu``.

      .. code-block:: bash

         syssim sweep examples/configs/models/qwen3-1_7b.yaml \
             --hardware examples/configs/hardware/isambard_gh200_4gpu.yaml \
             --micro-batch 1 --global-batch 8 \
             --over parallelism.tp=1,2,4 --metric mfu

Next steps
----------

- :doc:`configuration` — write your own model and hardware YAML.
- :doc:`concepts` — understand the report fields and what the simulator models.
- :doc:`api/highlevel` — the full Python API.
