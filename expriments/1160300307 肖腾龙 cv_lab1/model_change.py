"""
Created on 2018/12/1

@author: 1160300307肖腾龙
"""

import math
import struct
import numpy as np
import sys

def read_file(filename):  #读取bmp文件的像素值内容，存储在info列表中返回
    info = []
    pixel = []
    file = open(filename,"rb")
    header = file.read(54)
    info.append(header)
    s = struct.unpack('<ccIHHIIIIHHIIIIII', header)
    width = s[7]
    length = s[8]
    num = width * length
    for i in range(num):
        pixel.append(struct.unpack("<B", file.read(1))[0])
        pixel.append(struct.unpack("<B", file.read(1))[0])
        pixel.append(struct.unpack("<B", file.read(1))[0])
        info.append(pixel)
        pixel = []
    return info

def write_file(filename,header,pixel):  #根据header，pixel写bmp文件
    file = open(filename,"wb")
    file.write(header)
    for i in pixel:
        for j in i:
            file.write(struct.pack("B",j))
    file.close

def change(filename,header,pixel,matrix):       #根据不同色模型的转换矩阵，计算相应的色模型
    info = []
    temp = []
    pixel_matrix = np.mat(pixel).T
    pixel_matrix = (matrix * pixel_matrix).T
    m = pixel_matrix.tolist()
    for i in m:
        for j in i:
            if j <= 0:
                temp.append(0)
            elif j >= 255:
                temp.append(255)
            else:
                temp.append(int(j))
        info.append(temp)
        temp = []
    write_file(filename,header,info)

def change_to_yiq(string,header,pixel): #RGB -> YIQ
    filename = string + "-1160300307-YIQ.bmp"
    matrix = np.mat([[0.211, -0.523, 0.312], [0.596, -0.274, -0.322], [0.299, 0.587, 0.114]])
    change(filename, header, pixel, matrix)

def change_to_xyz(string,header,pixel): #RGB -> XYZ
    filename = string + "-1160300307-XYZ.bmp"
    matrix = np.mat([[0,0.01,0.99], [0.177,0.813,0.011], [0.49,0.31,0.2]])
    change(filename, header, pixel, matrix)


def change_to_ycbcr(string,header,pixel): #RGB -> YCbCr
    filename = string + "-1160300307-YCbCr.bmp"
    info = []
    temp = []
    matrix = np.mat([[0.4392,-0.3678,-0.0714], [-0.1482,-0.291,0.4392], [0.2568,0.5041,0.0979]])
    for i in pixel:
        m = matrix * np.mat(i).T + np.mat([128,128,16]).T
        m = m.tolist()
        for j in m:
            j[0] = j[0] * 0.6666
            if j[0] <= 0:
                temp.append(0)
            elif j[0] >= 255:
                temp.append(255)
            else:
                temp.append(int(j[0]))
        info.append(temp)
        temp = []
    write_file(filename,header,info)


def change_to_hsi(string,header,pixel):  #RGB -> HSI
    filename = string + "-1160300307-HSI.bmp"
    info = []
    temp = []
    for i in pixel:
        g = i[0]
        b = i[1]
        r = i[2]
        temp.append(int((r+g+b)/3))
        if g + r + b == 0:
            temp.append(int(1 - minimum(g, b, r) / 3))
        else:
            temp.append(int(1-minimum(g,b,r)/(g+b+r)))
        if minimum(r,g,b) == b:
            if r+g-2*b == 0:
                temp.append(int((g - b) / 2))
            else:
                temp.append(int((g-b)/(3*(r+g-2*b))))
        elif minimum(r,g,b) == r:
            if g+b-2*r == 0:
                temp.append(int((b - r) / 2))
            else:
                temp.append(int((b-r)/(3*(g+b-2*r))))
        else:
            if r+b-2*g == 0:
                temp.append(int((r - g) / 2))
            else:
                temp.append(int((r-g)/(3*(r+b-2*g))))
        info.append(temp)
        temp = []
    write_file(filename,header,info)

def minimum(a,b,c):  #返回a,b,c中的最小值
    if a <= b and a <= c:
        return a
    elif b < a and b <=c:
        return b
    else:
        return c

def get_info(filename):
    info = read_file(filename)
    result = []
    string = filename[0:-4]
    pixel = []
    header = info[0]
    for i in range(len(info)):
        if i != 0:
            pixel.append(info[i])
    result.append(string)
    result.append(header)
    result.append(pixel)
    return result

def main():
    filename = sys.argv[1]
    model = sys.argv[2]
    result = get_info(filename)
    if model == "YIQ" or model == "yiq":
        change_to_yiq(result[0],result[1],result[2])
    elif model == "HSI" or model =="hsi":
        change_to_hsi(result[0],result[1],result[2])
    elif model == "YCbCr" or model =="ycbcr":
        change_to_ycbcr(result[0],result[1],result[2])
    elif model == "XYZ" or model =="xyz":
        change_to_xyz(result[0],result[1],result[2])
    else:
        print("不支持转换成"+model+"这种格式")


if __name__ == "__main__":
    main()
