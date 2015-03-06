Heppy-fcc : heppy adapter package for the FCC experiments
================================================================

Prerequisites
-------------

Install the following packages in this order: 

albers-core : https://github.com/HEP-FCC/albers-core

fcc-edm : https://github.com/HEP-FCC/fcc-edm

heppy : https://github.com/HEP-FCC/heppy


Installation
------------

Every time you want to use the package set up your environment by sourcing
the following script:

    source init.sh


Examples
--------

Several examples are provided in the test/ directory:

    cd test/

Read a root file and print each event:

    ${FCCEDM}/bin/fccedm-write
    heppy_loop.py  Output simple_analysis_cfg.py -N 1000
