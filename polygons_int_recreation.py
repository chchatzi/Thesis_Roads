import networkx as nx
import matplotlib as plt
import osmnx as ox
import geopandas as gpd
import pandas as pd
import math
from shapely.geometry import Polygon,MultiPolygon,LineString
from shapely.ops import unary_union
from shapely.ops import split
from shapely.geometry import box
from shapely.validation import explain_validity
from shapely.geos import TopologicalError
from road_lines_polygons import small_h_polygons, big_h_polygons, polygons_to_dissolve, big_p_polygons
import os

''' This file recreates the road polygons of an area. Starting by some given road polygons for some area, we download the graph (nodes and edges).
Then based on the intersection nodes we recreate the shape of those polygons in order to model the intersections separetly.
We dissolve the initial road polygons to a Multipolygon, then we create a buffer around each node and we find the intersection of this buffer with the dissolved polygon
this creates new polygons.

2 things need to change for the different datasets. 1) The EPSG line 57,136,169 +  2) The distance of the buffers around the intersection nodes!'''
def makeoffsets(line, dist):
    leftline = line.parallel_offset(dist, 'left')
    rightline = line.parallel_offset(dist, 'right')
    #print(leftline)
    #print(rightline)
    #we find the 2 midpoints of the 2 offset lines in order to connect them and create the prependicular line segment
    midpointleft = leftline.interpolate(0.5, normalized = True)
    midpointright = rightline.interpolate(0.5, normalized = True)
    #print(midpointleft)
    #print(midpointright)
    prependicular_line = LineString([midpointleft, midpointright])
    #print(prependicular_line)
    prep_line = prependicular_line
    return prep_line

def recreate_int_polygons(shapefile_polygons, epgs, bufr):
    #read a polygons file, create a new field same for all entries and dissolve everything to a big Multipolygon
    #save the dissolved Multipoligon to a new shp file
    p = gpd.read_file(shapefile_polygons)
    p['d_field'] = 1
    p_new = p.dissolve(by='d_field')
    p_new.to_file("diss_polygons.shp")

    #Before generate a graph with osmnx we need to project shapefile to wgs84 lat lon!! Later we ll project the generated nodes to the CRS of the specific shapefile
    nn = gpd.read_file("diss_polygons.shp")
    print(nn.crs)
    nn = nn.to_crs("EPSG:4326")
    nn.to_file("wgs84_dissolved_polygons.shp")

    d_polygons = gpd.read_file("wgs84_dissolved_polygons.shp")
    pl = d_polygons.loc[0,'geometry']
    print(pl.bounds)
    b = box(pl.bounds[0],pl.bounds[1],pl.bounds[2],pl.bounds[3])
    print(b)

    #Generate the graph WGS84
    G = ox.graph_from_polygon(b, network_type='drive')
    #ox.plot_graph(G)
    ox.io.save_graph_shapefile(G,"graph")

    nodes_shapefile = "C:/Users/chcha/Desktop/GEOMATICS/2nd Year/Thesis/p2_technical/code/methodology1/graph/nodes.shp"
    nod = gpd.read_file(nodes_shapefile)

    deg_higher_3 = nod[(nod.street_cou > 2)]
    deg3 = deg_higher_3.to_file("int_nodes.shp")

    #open the intersection nodes file and create a buffer for each node
    #int_nodes is projected at WGS84 --> Change to correspondig crs
    df_multipolygon = gpd.read_file("diss_polygons.shp")
    df_nodes = gpd.read_file("int_nodes.shp")
    df_nodes = df_nodes.to_crs(epgs)
    df_nodes.to_file("int_nodes_projected.shp")
    df_final_nodes = gpd.read_file("int_nodes_projected.shp")
    #find the projected nodes with degree higher than 3 and write it to a new file. Do that in order to use it for cross intersection identification
    nodes_degree_4 = df_final_nodes[(df_final_nodes.street_cou > 3)]
    nodes_degree_4.to_file("nodes_degree_4_projected.shp")
    print(df_final_nodes.crs)
    print(df_multipolygon.crs)
    all_polygons = df_multipolygon.loc[0,'geometry']
    v = all_polygons.is_valid
    print(v)
    if v == False:
        print(explain_validity(all_polygons))
        all_polygons = all_polygons.buffer(0)
        print(explain_validity(all_polygons))

    print("This is the len of all nodes with degree > 2: ", len(df_final_nodes))

    #exclude all the nodes that belong to motorway, by using nodes attribute highway
    for i in range(len(df_final_nodes)-1):
        if df_final_nodes.loc[i,'highway'] == "motorway_junction":
            print(df_final_nodes.loc[i,'geometry'])
            df_final_nodes = df_final_nodes.drop(i)
    
    print("This is len after removing all the nodes with attribute = Motorway: ", len(df_final_nodes))
    df_final_nodes.to_file("gamimeno.shp")
    upd_nodes = gpd.read_file("gamimeno.shp")

    #exclude the nodes that are touched only by motorways or trunks!
    #exclude the nods that are touched by 2 or less edges!
    edges_shapefile = "C:/Users/chcha/Desktop/GEOMATICS/2nd Year/Thesis/p2_technical/code/methodology1/graph/edges.shp"
    ed = gpd.read_file(edges_shapefile)
    ed = ed.to_crs(epgs)
    ed.to_file("edges_projected.shp")
    edges_projected = gpd.read_file("edges_projected.shp")
    
    l = dict()
    for i in range(len(upd_nodes)-1):
        rec = upd_nodes.loc[i]
        rec_geom = rec['geometry']
        l[i] = []
        for ii in range(len(edges_projected)):
            ed = edges_projected.loc[ii]
            ed_geom = ed['geometry']
            ed_high = ed['highway']
            if ed_geom.touches(rec_geom):
                l[i].append(ed_high)
    keys = []     
    for j in l:
        notkeys = []
        if len(l[j]) < 3:
            #print(j)
            #print(upd_nodes.loc[j,'geometry'])
            keys.append(j)
        for v in l[j]:
            if v != "motorway" and v!= 'motorway_link' and v!= 'trunk' and v != "trunk_link":
                notkeys.append(j)
        if len(notkeys) == 0 and j not in keys:
            #print(j)
            #print(upd_nodes.loc[j,'geometry'])
            keys.append(j)
    
    for k in keys:
        print(upd_nodes.loc[k,'geometry'])
        upd_nodes = upd_nodes.drop(k)
        
    print("this is after removing moterway points based on edges attributes: ", len(upd_nodes))

    upd_nodes.to_file("gamimeno2.shp")
    nods_nomotorways = gpd.read_file("gamimeno2.shp")
    #print(nods_nomotorways)
    #exclude all the nodes that are coorespond to roundabouts --> to treat the differently!
    
    round_edges = edges_projected[(edges_projected.junction == "roundabout")]
    r = round_edges.reset_index(drop=True)

    #print(nods_nomotorways)
    nodes_roundabout = []
    for nd in range(len(nods_nomotorways)-1):
        rec = nods_nomotorways.loc[nd]
        rec_geom = rec['geometry']
        for ln in range(len(r)-1):
            ed = r.loc[ln]
            ed_geom = ed['geometry']
            if ed_geom.touches(rec_geom):
                #print(nods_nomotorways.loc[nd,'geometry'])
                nodes_roundabout.append(nods_nomotorways.loc[nd,'geometry'])
                nods_nomotorways = nods_nomotorways.drop(nd)
                break

    for i in nodes_roundabout:
        print(i)
    print("this is len after removing the roundabout nodes: ", len(nods_nomotorways))
    final_nodes = nods_nomotorways.reset_index(drop=True)
    print("those are all the small buffers")

    #first create a small buffer for each node in order to find the nodes that are close together (in the same polygon or really close)
    buffers_small = []
    for i in range(len(final_nodes)-1):
        geomm = final_nodes.loc[i,'geometry']
        bf = geomm.buffer(bufr/2-1)
        #print(bf)
        buffers_small.append([bf,geomm])
    #find which nodes are intersecting with the initial dissolved polygon and keep only them
    bufs = []
    only_nodes2 = []
    for b in buffers_small:
        if b[0].intersects(all_polygons):
            bufs.append(b)
            only_nodes2.append(b[1])

    #based on if the small buffers are intersecting find the nodes that are close together (remove them from only_nodes2 list)
    only_buffers = []
    only_nodes = []
    for bb in bufs:
        for bbb in bufs:
            if bb[0]!=bbb[0] and bb[0].intersects(bbb[0]):
                only_nodes.append(bb[1])
                only_buffers.append(bb[0])
                if bb[1] in only_nodes2:
                    only_nodes2.remove(bb[1])
    #make a union of buffers of the nodes that are close together, and find the centroid of this union buffer
    op = []
    for i in only_nodes:
        test = []
        s = i.buffer(bufr)
        for b in only_buffers:
            if s.intersects(b):
                test.append(b)
        cu = unary_union(test)
        if cu not in op:
            op.append(cu)

    opop = []
    for mult in op:
        cent = mult.centroid
        opop.append(cent)
    print("those are the multibuffers")
    #for i in op:
        #print(i)
    #all_pnts is a list which contains all the unique (isolate) nodes from the only_nodes2 list (the nodes that are not too close with other nodes) +
    #+ the centroids of the union buffer of the nodes that are close together
    all_pnts = []
    for i in only_nodes2:
        all_pnts.append(i)

    for ii in opop:
        all_pnts.append(ii)

    print("those are all the final points")
    #for i in all_pnts:
        #print(i)
    print("we have all nodes for intersection polygons")
    #int_polygons a list that contains all the intersection polygons (based on the intersection of the buffer with the initial dissolved layer of road polygons)
    int_polygons = []
    for i in all_pnts:
        #print(i)
        bfr = i.buffer(bufr)
        #print(bfr)
        check = bfr.intersection(all_polygons)
        c = check.simplify(0.005, preserve_topology=False)
        int_polygons.append(c)

    #dissolve the separate intersection polygons to one Multipolygon(use it later to find the symmetric difference with the dissolced intial polygon)
    cu2 = unary_union(int_polygons)
    print(cu2.geom_type)
    if cu2.geom_type == "GeometryCollection":
        aou = []
        for ii in cu2:
            if ii.geom_type == "Polygon" or ii.geom_type == "MultiPolygon":
                aou.append(ii)
        cu2 = unary_union(aou)

    print("this is all the dissolved intersection polygons")
    print(cu2)
    print("opa")

    #Split big intersection polygons into smaller polygons
    for p in cu2:
        nn = []
        for i in all_pnts:
            if p.contains(i):
                nn.append(i)
        if len(nn) == 2: 
            print("this polygon contains 2 nodes: ", p)
            dd = nn[0].distance(nn[1])
            print("this is distance between nodes: ", dd)
            if dd > 29:
                ln = LineString([nn[0], nn[1]])
                print(ln)
                prep_line = makeoffsets(ln,40)
                print(prep_line)
                result = split(p,prep_line)
                #print(result2)
                print(result[0])
                print(result[1])
                print(len(result))
            else:
                print("the 2 nodes are quite close together so i do not split")

        if len(nn) == 3:
            # check if the points are not lie in almost the same line: (we dont split intersections of type y (or similar type))
            print("this polygon contains 3 nodes CHECK CHEKC CHECK: ", p)
            myradians1 = math.atan2(nn[1].y-nn[0].y, nn[1].x - nn[0].x)
            mydegrees1 = math.degrees(myradians1)

            myradians2 = math.atan2(nn[2].y-nn[0].y, nn[2].x-nn[0].x)
            mydegrees2 = math.degrees(myradians2)
            print(mydegrees1, "Degrees", mydegrees2)

            if mydegrees1 > 30 or mydegrees2 >30:
                print("propably y or similar intersection, not split")
            else:
                d1 = nn[0].distance(nn[1])
                d2 = nn[0].distance(nn[2])
                if d2<d1:
                    ln = LineString([nn[0], nn[2]])
                    print(ln)
                    #line to split polygon
                    prep_line = makeoffsets(ln,40)
                    print(prep_line)
                    result = split(p,prep_line)
                    #print(result)
                    print(result[0])
                    print(result[1])
                    print(len(result))
                    a1 = result[0].area
                    a2 = result[1].area
                    print(a1, " Areas ", a2)
                    if a1 > a2:
                        print(result[0])
                        neww = []
                        for rec in nn:
                            if result[0].contains(rec):
                                neww.append(rec) 
                        print("this is len of new polygon with 2 from 3 nodes: ", len(neww)) 
                        new_ln = LineString([neww[0], neww[1]])
                        print(new_ln)
                        #line to split polygon
                        new_prep_line = makeoffsets(new_ln,40)
                        print(new_prep_line)
                        new_result = split(result[0],new_prep_line)
                        print(new_result)
                        print(new_result[0])
                        print(new_result[1])
                        print(len(new_result))
                        if len(new_result) > 2:
                            areas = []
                            for jh in new_result:
                                if jh.geom_type == 'Polygon'

                    else:
                        print("a2 is bigger than a1")
                        neww = []
                        for rec in nn:
                            if result[1].contains(rec):
                                neww.append(rec)
                        print("this is len of new polygon with 2 from 3 nodes: ", len(neww)) 
                        new_ln = LineString([neww[0], neww[1]])
                        print(new_ln)
                        #line to split polygon
                        new_prep_line = makeoffsets(new_ln,40)
                        print(new_prep_line)
                        new_result = split(result[1],new_prep_line)
                        #print(result)
                        print(new_result[0])
                        print(new_result[1])
                        print(len(new_result))
                else:
                    ln = LineString([nn[0], nn[1]])
                    print(ln)
                    prep_line = makeoffsets(ln,50)
                    print(prep_line)
                    result = split(p,prep_line)
                    #print(result2)
                    print(result[0])
                    print(result[1])
                    print(len(result))
                    a1 = result[0].area
                    a2 = result[1].area
                    print(a1, " Areas ", a2)
                    if a1 > a2:
                        neww = []
                        for rec in nn:
                            if result[0].contains(rec):
                                neww.append(rec) 
                        print("this is len of new polygon with 2 from 3 nodes: ", len(neww)) 
                        new_ln = LineString([neww[0], neww[1]])
                        print(new_ln)
                        #line to split polygon
                        new_prep_line = makeoffsets(new_ln,40)
                        print(new_prep_line)
                        new_result = split(result[0],new_prep_line)
                        #print(result)
                        print(new_result[0])
                        print(new_result[1])
                        print(len(new_result))
                    else:
                        neww = []
                        for rec in nn:
                            if result[1].contains(rec):
                                neww.append(rec)
                        print("this is len of new polygon with 2 from 3 nodes: ", len(neww)) 
                        new_ln = LineString([neww[0], neww[1]])
                        print(new_ln)
                        #line to split polygon
                        new_prep_line = makeoffsets(new_ln,40)
                        print(new_prep_line)
                        new_result = split(result[1],new_prep_line)
                        #print(result)
                        print(new_result[0])
                        print(new_result[1])
                        print(len(new_result))
        
        if len(nn) > 3:
            print("this polygon has more 4 or even more final nodes CHECK CHECK CHECK: ", p)

    #create a file with all the intersection polygons
    d = {'geometry':[]}
    for p in cu2:
        #print(p)
        d['geometry'].append(p)

    gdf = gpd.GeoDataFrame(d, crs = epgs)
    gdf.to_file("intersection_polygons.shp")
    print("intersection polygons are written to a file")


    cu22 = cu2.buffer(0.001)
    all_polygons2 = all_polygons.buffer(0.001)
    #r = cu2.symmetric_difference(all_polygons)
    #rr = list(r)
    rest_polygons_multi = cu22.symmetric_difference(all_polygons2)
    rest_polygons = list(rest_polygons_multi)
    print("check")
    #print(r)

    new_road_polygons = []
    for i in int_polygons:
        #print(i.geom_type)
        if i.geom_type == "GeometryCollection": 
            print(i)
            n = []
            for ii in i:
                print(ii.geom_type)
                if ii.geom_type == "Polygon" or ii.geom_type == "MultiPolygon":
                    print(ii)
                    n.append(ii)
            un = unary_union(n)
            new_road_polygons.append(un)

        else:
            new_road_polygons.append(i)

    for ii in rest_polygons:
        new_road_polygons.append(ii)


    dd = {'geometry':[]}
    for p in new_road_polygons:
        dd['geometry'].append(p)

    gddf = gpd.GeoDataFrame(dd, crs= epgs)
    gddf.to_file("new_road_polygons.shp")
    #os.remove("demofile.txt")
    return "new_road_polygons.shp", "nodes_degree_4_projected.shp", "C:/Users/chcha/Desktop/GEOMATICS/2nd Year/Thesis/p2_technical/code/methodology1/graph/edges.shp"

a = recreate_int_polygons(polygons_to_dissolve, "EPSG:32617", 24)[0]
#Poznan --> Smaller buffer for intersection polygons compare with Helsinki. A good value around 20-22
#Poznan --> Smaller buffer for merging the nodes that are close together. A good value around 10
#Helsinki --> a good buffer value 18-20
#Toronto --> a good buffer value around 23-25