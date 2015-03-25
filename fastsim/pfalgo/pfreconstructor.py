from heppy_fcc.fastsim.pdt import particle_data
from heppy_fcc.fastsim.path import StraightLine, Helix
from heppy_fcc.fastsim.pfobjects import Particle

from ROOT import TVector3, TLorentzVector
import math
import pprint

class PFReconstructor(object):

    def __init__(self, links, detector):
        self.links = links
        self.detector = detector
        self.particles = self.reconstruct(links)

    def reconstruct(self, links):
        particles = []
        all_subgroups = dict()
        # pprint.pprint( links.groups )
        for groupid, group in links.groups.iteritems():
            if self.simplify_group(group):
                all_subgroups[groupid] = links.subgroups(groupid)
        for group_id, subgroups in all_subgroups.iteritems():
            del links.groups[group_id]
            links.groups.update(subgroups)
        for group_id, group in links.groups.iteritems():
            print "GROUP", group_id, group
            particles.extend( self.reconstruct_group(group) ) 
        return particles
            
    def simplify_group(self, group):
        # for each track, keeping only the closest hcal link
        simplified = False
        assert(len(group)!=0)
        if len(group)==1:
            return False
        tracks = [elem for elem in group if elem.layer=='tracker']
        for track in tracks:
            first_hcal = True
            to_unlink = []
            for linked in track.linked:
                if linked.layer == 'hcal_in':
                    if first_hcal:
                        first_hcal = False
                    else:
                        to_unlink.append(linked)
            for linked in to_unlink:
                self.links.unlink(track, linked)
                simplified = True
        # remove all ecal-hcal links. ecal linked to hcal give rise to a photon anyway.
        ecals = [elem for elem in group if elem.layer=='ecal_in']
        for ecal in ecals:
            to_unlink = []
            for linked in ecal.linked:
                if linked.layer == 'hcal_in':
                    to_unlink.append(linked)
            for linked in to_unlink:
                self.links.unlink(ecal, linked)
                simplified = True
        return simplified
            
    def reconstruct_group(self, group):
        particles = []
        if len(group)==1: #TODO WARNING
            elem = group[0]
            layer = elem.layer
            if layer == 'ecal_in' or layer == 'hcal_in':
                particles.append(self.reconstruct_cluster(elem, layer))
            elif layer == 'tracker':
                particles.append(self.reconstruct_track(elem))
            elem.locked = True
        else:
            hcals = [elem for elem in group if elem.layer=='hcal_in']
            for hcal in hcals:
                particles.append(self.reconstruct_hcal(hcal))
        return particles 

    def reconstruct_hcal(self, hcal):
        particles = []
        tracks = []
        ecals = []
        for elem in hcal.linked:
            assert(elem.layer!='ecal_in') # should have killed ecal-hcal links
            if elem.layer == 'hcal_in':
                continue
            elif elem.layer == 'tracker':
                tracks.append(elem)
                ecals.extend([te for te in elem.linked if te.layer=='ecal_in'])
        print hcal
        print '\tT', tracks
        print '\tE', ecals
        hcal_energy = hcal.energy
        ecal_energy = sum(ecal.energy for ecal in ecals)
        track_energy = sum(track.energy for track in tracks)
        if len(tracks):
            for track in tracks:
                particles.append(self.reconstruct_track(track))
            e_over_p = (hcal_energy + ecal_energy) / track_energy
            calo_eres = self.detector.elements['hcal'].energy_resolution(track_energy)
            print 'E/p, res = ' e_over_p, calo_eres
            if e_over_p - 1 > calo_eres:
                print 'excess!'
        return particles 
                
    def reconstruct_cluster(self, cluster, layer, vertex=None):
        if vertex is None:
            vertex = TVector3()
        pdg_id = None
        if layer=='ecal_in':
            pdg_id = 22
        elif layer=='hcal_in':
            pdg_id = 130
        else:
            raise ValueError('layer must be equal to ecal_in or hcal_in')
        assert(pdg_id)
        mass, charge = particle_data[pdg_id]
        energy = cluster.energy
        momentum = math.sqrt(energy**2 - mass**2) 
        p3 = cluster.position.Unit() * momentum
        p4 = TLorentzVector(p3.Px(), p3.Py(), p3.Pz(), energy)
        particle = Particle(p4, vertex, charge, pdg_id)
        path = StraightLine(p4, vertex)
        path.points[layer] = cluster.position
        particle.set_path(path)
        particle.clusters_smeared[layer] = cluster
        cluster.locked = True
        return particle
        
    def reconstruct_track(self, track):
        vertex = track.path.points['vertex']
        pdg_id = 211 * track.charge
        mass, charge = particle_data[pdg_id]
        p4 = TLorentzVector()
        p4.SetVectM(track.p3, mass)
        particle = Particle(p4, vertex, charge, pdg_id)
        particle.set_path(track.path)
        track.locked = True
        return particle


    def __str__(self):
        return '\n'.join( map(str, self.particles) ) 
