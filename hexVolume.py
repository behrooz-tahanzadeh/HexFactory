import rhinoscriptsyntax as rs
from math import fabs
import util




class HexVolume:
    def __init__(self, hexShape, hexProjection, name=0):
        self.hexShape = hexShape
        self.hexProjection = hexProjection
        self.name = name
        self.srfList = []
        self.unrollList = []
        
        
        self.adjustCenterPoints()
        self.make()
    #eof
    
    
    def adjustCenterPoints(self):
        s = self.hexShape.grid.srf
        sp = self.hexProjection.targetSrf
        
        m = self.hexShape.centerPt
        mp = self.hexProjection.centerPt
        
        c = util.getCurvatureOfClosestPoint(m, s)
        cp = util.getCurvatureOfClosestPoint(mp, sp)
        
        m,mp = self.move2PtInside(m, mp, c, cp)
        
        self.hexShape.centerPt = m
        self.hexProjection.centerPt = mp
    #eof
    
    
    
    def make(self):
        group = rs.AddGroup()
        
        if(self.hexShape.length == 6):
            r = range(-1, self.hexShape.length-1)
        else:
            r = range(self.hexShape.length-1)
        
            
        for i in r:
            srf = self.makeTriangleSrf(i)
            unroll = self.makeUnrollPattern(i)
            
            self.srfList.append(srf)
            self.unrollList.append(unroll)
        #
        
        txt = rs.AddTextDot(str(self.name), self.hexProjection.centerPt, )
        
        
        rs.AddObjectsToGroup(txt ,group)
        rs.AddObjectsToGroup(self.srfList ,group)
        rs.AddObjectsToGroup(self.unrollList ,group)
        
        return self
    #eof
    
    
    
    
    def makeUnrollPattern(self, i):
        crvList = []
        
        c0 = self.hexShape.cornersPt[i]
        c1 = self.hexShape.cornersPt[i+1]
        
        
        p0 = self.hexProjection.cornersPt[i]
        p1 = self.hexProjection.cornersPt[i+1]
        
        m = self.hexShape.centerPt
        mp = self.hexProjection.centerPt
        
        tp0,tp1 = self.move2PtInside(c0, p0)
        crvList.append(rs.AddLine(tp0, tp1))
        
        tp0,tp1 = self.move2PtInside(c1, p1)
        crvList.append(rs.AddLine(tp0, tp1))
        
        tp0,tp1 = self.move2PtInside(m, mp)
        crvList.append(rs.AddLine(tp0, tp1))
        
        return crvList
    #eof
    
    
    
    
    def makeTriangleSrf(self, i):
        srfList = []
        
            
        c0 = self.hexShape.cornersPt[i]
        c1 = self.hexShape.cornersPt[i+1]
        
        
        p0 = self.hexProjection.cornersPt[i]
        p1 = self.hexProjection.cornersPt[i+1]
        
        
        m = self.hexShape.centerPt
        mp = self.hexProjection.centerPt
        
        tm, tmp = self.move2PtInside(m, mp)
        
        t = rs.PointAdd(m, (0,0.6,0))
        tp = util.projectPtOnSrf(self.hexProjection.attractorPt, self.hexProjection.targetSrf, t)
        
        t,tp = self.move2PtInside(t, tp, 0.5)
            
        srfList.append(rs.AddSrfPt([t,tm,tmp,tp]))
            
        srfList.append(rs.AddSrfPt([c0,m,mp,p0]))
            
        srfList.append(rs.AddSrfPt([c0,c1,p1,p0]))
            
        srfList.append(rs.AddSrfPt([c1,m,mp,p1]))
            
        vt = rs.VectorCreate(c1, p1)
        
        rs.RotateObject(srfList[3], c1, 2, vt)
        
        return rs.JoinSurfaces(srfList, True)
    #eof
    
    
    
    
    def unroll(self):
        x = 0
        
        for i in range(len(self.srfList)):
            g = rs.AddGroup()
            
            s, p = rs.UnrollSurface(self.srfList[i], False, self.unrollList[i])
            
            s = rs.JoinSurfaces(s, True)
            
            p = rs.MoveObjects(p, [x, self.name*10, 0])
            s = rs.MoveObject(s, [x, self.name*10, 0])
            
            b =rs.DuplicateSurfaceBorder(s, 1)
            
            rs.ObjectLayer(b, "cut");
            
            rs.AddObjectsToGroup(b ,g)
            rs.AddObjectsToGroup(p ,g)
            
            bb = rs.BoundingBox(s)
            x += fabs(bb[0].X - bb[1].X)+1
            
            t = rs.AddText(
                           str(self.name)+"-"+str(i),
                           util.averagePt(rs.CurvePoints(b)),
                           0.3
                           )
            
            t = util.makeEngravingFont(t)
            
            rs.AddObjectsToGroup(t,g)
            
            rs.DeleteObjects(s)
            
    #eof
    
    
    
    
    def move2PtInside(self, p0, p1, scale0=0.2, scale1=None):
        
        if scale1 is None:
            scale1 = scale0
        
        mp =[
             (p0[0]+p1[0])/2,
             (p0[1]+p1[1])/2,
             (p0[2]+p1[2])/2,
             ]
        
        v0 = rs.VectorCreate(mp, p0)
        v1 = rs.VectorCreate(mp, p1)
        
        v0 = rs.VectorScale(rs.VectorUnitize(v0), scale0)
        v1 = rs.VectorScale(rs.VectorUnitize(v1), scale1)
        
        v0 = rs.PointAdd(p0, v0)
        v1 = rs.PointAdd(p1, v1)
        
        return v0,v1
    #eof
#eoc