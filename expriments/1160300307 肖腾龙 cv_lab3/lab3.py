import cv2
import numpy as np

def merge(image,image1,gray):  #图像叠加，image为原图，image1为滤波图，gray为用于判断人脸区域的灰度图
    for i in range(len(image)):
        for j in range(len(image[0])):
            for k in range(3):
                if gray[i][j] > 50:
                    temp = int(image[i][j][k]) + 2*int(image1[i][j][k])
                    image[i][j][k] = int(temp/3)
    return image

def expand(image): #膨胀算法
    length = len(image)
    width = len(image[0])
    dst = np.array([[0for i in range(width)]for j in range(length)])#存储膨胀后的图像
    for i in range(length-1): #遍历图像像素点
        for j in range(width-1):
            if i > 0 and j > 0:
                if image[i][j] > 50: #若该像素点是白色（人脸区域）则直接赋值
                    dst[i][j] = image[i][j]
                else: #若不是白色，但其八邻域像素有白色，则将其设为白色
                    judge1 = image[i][j-1] > 50 or image[i][j+1]>50 or image[i+1][j] >50 or image[i+1][j+1]>50
                    judge2 = image[i-1][j-1]>50 or image[i-1][j+1]>50 or image[i+1][j-1]>50 or image[i+1][j+1]>50
                    if judge1 or judge2:
                        dst[i][j] = 200
    return dst

def corrosion(image):
    length = len(image)
    width = len(image[0])
    dst = np.array([[200 for i in range(width)] for j in range(length)])
    for i in range(length - 1):
        for j in range(width - 1):
            if i > 0 and j > 0:
                if image[i][j] < 50:
                    dst[i][j] = image[i][j]
                else:
                    judge1 = image[i][j-1]<50 or image[i][j+1]<50 or image[i+1][j]<50 or image[i+1][j+1]<50
                    judge2 = image[i-1][j-1]<50 or image[i-1][j+1]<50 or image[i+1][j-1]<50 or image[i+1][j+1]<50
                    if judge1 or judge2:
                        dst[i][j] = 0
    return dst

def get_face(image): #根据人脸肤色的阈值，直接抠出人脸，并转为灰度图存储
    length = len(image)
    width = len(image[0])
    for i in range(length):
        for j in range(width):
            if image[i][j][0] < 160 and image[i][j][1] < 180 and image[i][j][2] < 200:
                image[i][j] = [0, 0, 0]
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    for i in range(length):
        for j in range(width):
            if gray[i][j] > 50: #为了便于判断，直接将脸区域设为200的白色
                gray[i][j] = 200
    return gray

if __name__ == "__main__":
    image = cv2.imread("graph/test.bmp")
    gray = get_face(image)  #抠人脸
    cv2.imwrite("graph/face.bmp", gray)
    for i in range(20):     #膨胀20个像素
        gray = expand(gray)
    cv2.imwrite("graph/expand.bmp",gray)
    for i in range(5):      #腐蚀5个像素
        gray = corrosion(gray)
    cv2.imwrite("graph/corrsion.bmp",gray)
    image = cv2.imread("graph/test.bmp")        #两次双边滤波
    image = cv2.bilateralFilter(src=image, d=0, sigmaColor=200, sigmaSpace=5)#第一次粗略一点，颜色范围大，空间小
    cv2.imwrite("graph/test_filter1.bmp",image)
    image = cv2.bilateralFilter(src=image, d=0, sigmaColor=60, sigmaSpace=10)#第二次细致一点，颜色范围小，空间大
    cv2.imwrite("graph/test_filter2.bmp", image)
    image = cv2.imread("graph/test.bmp")
    image1 = cv2.imread("graph/test_filter2.bmp")
    image = merge(image,image1,gray)        #图像加权叠加
    cv2.imwrite("graph/result.bmp", image)
    image = cv2.bilateralFilter(src=image, d=0, sigmaColor=60, sigmaSpace=5) #再次双边滤波
    cv2.imwrite("graph/result_final.bmp",image)


