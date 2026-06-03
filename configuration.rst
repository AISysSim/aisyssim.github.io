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

Other accelerator vendors
-------------------------

Hardware targets are vendor-neutral. To simulate another accelerator family, provide that device's
compute peaks, memory bandwidth, HBM capacity, and topology. For example, an AMD MI300-style target
uses the same schema:

.. code-block:: yaml

   # examples/configs/hardware/amd_mi300_8gpu.yaml
   peak_tflops_mm: 653             # tensor-unit peak (TFLOP/s)
   peak_tflops_math: 326.5         # vector/math peak (TFLOP/s)
   peak_memory_bandwidth_GBps: 5200

   gpus_per_node: 8
   gpu_memory_GB: 192              # set to the HBM capacity of the target card

   topology:
     dims:      [ fully_connected ]   # choose fully_connected | switch | ring to match the fabric
     size:      [ 8 ]
     bandwidth: [ 300 ]               # replace with measured per-GPU uni-directional GB/s
     latency:   [ 12000 ]             # replace with measured latency (ns)

Only the hardware YAML changes; the model YAML, parallelism config, and training config stay the
same. The default roofline estimator uses these hardware peaks directly. For higher accuracy on a
specific accelerator, build a calibrated estimator for that device and set ``calibrated_model`` in
the hardware YAML.

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
