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
