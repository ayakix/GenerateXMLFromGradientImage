#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PIL import Image

def getCenterList(_list, order=1):
    if order > 0:
        return [i for (i, x) in enumerate(_list) if x == max(_list)]
    else:
        return [i for (i, x) in enumerate(_list) if x == min(_list)]

def getHexColor(rgb):
    return '#FF' + getHexStr(rgb[0]) + getHexStr(rgb[1]) + getHexStr(rgb[2])

def getHexStr(color):
    hexStr = hex(color)[2:].upper()
    return hexStr if len(hexStr) == 2 else '0' + hexStr

def main(path):
    img = Image.open(path)
    img = img.resize((1, img.size[1]))
    img = img.convert("RGB")

    rgbs        = list(img.getdata())
    height      = len(rgbs)
    startRGB    = rgbs[0]
    endRGB      = rgbs[len(rgbs) - 1]
    centerRGB   = None
    centerIndex = 0

    rs, gs, bs = [], [], []
    for rgb in rgbs:
        rs.append(rgb[0])
        gs.append(rgb[1])
        bs.append(rgb[2])

    for i in [-1, 1]:
        centerSet = set(getCenterList(rs, i)) & set(getCenterList(gs, i)) & set(getCenterList(bs, i))
        if len(centerSet) == 0: continue
        index = list(centerSet)[0]
        if index != 0 and index != (height - 1):
            centerRGB   = rgbs[index]
            centerIndex = index

    centerStr = ""
    if centerRGB:
        centerStr = """
        android:centerColor="%s"
        android:centerY="%s"
        """ % (getHexColor(centerRGB), round(float(centerIndex) / float(height - 1), 1))


    print """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <gradient
        android:angle="270"
        android:type="linear"
        android:startColor="%s"
        android:endColor="%s"%s
        />
</shape>""" % (getHexColor(startRGB), getHexColor(endRGB), centerStr)

if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) != 2:
        print("python " + argvs[0] + " [img_path]")
    else:
        main(argvs[1])
