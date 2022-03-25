import cv2  
from PIL import Image 
import numpy as np 
import os 
from yoloface import face_analysis
import numpy
import cv2
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


pathDir='result'
paths = os.listdir(f"{pathDir}/image1") 

for path in paths: 

    with open(f'{pathDir}/txt1/{path[:-4]}.txt') as f: 
        lines = f.readlines() 
    
    lines = list(lines)
    points = list() 
    image = cv2.imread(f'{pathDir}/image1/{path}')
    imageOriginal = image.copy()
    




    for i, line in enumerate(lines): 
        line = list(line.split(","))
        x = int(len(line)/2)
        print (len(line))
    
        points.append([int(line[0]),int(line[1]),int(line[x]),int(line[x+1])])
    
        #point = midpoint((int(line[2]),int(line[3])),(int(line[6]), int(line[7])))
        #points.append(point)
    
    
    result = list()
    storePoints = list()
    out = True 
    while out: 
        process = True 
        try: 
            for i in range(len(points)): 
                for j in range(len(points)): 
                    if i == j : 
                        continue
                    else: 
                        kx = abs(points[i][1] - points[j][1])
                        #ky = abs(points[i][0] - points[j][0])
                        if kx < 150 : 
                            process = False 
                            break 
                if process == False: 
                    break 
            if process == False :
                points.pop(j)
                points[i][0] = min(points[i][0],points[j][0]) 
                points[i][1] = min(points[i][1],points[j][1])
                points[i][2] = max(points[i][2],points[j][2]) 
                points[i][3] = max(points[i][3],points[j][3]) 
                storePoints.append(points[i])
            if i == len(points) - 1 : 
                if process == True: 
                    storePoints.append(points[i])
                out = False 
        except: 
            continue
    print ( storePoints )
    
    #Process Over lap 
    points = storePoints
    storePoints = list()
    out = True 
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
    
    
    for newPoint in points : 
        
        point1 = (newPoint[0], newPoint[1]) 
        point2 = (newPoint[2], newPoint[3]) 
        
        image = cv2.circle(image, point1 , 2, (255,0,0),thickness=3 )  
        image = cv2.circle(image, point2 , 2, (255,0,0),thickness=3 )  
        cv2.rectangle(image, point1, point2, (255,0,0), thickness=3)

    _,box,conf=face.face_detection(frame_arr=image,frame_status=True,model='tiny')
    output_frame=face.show_output(image,box,frame_status=True)                    



    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    #cv2.namedWindow("original", cv2.WINDOW_NORMAL)
    cv2.imshow( "output", image )
    #cv2.imshow( "original", imageOriginal )
    cv2.waitKey()
    print ( storePoints )
#


#while (countMax >= 11 or countMax <= 3 ): 
#    if theshold == 100: 
#        process = False
#        
#        break 
#    theshold +=10
#    
#if process == True:
#
#    for newPoint in storePoints[indexMax] : 
#        image = cv2.circle(image, newPoint, 2, (255,0,0),thickness=3 )
#    print ( storePoints[indexMax][3])
#    print ( storePoints[indexMax][0])
#    x = len (storePoints[indexMax])-1
#    cv2.line(image, storePoints[indexMax][1], storePoints[indexMax][x], (255,255,0), thickness=10)
#    vectorAB = (storePoints[indexMax][x][0]-storePoints[indexMax][1][0],storePoints[indexMax][x][1]-storePoints[indexMax][1][1])
#    vectorO = (-1,0)
#    def angle_between(p1, p2):
#        ang1 = np.arctan2(*p1[::-1])
#        ang2 = np.arctan2(*p2[::-1])
#        return np.rad2deg((ang1 - ang2) % (2 * np.pi))
#    
#    
#    
#    
#    direction = -1
#    angle = angle_between(vectorO, vectorAB)
#    if angle > 90: 
#        angle = 180-angle  
#        direction = 1
#    
#    newImg = Image.fromarray(image)
#    image = np.array(newImg.rotate(direction * angle))
#    w,h,_ = image.shape 
#    print (w,h) 
    
    #b = image[:,:,1]
    #print(len(b[0]))
    #if direction == 1: 
    #    for i in  range(h): 
    #        if b[i][0] != 0:
    #            print (i)
    #            break 
    #    image=image[i:,:]
    #    image=image[:-i,:]
    #    for j in  range(w): 
    #        if b[-1][j] != 0:
    #            print(j)
    #            break 
    #    image=image[:,j:]
    #    image=image[:,:-j]
    #else: 
    #    for i in  range(h): 
    #        if b[i][-1] != 0:
    #            print(i)
    #            break 
    #    image=image[i:,:]
    #    image=image[:-i,:]
    #    for j in  range(w): 
    #        if b[0][j] != 0:
    #            print(j)
    #            break 
    #    image=image[:,j:]
    #    image=image[:,:-j]
    
    
    
    
    
#    h,w,_ = image.shape 
#    try:
#
#        cv2.namedWindow("output", cv2.WINDOW_NORMAL)
#        cv2.namedWindow("original", cv2.WINDOW_NORMAL)
#        cv2.imshow( "output", image )
#        cv2.imshow( "original", imageOriginal )
#        cv2.waitKey()
#        print ( direction )
#    except: 
#        print ("fail case except ")
#        continue
#else: 
#    print ("fail case")
#int ( points )
