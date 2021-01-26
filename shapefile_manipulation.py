import shapefile
import shapely.wkt
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString
from shapely.geometry import Point
from shapely.validation import explain_validity
import matplotlib.pyplot as plt
import geopandas
from merge_lines_lfnid_toronto import merge_toronto_lines_lfnid

line = "toronto_sample_lines.shp"
polygons = "toronto_sample_polygons.shp"

def readpolygons(shapefile_name):
    polygons_test = shapefile.Reader(shapefile_name)
    shapes = polygons_test.shapes()
    allpolygons = []
    for i in range(len(shapes)):
        shape = shapes[i].points
        #st = str(shape)
        p = Polygon(shape)
        validit = p.is_valid
        if validit == False:
            print(explain_validity(p))
            clean_p = p.buffer(0)
            print(explain_validity(clean_p))
            allpolygons.append(clean_p)
        elif validit == True:
            allpolygons.append(p)

    return allpolygons

def readlines(shapefile_name):
    polygons_test = shapefile.Reader(shapefile_name)
    shapes = polygons_test.shapes()
    alllines = []
    road_id = 0
    for i in range(len(shapes)):
        shape = shapes[i].points
        p = LineString (shape)
        alllines.append([p, road_id])
        road_id+=1
    return alllines

merg_lines = merge_toronto_lines_lfnid(line)
alllines = readlines(merg_lines)
allpolygons = readpolygons(polygons)


