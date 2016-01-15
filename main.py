import rhinoscriptsyntax as rs
from grid import Grid
from hexFactory import HexFactory
import util




rs.EnableRedraw(False)


util.curvatureScale = -15

attractorPt = rs.AddPoint(0, 0, 0)
baseSrf = rs.GetSurfaceObject("Base Surface")[0]


projSrf = rs.GetSurfaceObject("Proj. Surface")[0]
gridObj = Grid(10,10 , baseSrf)
factory = HexFactory(gridObj, projSrf, attractorPt)