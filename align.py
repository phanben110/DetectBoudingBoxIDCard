import cv2  
from PIL import Image 
import numpy as np 
import os 

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
paths = os.listdir(f"{pathDir}/image") 

for path in paths: 

    with open(f'{pathDir}/txt/{path[:-4]}.txt') as f: 
        lines = f.readlines() 
    
    lines = list(lines)
    points = list() 
    image = cv2.imread(f'{pathDir}/image/{path}')
    imageOriginal = image.copy()
    
    for i, line in enumerate(lines): 
        line = list(line.split(","))
        point = midpoint((int(line[2]),int(line[3])),(int(line[6]), int(line[7])))
        points.append(point)
    countMax = 0  
    theshold = 10
    process = True
    while (countMax >= 11 or countMax <= 3 ): 
        if theshold == 100: 
            process = False
            
            break 
        result = list()
        storePoints = list()
        for i in range(len(points)): 
            count = 0 
            localPoints = list()
            localPoints.append(points[i])
            for j in range(len(points)): 
                kx = abs(points[i][1] - points[j][1])
                ky = abs(points[i][0] - points[j][0])
        
                if kx < theshold and ky < 600: 
                    count +=1 
                    localPoints.append(points[j])
            result.append ( count )
            storePoints.append(localPoints)
        
        countMax = max(result) 
        indexMax = result.index(countMax)
        print ( countMax )
        print (theshold)
        theshold +=10
        
    if process == True:

        for newPoint in storePoints[indexMax] : 
            image = cv2.circle(image, newPoint, 2, (255,0,0),thickness=3 )
        print ( storePoints[indexMax][3])
        print ( storePoints[indexMax][0])
        x = len (storePoints[indexMax])-1
        cv2.line(image, storePoints[indexMax][1], storePoints[indexMax][x], (255,255,0), thickness=10)
        vectorAB = (storePoints[indexMax][x][0]-storePoints[indexMax][1][0],storePoints[indexMax][x][1]-storePoints[indexMax][1][1])
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
        
        
        
        
        
        h,w,_ = image.shape 
        try:

            cv2.namedWindow("output", cv2.WINDOW_NORMAL)
            cv2.namedWindow("original", cv2.WINDOW_NORMAL)
            cv2.imshow( "output", image )
            cv2.imshow( "original", imageOriginal )
            cv2.waitKey()
            print ( direction )
        except: 
            print ("fail case except ")
            continue
    else: 
        print ("fail case")
##print ( points )
