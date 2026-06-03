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
