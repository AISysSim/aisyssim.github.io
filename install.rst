Installation
============

Requirements
------------

- **Python 3.10+**
- A working PyTorch install (``torch >= 2.6``).
- A CUDA-capable GPU for tracing and simulation. SysSim uses PyTorch fake tensors marked with
  ``device="cuda"``, so PyTorch still needs CUDA kernel dispatch to build the operator graph.
  Profiling real layers for a calibrated estimator also needs GPUs.

SysSim depends on ``torch``, ``megatron-core``, ``megatron-bridge``, ``numpy``, ``pandas``,
``pyarrow``, ``pyyaml``, ``scikit-learn``, ``lightgbm``, and ``transformers`` (installed
automatically).

Install from source
-------------------

.. code-block:: bash

   git clone https://github.com/AISysSim/SysSim.git
   cd SysSim
   pip install -e .

Verify
------

.. code-block:: bash

   syssim --help

You should see the ``run``, ``memory``, ``summary``, ``sweep``, ``profile``, and ``calibrate``
subcommands. ``run`` is the CLI name for the full ``simulate`` mode. Continue to
:doc:`quickstart`.
