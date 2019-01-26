import cv2
import numpy as np
from fourPoint import warp
import re

def diamondDetect(img):
	##########  1  #########
	#create a default coordinates incase no diamond is found
	height,width, _ = img.shape
	pts_src = [[[height//2, 0]],[[0,width//2]],[[height//2,width]],[[height,width//2]]]

	##########  2  #########
	#convert the image to grey
	grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#apply a bilateral filter
	grey = cv2.bilateralFilter( grey, 11, 17, 17 )
	#find the canny edges of the image
	edges = cv2.Canny(grey,10, 250)
	#create a kernal
	kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( 7, 7 ) )
	#morph the image
	closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )
	#find contours in the image
	a, contours, h = cv2.findContours( edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
	

	##########  3  #########
	#for each contour calulate if its possible its a diamond
	for cont in contours:
		#ignore small contours
		if cv2.contourArea( cont ) > 5000 :
			arc_len = cv2.arcLength( cont, True )
			approx = cv2.approxPolyDP( cont, 0.05 * arc_len, True )
			#diamonds will have 4 sides
			if ( len( approx ) == 4 ):
				pts_src = np.array( approx, np.float32 )
			else : pass


	##########  4  #########
	l = []
	#convert pts_src into a string and make a = to it
	a = str(pts_src)
	#make l a list of the integers in the string (the coordinates of the diamond)
	l =re.findall(r'\d+',a)
	#change l to being a list
	l = list(map(int, l))
	
	#transform list into more desireable form
	coordinates = [(l[0],l[1]),(l[2],l[3]),(l[4],l[5]),(l[6],l[7])]
	#convert into an array
	coordinates = np.array(coordinates)
	#use the corners to warp the image
	crop = warp(coordinates, img)

	return(crop)

