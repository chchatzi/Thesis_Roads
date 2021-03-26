import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
import geopandas as gpd
import pandas as pd
import shapefile
from shapely.geometry import Polygon
from road_lines_polygons import line, line2,line3,line4,line5,line6, polygons,polygons2,polygons3,polygons4,polygons5,polygons6

#bbox to polygon 'POLYGON(x1 y1, x1 y2, x2 y2, x2 y1, x1 y1)'
def projectnodes(shapefile_polygons):
    
    sf = shapefile.Reader(shapefile_polygons)
    bb = sf.bbox
    poll = Polygon([(bb[0],bb[1]), (bb[0],bb[3]), (bb[2],bb[3]), (bb[2],bb[1]), (bb[0],bb[1])])
    print(poll)

    G = ox.graph_from_polygon(poll, network_type='drive')
    ox.plot_graph(G)
    ox.io.save_graph_shapefile(G,"graph")

    nodes_shapefile = "C:/Users/chcha/Desktop/GEOMATICS/2nd Year/Thesis/p2_technical/code/methodology1/graph/nodes.shp"
    nod = gpd.read_file(nodes_shapefile)
    nod = nod.to_crs("EPSG:4267")
    nod.to_file("projected_nodes_shapefile.shp")
    nod2 = gpd.read_file("projected_nodes_shapefile.shp")

    n_degree3 = nod2[(nod2.street_cou == 3)]
    deg3 = n_degree3.to_file("nodes_degree3.shp")

    n_degree4 = nod2[(nod2.street_cou == 4)]
    deg4 = n_degree4.to_file("nodes_degree4.shp")

    return "nodes_degree3.shp", "nodes_degree4.shp", "C:/Users/chcha/Desktop/GEOMATICS/2nd Year/Thesis/p2_technical/code/methodology1/graph/edges.shp"

