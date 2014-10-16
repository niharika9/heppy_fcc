Heppy-fcc : heppy adapter package for the FCC experiments
================================================================

Prerequisites
-------------

heppy : https://github.com/HEP-FCC/heppy

albers : https://github.com/HEP-FCC/albers

use albers to produce the example.root file and put it in the test/ directory

Installation
-

Define the following variable:
	export HEPPY_FCC=$PWD

Put the following in your python path:

    export PYTHONPATH=$HEPPY_FCC/..:$PYTHONPATH

Examples
--------

Several examples are provided in the test/ directory:

	cd test/

Read a root file and print each event:

	multiloop.py  Trash   print_events_cfg.py

