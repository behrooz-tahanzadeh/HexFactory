"""
directions definition:
    v = j*vStep
    u = i*uStep
    
    __ v,j
    
    | u,i
"""
import rhinoscriptsyntax as rs
from math import floor
from __builtin__ import str




class Grid:
    
    def __init__(self, uNum, vNum, srf):
        self.uNum = uNum
        self.vNum = vNum
        self.srf = srf
        
        self.calDomains()
    #eof
    
    
    
    
    def calDomains(self):
        self.uDomain = rs.SurfaceDomain(self.srf, 0)
        self.vDomain = rs.SurfaceDomain(self.srf, 1)
        
        self.uStep = (self.uDomain[1]-self.uDomain[0])/self.uNum
        self.vStep = (self.vDomain[1]-self.vDomain[0])/self.vDivisionAtStep(self.vNum)
    #eof
    
    
    
    
    def vDivisionAtStep(self, num):
        seq = [0,1]
        return (floor(num/2)*3) + seq[num%2]
    #eof
    
    
    
    
    def getUV(self, i, j):
        if(self.inRange(i,j)):
            
            u = (i*self.uStep) + self.uDomain[0]
            v = (self.vStep*self.vDivisionAtStep(j)) + self.vDomain[0]
            
            return u,v
        else:
            return False
    #eof
    
    
    
    
    def inRange(self, i, j):
        return i>=0 and i<=self.uNum and j <= self.vNum and j>=0
    #eof
    
    
    
    
    def getPt(self, i, j):
        u,v = self.getUV(i,j)
        
        return rs.EvaluateSurface(self.srf, u, v)
    #eof
    
    
    
    
    def draw(self):
        for i in range(self.uNum+1):
            for j in range(self.vNum+1):
                pt = self.getPt(i, j)
                
                rs.AddPoint(pt)
                rs.AddText(str(i)+','+str(j), pt, height=0.2)
            #
        #
        return self
    #eof
    
#eoc