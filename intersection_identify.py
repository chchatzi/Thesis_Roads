from geomet import wkt
import json
import math
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas

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
#checkforcross also checks if there is a T intersection 
def checkforcross(twentylines, roadline):
    '''this function takes the measuring lines that are not empty with their widths and checks for cross intersection
    the main condition is the value of the mean of the values that located in the center of the line to be 2 times higher than the 2 other means
    the one for the first 3 lines and the one of the last 3 lines. If that is the case then the road is tested if it is T intersection as well'''

    #print("this is the number of the actual widths: ", len(twentylines))
    if len(twentylines) > 19:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]]#, twentylines[3], twentylines[4], twentylines[5]]
        mid = [twentylines[7][0], twentylines[8][0], twentylines[9][0], twentylines[10][0], twentylines[11][0], twentylines[12][0]]
        last = [twentylines[17][0], twentylines[18][0], twentylines[19][0]]
    elif len(twentylines) > 18:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]] #, twentylines[3], twentylines[4], twentylines[5]]
        mid = [twentylines[7][0], twentylines[8][0], twentylines[9][0], twentylines[10][0], twentylines[11][0], twentylines[12][0]]
        last = [twentylines[16][0], twentylines[17][0], twentylines[18][0]]

    elif len(twentylines) > 17:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]] #, twentylines[3], twentylines[4], twentylines[5]]
        mid = [twentylines[6][0],twentylines[7][0], twentylines[8][0], twentylines[9][0], twentylines[10][0], twentylines[11][0], twentylines[12][0]]
        last = [twentylines[15][0], twentylines[16][0], twentylines[17][0]]
        
    f = avgwidth2(first)
    m = avgwidth2(mid)
    l = avgwidth2(last)
    print(f, "",m, "", l)
    #print(twentylines[0][1])
    #print(twentylines[1][1])
    #print(twentylines[2][1])
    #print(twentylines[7][1])
    #print(twentylines[8][1])
    #print(twentylines[9][1])
    #print(twentylines[10][1])
    #print(twentylines[11][1])
    #print(twentylines[12][1])
    #print(twentylines[17][1])
    #print(twentylines[18][1])
    #print(twentylines[19][1])
    if m>f*2 and m>l*2:
        #check if it is a T intersection case1
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
        #print(end8one,end8tow)
        #print(end9one,end9tow)
        #print(end10one,end10tow)
        #print(end11one,end11tow)
        #find the midpoints of the road lines that are in line with the 4 mid lines
        line9 = LineString([roadline.interpolate(0.4, normalized = True), roadline.interpolate(0.45, normalized = True)])
        line10 = LineString([roadline.interpolate(0.45, normalized = True), roadline.interpolate(0.5, normalized = True)])
        line11 = LineString([roadline.interpolate(0.5, normalized = True), roadline.interpolate(0.55, normalized = True)])
        line12 = LineString([roadline.interpolate(0.55, normalized = True), roadline.interpolate(0.6, normalized = True)])
        mid9 = line9.interpolate(0.5, normalized = True)
        #print(mid9)
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
            if (dif11start - dif11end) > dif11end:
                differences.append(1)
        elif (dif11start-dif11end) < 0:
            if dif11end-dif11start > dif11start:
                differences.append(1)

        if len(differences) >= 3:
            print("there is a T intersection")
            bool_val = True
            lst = [bool_val, "T"]
            return lst
        else:
            print("there is a cross intersection")
            bool_val = True
            lst = [bool_val, "C"]
            return lst
    else :
        print("passes the test for cross intersection!")
        return False, "aoua"

#this function checks also for T intersection  BUT 
def checkforTcase2(twentylines, roadline):
    #print("it passes the test for cross intersection i am checking for T intersection of case 2")
    if len(twentylines) > 19:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]]#, twentylines[3], twentylines[4], twentylines[5]]
        mid = [twentylines[7][0], twentylines[8][0], twentylines[9][0], twentylines[10][0], twentylines[11][0], twentylines[12][0]]
        last = [twentylines[17][0], twentylines[18][0], twentylines[19][0]]
    elif len(twentylines) > 18:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]] #, twentylines[3], twentylines[4], twentylines[5]]
        mid = [twentylines[7][0], twentylines[8][0], twentylines[9][0], twentylines[10][0], twentylines[11][0], twentylines[12][0]]
        last = [twentylines[16][0], twentylines[17][0], twentylines[18][0]]
    elif len(twentylines) > 17:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]] #, twentylines[3], twentylines[4], twentylines[5]]
        mid = [twentylines[6][0],twentylines[7][0], twentylines[8][0], twentylines[9][0], twentylines[10][0], twentylines[11][0], twentylines[12][0]]
        last = [twentylines[15][0], twentylines[16][0], twentylines[17][0]]
    f = avgwidth2(first)
    m = avgwidth2(mid)
    l = avgwidth2(last)
    #print(f, "",m, "", l)
    if m>f*1.5 and m>l*1.5:
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

        if len(differences) >= 2:
            print("there is a T intersection case2")
            return True
        else:
            print("the road is wider in the middle but is not T intersection or cross intersection")
            return False
    else :
        return False

def checkforTmaincase(twentylines, roadline):
    print("it passed the test for T intersection of case 1 and 2, checking for T intersection Main case!")
    if len(twentylines) > 19:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0], twentylines[3][0]]
        last = [twentylines[17][0], twentylines[18][0], twentylines[19][0]]
    elif len(twentylines) > 18:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0], twentylines[3][0]] 
        last = [twentylines[16][0], twentylines[17][0], twentylines[18][0]]
    elif len(twentylines) > 17:
        first = [twentylines[0][0], twentylines[1][0], twentylines[2][0]] #, twentylines[3], twentylines[4], twentylines[5]]
        last = [twentylines[15][0], twentylines[16][0], twentylines[17][0]]      
    f = avgwidth2(first)
    l = avgwidth2(last)
    print("first lines mean: ", f, " " "and last lines mean: ", l)
    if  f > 3*l or l> 3*f:
        print("Main case of T intersection")
        return True
    else:
        print("it passes the test for T main case intersection")
        return False

