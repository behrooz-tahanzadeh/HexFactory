from hexBase import HexBase
import Rhino.Geometry.Point3d as Point3d

class HexShape(HexBase):
    
    def __init__(self, grid, pointer):
        
        self.cornersPt = []
        self.centerPt = None
        
        self.grid = grid
        self.pointer = pointer
        self.corners = []
        self.seq = [[0,0] , [-1,1], [-1,2], [0,3], [1,2], [1,1]]
        
        self.calCorners()
        
        
        if(self.isValid):
            self.calCornersPt()
            self.calCenterPt()
    #eof
    
    
    
    def calCorners(self):
        for s in self.seq:
            i = self.pointer[0] + s[0]
            j = self.pointer[1] + s[1]
            
            if(self.grid.inRange(i,j)):
                self.corners.append([i,j])
        #
        
        return self
    #eof
    
    
    
    def calCornersPt(self):
        
        for c in self.corners:
            pt = self.grid.getPt(c[0], c[1])
            self.cornersPt.append(pt)
        #
        return self
    #eof
    
    
    
    def calCenterPt(self):
        p = []
        
        i = self.pointer[0]
        j = self.pointer[1]+1
        j2 = self.pointer[1]+2
        
        if(self.grid.inRange(i,j)):
            p.append( self.grid.getPt(i,j) )
        
        if(self.grid.inRange(i,j2)):
            p.append( self.grid.getPt(i,j2) )
        
        mp = [0,0,0]
        
        for pt in p:
            mp[0] += pt.X
            mp[1] += pt.Y
            mp[2] += pt.Z
        
        mp[0] /= len(p)
        mp[1] /= len(p)
        mp[2] /= len(p)
        
        self.centerPt = Point3d(mp[0], mp[1], mp[2])
        
        return self
    #eof
    
    
    
    @property
    def isValid(self):
        if (len(self.corners) > 2):
            return True
        
        if (len(self.corners) == 2):
            return self.corners[0][0] != self.corners[1][0]
        
        return False
    #eof
#eoc