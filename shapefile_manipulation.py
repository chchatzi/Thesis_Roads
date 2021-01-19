import shapefile
import shapely.wkt
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas

shapefile_name = "polygons_test.shp"
shapefile_name2 = "lines_test.shp"
#shape = shapes[1].points
toronto_polygons = "toronto_test_polygons.shp"
toronto_lines = 'toronto_test_lines.shp'
toronto_allkeys = 'allkeys_toronto.shp'
#Read a shapefile with polygons and right their wkt !
def readpolygons(shapefile_name):
    polygons_test = shapefile.Reader(shapefile_name)
    shapes = polygons_test.shapes()
    allpolygons = []
    for i in range(len(shapes)):
        shape = shapes[i].points
        #st = str(shape)
        p = Polygon(shape)
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


alllines = readlines(shapefile_name2)
allpolygons = readpolygons(shapefile_name)


