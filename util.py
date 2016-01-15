import rhinoscriptsyntax as rs
import Rhino.Geometry.Interval as Interval
import Rhino.Geometry.Intersect.Intersection as Intersection




def MovePt2PtBasedOnSrf(fromPt, toPt, toSrf):
    
    u,v = rs.SurfaceClosestPoint(toSrf, toPt)
    
    vt = rs.VectorCreate(toPt, fromPt)
    vt = rs.VectorUnitize(vt)
    
    c = rs.SurfaceCurvature(toSrf, (u, v))
    c = c[7]
    
    vt = rs.VectorScale(vt, 10*c)
    
    return rs.PointAdd(toPt, vt)
#eof




def projectPtOnSrf(attractorPt, targetSrf, pt):
    r = rs.AddLine(attractorPt, pt)
    r = rs.ScaleObject(r, attractorPt, (10, 10,10))
    
    dom = rs.CurveDomain(r)
    crv = rs.coercecurve(r)
    
    srf = rs.coercesurface(targetSrf).ToNurbsSurface()
    inv = Interval(dom[0], dom[1])
    
    rs.DeleteObject(r)
    
    xobj = Intersection.CurveSurface(crv, inv, srf, 0.1, 1)
    
    return xobj[0].PointB
#eof


def averagePt(ptList):
    x = 0
    y = 0
    z = 0
    
    for pt in ptList:
        x+= pt.X
        y+= pt.Y
        z+= pt.Z
    
    x /= len(ptList)
    y /= len(ptList)
    z /= len(ptList)
    
    return (x,y,z)
#eof


def makeEngravingFont(txt):
    return rs.ExplodeText(txt, True)
#eof



def getCurvatureOfClosestPoint(pt, srf, scale=None):
    if scale is None:
        global curvatureScale
        scale = curvatureScale
    
    u,v = rs.SurfaceClosestPoint(srf, pt)
    c = rs.SurfaceCurvature(srf, (u, v))
    
    if c is None:
        return 0
    else:
        return c[7]*scale       
#eof

curvatureScale = 15