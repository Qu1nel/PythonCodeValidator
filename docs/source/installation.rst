************
Installation
************

This page provides instructions for installing the ``python-code-validator`` package.

.. grid:: 1 2 2 1
   :gutter: 2

   .. grid-item-card:: For Users
      :shadow: md

      The recommended way to install the package for regular use is from the
      Python Package Index (PyPI) using ``pip`` or any compatible package manager.
      This will install the latest stable version and make the ``validate-code``
      command-line tool available in your environment.

      .. code-block:: bash

         pip install python-code-validator

      To upgrade to a new version, use:

      .. code-block:: bash

         pip install --upgrade python-code-validator

   .. grid-item-card:: For Developers
      :shadow: md

      If you intend to contribute to the project, you should set up a local
      development environment from the source code. This will install the package
      in "editable" mode and include all dependencies for testing and documentation.

      1. First, clone the repository from GitHub:

         .. code-block:: bash

            git clone https://github.com/Qu1nel/PythonCodeValidator.git
            cd PythonCodeValidator

      2. Then, use the provided ``Makefile`` for a one-command setup:

         .. code-block:: bash

            make setup

      This command automates the creation of a virtual environment and the
      installation of all required packages. For more details on contributing,
      please see the :doc:`../contributing` guide.

Verifying the Installation
==========================

After installation, you can verify that the command-line tool is working
by checking its version:

.. code-block:: bash

   validate-code --version

This should print the installed version of the package, for example:

.. code-block:: text

   validate-code 0.1.1