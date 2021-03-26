import shapefile
import shapely.wkt
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas
from geopandas import GeoDataFrame
import pandas as pd
import numpy as np
from shapely.validation import explain_validity
from operator import itemgetter
from shapely.ops import linemerge

def merge_lines_osmid(lines_file, epgs):
    nn = geopandas.read_file(lines_file)
    nn = nn.to_crs(epgs)
    nn.to_file("projected_lines_shapefile.shp")

    lines = geopandas.read_file("projected_lines_shapefile.shp")
    print(lines.crs)
    lstt = []
    for i in range(len(lines)):
        rec = lines.loc[i]
        #print(rec['geometry'])
        lfn = rec['osmid']
        g = rec['geometry']
        lstt.append([lfn,g])

    f = dict()
    for opa in lstt:
        #print(opa)
        if opa[0] not in f:
            f[opa[0]] = [opa[1]]
        else:
            f[opa[0]].append(opa[1])
    merged_lines = []
    for ii in f:
        m = linemerge(f[ii])
        merged_lines.append(m)
    #print("MERGED")
    #for lnm in merged_lines:
        #print(lnm)
    hmm = 0
    final_merged = []
    for il in merged_lines:
        final_merged.append([hmm,il])
        hmm+=1

    lines_output = []
    for lnn in final_merged:
        if lnn[1].type == 'MultiLineString':
            for lin in lnn[1]:
                lines_output.append([lnn[0],lin.coords])
        else:
            lines_output.append([lnn[0], lnn[1].coords])


    check = []
    for i in lines_output:
        for cor in i[1]:
            check.append([i[0],cor[0],cor[1]])

    lat = []
    lon = []
    ids = []
    for record in check:
        ids.append(record[0])
        lat.append(record[2])
        lon.append(record[1])

    d = {'ids':[],'lat':[], 'lon':[]}

    for idd in ids:
        d['ids'].append(idd)

    for nl in lat:
        d['lat'].append(nl)

    for nln in lon:
        d['lon'].append(nln)

    df = pd.DataFrame(data=d)

    #print(df)

    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    df = GeoDataFrame(df, geometry=geometry)

    df = df.groupby(['ids'])['geometry'].apply(lambda x: LineString(x.tolist()))
    df = GeoDataFrame(df, geometry='geometry')

    #print(df)
    df.to_file("merged_osmid_lines.shp")
    return "merged_osmid_lines.shp"
