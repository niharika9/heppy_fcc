import copy
from links import Links
from distance import distance
from ROOT import TVector3


def merge_clusters(elements, layer):
    merged = []
    elem_in_layer = [elem for elem in elements if elem.layer==layer]
    links = Links(elem_in_layer, distance)
    for group in links.groups.values():
        if len(group) == 1:
            merged.append(group[0]) 
            continue
        supercluster = None
        for cluster in group: 
            if supercluster is None:
                supercluster = copy.copy(cluster)
                merged.append(supercluster)
                continue
            else: 
                supercluster += cluster
    return merged
