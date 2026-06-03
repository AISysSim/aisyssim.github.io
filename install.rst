Installation
============

Requirements
------------

- **Python 3.10+**
- A working PyTorch install (``torch >= 2.6``). For *simulation* no GPU is required; a GPU is only
  needed to *profile* real layers when building a calibrated estimator.

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
subcommands. Continue to :doc:`quickstart`.
