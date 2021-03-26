import networkx as nx
import matplotlib as plt
import osmnx as ox
import geopandas as gpd
import pandas as pd
import math
from shapely.geometry import Polygon,MultiPolygon,LineString, Point
from shapely.ops import unary_union
from shapely.ops import split
from shapely.geometry import box
from shapely.validation import explain_validity
from shapely.geos import TopologicalError
from road_lines_polygons import small_h_polygons, big_h_polygons, polygons_to_dissolve, big_p_polygons, polygons_to_dissolve_clean
import os

''' This file recreates the road polygons of an area. Starting by some given road polygons for some area, we download the graph (nodes and edges).
Then based on the intersection nodes we recreate the shape of those polygons in order to model the intersections separetly.
We dissolve the initial road polygons to a Multipolygon, then we create a buffer around each node and we find the intersection of this buffer with the dissolved polygon
this creates new polygons.

2 things need to be definde for the different datasets. 1) The EPSG   2) The size of the buffers around the intersection nodes
+
other values to define per dataset: 1) Distance tolerance for spliting big intersection polygons, 2)buffer (or not) to exclude non road polygons, 3)Area of small polygons to be merged'''

def list_to_dgf(listt,epgs):
    d = {'geometry':[]}
    for pp in listt:
        d['geometry'].append(pp)

    gdf = gpd.GeoDataFrame(d, crs = epgs)
    return gdf

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

def centroid_from_pntlist(pnt_list):
    x = 0.0
    y = 0.0
    for pnt in pnt_list:
        x += pnt.x
        y += pnt.y
    centx = x/len(pnt_list)
    centy = y/len(pnt_list)
    cent = Point(centx,centy)
    return cent

def splitintpolygons(all_pnts,cu2, v1):
    print("Start spliting big intersectio polygons into smaller parts!!!")
    final_int_pols = []
    for p in cu2:
        nn = []
        for i in all_pnts:
            if p.contains(i):
                nn.append(i)
        if len(nn) == 0 or len(nn) == 1:
            final_int_pols.append(p)
        if len(nn) == 2: 
            #print("this polygon contains 2 nodes: ", p)
            dd = nn[0].distance(nn[1])
            #print("this is distance between nodes: ", dd)
            if dd > v1:
                ln = LineString([nn[0], nn[1]])
                #print(ln)
                prep_line = makeoffsets(ln,40)
                #print(prep_line)
                result = split(p,prep_line)
                #print(result[0])
                #print(result[1])
                #print(len(result))
                if len(result) > 2:
                    for rr in result:
                        if rr.area > 15:
                            final_int_pols.append(rr)
                else:
                    final_int_pols.append(result[0])
                    final_int_pols.append(result[1])
            else:
                final_int_pols.append(p)
                #print("the 2 nodes are quite close together so i do not split")
        
        if len(nn) == 3:
            # check if the points are not lie in almost the same line: (we dont split intersections of type y (or similar type))
            #print("this polygon contains 3 nodes CHECK CHEKC CHECK: ", p)
            myradians1 = math.atan2(nn[1].y-nn[0].y, nn[1].x - nn[0].x)
            mydegrees1 = math.degrees(myradians1)

            myradians2 = math.atan2(nn[2].y-nn[0].y, nn[2].x-nn[0].x)
            mydegrees2 = math.degrees(myradians2)
            #print(mydegrees1, "Degrees", mydegrees2)

            if mydegrees1 > 30 or mydegrees2 >30:
                #print("propably y or similar intersection, not split")
                final_int_pols.append(p)
            else:
                d1 = nn[0].distance(nn[1])
                d2 = nn[0].distance(nn[2])
                if d2<d1:
                    ln = LineString([nn[0], nn[2]])
                    #print(ln)
                    prep_line = makeoffsets(ln,40)
                    #print(prep_line)
                    result = split(p,prep_line)
                    #print(result[0])
                    #print(result[1])
                    #print(len(result))
                    a1 = result[0].area
                    a2 = result[1].area
                    #print(a1, " Areas ", a2)
                    if a1 > a2:
                        neww = []
                        for rec in nn:
                            if result[0].contains(rec):
                                neww.append(rec) 
                        #print("this is len of new polygon with 2 from 3 nodes: ", len(neww)) 
                        new_ln = LineString([neww[0], neww[1]])
                        #print(new_ln)
                        new_prep_line = makeoffsets(new_ln,40)
                        #print(new_prep_line)
                        new_result = split(result[0],new_prep_line)
                        #print(new_result)
                        #print(new_result[0])
                        #print(new_result[1])
                        #print(len(new_result))
                        if len(new_result) > 2:
                            #print("WEIRD")
                            final_int_pols.append(result[1])
                            for jh in new_result:
                                if jh.geom_type == "Polygon":
                                    #print(jh)
                                    #print(jh.area) 
                                    if jh.area > 20:
                                        final_int_pols.append(jh)
        
                        else:
                            final_int_pols.append(result[1])
                            final_int_pols.append(new_result[0])
                            final_int_pols.append(new_result[1])

                    else:
                        neww = []
                        for rec in nn:
                            if result[1].contains(rec):
                                neww.append(rec)
                        #print("this is len of new polygon with 2 from 3 nodes: ", len(neww)) 
                        new_ln = LineString([neww[0], neww[1]])
                        #print(new_ln)
                        new_prep_line = makeoffsets(new_ln,40)
                        #print(new_prep_line)
                        new_result = split(result[1],new_prep_line)
                        #print(new_result[0])
                        #print(new_result[1])
                        #print(len(new_result))
                        if len(new_result) > 2:
                            final_int_pols.append(result[0])
                            #print("WEIRD")
                            for jh in new_result:
                                if jh.geom_type == "Polygon":
                                    #print(jh)
                                    #print(jh.area)
                                    if jh.area > 20:
                                        final_int_pols.append(jh)         
                        else:
                            final_int_pols.append(result[0])
                            final_int_pols.append(new_result[0])
                            final_int_pols.append(new_result[1])
                else:
                    ln = LineString([nn[0], nn[1]])
                    #print(ln)
                    prep_line = makeoffsets(ln,50)
                    #print(prep_line)
                    result = split(p,prep_line)
                    #print(result[0])
                    #print(result[1])
                    #print(len(result))
                    a1 = result[0].area
                    a2 = result[1].area
                    #print(a1, " Areas ", a2)
                    if a1 > a2:
                        neww = []
                        for rec in nn:
                            if result[0].contains(rec):
                                neww.append(rec) 
                        #print("this is len of new polygon with 2 from 3 nodes: ", len(neww)) 
                        new_ln = LineString([neww[0], neww[1]])
                        #print(new_ln)
                        new_prep_line = makeoffsets(new_ln,40)
                        #print(new_prep_line)
                        new_result = split(result[0],new_prep_line)
                        #print(new_result[0])
                        #print(new_result[1])
                        #print(len(new_result))
                        if len(new_result) > 2:
                            #print("WEIRD")
                            final_int_pols.append(result[1])
                            for jh in new_result:
                                if jh.geom_type == "Polygon":
                                    #print(jh)
                                    #print(jh.area)
                                    if jh.area > 20:
                                        final_int_pols.append(jh)         
                        else:
                            final_int_pols.append(result[1])
                            final_int_pols.append(new_result[0])
                            final_int_pols.append(new_result[1])
                    else:
                        neww = []
                        for rec in nn:
                            if result[1].contains(rec):
                                neww.append(rec)
                        #print("this is len of new polygon with 2 from 3 nodes: ", len(neww)) 
                        new_ln = LineString([neww[0], neww[1]])
                        #print(new_ln)
                        new_prep_line = makeoffsets(new_ln,40)
                        #print(new_prep_line)
                        new_result = split(result[1],new_prep_line)
                        #print(new_result[0])
                        #print(new_result[1])
                        #print(len(new_result))
                        if len(new_result) > 2:
                            final_int_pols.append(result[0])
                            #print("WEIRD")
                            for jh in new_result:
                                if jh.geom_type == "Polygon":
                                    #print(jh)
                                    #print(jh.area)
                                    if jh.area > 20:
                                        final_int_pols.append(jh)         
                        else:
                            final_int_pols.append(result[0])
                            final_int_pols.append(new_result[0])
                            final_int_pols.append(new_result[1])
        
        if len(nn) > 3:
            #print("this polygon has more 4 or even more final nodes CHECK CHECK CHECK: ", p)
            final_int_pols.append(p)
            #x = 0.0
            #y = 0.0
            #for pnt in nn:
                #x += pnt.x
                #y += pnt.y
            #centx = x/len(nn)
            #centy = y/len(nn)
            #cent = Point(centx,centy)
    return final_int_pols

def remove_motor_nodes(df_final_nodes, epgs, edges_projected):
    l = dict()
    for i in range(len(df_final_nodes)):
        l[i] = []
        nod = df_final_nodes.loc[i, 'geometry']
        aa = edges_projected.sindex.query(nod,  predicate="touches")
        if len(aa) > 0:
            for edg_ind in aa:
                eee = edges_projected.loc[edg_ind,'highway']
                #print(eee)
                l[i].append(eee)
    keys = []     
    for j in l:
        notkeys = []
        if len(l[j]) < 3:
            keys.append(j)
        for v in l[j]:
            if v != "motorway" and v!= 'motorway_link' and v!= 'trunk' and v != "trunk_link":
                notkeys.append(j)
        if len(notkeys) == 0 and j not in keys:
            keys.append(j)
    
    for k in keys:
        #print(df_final_nodes.loc[k,'geometry'])
        df_final_nodes = df_final_nodes.drop(k)  
    
    print("this is the number of nodes after removing moterway nodes (based on edges attributes): ", len(df_final_nodes))

    df_final_nodes.to_file("gamimeno.shp")
    nods_nomotorways = gpd.read_file("gamimeno.shp")
    return nods_nomotorways

def handle_roundabouts(nodes_roundabout, bufr, epgs):
    t = []
    check = []
    for i in nodes_roundabout:
        if i not in check:
            rounds = []
            rounds.append(i)
            b = i.buffer(bufr*2.5)
            for ii in nodes_roundabout:
                if ii!= i and b.contains(ii):
                    check.append(ii)
                    rounds.append(ii)
            t.append(rounds)
    bs = []
    for tt in t:
        c = centroid_from_pntlist(tt)
        print("this is centroid of roundabout")
        print(c)
        gg = c.buffer(bufr+(bufr/2))
        bs.append(gg)
    
    bs_gdf = list_to_dgf(bs,epgs)
    return bs_gdf

def mergesmallpolygons_withneighbours(new_road1,epgs,v2):
    small = []
    okeis = []
    for polyg in new_road1:
        if polyg.area < v2:
            small.append(polyg)
        else:
            okeis.append(polyg)

    dd = {'geometry':[]}
    for ax in okeis:
        dd['geometry'].append(ax)
    test1 = gpd.GeoDataFrame(dd, crs= epgs)
    
    big_polygons_alreadymerged = []
    for i in small:
        #print(i)
        #print(i.area)
        aa = test1.sindex.query(i)
        #print(len(aa))
        if len(aa)>0:
            pll = test1.loc[aa[0], 'geometry']
            #print(pll)
            if (pll not in big_polygons_alreadymerged):
                big_polygons_alreadymerged.append(pll)
                okeis.remove(pll)    
                #new_dissolved_multipolygon = MultiPolygon([pll,i])
                n = unary_union([pll,i])
                #print(n)
                #print(new_dissolved_multipolygon)
                okeis.append(n)

            elif (pll in big_polygons_alreadymerged) and len(aa)>1:
                pll1 = test1.loc[aa[1], 'geometry']
                if pll1 not in big_polygons_alreadymerged:
                    big_polygons_alreadymerged.append(pll1)
                    okeis.remove(pll1)    
                    #new_dissolved_multipolygon = MultiPolygon([pll1,i])
                    n = unary_union([pll1,i])
                    #print(n)
                    #print(new_dissolved_multipolygon)
                    okeis.append(n)

                elif (pll1 in big_polygons_alreadymerged):
                    #leave the small polygon (i) as it is to the final dataset in order to avoid overlapping multipolygons
                    #print("not merged we add the small polygon")
                    #print(i)
                    okeis.append(i)
                    continue

            elif (pll in big_polygons_alreadymerged) and len(aa) == 1:
                #leave the small polygon (i) as it is to the final dataset in order to avoid overlapping multipolygons
                #print("not merged we add the small polygon")
                #print(i)
                okeis.append(i)
                continue   
        else:
            #print("not merged we add the small polygon")
            #print(i)
            okeis.append(i)
            continue
    
    print("CHECKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    almost_final = []
    for ooppaa in okeis:
        if ooppaa.geom_type == "MultiPolygon":
            #print(ooppaa)
            for pp in ooppaa:
                almost_final.append(pp)
        else:
            almost_final.append(ooppaa)

    #Merge for second time, cause we still have some small polygons that need to be merged

    new_gdd = list_to_dgf(almost_final,epgs)
    new_gdd.to_file("road_polygons_final.shp")
    
    return [almost_final, new_gdd, "road_polygons_final.shp"]

def find_final_points(final_nodes,bufr,all_polygons):
    buffers_small = []
    #print("those are the small buffers")
    for i in range(len(final_nodes)):
        geomm = final_nodes.loc[i,'geometry']
        bf = geomm.buffer(bufr/2-1.5)
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
    #print("those are multibuffers")
    #for i in op:
        #print(i)
    all_pnts = []
    for i in only_nodes2:
        all_pnts.append(i)

    for ii in opop:
        all_pnts.append(ii)
    #print("those are all the final points")
    #for i in all_pnts:
        #print(i)
    return all_pnts

def exclude_no_road_polygons(shp_file, edges_shp, epgs, v3):
    p = gpd.read_file(shp_file)
    e = gpd.read_file(edges_shp)
    e['geometry'] = e.geometry.buffer(v3)
    f_polygons = []
    for i in range(len(p)):
        pol = p.loc[i,'geometry']
        aa = e.sindex.query(pol)
        bb = e.sindex.query(pol, predicate="touches")
        if len(aa)>0 or len(bb)>0:
            #print("this polygon is touched by a road edge: ")
            #print(pol)
            if len(aa)>0:
                print("a")
                #print(e.loc[aa[0], 'geometry'])
            elif len(bb) >0:
                print("b")
                #print(e.loc[bb[0]], 'geometry')
            f_polygons.append(pol)
        else:
            print("this polygon is not crossed by any road edge: ")
            print(pol)
    print(f_polygons)
    
    road_polygons =  list_to_dgf(f_polygons,epgs)
    return road_polygons

def delete_files_1():
    os.remove("diss_polygons.shp")
    os.remove("diss_polygons.cpg")
    os.remove("diss_polygons.dbf")
    os.remove("diss_polygons.prj")
    os.remove("diss_polygons.shx")
    os.remove("gamimeno.shp")
    os.remove("gamimeno.cpg")
    os.remove("gamimeno.dbf")
    os.remove("gamimeno.prj")
    os.remove("gamimeno.shx")
    os.remove("int_nodes.shp")
    os.remove("int_nodes.cpg")
    os.remove("int_nodes.dbf")
    os.remove("int_nodes.prj")
    os.remove("int_nodes.shx")
    os.remove("int_nodes_projected.shp")
    os.remove("int_nodes_projected.cpg")
    os.remove("int_nodes_projected.dbf")
    os.remove("int_nodes_projected.prj")
    os.remove("int_nodes_projected.shx")
    os.remove("wgs84_dissolved_polygons.shp")
    os.remove("wgs84_dissolved_polygons.cpg")
    os.remove("wgs84_dissolved_polygons.dbf")
    os.remove("wgs84_dissolved_polygons.prj")
    os.remove("wgs84_dissolved_polygons.shx")

#def check angles between lines
#def roundabouts()

def recreate_int_polygons(shapefile_polygons, epgs, bufr, v1, v2):
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

    #Clear file from non-useful nodes
    print("This is len of nodes: " ,len(df_final_nodes))
    edges_shapefile = "C:/Users/chcha/Desktop/GEOMATICS/2nd Year/Thesis/p2_technical/code/methodology1/graph/edges.shp"
    ed = gpd.read_file(edges_shapefile)
    ed = ed.to_crs(epgs)
    ed.to_file("edges_projected.shp")
    edges_projected = gpd.read_file("edges_projected.shp")  
    nods_nomotorways = remove_motor_nodes(df_final_nodes, epgs, edges_projected)

    #exclude all the nodes that are coorespond to roundabouts --> to treat the differently!
    round_edges = edges_projected[(edges_projected.junction == "roundabout")]
    r = round_edges.reset_index(drop=True)

    #print(nods_nomotorways)
    nodes_roundabout = []
    for nd in range(len(nods_nomotorways)-1):
        rec = nods_nomotorways.loc[nd]
        rec_geom = rec['geometry']
        for ln in range(len(r)):
            ed = r.loc[ln]
            ed_geom = ed['geometry']
            if ed_geom.touches(rec_geom):
                #print(nods_nomotorways.loc[nd,'geometry'])
                nodes_roundabout.append(nods_nomotorways.loc[nd,'geometry'])
                nods_nomotorways = nods_nomotorways.drop(nd)
                break

    # Treat differntly the roundabouts
    #bs = handle_roundabouts(nodes_roundabout,bufr,epgs)
    
    print("this is len after removing the roundabout nodes: ", len(nods_nomotorways))

    final_nodes = nods_nomotorways.reset_index(drop=True)
    #roundabout_nodes_gdf = list_to_dgf(nodes_roundabout)
    print("those are roundaboutpoints: ")
    for i in nodes_roundabout:
        print(i)
    all_pnts = find_final_points(final_nodes,bufr,all_polygons)
    #first create a small buffer for each node in order to find the nodes that are close together (in the same polygon or really close)
    
    print("we have all nodes for intersection polygons")
    #create the buffers and store them in a list
    buffers_final = []
    for i in all_pnts:
        bfr = i.buffer(bufr)
        buffers_final.append(bfr)

    #create a file with all the buffer polygons
    d = {'geometry':[]}
    for p in buffers_final:
        d['geometry'].append(p)

    gdf = gpd.GeoDataFrame(d, crs = epgs)
    gdf.to_file("final_buffers.shp")
    print("final buffer s are written to a file")

    #road_polygons = gpd.read_file(shapefile_polygons)
    buffers = gpd.read_file("final_buffers.shp")
    #real_roads = exclude_no_road_polygons(shapefile_polygons,"edges_projected.shp", epgs, v3)
    real_roads = gpd.read_file(shapefile_polygons)
    #print(real_roads)
    res_intersection = gpd.overlay(real_roads, buffers, how='intersection')
    res_difference =  gpd.overlay(real_roads,buffers, how = 'difference')
    res_intersection.to_file("intersection_polygons.shp")
    res_difference.to_file("non_int_road_polyogns.shp")

    # 1) Manipulate The Intersection Polygons
    df_int = gpd.read_file("intersection_polygons.shp")
    int_polygons = []
    for i in range(len(df_int)):
        int_polygons.append(df_int.loc[i,'geometry'])

    #dissolve the separate intersection polygons to one Multipolygon
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

    fnl_int_polygons = splitintpolygons(all_pnts,cu2, v1)
    #for p in fnl_int_polygons:
        #print(p)
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # 2) Manipulate non intersection road polygons
    print("AOUAOAOUAOAUAOU")
    df_nonint = gpd.read_file("non_int_road_polyogns.shp")
    non_int_polygons = []
    for i in range(len(df_nonint)):
        non_int_polygons.append(df_nonint.loc[i,'geometry'])

    fnl_non_int_polygons = []
    for niiis in non_int_polygons:
        if niiis.geom_type != "Polygon":
            #print(niiis.geom_type)
            for i in niiis:
                #print(i)
                fnl_non_int_polygons.append(i)
        else:
            fnl_non_int_polygons.append(niiis)

    #all the new polygons but not final (before merge the small polygons with their adjacent)
    new_road1 = []
    for pp in fnl_int_polygons:
        new_road1.append(pp)
    for ppp in fnl_non_int_polygons:
        new_road1.append(ppp)

    merge_polygons = mergesmallpolygons_withneighbours(new_road1,epgs,v2)
    
    final_pol_noroundabout_list = merge_polygons[0]
    final_pol_noroundabout_geodataframe = merge_polygons[1]
    final_pol_noroundabout_filename = merge_polygons[2]

    delete_files_1()
    return [final_pol_noroundabout_filename, "nodes_degree_4_projected.shp", 
    "C:/Users/chcha/Desktop/GEOMATICS/2nd Year/Thesis/p2_technical/code/methodology1/graph/edges.shp", nodes_roundabout]

    #round_abouts_intersection = gpd.overlay(real_roads, bs, how='intersection')

    #for abb in range(len(bs)):
        #print('ggg')
        #print(bs.loc[abb,'geometry'])

    #print("hm")
    #for s in range(len(round_abouts_intersection)):
        #print(round_abouts_intersection.loc[s,'geometry'])

#a = recreate_int_polygons(polygons_to_dissolve_clean, "EPSG:32617", 26, 27, 45)[1]

#Poznan -->  
# a good buffer value = 14.5-16.5 
# distance tolerance = 19-21 (v1)
#area of small polygons to be merged 25-30 (v2)
# area of small polygons that not taken into acount after splitting 7-10 (v2/3)
# buffer for non road polygons = (0.01) (v3)

#Helsinki -->
# a good buffer value = 18-20 (19.2 perfect) 
# distance tolerance = 25-27 (v1)
#area of small polygons to be merged 30-35 (v2)
# area of small polygons that not taken into acount after splitting 10-12 (v2/3)
# buffer for non road polygons = yes (0.1-0.3) (v3)


#Toronto --> 
# a good buffer value = 25-26 (25.4 perfect),
# distance tolerance = 27-28 (v1)
# #area of small polygons to be merged 42-48 (v2) 
# area of small polygons that not taken into acount after splitting 15-20 (v2/3)
# buffer for non road polygons = yes (0.3-0.8) (v3)
