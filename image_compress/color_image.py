from tabulate import tabulate
import statistics
import math
from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import pandas as pd
np.seterr(over='ignore')

#---- INPUT/OUTPUT
inputFile='lena_color_256.tif'
outputFile='lena_color_256_NEW.tif'

def beforeQuantize():
    img  = cv2.imread(inputFile, 1)
    height = img.shape[0]
    width = img.shape[1]

    blueChannel = img[:,:,0]
    blueChannel = np.array(blueChannel)
    #print("blueChannel Length: ", len(blueChannel))
    #print("blueChannel Values: ", blueChannel)
    greenChannel = img[:,:,1]
    greenChannel = np.array(greenChannel)
    #print("greenChannel Length: ", len(greenChannel))
    #print("greenChannel Values: ", greenChannel)
    redChannel = img[:,:,2]
    redChannel = np.array(redChannel)
    #print("redChannel Length: ", len(redChannel))
    #print("redChennel Values: ", redChannel)

    blue_Img = np.zeros(img.shape).astype(np.uint8)
    green_Img = np.zeros(img.shape).astype(np.uint8)
    red_Img = np.zeros(img.shape).astype(np.uint8)

    blue_Img[:,:,0] = blueChannel
    green_Img[:,:,1] = greenChannel
    red_Img[:,:,2] = redChannel

    print("Original Image Size: ", os.path.getsize(inputFile), "Bytes")

    cv2.imshow('INPUT IMAGE', img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.imshow('RedImage', red_Img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.imshow('greenImage', green_Img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.imshow('BlueImage', blue_Img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image


    #print("Original Image Value in 2D: ", img)
    numpydata = np.array(img)
    res = numpydata.flatten() # 2D array to 1D array

    #print("Oringinal Image Value In 1D", res)

    bluex = blueChannel.flatten()
    greenx = greenChannel.flatten()
    redx = redChannel.flatten()

    #print("IN 2D ARRAY")
    #print(numpydata)
    #print(" ")
    #print("IN 1D ARRAY")
    #print(res)

    li = res
    #print("Enter the Grid Size, Which should be >= 50:")
    #u = int(input("Enter the Grid: "))
    #interval = math.ceil(rang/u)
    #mid = round((interval/2), 2)
    #print("Interval: ", interval)
    #print("Midpoint: ", mid)
    #print(" ")
    #print(" ")
    #print("Length li(Total Size Of Pixel): ", li.size) #total size of Pixel of Original Image
    #print("TYPE OF li: ", type(li)) # Type Of Pixel
    return li, height, width, img, bluex, greenx, redx

def range_mid(lis):


    rang = max(lis)-min(lis)
    pp = math.ceil(rang/5)
    print("Enter the Grid Size, Which should be >=: ", pp)
    u=int(input("Enter the Grid: "))
    interval = math.ceil(rang/u)
    mid = round((interval/2), 2)
    print("Interval: ", interval)
    print("Midpoint: ", mid)
    print(" ")
    #if u2 > pp:
    #    print("Entered Grid Size, is >=:", pp)
    #    print("continue..")
    #print(" ")
    #u = int(input("Enter the Grid: "))
    #interval = math.ceil(rang/u)
    #mid = round((interval/2), 2)
    #print("Interval: ", interval)
    #print("Midpoint: ", mid)
    #print(" ")

    key = 1
    codebook = dict()
    while key<((u*u)+1):
        a=mid
        for i in range(1, u+1, 1):
            b=mid
            for j in range(1, u+1, 1):
                temp=[a, b]
                codebook.update({key: temp})
                key=key+1
                b=b+interval
            a=a+interval
    #print("CodeBook Length: ", len(codebook))

    main=[]
    tmp=[]
    for i in range(0, (len(lis)), 2):
        for j in range(2, (u*2+1), 2):
            if lis[i]<=j*mid:
                break

        for k in range(2, (u*2+1), 2):
            if lis[i+1]<=k*mid:
                break

        tmp=[j//2, k//2] #floor Value
        main.append(tmp)
    main = np.asarray(main) # main is Converted from 'list' to 'array'

    quantizeData = []
    for i in range(len(main)):
        x = (main[i][0]-1)*u+main[i][1]
        quantizeData.append(x)
    quantizeData = np.asarray(quantizeData)
    print("QuantizeData Length: ", len(quantizeData))

    midarray1 = []
    midarray2 = []
    for i in range(0, len(quantizeData), 1):
        key = quantizeData[i]
        if key in codebook:
            midarray1 = [codebook[key]]
            midarray2.extend(midarray1)

    midarray2 = np.array(midarray2) # 2D Array
    #print("midarray2 Length: ", len(midarray2))
    #print("midarray2 Values: ", midarray2)
    midarray3 = midarray2.flatten() # 2D Array to 1D Array
    midarray4 = np.array(midarray3).astype(np.uint8)
    #print("midarray4 Lenth: ", len(midarray4))
    #print("midaaray4 Values: ", midarray4)
    
    return midarray4, quantizeData

def errorImage(lis3, newimg):
    y1 = np.array(newimg)
    mid_array_1 = y1.flatten()
    errors=[]
    for i in range(0,len(lis3),3):
        s4=(pow((lis3[i]-mid_array_1[i]),2)+(pow((lis3[i+1]-mid_array_1[i+1]),2))+(pow((lis3[i+2]-mid_array_1[i+2]),2))) # Using Distance Formula
        s3=math.sqrt(s4)
        errors.append(s3)
    errors = np.asarray(errors)
	#print("Error length: ",len(error)) # Size of Error Values
    return errors


#----Calling All Function As Required-----------------------------------------------------------
var1, h1, w1, img1, blue, green, red= beforeQuantize()

print(" ")
print("Calculating Blue Pixel: ")
mid_blue, quantizeBlue = range_mid(blue)
print(" ")
print("Calculating Green Piexl: ")
mid_green, quantizeGreen = range_mid(green)
print(" ")
print("Calculating Red Pixel: ")
mid_red, quantizeRed = range_mid(red)

#----Saving Pixel Original Image in text file
with open('Colour_PixelOfOriginalImage.txt', 'w+') as file:
    for v in var1:
        file.write("%i " % v)

mid_bluex = np.ceil(np.array(mid_blue)).astype(np.uint8)
mid_blueG = mid_bluex.reshape(h1, w1)
mid_greenx = np.ceil(np.array(mid_green)).astype(np.uint8)
mid_greenG = mid_greenx.reshape(h1, w1)
mid_redx = np.ceil(np.array(mid_red)).astype(np.uint8)
mid_redG = mid_redx.reshape(h1, w1)

merged = cv2.merge([mid_redG, mid_greenG, mid_blueG])
arrCen = np.ceil(np.array(merged)).astype(np.uint8)

src2 = Image.fromarray(arrCen, mode="RGB")
src2.save(outputFile)
print('Image is Successfully Saved as file.')
print("Re Constructed Image Size: ", os.path.getsize(outputFile), "Bytes")

arrCen2 = arrCen.flatten()
error1 = errorImage(var1, arrCen2)
#print("Error Values: ", error1)

#----Correaltion & Co-efficient
bluecc = np.corrcoef(blue, mid_blue)
greencc = np.corrcoef(green, mid_green)
redcc = np.corrcoef(red, mid_red)
cc1 = np.mean(bluecc)
cc2 = np.mean(greencc)
cc3 = np.mean(redcc)
cc4 = (cc1+cc2+cc3)/3
print(" ")
print(" Correlation Co-efficient: ", cc4)
print(" ")

#----Displaying the Output Image
s = cv2.imread(outputFile, 1)
cv2.imshow('OUTPUT IMAGE', s)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(" ")
quantizeData1 = np.append(quantizeRed, quantizeGreen) # RED & GREEN
#print("Qunatize Data length: ", len(quantizeData1))
quantizeData2 = np.append(quantizeData1, quantizeBlue) #(RED, GREEN) & BLUE
#print("Qunatize Data length: ", len(quantizeData2))

#----Saving Quantized Data in text file
with open('Colour_PixelOfQuantizedData.txt', 'w+') as file:
    for qD in quantizeData2:
        file.write("%i " % qD)

#----Saving Re-Generated Pixel in text file
with open('Colour_PixelOfRe-GeneratedImage.txt', 'w+') as file:
    for aC in arrCen2:
        file.write("%i " % aC)

print("All Quantizaton details are Saved in files!")









    

