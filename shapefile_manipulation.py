import shapefile
import shapely.wkt
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString
from shapely.geometry import Point



shapefile_name = "polygons_test.shp"
shapefile_name2 = "lines_test.shp"
#shape = shapes[1].points
toronto_polygons = "toronto_test_polygon.shp"
toronto_lines = 'toronto_test_lines.shp'
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
    for i in range(len(shapes)):
        shape = shapes[i].points
        p = LineString (shape)
        alllines.append(p)

    return alllines


alllines = readlines(shapefile_name2)
bigcenterline = alllines[-1]
allpolygons = readpolygons(shapefile_name)


