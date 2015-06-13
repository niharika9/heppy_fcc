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

gun_13_0_50 = cfg.Component(
    'gun_13_0_50',
    files = getFiles("/Gun_13_0_50/743_v1/RECOSIM", "cbern", ".*.root"),
) 

gun_12_0_50 = cfg.Component(
    'gun_12_0_50',
    files = getFiles("/Gun_12_0_50/743_v1/RECOSIM", "cbern", ".*.root"),
) 

guns = [
    gun_22_0_50, 
    gun_11_0_50,
    gun_13_0_50,
    gun_12_0_50,
]
