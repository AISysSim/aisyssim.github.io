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
