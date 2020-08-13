import cv2
import numpy as np

framewidth=640
frameheight=480

cap=cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(5,150)

my_color=[[53,61,35,99,255,255],[116,86,56,179,248,255]]
my_colorvalues=[[51,255,51],[76,0,153]]  #BGR

mypoints=[]   #[x,y,id]

def findcolor(img,my_color,my_colorvalues):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newpoints=[]
    for color in my_color:
        upper=np.array(color[3:6])
        lower=np.array(color[0:3])
        mask=cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        #cv2.circle(imgResult,(x,y),10,(255,0,0),cv2.FILLED)
        cv2.circle(imgResult,(x, y),10,my_colorvalues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count +=1
        #cv2.imshow("img",mask)
        #cv2.imshow(str(color[0]),mask)

    return newpoints

def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),2)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            #print(len(approx))
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y

def drawoncanvas(mypoints,my_colorvalues):
    for point in mypoints:
        cv2.circle(imgResult, (point[0],point[1]), 10, my_colorvalues[point[2]], cv2.FILLED)

while True:
    success,img=cap.read()
    imgResult = img.copy()
    newpoints=findcolor(img,my_color,my_colorvalues)
    if len(newpoints)!=0:
        for newp in newpoints:
            mypoints.append(newp)

    if len(mypoints)!=0:
        drawoncanvas(mypoints,my_colorvalues)
    cv2.imshow("output",imgResult)
    if cv2.waitKey(1) & 0xFF== ord('q'):
        break
