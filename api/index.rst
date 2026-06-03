API Reference
=============

SysSim's public API has three layers. Most users only need the **high-level** functions.

.. grid:: 1
   :gutter: 3

   .. grid-item-card:: High-level API
      :link: highlevel
      :link-type: doc

      ``simulate``, ``estimate_memory``, ``sweep`` and the config dataclasses
      (``ModelConfig``, ``ParallelismConfig``, ``TrainingConfig``, ``HardwareConfig``).

   .. grid-item-card:: Configuration & Hardware
      :link: config
      :link-type: doc

      Lower-level hardware modeling: ``HardwareInfo``, ``NetworkParams``, ``get_hardware_info``.

   .. grid-item-card:: Operator Graph
      :link: operator_graph
      :link-type: doc

      The traced IR: ``OperatorGraph``, ``OperatorNode``, ``OperatorType``, ``TensorMeta``.

The :doc:`command-line interface <../cli>` wraps the high-level functions.
