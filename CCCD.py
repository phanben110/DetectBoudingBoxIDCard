import cv2  
from PIL import Image 
import numpy as np 
import os 
from yoloface import face_analysis
import numpy
import cv2
import math
face=face_analysis()               


def midpoint(pointA, pointB): 
    return (int((pointA[0]+pointB[0])/2),int((pointA[1]+pointB[1])/2))
def distanceFromCtoAB(TABLE,C):
	xa = TABLE[0][0]
	ya = TABLE[0][1]
	xb = TABLE[1][0]
	yb = TABLE[1][1]
	xc = C[0]
	yc = C[1]
	a = abs((ya-yb)*xc+(xb-xa)*yc-xa*(ya-yb)-ya*(xb-xa))/ ma.sqrt(xc*xc + yc*yc)
	# print("CH")
	# print(a)
	return abs((ya-yb)*xc+(xb-xa)*yc-xa*(ya-yb)-ya*(xb-xa))/ ma.sqrt(xc*xc + yc*yc)

def calculateDistance(points):
    x1,y1,x2,y2 = points 
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

pathDir='result'
paths = os.listdir(f"{pathDir}/CCCD") 

for path in paths: 

    with open(f'{pathDir}/txt1/{path[:-4]}.txt') as f: 
        lines = f.readlines() 
    
    lines = list(lines)
    points = list() 
    image = cv2.imread(f'/home/pcwork/ai/ftech/DeepFake/CMND/visual_phone_crop_binary/{path[4:]}')

    imageOriginal = image.copy()
    



    distances = list()
    pointx = list()
    pointy = list()
    for i, line in enumerate(lines): 
        line = list(line.split(","))
        x = int(len(line)/2)
        print (len(line))
             
        points.append([int(line[0]),int(line[1]),int(line[2]),int(line[3])])         
        pointx.append(int(line[0]))
        pointx.append(int(line[2]))
        pointy.append(int(line[3]))
        pointy.append(int(line[x+1]))
        dist = calculateDistance([int(line[0]),int(line[1]),int(line[2]),int(line[3])])
        distances.append(dist)
    maxDis = max(distances)
    index = distances.index(maxDis)
    points = points[index]
    minPointx= min(pointx)
    minPointy=min(pointy)
    maxPointx = max(pointx)
    maxPointy = max(pointy)
        
    point1 = (points[0], points[1]) 
    point2 = (points[2], points[3]) 
    
    image = cv2.circle(image, point1 , 2, (255,0,0),thickness=3 )  
    image = cv2.circle(image, point2 , 2, (255,0,0),thickness=3 )  
    #cv2.line(image, point1, point2, (255,0,0), thickness=3)

    vectorAB = (points[2]-points[0],points[3]-points[1])
    vectorO = (-1,0)
    def angle_between(p1, p2):
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return np.rad2deg((ang1 - ang2) % (2 * np.pi))
    
    
    
    
    direction = -1
    angle = angle_between(vectorO, vectorAB)
    if angle > 90: 
        angle = 180-angle  
        direction = 1
    
    newImg = Image.fromarray(image)
    image = np.array(newImg.rotate(direction * angle))
    w,h,_ = image.shape 
    print (w,h) 


    _,box,conf=face.face_detection(frame_arr=image,frame_status=True,model='tiny')


    from math import cos, sin

    import numpy as np

    theta = np.deg2rad(-direction*angle)

    rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])

    v2 = np.array([maxPointx, maxPointy])

    #v2 = np.dot(rot, v2) 
    #pointx = int (v2[0])
    #pointy = int (v2[1])
    #w2 = np.dot(rot, w)


    if len(box) > 0: 

        print ( box  )
        area = box[0][2]*box[0][3]/10000
        print (area)
        w,h,_ = image.shape
        box[0][0] = box[0][0]
        box[0][1] = box[0][1]
        box[0][2] = box[0][2] 
        box[0][3] = box[0][3] 
        if minPointx <= box[0][0] : 
            minPointx = minPointx + int(area)*2
            x =  box[0][0] - minPointx
            pointA = (minPointx-int(area)*2,box[0][1]-x) 
            #pointA = (box[0][0],box[0][1]) 
            #pointB = (box[0][0]+box[0][3]+x,box[0][1]+box[0][2]+x)
            pointB = (box[0][0]+box[0][3]+x,maxPointy)
            pointC = (pointB[0] + int(area), pointA[1] )  
            pointD = (int(h - h/18), maxPointy )

            pointQR1 = ( int(h*0.78), minPointy )                                       
            pointQR2 = ( pointD[0], pointA[1] - int(w*0.05)  )
            cv2.rectangle(image, pointQR1, pointQR2, (0,255,0), thickness=5)

            
            cv2.rectangle(image, pointA, pointB, (0,0,255), thickness=5)
            cv2.rectangle(image, pointC, pointD, (255,0,0), thickness=5)
            classify = True
            print ("fron face")
        else : 
            print("error")
            continue
    else: 
        print ("back face")
        w,h,_ = image.shape
        print ( w,h )

        if minPointx < w/4:
            pointA = (minPointx, minPointy)
            pointB = (int(h/1.9), int(w/4))
            cv2.rectangle(image, pointA, pointB, (0,0,255), thickness=5)
            pointC = (pointB[0]+30, minPointy) 
            pointD = (maxPointx + 60, int(w/2)) 
            cv2.rectangle(image, pointC, pointD, (0,255,0), thickness=5)
            pointE = (minPointx, int(w*0.68)) 
            pointF = (maxPointx, maxPointy )  
            cv2.rectangle(image, pointE, pointF, (255,0,0), thickness=5)
            classify = False 
        else: 
            print("error")
            continue



    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.namedWindow("original", cv2.WINDOW_NORMAL)
    cv2.imshow( "output", image )
    cv2.imshow( "original", imageOriginal )
    cv2.waitKey()


        #point = midpoint((int(line[2]),int(line[3])),(int(line[6]), int(line[7])))
        #points.append(point)
    
    
    #result = list()
    #storePoints = list()
    #out = True 
    #while out: 
    #    process = True 
    #    try: 
    #        for i in range(len(points)): 
    #            for j in range(len(points)): 
    #                if i == j : 
    #                    continue
    #                else: 
    #                    kx = abs(points[i][1] - points[j][1])
    #                    #ky = abs(points[i][0] - points[j][0])
    #                    if kx < 150 : 
    #                        process = False 
    #                        break 
    #            if process == False: 
    #                break 
    #        if process == False :
    #            points.pop(j)
    #            points[i][0] = min(points[i][0],points[j][0]) 
    #            points[i][1] = min(points[i][1],points[j][1])
    #            points[i][2] = max(points[i][2],points[j][2]) 
    #            points[i][3] = max(points[i][3],points[j][3]) 
    #            storePoints.append(points[i])
    #        if i == len(points) - 1 : 
    #            if process == True: 
    #                storePoints.append(points[i])
    #            out = False 
    #    except: 
    #        continue
    #print ( storePoints )
    #
    ##Process Over lap 
    #points = storePoints
    #storePoints = list()
    #out = True 
    #while out: 
    #    process = True 
    #    for i in range(len(points)): 
    #        for j in range(len(points)): 
    #            if i == j : 
    #                continue
    #            else: 
    #                #ky = abs(points[i][0] - points[j][0])
    #                if points[j][3] >= points[i][1] and points[j][3] <= points[i][3] :
    #                    process = False 
    #                    break 
    #        if process == False: 
    #            break 
    #    if process == False :
    #        points[i][0] = min(points[i][0],points[j][0]) 
    #        points[i][1] = min(points[i][1],points[j][1])
    #        points[i][2] = max(points[i][2],points[j][2]) 
    #        points[i][3] = max(points[i][3],points[j][3]) 
    #        storePoints.append(points[i])
    #        points.pop(j)
    #        if i == len(points) - 1 : 
    #            points.pop(i)
    #            
    #    if i == len(points) - 1 : 
    #        out = False 
