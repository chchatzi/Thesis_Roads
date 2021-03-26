import shapefile
import shapely.wkt
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString
from shapely.geometry import Point
from shapely.validation import explain_validity
import matplotlib.pyplot as plt
import geopandas
import os
from merge_lines_lfnid_toronto import merge_toronto_lines_lfnid
from road_lines_polygons import small_h_polygons, polygons_to_dissolve_clean, big_h_polygons, big_p_polygons
from merge_lines_based_osmid import merge_lines_osmid
from recreate_polygons import recreate_int_polygons, list_to_dgf

def delete_files_2():
    os.remove("projected_lines_shapefile.shp")
    os.remove("projected_lines_shapefile.cpg")
    os.remove("projected_lines_shapefile.dbf")
    os.remove("projected_lines_shapefile.prj")
    os.remove("projected_lines_shapefile.shx")
    os.remove("projected_polygons_shapefile.shp")
    os.remove("projected_polygons_shapefile.cpg")
    os.remove("projected_polygons_shapefile.dbf")
    os.remove("projected_polygons_shapefile.prj")
    os.remove("projected_polygons_shapefile.shx")

def readpolygons(shapefile_name, epgs):
    nn = geopandas.read_file(shapefile_name)
    nn = nn.to_crs(epgs)
    nn.to_file("projected_polygons_shapefile.shp")
    polygons_test = shapefile.Reader("projected_polygons_shapefile.shp")
    shapes = polygons_test.shapes()
    allpolygons = []
    for i in range(len(shapes)):
        shape = shapes[i].points
        #st = str(shape)
        p = Polygon(shape)
        validit = p.is_valid
        if validit == False:
            #print(explain_validity(p))
            clean_p = p.buffer(0)
            #print(explain_validity(clean_p))
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

def readnodes(p_nodes):
    nodes = shapefile.Reader(p_nodes)
    shapes = nodes.shapes()
    allnodes = []
    for i in range(len(shapes)):
        shape = shapes[i].points
        p = Point(shape[0][0], shape[0][1])
        allnodes.append(p)
    return allnodes

#read nodes, merge and read lines,  re-create and read polygons
new_roads = recreate_int_polygons(big_h_polygons, "EPSG:3879", 19.5, 25, 35)
p_nodes4 = new_roads[1]
allpoints4 = readnodes(p_nodes4)
edges_shp = new_roads[2]
merg_lines = merge_lines_osmid(edges_shp,"EPSG:3879")
#merg_lines2 = merge_toronto_lines_lfnid(line4)
alllines = readlines(merg_lines)
print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

recreated_polygons = new_roads[0]
allpolygons = readpolygons(recreated_polygons, "EPSG:3879")


delete_files_2()

#for p in allpolygons:
    #print(p)

#for i in allpoints4:
    #print(i)
# Among the list with all the polygons, find those polygons that contain 2 nodes of degree 3
#Dont use that for now! find only intersections based on nodes of degree4
'''
polygons_deg3 = []
for p in allpolygons:
    for pnt in allpoints3:
        if p.contains(pnt):
            polygons_deg3.append(p)

occurrences = [] 
for item in polygons_deg3 :
    count = 0
    for x in polygons_deg3 :
        if x == item :
            count += 1
    occurrences.append(count)


duplicates = []
index = 0
while index < len(polygons_deg3) :
    if occurrences[index] == 2 and occurrences[index] :
        duplicates.append(polygons_deg3[index])
    index += 1'''

# Among the list with all the polygons, find those polygons that contain at least 1 node of degree 4
polygons_deg4 = []
for pp in allpolygons:
    for pntt in allpoints4:
        if pntt.within(pp):
            polygons_deg4.append(pp)

#check results (all polygons of sample area, the double t intersections polygons and the cross intersection polygons)

#for pp in allpolygons:
    #print(pp)
#print("1")
#for p in duplicates:
    #print(p)
#print("2")
#for poll in polygons_deg4:
    #print(poll)
#print("3")
#the dt and cross polygons make them tuple in the whole allpolygons list
'''
for polyg in allpolygons:
    for pl in duplicates:
        if polyg == pl and polyg in allpolygons:
            allpolygons.remove(polyg)
            allpolygons.append([polyg,"dt"])'''

for p in allpolygons:
    for pp in polygons_deg4:
        if type(p) == list:
            continue
        else:
            if p == pp and p in allpolygons: 
                allpolygons.remove(p)
                allpolygons.append([p,"cross"])
'''
for check in allpolygons:
    if type(check) == list:
        print(check[0])
    else:
        print(check)'''
cross_polygons = []
for p in allpolygons:
    if type(p) == list:
        cross_polygons.append(p[0])

df_cross = list_to_dgf(cross_polygons,"EPSG:32617")
df_cross.to_file("cross_polygons.shp")