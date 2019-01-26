# import the necessary packages
import numpy as np
import cv2
import re

def order_points(pts):
	#create the new shuffled points array
	rect = np.zeros((4, 2), dtype = "float32")

	########   1   ########	
	b = 0
	#for loop will first do the x values and then the y values
	for a in (0,1):
		#retrieve the required values (x or y)
		string = str(pts[0:,a])
		#convert them into a list
		l =re.findall(r'\d+',string)
		l = list(map(int, l))
		#find the min and max value
		maxVal = max(l)
		minVal = min(l)
		#find the index of these min and max values
		maxIndex = l.index(maxVal)
		minIndex = l.index(minVal)
		#for x the min and max will be the left and right points respectively
		#for y the min and max will be the top and bottom poitns respectively
		#using this we can warp the diamond accordingly
		rect[b] = pts[maxIndex]
		rect[b+1] = pts[minIndex]
		#first run 0,1 second run +2 is 2,3 therefore rect[0,1,2,3] (the 4 corners
		b = b + 2
		
	return rect

def four_point_transform(image, pts):
	
	#map which points go where
	rect = order_points(pts)
	(tr, bl, br, tl) = rect
 
	#using the points figure out the width of the new image
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
 
	#using the points figure out the width of the new image
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
 
	# this provides the new position of the points
	dst = np.array([
		[maxWidth - 1, 0],
		[0, maxHeight - 1],
		[maxWidth - 1, maxHeight - 1],
		[0, 0]], dtype = "float32")
		
 	########   2   ########
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	
	# return the warped image
	return warped

def rotateAndScale(img, scaleFactor = 1.5, degreesCCW = -45):
	#find the rotation matrix
    oldY,oldX, a = img.shape 
    M = cv2.getRotationMatrix2D(center=(oldX/2,oldY/2), angle=degreesCCW, scale=scaleFactor) #rotate about center of image.

    #choose a new image size.
    newX,newY = oldX*scaleFactor,oldY*scaleFactor
    #prevent corners being cut off
    r = np.deg2rad(degreesCCW)
    newX,newY = (abs(np.sin(r)*newY) + abs(np.cos(r)*newX),abs(np.sin(r)*newX) + abs(np.cos(r)*newY))

    #move image to the centre
    (tx,ty) = ((newX-oldX)/2,(newY-oldY)/2)
    M[0,2] += tx 
    M[1,2] += ty
    
	########   3   ########
	#rotate the image while maintaining its full size
    rotatedImg = cv2.warpAffine(img, M, dsize=(int(newX),int(newY)))
    return rotatedImg
    
def warp(pts2, image):
	warped = four_point_transform(image, pts2)
	result = rotateAndScale(warped)
	return(result)
