export HEPPY_FCC=$PWD
if [ -z ${PODIO+x} ]; then
    echo 'PODIO not set'
else
    export PYTHONPATH=$PODIO/python:$PYTHONPATH
fi
export PYTHONPATH=$PWD/..:$PYTHONPATH
