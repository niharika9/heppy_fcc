import operator

class PFInput(object):
    '''Builds the inputs to particle flow from a collection of simulated particles:
    - collects all smeared tracks and clusters
    - merges overlapping clusters 
    '''
    
    def __init__(self, ptcs):
        '''
        attributes: 
        - tracks: list of tracks
        - clusters: dictionary of clusters sorted by layer, with this format: 
          ecal: [cluster0, cluster1, ...]
          hcal: [... ]
        '''
        self.clusters = dict()
        self.tracks = []
        self.build(ptcs)
        
    def build(self, ptcs):
        for ptc in ptcs:
            for key, cluster in ptc.clusters_smeared.iteritems():
                self.clusters.setdefault(key, []).append(cluster)
            if ptc.track_smeared: 
                self.tracks.append(ptc.track_smeared)
        self.tracks.sort(key=operator.attrgetter('pt'), reverse=True)
        for clusters in self.clusters.values():
            self.merge_clusters(clusters)
            clusters.sort(key=operator.attrgetter('energy'), reverse=True)
            
    def merge_clusters(self, clusters):
        pass
            
    def __str__(self):
        lines = ['PFInput:']
        lines.append('\tTracks:')
        def tab(astr, ntabs=2):
            return ''.join(['\t'*ntabs, str(astr)])
        for track in self.tracks:
            lines.append(tab(str(track)))
        lines.append('\tClusters:')
        for layer, clusters in sorted(self.clusters.iteritems()):
            lines.append(tab(layer))
            for cluster in clusters:
                lines.append(tab(str(cluster), 3))
        return '\n'.join(lines)
