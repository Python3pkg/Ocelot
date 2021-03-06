Installation
------------

Ocelot is designed for Python 3.4 or higher.

Most Ocelot dependencies are pure Python, and this easy to install, but Ocelot uses `lxml <http://lxml.de/>`__. (`cytoolz <https://pypi.python.org/pypi/cytoolz>`__, another compiled library, is optional but highly recommended). Therefore, the easiest way to install Ocelot is using `Anaconda <https://www.continuum.io/downloads>`__. Other installation pathways (e.g. `macports <https://www.macports.org/>`__, `homebrew <http://brew.sh/>`__, Christoph Gohlke's `unofficial binaries <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`__ should also work as well.

To install using ``Anaconda``, download `the relevant Miniconda installer <http://conda.pydata.org/miniconda.html>`__. Be sure to get Python 3.5, and the 64 bit version.

.. note:: On OS X, you may have to make the downloaded script executable using something like ``chmod +x ~/Downloads/Miniconda3-latest-MacOSX-x86_64.sh``.

Run the installation script in the terminal/powershell/command window.

.. warning:: If you have other Python installations on your machine, be sure to answer **no** to the questions about making this your default Python, and add Miniconda to your path. You will then need to adjust the following commands to the ``bin`` directory of your miniconda installation.

Then, run the following commands to create an Ocelot environment:

.. code-block:: bash

    conda create -y -n ocelot python=3.6

On Windows, then run:

.. code-block:: bash

    activate ocelot
    conda install -y pywin32
    conda install -c conda-forge -c cmutel appdirs bw2parameters docopt docutils jinja2 lxml pandas pyprind psutil pytest stats_arrays cytoolz toolz voluptuous wrapt jupyter
    pip install --no-cache-dir https://github.com/OcelotProject/Ocelot/zipball/master

Otherwise, do:

.. code-block:: bash

    source activate ocelot
    conda install -c conda-forge -c cmutel appdirs bw2parameters docopt docutils jinja2 lxml pandas pyprind psutil pytest stats_arrays cytoolz toolz voluptuous wrapt jupyter
    pip install --no-cache-dir https://github.com/OcelotProject/Ocelot/zipball/master

.. note:: If you install from pypi, you will have to install the ``ocelot-lca`` package - someone pipped us during development!

If Ocelot is correctly installed, you should be able to run the command line application:

.. code-block:: bash

    ocelot-cli --help

To run Ocelot, you will need an unlinked database in `ecospold2 <http://www.ecoinvent.org/data-provider/data-provider-toolkit/ecospold2/ecospold2.html>`__ format.

Installing Brightway2 in the Ocelot environment
-----------------------------------------------

If you want, you can also install `Brightway2 <https://brightwaylca.org/>`__ in your Ocelot environment. While the ``ocelot`` environment is activated, enter the following:

.. code-block:: bash

    conda install -y -q -c conda-forge -c cmutel -c haasad brightway2
