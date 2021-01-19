from geomet import wkt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas
from geopandas import GeoDataFrame
import shapefile
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString
from shapely.geometry import Point
from test_road_width import final_list
from shapefile_manipulation import alllines, allpolygons

#after computing final width we assign the line geometry with the widht and the further parameters (num of intersections etc)
lines_output = []
for lnn in alllines:
    for lnnn in final_list:
        if lnn[1] == lnnn[1]:
            lines_output.append([lnn[1], lnn[0].coords, lnnn[0], lnnn[2], lnnn[3]])

#lines_output --> id, linestring, widht, t_intersections_number, cross_intersections_number
w2 = []
t2= []
c2 = []
for i in lines_output:
    w2.append(round(i[2],3))
    t2.append(i[3])
    c2.append(i[4])

check = []
for i in lines_output:
    for cor in i[1]:
        check.append([i[0],cor[0],cor[1],i[2],i[3],i[4]])

ids = []
lat = []
lon = []
widths = []
t_int = []
cross_int = []
for record in check:
    ids.append(record[0])
    lat.append(record[2])
    lon.append(record[1])
    widths.append(record[3])
    t_int.append(record[4])
    cross_int.append(record[5])



d = {'ids':[], 'lat':[], 'lon':[], 'widths':[], 't_int':[], 'cross_int':[]}

for idd in ids:
    d['ids'].append(idd)

for nl in lat:
    d['lat'].append(nl)

for nln in lon:
    d['lon'].append(nln)

for ww in widths:
    d['widths'].append(ww)

for t in t_int:
    d['t_int'].append(t)

for cr in cross_int:
    d['cross_int'].append(cr)

df = pd.DataFrame(data=d)

#print(df)

geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
df = GeoDataFrame(df, geometry=geometry)

df = df.groupby(['ids'])['geometry'].apply(lambda x: LineString(x.tolist()))
df = GeoDataFrame(df, geometry='geometry')

df['width'] = w2
df['t_num'] = t2
df['cross_num'] = c2

#print(df)
df.to_file("lines_isws.shp")


