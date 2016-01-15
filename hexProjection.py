from hexBase import HexBase
import rhinoscriptsyntax as rs
import Rhino.Geometry.Interval as Interval
import Rhino.Geometry.Intersect.Intersection as Intersection




class HexProjection(HexBase):
    
    def __init__(self, hexShape, targetSrf, attractorPt):
        
        self.cornersPt = []
        self.centerPt = None
        
        self.hexShape = hexShape
        self.targetSrf = targetSrf
        self.attractorPt = attractorPt
        
        self.calCornersPt()
        self.calCenterPt()
    #eof
    
    
    
    def calCornersPt(self):
        for pt in self.hexShape.cornersPt:
            p = self.projectPt(pt)
            self.cornersPt.append(p)
            rs.AddPoint(p)
    #eof
    
    
    
    def calCenterPt(self):
        self.centerPt = self.projectPt(self.hexShape.centerPt)
    #eof
    
    
    
    def projectPt(self, pt):
        r = rs.AddLine(self.attractorPt, pt)
        r = rs.ScaleObject(r, self.attractorPt, (10, 10,10))
        
        dom = rs.CurveDomain(r)
        crv = rs.coercecurve(r)
        
        srf = rs.coercesurface(self.targetSrf).ToNurbsSurface()
        inv = Interval(dom[0], dom[1])
        
        rs.DeleteObject(r)
        
        xobj = Intersection.CurveSurface(crv, inv, srf, 0.1, 1)
        
        return xobj[0].PointB
    #eof
    
#eoc