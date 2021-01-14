from geomet import wkt
import json
import math
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString
from shapely.geometry import Point
from intersection_identify import checkforcross, checkforTcase2, checkforTmaincase
from shapefile_manipulation import allpolygons, bigcenterline


def fitlinetopolygons(line, polygonlist):
    lines_polygons_pairs = []
    for i in polygonlist:
        if line.intersects(i):
            fitline = line.intersection(i)
            lines_polygons_pairs.append([fitline,i])
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
def makeoffsets(line):
    leftline = line[0].parallel_offset(1, 'left')
    rightline = line[0].parallel_offset(1, 'right')
    #print(leftline)
    #print(rightline)
    #print(leftline)
    #print(rightline)
    #we find the 2 midpoints of the 2 offset lines in order to connect them and create the prependicular line segment
    midpointleft = leftline.interpolate(0.5, normalized = True)
    midpointright = rightline.interpolate(0.5, normalized = True)
    #print(midpointleft)
    #print(midpointright)
    prependicular_line = LineString([midpointleft, midpointright])
    #print(prependicular_line)
    prep_line = [prependicular_line, line[1]]
    return prep_line



def widt(prepedicularline, polygon, roadline):
    #prependicular line between 2 offsets intersects polygon
    ln = prepedicularline.intersection(polygon)
    #if returns 2 or more linestrings we need to find the one that intersects the roadline
    
    if ln.type == 'MultiLineString':
        ll = list(ln)
        for i in ll:
            if i.intersects(roadline):
                measureline = i
                w = round(measureline.length, 6)
                ln = measureline
                #print(measureline)
    else:
        w = round(ln.length, 4)
        #print(ln)
    return w, ln

def avgwidth(w):
    s = 0
    for i in w:
        s += i[0]
    avg = s / len(w)
    return round(avg, 6)

def avgwidth2(lst):
    s = 0
    for i in lst:
        s += i
    avg = s / len(lst)
    return round(avg, 6)

def mean_w_centerline(widthsofcenterline):
    for i in widthsofcenterline:
        print(i)
        if i == 0:
            widthsofcenterline.remove(i)
    if len(widthsofcenterline) == 0:
        print("this is only intersections")
        return 0
    print(len(widthsofcenterline))
    s = 0
    for ii in widthsofcenterline:
        s += ii
    mean = s / len(widthsofcenterline)
    return mean

def widthcalculation(line, polygon):
    tenlines = cutlinetotwenty(line)
    w = []
    outliers = []
    allpreplines = []
    for i in tenlines:
        prep_line = makeoffsets(i)
        allpreplines.append(prep_line)
        width = widt(prep_line[0], polygon, i[0])[0]
        measuringline = widt(prep_line[0], polygon, i[0])[1]
        w.append([width,prep_line[1],measuringline])
    # w list contains --> [width value, number of measuring line, measuring line wkt]
    for isss in w:
        print("this is width of measuring line: ", isss)
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
    std = round(math.sqrt(s/19), 6)
    #make the code a bit more robust (by marking widths as an outliers a bit easier)
    #std = round(std1 - std1*0.08, 6)
    print("this was std: ", std)
    #check if a width record is higher or lower than 1 std and if so mark it as an outlier (append it to an outliers list and remove it later)

    if checkforcross(onlywidths, line):
        return 0
    elif checkforTcase2(onlywidths, line):
        return 0
    elif checkforTmaincase(onlywidths, line):
        return 0
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
                    print("i removed", out[0])
                    w.remove(widths)
        #find the lines that are marked as outliers
        outlier_linestrings = [] # --> []
        outliers2 = [] # a list that contains linestring, id, width of outlier and 0 if lower from mean 1 if higher of mean
        for ln in allpreplines:
            for outl in outliers:
                if ln[1] == outl[0]:
                    outlier_linestrings.append(ln[0])
                    outliers2.append([ln[0], outl[0], outl[1], outl[2]])
        
        #print the outlier prependicular lines
        for o in outlier_linestrings:
            print(o)
        for ooo in outliers2:
            print(ooo)

        n = round(avgwidth(w), 5)
        return n

#fit the big centerline of the road to each polygon that intersects   
lines_polygons_pairs = fitlinetopolygons(bigcenterline, allpolygons)
widthsofcenterline = []
#estimate the width for each pair of centerline-polygon
for i in lines_polygons_pairs:

    n = widthcalculation(i[0], i[1])
    widthsofcenterline.append(n)
#show the width of each polygon
num_of_width = 1   
for i in widthsofcenterline:
    print("width of ", num_of_width, " polygon is: ", i)
    num_of_width += 1

#compute a mean width for the whole centerline
final_w_road = mean_w_centerline(widthsofcenterline)
print("this is the final width of the road: ", final_w_road)






