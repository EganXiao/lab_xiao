"""
Created on 2018/12/10

@author: 1160300307肖腾龙
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

def draw(filename):  #输入图片文件路径，画出R，G，B三种颜色的统计直方图
    image = cv2.imread(filename)
    image = image.tolist()
    size = 20000
    r = []
    b = []
    g = []
    for i in image:
        for j in i:
            b.append(j[0])
            g.append(j[1])
            r.append(j[2])
    draw_histogram(r, size, "r_histogram")
    draw_histogram(g, size, "g_histogram")
    draw_histogram(b, size, "b_histogram")

def draw_histogram(list,size,title): #传入需要统计的数值列表，即可画出其统计直方图
    plt.hist(list,100)
    plt.xlabel("pixel")
    plt.ylabel("number")
    plt.xlim(0,255)
    plt.ylim(0,size)
    plt.title(title)
    plt.show()

def file_close(string):
    image = middle_filter(string)
    filename = string[0:-4] + "middle_filter_fast.bmp"
    cv2.imwrite(filename, image)

def adjustment(filename):
    image = cv2.imread(filename)
    hls = cv2.cvtColor(image,cv2.COLOR_RGB2HLS)
    luminance_adjust(hls)
    saturability_adjust(hls)
    chroma_adjust(hls)

def luminance_adjust(hls): #亮度调整
    for i in hls:
        for j in i:
            if j[1] <= 100:
                j[1] = 0
            elif j[1] >= 200 and j[1] <= 220:
                j[1] = j[1] + 30
    image = cv2.cvtColor(hls,cv2.COLOR_HLS2RGB)
    cv2.imwrite("L_adjust.bmp",image)

def saturability_adjust(hls): #饱和度调整
    for i in hls:
        for j in i:
            if j[2] <= 100:
                j[2] = int(j[2]*2)
            elif j[2] >= 100 and j[2] <= 250:
                j[2] = int(j[2]/2)
    image = cv2.cvtColor(hls,cv2.COLOR_HLS2RGB)
    cv2.imwrite("S_adjust.bmp",image)

def chroma_adjust(hls): #色度调整
    for i in hls:
        for j in i:
            if j[0] <= 100:
                j[0] = 0
            elif j[0] >= 100 and j[0] <= 150:
                j[0] = j[0] + 100
    image = cv2.cvtColor(hls, cv2.COLOR_HLS2RGB)
    cv2.imwrite("H_adjust.bmp", image)

def middle_filter(filename): #中值滤波
    string = filename[0:-4] + "middle_filter.bmp"
    image = cv2.imread(filename)
    length = len(image)
    width = len(image[0])
    temp = []
    for i in range(length):
        for j in range(width):
            if i >= 1 and i <= length-2 and j >= 1 and j <= width-2:
                for k in range(3):
                    temp.append(image[i-1][j-1][k])
                    temp.append(image[i-1][j][k])
                    temp.append(image[i-1][j+1][k])
                    temp.append(image[i][j-1][k])
                    temp.append(image[i][j][k])
                    temp.append(image[i][j+1][k])
                    temp.append(image[i+1][j-1][k])
                    temp.append(image[i+1][j][k])
                    temp.append(image[i+1][j+1][k])
                    temp.sort()
                    image[i][j][k] = temp[4]
                    temp = []
    cv2.imwrite(string, image)
    return image

def average_filter(filename): #均值滤波
    string = filename[0:-4] + "average_filter.bmp"
    image = cv2.imread(filename)
    length = len(image)
    width = len(image[0])
    for i in range(length):
        for j in range(width):
            if i >= 1 and i <= length-2 and j >= 1 and j <= width-2:
                for k in range(3):
                    pixel_1 = int(image[i-1][j-1][k]/3 + image[i-1][j][k]/3 + image[i-1][j+1][k]/3)
                    pixel_2 = int(image[i][j-1][k]/3 + image[i][j][k]/3 + image[i][j+1][k]/3)
                    pixel_3 = int(image[i+1][j-1][k]/3 + image[i+1][j][k]/3 + image[i+1][j+1][k]/3)
                    image[i][j][k] = int((pixel_1+pixel_2+pixel_3)/3)
    cv2.imwrite(string,image)

def robert_border_detection(filename): #Robert算子边缘检测
    string = filename[0:-4] + "robert_border_detection.bmp"
    image = cv2.imread(filename)
    length = len(image)
    width = len(image[0])
    for i in range(length):
        for j in range(width):
            if i >= 1 and i <= length - 2 and j >= 1 and j <= width - 2:
                for k in range(3):
                    sub_1 = abs(int(image[i-1][j-1][k]) - int(image[i+1][j+1][k]))
                    sub_2 = abs(int(image[i-1][j+1][k]) - int(image[i+1][j-1][k]))
                    if maxmum(sub_1,sub_2) > 200:
                        image[i][j][k] = 0
                    else:
                        image[i][j][k] = 255
    cv2.imwrite(string, image)

def maxmum(a,b):
    if a >= b:
        return a
    else:
        return b

def sobel_border_detection(filename): #sobel算子边缘检测
    string = filename[0:-4] + "sobel_border_detection.bmp"
    image = cv2.imread(filename)
    length = len(image)
    width = len(image[0])
    for i in range(length):
        for j in range(width):
            if i >= 1 and i <= length - 2 and j >= 1 and j <= width - 2:
                for k in range(3):
                    sum_1 = int(image[i-1][j-1][k]) + 2*int(image[i-1][j][k]) + int(image[i-1][j+1][k])
                    sum_2 = int(image[i+1][j-1][k]) + 2*int(image[i+1][j][k]) + int(image[i+1][j+1][k])
                    sum_3 = int(image[i-1][j-1][k]) + 2*int(image[i][j-1][k]) + int(image[i+1][j-1][k])
                    sum_4 = int(image[i-1][j+1][k]) + 2*int(image[i][j+1][k]) + int(image[i+1][j+1][k])
                    sobel = (abs(sum_1 - sum_2) + abs(sum_3 - sum_4))/8
                    if sobel >= 150:
                        image[i][j][k] = 0
                    else:
                        image[i][j][k] = 255
    cv2.imwrite(string, image)

def middle_filter_fast(filename):  #中值滤波快速算法
    string = filename[0:-4] + "middle_filter_fast.bmp"
    image = cv2.imread(filename)
    length = len(image)
    width = len(image[0])
    for k in range(3):
        for i in range(length):
            for j in range(width):
                if i >= 1 and i <= length - 2 and j >= 1 and j <= width - 2:
                    if j == 1:
                        temp = []
                        temp.append(image[i-1][0][k])
                        temp.append(image[i-1][1][k])
                        temp.append(image[i-1][2][k])
                        temp.append(image[i][0][k])
                        temp.append(image[i][1][k])
                        temp.append(image[i][2][k])
                        temp.append(image[i+1][0][k])
                        temp.append(image[i+1][1][k])
                        temp.append(image[i+1][2][k])
                        temp.sort()
                        chain = Chain_list(temp)
                        image[i][j][k] = chain.get_middle()
                    else:
                        chain.delete(image[i-1][j-2][k])
                        chain.delete(image[i][j-2][k])
                        chain.delete(image[i+1][j-2][k])
                        chain.add(image[i-1][j+1][k])
                        chain.add(image[i][j+1][k])
                        chain.add(image[i+1][j+1][k])
                        image[i][j][k] = chain.get_middle()
    cv2.imwrite(string, image)
    file_close(filename)

class Chain_list(object): #定义中值滤波快速算法所需要的数据结构
    def __init__(self,chain):
        self.list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(chain)):
            self.list[i] = chain[i]

    def delete(self,num):
        for i in range(len(self.list)):
            if self.list[i] == num:
                del self.list[i]
                self.list.append(0)
                self.list.sort()

    def add(self,num):
        self.list.append(num)
        self.list.sort()
        del self.list[0]
        self.list.sort()

    def get_middle(self):
        return self.list[4]

if __name__ == "__main__":
    adjustment("test.bmp")
    draw("test.bmp")
    average_filter("noise1.bmp")
    middle_filter("noise1.bmp")
    average_filter("noise2.bmp")
    middle_filter("noise2.bmp")
    robert_border_detection("test.bmp")
    sobel_border_detection("noise2.bmp")
    middle_filter_fast("noise2.bmp")


