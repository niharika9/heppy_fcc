Heppy-fcc : heppy adapter package for the FCC experiments
================================================================

Prerequisites
-------------

Install the following packages: 

heppy : https://github.com/HEP-FCC/heppy

fcc-edm : https://github.com/HEP-FCC/fcc-edm


Installation
------------

Every time you want to use the package set up your environment by sourcing
the following script:

    source init_macos.sh


Examples
--------

Several examples are provided in the test/ directory:

    cd test/

Read a root file and print each event:

    heppy_loop.py  Trash  simple_analysis_cfg.py -N 1000

