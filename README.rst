ros-answers-miner
=================

A web scraper for ROS Answers


Installation
------------

We strongly recommend that you install this package inside a Python virtual
environment (via virtualenv or pipenv) to avoid interfering with the rest of
your system (i.e., to avoid Python’s equivalent of DLL hell).
To install this package from source within a virtual environment using pipenv:

.. code::

   $ git clone git@github.com:squaresLab/ros-answers-miner ros-answers-miner
   $ cd ros-answers-miner
   $ pipenv shell
   (rosdiscover) $ pip install -r requirements.dev.txt
   (rosdiscover) $ pip install -e .
