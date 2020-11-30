from geomet import wkt
import json
import math
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiLineString

line = LineString([(5.54984644791813331, -2.93113995998589694), (5.41443240434236017 ,-2.78049183650784926), (5.33995468037568521,-2.61460963312752703), (5.11313615738626392,-1.90368590435471829)])
polygon = Polygon([(5.0606632155006519, -1.93753941524866136), (5.17576515254005898, -1.91722730871229552), (5.42289578206584544 ,-2.71278481471996269), (5.58539263435677302 ,-2.9125205289942282), (5.5143002614794927, -2.95991544424574915), (5.34841805809917048, -2.75679437888208945), (5.24685752541734018, -2.50627839826690879), (5.0606632155006519 ,-1.93753941524866136)])
print(line)
print(polygon)
line22 = LineString([(4.98653654815829395, -7.49880555340785193), (5.01271375913349893, -5.79074253727571175), (5.47081495119959094, -5.58132484947407015), (6.64224514234002328, -5.78419823453191029), (7.02835900422430093, -6.41899560068063657)])
polygon22 = Polygon ([(4.7640302548690503, -7.45299543420124344), (4.81638467681946025, -5.79728684001951322), (5.40537192376157805, -5.37190716167242854), (6.73386538075324204, -5.58786915221787162), (7.23123238928214107 ,-6.49752723360625239), (6.81894131642265933 ,-6.53024874732525884), (6.45900466551358754, -5.91508428940793607), (5.4773592539433924, -5.699122298862493), (5.20249853870373702, -5.98052731684594896), (5.24176435516654493, -7.61660300279627478), (4.7640302548690503, -7.45299543420124344)])
#print(line22)
#print(line22.length)
#print(polygon22)


def cutlinetoten(line):
    tenlines = []
    line1 = LineString([line.interpolate(0, normalized = True), line.interpolate(0.1, normalized = True)])
    line2 = LineString([line.interpolate(0.1, normalized = True), line.interpolate(0.2, normalized = True)])
    line3 = LineString([line.interpolate(0.2, normalized = True), line.interpolate(0.3, normalized = True)])
    line4 = LineString([line.interpolate(0.3, normalized = True), line.interpolate(0.4, normalized = True)])
    line5 = LineString([line.interpolate(0.4, normalized = True), line.interpolate(0.5, normalized = True)])
    line6 = LineString([line.interpolate(0.5, normalized = True), line.interpolate(0.6, normalized = True)])
    line7 = LineString([line.interpolate(0.6, normalized = True), line.interpolate(0.7, normalized = True)])
    line8 = LineString([line.interpolate(0.7, normalized = True), line.interpolate(0.8, normalized = True)])
    line9 = LineString([line.interpolate(0.8, normalized = True), line.interpolate(0.9, normalized = True)])
    line10 = LineString([line.interpolate(0.9, normalized = True), line.interpolate(1, normalized = True)])
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
    leftline = line.parallel_offset(3, 'left')
    rightline = line.parallel_offset(3, 'right')
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
    return prependicular_line



def widt(prepedicularline, polygon, roadline):
    #prependicular line between 2 offsets intersects polygon
    ln = prepedicularline.intersection(polygon)
    #if returns 2 or more linestrings we need to find the one that intersects the roadline
    if ln.type == 'MultiLineString':
        ll = list(ln)
        for i in ll:
            if i.intersects(roadline):
                measureline = i
                w = measureline.length
                print(measureline)
    else:
        w = ln.length
        print(ln)
    return w

def avgwidth(w):
    s = 0
    for i in w:
        s += i
    avg = s / len(w)
    return avg

def widthcalculation(line, polygon):
    tenlines = cutlinetoten(line)
    w = []
    for i in tenlines:
        prep_line = makeoffsets(i)
        width = widt(prep_line, polygon, i)
        w.append(width)
    m = avgwidth(w)
    s = 0
    for ii in w:
        d = (ii - m) ** 2
        s += d
    std = math.sqrt(s/10)
    for iii in w:
        if abs(m-iii) > std :
            w.remove(iii)
    n = avgwidth(w)
    return n

    

n = widthcalculation(line,polygon)
print(n)
print(line.length)

