export HEPPY_FCC=$PWD
if [ -z ${ALBERS+x} ]; then
    echo 'albers not set'
else
    export PYTHONPATH=$pyalbers/python:$PYTHONPATH
fi
export PYTHONPATH=$PWD/..:$PYTHONPATH
