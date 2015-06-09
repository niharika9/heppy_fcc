import heppy.framework.config as cfg

from CMGTools.Production.getFiles import getFiles 

gun_22_0_50 = cfg.Component(
    'gun_22_0_50',
    files = getFiles("/Gun_22_0_50/743_v1/RECOSIM", "cbern", ".*.root"),
) 

gun_11_0_50 = cfg.Component(
    'gun_11_0_50',
    files = getFiles("/Gun_11_0_50/743_v1/RECOSIM", "cbern", ".*.root"),
) 

guns = [
    gun_22_0_50, 
    gun_11_0_50
]

for gun in guns: 
    gun.splitFactor = 5
