from PhysicsTools.HeppyCore.utils.dataset import createDataset

def getFiles(dataset, basedir='/store/cmst3/user/cbern/CMG'):
    ds = createDataset('EOS', dataset, '.*root', 
                       readcache=True, basedir=basedir)
    filenames = ds.listOfGoodFiles()
    return ['root://eoscms.cern.ch//eos/cms{fname}'.format(fname=fname) 
            for fname in filenames]

