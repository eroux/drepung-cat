import csv
import json
import os
import gzip

def getcell(boxcoords, textcoords):
    """
    returns the (rownum, colnum) of the cell associated with the textcoords
    returns (99, 0) for things outside of cells (ex: page numbers)
    """
    topleft = textcoords[0]
    idxrow = 0
    for row in boxcoords:
        idxcolcell = 0
        for colcelll in boxcoords[idxrow]:
            # strange case of empty boxes
            if len(colcelll) == 0:
                continue
            # for some reason these are double lists, we take the first (and only) element
            colcell = colcelll[0]
            if topleft["x"] >= colcell[0] and topleft["x"] <= colcell[0]+colcell[2]:
                # match on the column
                if topleft["y"] >= colcell[1] and topleft["y"] <= colcell[1]+colcell[3]:
                    return (idxrow, idxcolcell)
            idxcolcell += 1
        idxrow += 1
    return (20, 0)


def addtores(res, rownum, colnum, text):
    """
    adds text to a cell with coordinate (rownum, colnum) in res
    """
    #print("rownum=%d"%rownum)
    for i in range(0, rownum+1):
        #print("i=%d, len=%d"%(i,len(res)))
        if len(res) < i+1:
            #print("adding")
            res.append([])
    row = res[rownum]
    for i in range(0, colnum+1):
        if len(row) < i+1:
            row.append("")
    row[colnum] += text

def coordstotable(boxcoords, visionjson):
    res = []
    tas = visionjson["textAnnotations"]
    for ta in tas[1:]:
        text = ta["description"]
        vcoords = ta["boundingPoly"]["vertices"]
        (idxrow, idxcolcell) = getcell(boxcoords, vcoords)
        addtores(res, idxrow, idxcolcell, text)
    return res

def maintest():
    with open("tests/00000049.json") as vfile:
        visionjson = json.load(vfile)
        with open("tests/coords.json") as boxcoordsf:
            coordsjson = json.load(boxcoordsf)
            res = coordstotable(coordsjson, visionjson)
            print(res)

def addfile(fbasename, iglname, res):
    vpath = "vision-archive/%s/%s.json.gz" % (iglname, fbasename)
    coordpath = "coords/W28949-%s/%s.json" % (iglname, fbasename)
    if not os.path.isfile(coordpath):
        print("skip %s"%coordpath)
        return
    with gzip.open(vpath) as vfile:
        visionjson = json.load(vfile)
        with open(coordpath) as boxcoordsf:
            coordsjson = json.load(boxcoordsf)
            resfile = coordstotable(coordsjson, visionjson)
            for row in resfile:
                if len(row) < 1:
                    continue
                res.append(['%s-%s'%(iglname,fbasename)]+row)

def main():
    res = []
    for i in range(49,2101):
       basefname = "%0.8d" % i
       #print("%s" % basefname)
       addfile(basefname, "I1KG10818", res)
    for i in range(11,1701):
        basefname = "%0.8d" % i
        addfile(basefname, "I1KG10819", res)
    with open('cat.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for row in res:
            writer.writerow(row)

def testgetcell():
    vcoords = [
          {
            "x": 1370,
            "y": 248
          },
          {
            "x": 1429,
            "y": 248
          },
          {
            "x": 1429,
            "y": 343
          },
          {
            "x": 1370,
            "y": 343
          }
        ]
    boxcoords = [[[[89, 221, 264, 253]], [[358, 220, 323, 253]], [[685, 211, 1770, 261]], [[2460, 206, 899, 257]], [[3364, 204, 298, 254]], [[3667, 203, 198, 253]], [[3870, 202, 310, 253]]], [[[89, 478, 264, 196]], [[358, 477, 323, 196]], [[686, 469, 1769, 202]], [[2460, 463, 900, 200]], [[3364, 462, 298, 195]], [[3667, 460, 199, 195]], [[3870, 459, 310, 196]]], [[[88, 677, 265, 197]], [[358, 676, 322, 196]], [[685, 668, 1770, 203]], [[2460, 663, 899, 199]], [[3364, 661, 298, 196]], [[3667, 660, 198, 196]], [[3870, 659, 310, 196]]], [[[88, 878, 265, 195]], [[357, 877, 322, 195]], [[685, 868, 1771, 203]], [[2459, 863, 901, 199]], [[3364, 861, 299, 196]], [[3667, 860, 198, 195]], [[3870, 859, 310, 195]]], [[[87, 1077, 266, 197]], [[357, 1075, 323, 196]], [[685, 1067, 1771, 203]], [[2460, 1062, 900, 199]], [[3364, 1060, 299, 196]], [[3667, 1060, 198, 195]], [[3871, 1058, 309, 196]]], [[[86, 1276, 266, 198]], [[357, 1275, 323, 196]], [[684, 1266, 1772, 203]], [[2461, 1261, 899, 199]], [[3364, 1260, 299, 195]], [[3667, 1259, 199, 195]], [[3871, 1257, 309, 196]]], [[[86, 1476, 265, 197]], [[357, 1475, 322, 196]], [[683, 1466, 1773, 204]], [[2460, 1461, 900, 199]], [[3364, 1460, 299, 195]], [[3667, 1459, 199, 195]], [[3871, 1457, 309, 197]]], [[[86, 1676, 266, 233]], [[353, 1675, 325, 232]], [[680, 1666, 1776, 240]], [[2460, 1661, 900, 235]], [[3365, 1659, 299, 232]], [[3668, 1659, 198, 231]], [[3871, 1656, 309, 234]]], [[[81, 1912, 269, 261]], [[354, 1911, 322, 258]], [[681, 1902, 1774, 266]], [[2460, 1897, 901, 261]], [[3366, 1895, 298, 258]], [[3668, 1895, 199, 258]], [[3872, 1893, 308, 259]]], [[[81, 2174, 269, 261]], [[355, 2174, 320, 259]], [[678, 2164, 1777, 269]], [[2460, 2159, 901, 263]], [[3366, 2158, 298, 260]], [[3668, 2158, 199, 260]], [[3872, 2155, 308, 262]]]]
    print(getcell(boxcoords, vcoords))

#testgetcell()
main()