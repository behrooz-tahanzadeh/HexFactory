from rhinoscriptsyntax import AddPolyline

class HexBase:
    
    def __init__(self, centerPt=None, cornersPt=[]):
        self.centerPt = centerPt
        self.cornersPt = cornersPt
    #eof
    
    
    
    @property
    def isCloseable(self):
        return len(self.cornersPt)>2
    #eof
    
    
    
    @property
    def length(self):
        return len(self.cornersPt)
    
    
    
    def draw(self):
        ptList = self.cornersPt[:]
        
        if not self.isCloseable:
            ptList.append(self.centerPt)
        
        ptList.append(self.cornersPt[0])    
        
        AddPolyline(ptList)
    #eof
    
#eoc