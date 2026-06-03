Operator Graph
==============

Importable from ``syssim``. The traced intermediate representation of a model step. Advanced —
needed only when inspecting or building graphs directly.

.. py:class:: OperatorType

   Enum of operator categories: ``GEMM``, ``ATTN``, ``MATH`` (compute); ``COLLECTIVE``
   (communication); ``MEMORY``; ``BARRIER``, ``STREAM_SYNC`` (sync).

.. py:class:: TensorMeta(shape, dtype, device)

   Frozen dataclass describing a tensor: ``shape`` (tuple), ``dtype`` (str), ``device`` (str).

   .. py:method:: to_dict()

      Serialize to ``{"shape": [...], "dtype": ..., "device": ...}``.

.. py:class:: OperatorNode(name, op_type, config=None, predecessors=None, stream_id=0, device_id=0, inputs=None, outputs=None, estimated_time_ms=0.0)

   A single node in the graph. ``predecessors`` lists same-stream FIFO and cross-stream sync
   dependencies; ``inputs``/``outputs`` are lists of :class:`TensorMeta`.

   .. py:method:: to_dict()

      Serialize all fields to a dict.

.. py:class:: OperatorGraph(name="model")

   DAG of :class:`OperatorNode` with multi-stream critical-path analysis. Holds ``operators``
   (dict by name) and ``streams`` (set of stream ids); ``len(graph)`` is the operator count.

   .. py:method:: add_operator(node)

      Add an :class:`OperatorNode` to the graph.

   .. py:method:: validate()

      Validate the DAG: reference integrity and cycle detection (DFS coloring).

   .. py:method:: topological_sort()

      Kahn's algorithm; cached until the graph is modified.

   .. py:method:: to_json()

      Serialize the graph to JSON.

   .. py:method:: to_dot()

      Graphviz DOT representation, color-coded by op type.

   .. py:method:: summary()

      Human-readable summary of op counts and total time.
