
class Material(object):
    def __init__(self, name, x0, lambdaI):
        self.name = name
        self.x0 = x0
        self.lambdaI = lambdaI

    def path_length(self, ptc):
        '''path before decay within material'''
        freepath = self.material.x0 if ptc.is_em() else self.material.lambdaI
        return np.random.exponential(freepath)

void = Material('void', 0, 0)
