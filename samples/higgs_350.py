import heppy.framework.config as cfg

from getFiles import getFiles 


wwh = cfg.Component(
    'wwh',
    files = getFiles("/WWH/HZHA_100k_v1/GEN"),
) 



samples = [
    wwh,
]

if __name__ == '__main__':

    import pprint 
    for g in samples:
        print g
