import heppy.framework.config as cfg

from getFiles import getFiles 

gun_211_0_50 = cfg.Component(
    'gun_211_0_50',
    files = getFiles("/Gun_211_0_50/743_v1/RECOSIM"),
) 

gun_22_0_50 = cfg.Component(
    'gun_22_0_50',
    files = getFiles("/Gun_22_0_50/743_v1/RECOSIM"),
) 

gun_11_0_50 = cfg.Component(
    'gun_11_0_50',
    files = getFiles("/Gun_11_0_50/743_v1/RECOSIM"),
) 

gun_13_0_50 = cfg.Component(
    'gun_13_0_50',
    files = getFiles("/Gun_13_0_50/743_v1/RECOSIM"),
) 

gun_12_0_50 = cfg.Component(
    'gun_12_0_50',
    files = getFiles("/Gun_12_0_50/743_v1/RECOSIM"),
) 

samples = [
    gun_22_0_50, 
    gun_11_0_50,
    gun_13_0_50,
    gun_12_0_50,
]

if __name__ == '__main__':

    import pprint 
    for g in samples:
        print g
