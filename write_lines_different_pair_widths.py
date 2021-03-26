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
from test_road_width import res, res2
from shapefile_manipulation import alllines, allpolygons


#measuring_lines -->  widht, linestring
lines_output = []
for i in res:
    lines_output.append([i[2],i[1].coords,i[0]])

lines_output2 = []
for i in res2:
    lines_output2.append([i[2],i[1].coords,i[0]])

check = []
for i in lines_output:
    for cor in i[1]:
        check.append([i[0],cor[0],cor[1],i[2]])

check2 = []
for i in lines_output2:
    for cor in i[1]:
        check2.append([i[0],cor[0],cor[1],i[2]])

ids = []
mean = []
lat = []
lon = []
for record in check:
    ids.append(record[0])
    lat.append(record[2])
    lon.append(record[1])
    mean.append(record[3])

ids2 = []
median = []
lat2 = []
lon2 = []
for record2 in check2:
    ids2.append(record2[0])
    lat2.append(record2[2])
    lon2.append(record2[1])
    median.append(record2[3])


d = {'id1':[],'lat':[], 'lon':[], 'typcl_df_mn':[]}
d2 = {'id2':[],'lat2':[], 'lon2':[], 'typcl_df_md':[]}

for idd in ids:
    d['id1'].append(idd)

for nl in lat:
    d['lat'].append(nl)

for nln in lon:
    d['lon'].append(nln)

for m in mean:
    d['typcl_df_mn'].append(m)

for idd2 in ids2:
    d2['id2'].append(idd2)

for nl2 in lat2:
    d2['lat2'].append(nl2)

for nln2 in lon2:
    d2['lon2'].append(nln2)

for m2 in median:
    d2['typcl_df_md'].append(m2)





df = pd.DataFrame(data=d)
geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
df = GeoDataFrame(df, geometry=geometry)

df2 = pd.DataFrame(data=d2)
geometry = [Point(xy) for xy in zip(df2.lon2, df2.lat2)]
df2 = GeoDataFrame(df2, geometry=geometry)


df.to_file("differences_mean.shp")
df2.to_file("differences_median.shp")

