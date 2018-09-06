#!/usr/bin/env python

from distutils.core import setup
from tm_distribute import __version__
from glob import glob

setup(
    name="tm-distribute",
    version=__version__,
    description="Distribute L1 trigger menus for synthesis",
    author="Bernhard Arnold",
    author_email="bernhard.arnold@cern.ch",
    url="https://github.com/arnobaer/tm-distribute",
    packages=["tm_distribute"],
    package_data={
        'tm_distribute': ['templates/*/*'],
    },
    scripts=[
        "scripts/tm-distribute",
    ],
    provides=["tm_distribute", ],
)
