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
