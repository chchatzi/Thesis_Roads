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
from test_road_width_approach2 import measuring_lines
from shapefile_manipulation import alllines, allpolygons


#measuring_lines -->  widht, linestring
lines_output = []
for i in measuring_lines:
    lines_output.append([i[1],i[2].coords,i[0],i[3],i[4],i[5],i[6]])

w2 = []

for i in lines_output:
    w2.append(round(i[2]*10000,3))


check = []
for i in lines_output:
    for cor in i[1]:
        check.append([i[0],cor[0],cor[1],i[2],i[3],i[4],i[5],i[6]])

ids = []
mean = []
std = []
lat = []
lon = []
widths = []
final_mean = []
final_std = []
for record in check:
    ids.append(record[0])
    lat.append(record[2])
    lon.append(record[1])
    widths.append(record[3])
    mean.append(record[4])
    std.append(record[5])
    final_mean.append(record[6])
    final_std.append(record[7])

d = {'ids':[],'lat':[], 'lon':[], 'widths':[],'mean_after':[],'std_after':[], 'mean_before':[], 'std_before':[]}

for idd in ids:
    d['ids'].append(idd)

for nl in lat:
    d['lat'].append(nl)

for nln in lon:
    d['lon'].append(nln)

for ww in widths:
    d['widths'].append(ww)

for tss in final_mean:
    d['mean_after'].append(tss)

for oas in final_std:
    d['std_after'].append(oas)

for m in mean:
    d['mean_before'].append(m)

for stdd in std:
    d['std_before'].append(stdd)


df = pd.DataFrame(data=d)


geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
df = GeoDataFrame(df, geometry=geometry)

#df['width'] = w2


#print(df)
df.to_file("measuring_lines.shp")


