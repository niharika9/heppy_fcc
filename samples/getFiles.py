from PhysicsTools.HeppyCore.utils.dataset import createDataset

def getFiles(dataset, cache=True, basedir='/store/cmst3/user/cbern/CMG'):
    ds = createDataset('EOS', dataset, '.*root', 
                       readcache=cache, basedir=basedir)
    filenames = ds.listOfGoodFiles()
    return ['root://eoscms.cern.ch//eos/cms{fname}'.format(fname=fname) 
            for fname in filenames]

