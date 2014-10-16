from heppy.framework.analyzer import Analyzer

class FCCPrinter(Analyzer):

    def process(self, event):
        print "printing event", event.iEv
        store = event.input
        jets = store.get("GenJet")
        for jet in jets:
            print 'jet', jet.P4().Pt
