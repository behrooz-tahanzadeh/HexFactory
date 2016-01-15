from hexShape import HexShape
from hexProjection import HexProjection
from hexVolume import HexVolume




class HexFactory:
    
    def __init__(self, grid, projSrf, attractorPt):
        self.pointer = [0, -2]
        self.grid = grid
        self.projSrf = projSrf
        self.attractorPt = attractorPt
        
        self.hexShapeList = []
        self.hexProjectionList = []
        self.hexVolumeList = []
        
        self.calHexShapes()
        self.calHexProjections()
        self.calHexVolumes()
    #eof
    
    
    
    
    def calHexShapes(self):
        
        e = HexShape(self.grid, self.pointer)
        
        jOffset = 1
        invalidScore = 0
        
        while(invalidScore < 2):
            while(e.isValid):
                invalidScore = 0
                self.hexShapeList.append(e)
                self.pointer[1]+=4
                e = HexShape(self.grid, self.pointer)
            #
            invalidScore += 1
            
            self.pointer[0] += 1
            
            jOffset = (jOffset+1)%2
            self.pointer[1] = -2 * jOffset
            
            e = HexShape(self.grid, self.pointer)
        #
        
        return self
    #eof
    
    
    
    
    def calHexProjections(self):
        
        for s in self.hexShapeList:
            p = HexProjection(s, self.projSrf, self.attractorPt)
            self.hexProjectionList.append(p)
            
        return self
    #eof
    
    
    
    
    def calHexVolumes(self):
        
        for i in range(len(self.hexShapeList)):
            s = self.hexShapeList[i]
            p = self.hexProjectionList[i]
            
            v = HexVolume(s, p, i)
            self.hexVolumeList.append(v)
            
            v.unroll()
        #
        
        return self
    #eof
    
#eoc