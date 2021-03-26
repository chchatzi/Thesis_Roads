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
from test_road_width_approach2 import final_list
from shapefile_manipulation import alllines, allpolygons

#after computing final width we assign the line geometry with the widht and the further parameters (num of intersections etc)
lines_output = []
for lnn in alllines:
    for lnnn in final_list:
        if lnn[1] == lnnn[1]:
            lines_output.append([lnn[1], lnn[0].coords, lnnn[0], lnnn[2], lnnn[3],lnnn[4], lnnn[5], lnnn[6]])
#lines_output --> id, linestring coords [x,y], widht, t_intersections_number, cross_intersections_number
w2 = []
t2= []
c2 = []
med2 = []
max2 = []
min2 = []

for i in lines_output:
    w2.append(round(i[2],3))
    t2.append(i[3])
    c2.append(i[4])
    med2.append(round(i[5],3))
    max2.append(i[6])
    min2.append(i[7])
   

check = []
for i in lines_output:
    for cor in i[1]:
        check.append([i[0],cor[0],cor[1],i[2],i[3],i[4],i[5],i[6],i[7]])

ids = []
lat = []
lon = []
widths = []
t_int = []
cross_int = []

medians = []
max_width = []
min_width = []
for record in check:
    ids.append(record[0])
    lat.append(record[2])
    lon.append(record[1])
    widths.append(record[3])
    t_int.append(record[4])
    cross_int.append(record[5])
    medians.append(record[6])
    max_width.append(record[7])
    min_width.append(record[8])



d = {'ids':[], 'lat':[], 'lon':[], 'mean_width':[], 't_int':[], 'cross_int':[], 'median_width':[], 'max_width':[], 'min_width':[]}

for idd in ids:
    d['ids'].append(idd)

for nl in lat:
    d['lat'].append(nl)

for nln in lon:
    d['lon'].append(nln)

for ww in widths:
    d['mean_width'].append(ww)

for t in t_int:
    d['t_int'].append(t)

for cr in cross_int:
    d['cross_int'].append(cr)

for mm in medians:
    d['median_width'].append(mm)

for mx in max_width:
    d['max_width'].append(mx)

for mn in min_width:
    d['min_width'].append(mn)



df = pd.DataFrame(data=d)


geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
df = GeoDataFrame(df, geometry=geometry)

df = df.groupby(['ids'])['geometry'].apply(lambda x: LineString(x.tolist()))
df = GeoDataFrame(df, geometry='geometry', crs = "EPSG:3879")

df['mean_width'] = w2
df['t_num'] = t2
df['cross_num'] = c2
df['median_width'] = med2
df['max_width'] = max2
df['min_width'] = min2


#print(df)

df.to_file("lines_with_width.shp")


