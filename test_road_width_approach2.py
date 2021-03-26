from geomet import wkt
import json
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas
from geopandas import GeoDataFrame
import shapefile
import statistics
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString
from shapely.geometry import Point
from intersection_identify import checkforcross, checkforTcase2, checkforTmaincase, checkforcross2
from shapefile_manipulation import allpolygons, alllines


def fitlinetopolygons(line, polygonlist):
    lines_polygons_pairs = []
    for i in polygonlist:
        if type(i) != list:
            if line[0].intersects(i):
                fitline = line[0].intersection(i)
                lines_polygons_pairs.append([fitline,i,"rd"])
        else:
            if line[0].intersects(i[0]):
                fitline = line[0].intersection(i[0])
                lines_polygons_pairs.append([fitline,i[0],i[1]])
    return lines_polygons_pairs


def cutlinetotwenty(line):
    #change to 20line for more accuracy
    tenlines = []
    line1 = [LineString([line.interpolate(0, normalized = True), line.interpolate(0.05, normalized = True)]), 1]
    line2 = [LineString([line.interpolate(0.05, normalized = True), line.interpolate(0.1, normalized = True)]), 2]
    line3 = [LineString([line.interpolate(0.1, normalized = True), line.interpolate(0.15, normalized = True)]), 3]
    line4 = [LineString([line.interpolate(0.15, normalized = True), line.interpolate(0.2, normalized = True)]), 4]
    line5 = [LineString([line.interpolate(0.2, normalized = True), line.interpolate(0.25, normalized = True)]), 5]
    line6 = [LineString([line.interpolate(0.25, normalized = True), line.interpolate(0.3, normalized = True)]), 6]
    line7 = [LineString([line.interpolate(0.3, normalized = True), line.interpolate(0.35, normalized = True)]), 7]
    line8 = [LineString([line.interpolate(0.35, normalized = True), line.interpolate(0.4, normalized = True)]), 8]
    line9 = [LineString([line.interpolate(0.4, normalized = True), line.interpolate(0.45, normalized = True)]), 9]
    line10 = [LineString([line.interpolate(0.45, normalized = True), line.interpolate(0.5, normalized = True)]), 10]
    line11 = [LineString([line.interpolate(0.5, normalized = True), line.interpolate(0.55, normalized = True)]), 11]
    line12 = [LineString([line.interpolate(0.55, normalized = True), line.interpolate(0.6, normalized = True)]), 12]
    line13 = [LineString([line.interpolate(0.6, normalized = True), line.interpolate(0.65, normalized = True)]), 13]
    line14 = [LineString([line.interpolate(0.65, normalized = True), line.interpolate(0.7, normalized = True)]), 14]
    line15 = [LineString([line.interpolate(0.7, normalized = True), line.interpolate(0.75, normalized = True)]), 15]
    line16 = [LineString([line.interpolate(0.75, normalized = True), line.interpolate(0.8, normalized = True)]), 16]
    line17 = [LineString([line.interpolate(0.8, normalized = True), line.interpolate(0.85, normalized = True)]), 17]
    line18 = [LineString([line.interpolate(0.85, normalized = True), line.interpolate(0.9, normalized = True)]), 18]
    line19 = [LineString([line.interpolate(0.9, normalized = True), line.interpolate(0.95, normalized = True)]), 19]
    line20 = [LineString([line.interpolate(0.95, normalized = True), line.interpolate(1, normalized = True)]), 20]
    tenlines.append(line1)
    tenlines.append(line2)
    tenlines.append(line3)
    tenlines.append(line4)
    tenlines.append(line5)
    tenlines.append(line6)
    tenlines.append(line7)
    tenlines.append(line8)
    tenlines.append(line9)
    tenlines.append(line10)
    tenlines.append(line11)
    tenlines.append(line12)
    tenlines.append(line13)
    tenlines.append(line14)
    tenlines.append(line15)
    tenlines.append(line16)
    tenlines.append(line17)
    tenlines.append(line18)
    tenlines.append(line19)
    tenlines.append(line20)
    return tenlines

def cutlinetoten(line):
    tenlines = []
    line1 = [LineString([line.interpolate(0, normalized = True), line.interpolate(0.1, normalized = True)]), 1]
    line2 = [LineString([line.interpolate(0.1, normalized = True), line.interpolate(0.2, normalized = True)]), 2]
    line3 = [LineString([line.interpolate(0.2, normalized = True), line.interpolate(0.3, normalized = True)]), 3]
    line4 = [LineString([line.interpolate(0.3, normalized = True), line.interpolate(0.4, normalized = True)]), 4]
    line5 = [LineString([line.interpolate(0.4, normalized = True), line.interpolate(0.5, normalized = True)]), 5]
    line6 = [LineString([line.interpolate(0.5, normalized = True), line.interpolate(0.6, normalized = True)]), 6]
    line7 = [LineString([line.interpolate(0.6, normalized = True), line.interpolate(0.7, normalized = True)]), 7]
    line8 = [LineString([line.interpolate(0.7, normalized = True), line.interpolate(0.8, normalized = True)]), 8]
    line9 = [LineString([line.interpolate(0.8, normalized = True), line.interpolate(0.9, normalized = True)]), 9]
    line10 = [LineString([line.interpolate(0.9, normalized = True), line.interpolate(1, normalized = True)]), 10]
    tenlines.append(line1)
    tenlines.append(line2)
    tenlines.append(line3)
    tenlines.append(line4)
    tenlines.append(line5)
    tenlines.append(line6)
    tenlines.append(line7)
    tenlines.append(line8)
    tenlines.append(line9)
    tenlines.append(line10)
    return tenlines

#function that takes a line and defines 2 offsets 
#we did this in order to create a line prependicular to our road (the 10 lines that used to define the width of the road should be prependicular to the linear representation of the road)
def makeoffsets(line, dist):
    leftline = line[0].parallel_offset(dist, 'left')
    rightline = line[0].parallel_offset(dist, 'right')
    #print("offsetsss")
    #print(leftline)
    #print(rightline)
    #we find the 2 midpoints of the 2 offset lines in order to connect them and create the prependicular line segment
    midpointleft = leftline.interpolate(0.5, normalized = True)
    midpointright = rightline.interpolate(0.5, normalized = True)
    #print(midpointleft)
    #print(midpointright)
    prependicular_line = LineString([midpointleft, midpointright])
    #print("prep")
    #print(prependicular_line)
    prep_line = [prependicular_line, line[1]]
    return prep_line

def widt(prepedicularline, polygon, roadline):
    #prependicular line between 2 offsets intersects polygon
    ln = prepedicularline.intersection(polygon)
    #if returns 2 or more linestrings we need to find the one that intersects the roadline

    if ln.type == 'MultiLineString':
        ll = list(ln)
        s = 0
        for i in ll:
            if i.intersects(roadline):
                measureline = i
                tom = measureline.length #* 111139 
                w = round(tom, 6)
                ln = measureline
                #print(measureline)
            else:
                s+=1
        if len(ll) > 1 and s == len(ll):
            d = []
            dd = []
            print("WEIRD CASE")
            for i in ll:
                midi = i.interpolate(0.5, normalized = True)
                midroadline = roadline.interpolate(0.5,normalized = True)
                distancetoroadline = LineString([midi, midroadline]).length
                d.append([distancetoroadline,i])
                dd.append(distancetoroadline)
            mindist = min(dd)
            for val in d:
                if val[0] == mindist:
                    tom = val[1].length #* 111139 
                    w = round(tom,6)
                    ln = val[1]
                    #print(ln)
    else:
        tom = ln.length# * 111139
        w = round(tom, 4)
        #print(ln)
    
    return w, ln

def avgwidth(w):
    s = 0
    for i in w:
        s += i[0]
    avg = s / len(w)
    return round(avg, 4)

def avgwidth2(lst):
    s = 0
    for i in lst:
        s += i
    avg = s / len(lst)
    return round(avg, 4)

def med_min_max(measuring_lines_lst):
    values_only = []
    for i in measuring_lines_lst:
        values_only.append(i[0])
    med = statistics.median(values_only)
    maxi = max(values_only)
    mini = min(values_only)
    return med,maxi,mini

def width_pair_differences(widthsofcenterline,line):
    widthsonly = []
    for w in widthsofcenterline:
        widthsonly.append(w[0])
    e = []
    t = []
    p = []
    h = []
    for k in range(len(widthsonly)):
        s = widthsonly[k]
        #print(s)
        for a in range(len(widthsonly)):
            #print(widthsonly[a])
            if widthsonly[a] != s:
                res = abs(s-widthsonly[a])
                #print(res)
                if res < 1.5:
                    e.append(res)
                elif res > 1.5 and res < 3:
                    t.append(res)
                elif res > 3 and res < 5:
                    p.append(res)
                elif res > 5 :
                    h.append(res)
    
    if len(h) > 0:
        return [h[0],line[0],line[1]]
    if len(p) > 0:
        return [p[0],line[0],line[1]]
    if len(t) > 0:
        return [t[0],line[0],line[1]]
    if len(e) > 0:
        return [e[0],line[0],line[1]]

def mean_w_centerline(widthsofcenterline):
    total = 0
    for i in widthsofcenterline:
        total += i[1]
    
    for i in widthsofcenterline:
        #print("here: ", i)
        if i == 0:
            widthsofcenterline.remove(i)
    if len(widthsofcenterline) == 0:
        print("this is only intersections")
        return 0, "max_min0"
    #print(len(widthsofcenterline))
    s = 0
    for ii in widthsofcenterline:
        weight = ii[1] / total
        s += ii[0] * weight
        print(weight, " ", s)

    return round(s,5), "check"           

def widthcalculation(line, polygon,dist):
    tenlines = cutlinetotwenty(line)
    w = []
    outliers = []
    allpreplines = []
    for i in tenlines:
        prep_line = makeoffsets(i, dist)
        allpreplines.append(prep_line)
        width = widt(prep_line[0], polygon, i[0])[0]
        measuringline = widt(prep_line[0], polygon, i[0])[1]
        w.append([width,prep_line[1],measuringline])
    # w list contains --> [width value, number of measuring line, measuring line wkt]
    for isss in w:
        print(isss[2])
        #print("this is width of measuring line: ", isss[0], "id: ", isss[1], isss[2])
        if isss[0] == 0.0:
            w.remove(isss)
            print("i found an empty line:", isss)
    #make a list only with the 20 widhts to use it for checking if there is a cross intersection

    # onlywidths contains --> [width value, measuring line wkt]
    onlywidths = []
    for wdt in w:
        onlywidths.append([wdt[0], wdt[2]])

    m = avgwidth(w)
    print("this is mean of widths: ", m)
    s = 0
    for ii in w:
        d = (ii[0] - m) ** 2
        s += d
    paro = len(w)-1
    std = round(math.sqrt(s/paro), 6)
    #make the code a bit more robust (by marking widths as an outliers a bit easier)
    #std = round(std1 - std1*0.08, 6)
    print("this was std: ", std)

    if checkforTcase2(onlywidths, line):
        return [0, "T"]
    elif checkforTmaincase(onlywidths, line):
        return [0, "T"]
    else:
        #outliers contains --> [number of measuring line, width, 1 or 0]
        for iii in w:
            if iii[0] > m + 1.5*std: 
                outliers.append([iii[1], iii[0], 1])
            elif iii[0] < m- 1.5*std:
                outliers.append([iii[1], iii[0], 0])
        #remove outliers from the widths list 
        for out in outliers:
            for widths in w:
                if out[0] == widths[1]:
                    #print("i removed", out[0])
                    w.remove(widths)
        #find the lines that are marked as outliers
        outlier_linestrings = [] # --> []
        outliers2 = [] # a list that contains linestring, id, width of outlier and 0 if lower from mean 1 if higher of mean
        for ln in allpreplines:
            for outl in outliers:
                if ln[1] == outl[0]:
                    outlier_linestrings.append(ln[0])
                    outliers2.append([ln[0], outl[0], outl[1], outl[2]])
        
        #for ooo in outliers2:
            #print("outlier, with id and width: ", ooo)

        #for isn in w:
            #print("accurate measure line, with id and width: ", isn)

        median = med_min_max(w)[0]
        maxi = med_min_max(w)[1]
        mini = med_min_max(w)[2]
        mean = round(avgwidth(w), 5)

        new_m = avgwidth(w)
        g = 0
        for plat in w:
            di = (plat[0] - new_m) ** 2
            g += di
        paro2 = len(w)-1
        new_std = round(math.sqrt(s/paro2), 6)

        return [mean, "R", w, outliers2, median, maxi, mini, m, std, new_m, new_std]

def width_lines_dataset(alllines, allpolygons, dist):
    line_id_finalwidth = []
    measuring_lines = []
    outliers = []
    for i in alllines:
        print("this is the line with id: ",i)
        lines_polygons_pairs = fitlinetopolygons(i,allpolygons)
        means = []
        t_intersections = []
        cross_intersections = []
        medians = []
        maxies = []
        minies = []
        for pair in lines_polygons_pairs:
            ftiline_length = pair[0].length#* 111139
            print(ftiline_length)
            if ftiline_length < 1:
                print("something is wrong, super small fitline!!")
            else:
                for pairi in pair:
                    print(pairi)
                if pair[2] == "rd":
                    n = widthcalculation(pair[0], pair[1], dist)
                    if n[1] == 'R':
                        means.append([n[0],ftiline_length])
                        measuring_lines.append([n[2],i[1],n[7],n[8],n[9],n[10]])
                        outliers.append([n[3],i[1]])
                        medians.append([n[4],ftiline_length])
                        maxies.append(n[5])
                        minies.append(n[6])
                    #m.append(n[7])
                    #stds.append(n[8])
                    if n[1] == "T":
                        t_intersections.append(n[0])

                elif pair[2] == "cross":
                    cross_intersections.append("c")

            #this is the mean of the mean values that is return for each polygon
            final_w_road_mean = mean_w_centerline(means)[0]
            #this is the mean of the median values that is returned for each polygon
            final_w_road_median = mean_w_centerline(medians)[0]
            if mean_w_centerline(means)[1] == "max_min0":
                max_of_max = 0
                min_of_min = 0
            else:
                max_of_max = round((max(maxies)),5)
                min_of_min = round((min(minies)),5)  
            
            line_id_finalwidth.append([final_w_road_mean, i[1], len(t_intersections), len(cross_intersections), final_w_road_median, max_of_max, min_of_min])
    return line_id_finalwidth, measuring_lines, outliers

widths_fnl = width_lines_dataset(alllines,allpolygons,40)

final_list = widths_fnl[0]
measuring_liness = widths_fnl[1]
outlierss = widths_fnl[2]


for i in final_list:
    print("this is line with id: ", i[1], "and the width based on mean is: ", i[0], "number of t intersections: ", i[2], "and number of cross intersections: ", i[3], "width based on median is: ", i[4], "max width is: ", i[5], "min width is: ", i[6])


measuring_lines = []
for mm in measuring_liness:
    for mmm in mm[0]:
        measuring_lines.append([mmm[0], mm[1], mmm[2], mm[2],mm[3],mm[4],mm[5]])     
