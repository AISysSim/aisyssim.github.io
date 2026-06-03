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
