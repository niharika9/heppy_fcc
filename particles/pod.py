import copy

class POD(object):
    '''Extends the cmg::PhysicsObject functionalities.'''

    def __init__(self, handle):
        self.handle = handle
        super(POD, self).__init__()

    def __copy__(self):
        '''Very dirty trick, the handle is deepcopied...'''
        handle = copy.deepcopy( self.handle )
        newone = type(self)(handle)
        newone.__dict__.update(self.__dict__)
        newone.handle = handle
        return newone        
        
    def __getattr__(self,name):
        '''all accessors  from cmg::DiTau are transferred to this class.'''
        return getattr(self.handle, name)

    def __eq__(self,other):
        if( hasattr(other, 'handle') ):
            # the two python PODs have the same C++ POD
            return self.handle == other.handle
        else:
            # can compare a python POD with a cpp POD directly
            return self.handle == other 

