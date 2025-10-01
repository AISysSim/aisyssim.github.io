AISysSim Quickstart
===================

Setup
~~~~~

Build the Docker environment required to run AISysSim:

.. code-block:: bash

   docker build -t syssim-env .

Profiling Hardware
~~~~~~~~~~~~~~~~~~

AISysSim can optionally profile your hardware to collect detailed performance metrics. This enables more accurate cost estimation.

**Note:** If this step is skipped, AISysSim will fall back on querying system APIs, which may be less precise.

To profile your cluster:

.. code-block:: bash

   bash profile_cluster.sh -o profile.json -n <num_nodes> -d <num_devices_per_node> [-p]

This command generates a JSON file containing a cost model specific to your hardware. ``-p`` is an optional option that generates the plots of the cost models.

Running AISysSim with Huggingface models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run AISysSim with a specified hardware profile and Huggingface models:

Single Device
^^^^^^^^^^^^^

.. code-block:: bash

   bash examples/huggingface/run_docker.sh -m facebook/opt-6.7b -e profile.json -n 1

Multiple Devices
^^^^^^^^^^

.. code-block:: bash

   bash examples/huggingface/run_docker.sh -m facebook/opt-6.7b -e profile.json -n 2

Arguments
^^^^^^^^^
- ``-n``: Number of GPUs
- ``-m``: Hugging Face model path (e.g., ``facebook/opt-6.7b``)
- ``-e``: Path to the hardware profile JSON file generated during profiling

