from geomet import wkt
import json
import math
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString
from shapely.geometry import Point
from road_lines_polygons import line, polygon,line22, polygon22, line01, polygon01, line1, polygon1
from road_lines_polygons import linecross1case1,linecross1case2, polygoncross1
from road_lines_polygons import linecross2case1, linecross2case2, polygoncross2
from road_lines_polygons import linesmall1, linesmall2,polygonsmall
from road_lines_polygons import toronto_intersection_cross_line, toronto_intersection_cross_polygon, toronto_intersection_t_line1, toronto_intersection_t_polygon
 

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
    leftline = line[0].parallel_offset(2, 'left')
    rightline = line[0].parallel_offset(2, 'right')
    print(leftline)
    print(rightline)
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
        w = round(ln.length, 6)
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

def checkforcross(twentylines, roadline):
    '''this function takes the measuring lines that are not empty with their widths and checks for cross intersection
    the main condition is the value of the mean of the values that located in the center of the line to be 2 times higher than the 2 other means
    the one for the first 3 lines and the one of the last 3 lines. If that is the case then the road is tested if it is T intersection as well'''

    print("this is the number of the actual widths: ", len(twentylines))
    if len(twentylines) > 19:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]]#, twentylines[3], twentylines[4], twentylines[5]]
        mid = [twentylines[7][0], twentylines[8][0], twentylines[9][0], twentylines[10][0], twentylines[11][0], twentylines[12][0]]
        last = [twentylines[17][0], twentylines[18][0], twentylines[19][0]]
    elif len(twentylines) > 18:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]] #, twentylines[3], twentylines[4], twentylines[5]]
        mid = [twentylines[7][0], twentylines[8][0], twentylines[9][0], twentylines[10][0], twentylines[11][0], twentylines[12][0]]
        last = [twentylines[16][0], twentylines[17][0], twentylines[18][0]]
        
    f = avgwidth2(first)
    m = avgwidth2(mid)
    l = avgwidth2(last)
    print(f, "",m, "", l)
    if m>f*2 and m>l*2:
        #check if it is a T intersection
        #take 4 measuring lines that are in the midlle
        #take the 2 end points of each line
        end8one = Point(twentylines[8][1].coords[0])
        end8tow = Point(twentylines[8][1].coords[-1])
        end9one = Point(twentylines[9][1].coords[0])
        end9tow = Point(twentylines[9][1].coords[-1])
        end10one = Point(twentylines[10][1].coords[0])
        end10tow = Point(twentylines[10][1].coords[-1])
        end11one = Point(twentylines[11][1].coords[0])
        end11tow = Point(twentylines[11][1].coords[-1])

        #find the midpoints of the road lines that are in line with the 4 mid lines
        line9 = LineString([roadline.interpolate(0.4, normalized = True), roadline.interpolate(0.45, normalized = True)])
        line10 = LineString([roadline.interpolate(0.45, normalized = True), roadline.interpolate(0.5, normalized = True)])
        line11 = LineString([roadline.interpolate(0.5, normalized = True), roadline.interpolate(0.55, normalized = True)])
        line12 = LineString([roadline.interpolate(0.55, normalized = True), roadline.interpolate(0.6, normalized = True)])
        mid9 = line9.interpolate(0.5, normalized = True)
        mid10 = line10.interpolate(0.5, normalized = True)
        mid11 = line11.interpolate(0.5, normalized = True)
        mid12 = line12.interpolate(0.5, normalized = True)
        #calculate the distance between end point1 of a mid line and the corresponding point in the road line and 
        # the distance between the other end point and the same point in road line
        #if distance differ a lot append them to a list so we can check the len of the list after
        differences = []
        dif8start = LineString([end8one, mid9]).length
        dif8end = LineString([end8tow, mid9]).length
        if (dif8start-dif8end) > 0:
            if (dif8start - dif8end) > 0.9*dif8end:
                differences.append(1)
        elif (dif8start-dif8end) < 0:
            if dif8end-dif8start > 0.9*dif8start:
                differences.append(1)

        dif9start = LineString([end9one, mid10]).length
        dif9end = LineString([end9tow, mid10]).length
        if (dif9start-dif9end) > 0:
            if (dif9start - dif9end) > 0.9*dif9end:
                differences.append(1)
        elif (dif9start-dif9end) < 0:
            if dif9end-dif9start > 0.9*dif9start:
                differences.append(1)
        
        dif10start = LineString([end10one, mid11]).length
        dif10end = LineString([end10tow, mid11]).length
        if (dif10start-dif10end) > 0:
            if (dif10start - dif10end) > 0.9*dif10end:
                differences.append(1)
        elif (dif10start-dif10end) < 0:
            if dif10end-dif10start > 0.9*dif10start:
                differences.append(1)
        
        dif11start = LineString([end11one, mid12]).length
        dif11end = LineString([end11tow, mid12]).length
        if (dif11start-dif11end) > 0:
            if (dif11start - dif11end) > 0.9*dif11end:
                differences.append(1)
        elif (dif11start-dif11end) < 0:
            if dif11end-dif11start > 0.9*dif11start:
                differences.append(1)

        if len(differences) >= 3:
            print("there is a T intersection")
            return True
        else:
            print("there is a cross intersection")
            return True 
    else :
        return False

def checkforTcase2(twentylines, roadline):
    print("it passes the test for cross intersection i am checking for T intersection of case 2")
    if len(twentylines) > 19:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]]#, twentylines[3], twentylines[4], twentylines[5]]
        mid = [twentylines[7][0], twentylines[8][0], twentylines[9][0], twentylines[10][0], twentylines[11][0], twentylines[12][0]]
        last = [twentylines[17][0], twentylines[18][0], twentylines[19][0]]
    elif len(twentylines) > 18:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]] #, twentylines[3], twentylines[4], twentylines[5]]
        mid = [twentylines[7][0], twentylines[8][0], twentylines[9][0], twentylines[10][0], twentylines[11][0], twentylines[12][0]]
        last = [twentylines[16][0], twentylines[17][0], twentylines[18][0]]
        
    f = avgwidth2(first)
    m = avgwidth2(mid)
    l = avgwidth2(last)
    print(f, "",m, "", l)
    if m>f*1.6 and m>l*1.6:
        #check if it is a T intersection
        #take 4 measuring lines that are in the midlle
        #take the 2 end points of each line
        end8one = Point(twentylines[8][1].coords[0])
        end8tow = Point(twentylines[8][1].coords[-1])
        end9one = Point(twentylines[9][1].coords[0])
        end9tow = Point(twentylines[9][1].coords[-1])
        end10one = Point(twentylines[10][1].coords[0])
        end10tow = Point(twentylines[10][1].coords[-1])
        end11one = Point(twentylines[11][1].coords[0])
        end11tow = Point(twentylines[11][1].coords[-1])

        #find the midpoints of the road lines that are in line with the 4 mid lines
        line9 = LineString([roadline.interpolate(0.4, normalized = True), roadline.interpolate(0.45, normalized = True)])
        line10 = LineString([roadline.interpolate(0.45, normalized = True), roadline.interpolate(0.5, normalized = True)])
        line11 = LineString([roadline.interpolate(0.5, normalized = True), roadline.interpolate(0.55, normalized = True)])
        line12 = LineString([roadline.interpolate(0.55, normalized = True), roadline.interpolate(0.6, normalized = True)])
        mid9 = line9.interpolate(0.5, normalized = True)
        mid10 = line10.interpolate(0.5, normalized = True)
        mid11 = line11.interpolate(0.5, normalized = True)
        mid12 = line12.interpolate(0.5, normalized = True)
        #calculate the distance between end point1 of a mid line and the corresponding point in the road line and 
        # the distance between the other end point and the same point in road line
        #if distance differ a lot append them to a list so we can check the len of the list after
        differences = []
        dif8start = LineString([end8one, mid9]).length
        dif8end = LineString([end8tow, mid9]).length
        if (dif8start-dif8end) > 0:
            if (dif8start - dif8end) > 0.9*dif8end:
                differences.append(1)
        elif (dif8start-dif8end) < 0:
            if dif8end-dif8start > 0.9*dif8start:
                differences.append(1)

        dif9start = LineString([end9one, mid10]).length
        dif9end = LineString([end9tow, mid10]).length
        if (dif9start-dif9end) > 0:
            if (dif9start - dif9end) > 0.9*dif9end:
                differences.append(1)
        elif (dif9start-dif9end) < 0:
            if dif9end-dif9start > 0.9*dif9start:
                differences.append(1)
        
        dif10start = LineString([end10one, mid11]).length
        dif10end = LineString([end10tow, mid11]).length
        if (dif10start-dif10end) > 0:
            if (dif10start - dif10end) > 0.9*dif10end:
                differences.append(1)
        elif (dif10start-dif10end) < 0:
            if dif10end-dif10start > 0.9*dif10start:
                differences.append(1)
        
        dif11start = LineString([end11one, mid12]).length
        dif11end = LineString([end11tow, mid12]).length
        if (dif11start-dif11end) > 0:
            if (dif11start - dif11end) > 0.9*dif11end:
                differences.append(1)
        elif (dif11start-dif11end) < 0:
            if dif11end-dif11start > 0.9*dif11start:
                differences.append(1)

        if len(differences) >= 3:
            print("there is a T intersection case2")
            return True
        else:
            print("the road is wider in the middle but is not T intersection or cross intersection")
            return False
    else :
        return False

#def checkforTmaincase 

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
    #for iss in allpreplines:
        #print("opaaa", iss)
    for isss in w:
        print("this is width of measuring line: ", isss)
        if isss[0] == 0.0:
            w.remove(isss)
            print("i found an empty line:", isss)
    #make a list only with the 20 widhts to use it for checking if there is a cross intersection
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
    else:
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
        outlier_linestrings = []
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

    

n = widthcalculation(line1, polygon1)
print("final width is: ", n)


