#!/bin/env python

def var( tree, varName, type=float ):
    tree.var(varName, type)

def fill( tree, varName, value ):
    tree.fill( varName, value )

# simple particle

def bookParticle( tree, pName ):
    var(tree, '{pName}_pdgid'.format(pName=pName))
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_theta'.format(pName=pName))
    var(tree, '{pName}_eta'.format(pName=pName))
    var(tree, '{pName}_phi'.format(pName=pName))
    var(tree, '{pName}_m'.format(pName=pName))

def fillParticle( tree, pName, particle ):
    fill(tree, '{pName}_pdgid'.format(pName=pName), particle.pdgid() )
    fill(tree, '{pName}_e'.format(pName=pName), particle.e() )
    fill(tree, '{pName}_pt'.format(pName=pName), particle.pt() )
    fill(tree, '{pName}_theta'.format(pName=pName), particle.theta() )
    fill(tree, '{pName}_eta'.format(pName=pName), particle.eta() )
    fill(tree, '{pName}_phi'.format(pName=pName), particle.phi() )
    fill(tree, '{pName}_m'.format(pName=pName), particle.m() )

def bookCluster( tree, name ):
    var(tree, '{name}_e'.format(name=name))
    var(tree, '{name}_layer'.format(name=name))

layers = dict(
    ecal_in = 0,
    hcal_in = 1
)
    
def fillCluster( tree, name, cluster ):
    fill(tree, '{name}_e'.format(name=name), cluster.energy )
    fill(tree, '{name}_layer'.format(name=name), layers[cluster.layer] )
    
# jet

def bookComponent( tree, pName ):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_num'.format(pName=pName))

def fillComponent(tree, pName, component):
    fill(tree, '{pName}_e'.format(pName=pName), component.e() )
    fill(tree, '{pName}_pt'.format(pName=pName), component.pt() )
    fill(tree, '{pName}_num'.format(pName=pName), component.num() )
    
    
pdgids = [211, 22, 130, 11, 13]
    
def bookJet( tree, pName ):
    bookParticle(tree, pName )
    for pdgid in pdgids:
        bookComponent(tree, '{pName}_{pdgid:d}'.format(pName=pName, pdgid=pdgid))
    # var(tree, '{pName}_npart'.format(pName=pName))

def fillJet( tree, pName, jet ):
    fillParticle(tree, pName, jet )
    for pdgid in pdgids:
        component = jet.constituents.get(pdgid, None)
        if component is not None:
            fillComponent(tree,
                          '{pName}_{pdgid:d}'.format(pName=pName, pdgid=pdgid),
                          component )
        else:
            import pdb; pdb.set_trace()
            print jet

iso_pdgids = [211, 22, 130]

def bookIso(tree, pName):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_num'.format(pName=pName))    
    
def fillIso(tree, pName, iso):
    fill(tree, '{pName}_e'.format(pName=pName), iso.sume )
    fill(tree, '{pName}_pt'.format(pName=pName), iso.sumpt )
    fill(tree, '{pName}_num'.format(pName=pName), iso.num )    

def bookLepton( tree, pName ):
    bookParticle(tree, pName )
    for pdgid in iso_pdgids:
        bookIso(tree, '{pName}_{pdgid:d}'.format(pName=pName, pdgid=pdgid))

def fillLepton( tree, pName, lepton ):
    fillParticle(tree, pName, lepton )
    for pdgid in iso_pdgids:
        iso = getattr(lepton, 'iso_{pdgid:d}'.format(pdgid=pdgid))
        fillIso(tree, '{pName}_{pdgid:d}'.format(pName=pName, pdgid=pdgid), iso)
