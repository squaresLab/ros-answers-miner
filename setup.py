# -*- coding: utf-8 -*-
import os
import setuptools

PACKAGE = 'ros_answers_miner'
PATH = os.path.join(os.path.dirname(__file__),
                    'src/{}/version.py'.format(PACKAGE))
with open(PATH, 'r') as fh:
    exec(fh.read())

setuptools.setup(version=__version__)
