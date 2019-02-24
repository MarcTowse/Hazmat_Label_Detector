#Necessary Imports
import cv2
import numpy as np
from mask import colour
from ocr import ocr
from diamondDetect import diamondDetect
from template import match
import glob

#Find the templates for template matching
templatesSymbol = [cv2.imread(file) for file in glob.glob("templates/*.png")]
templatesClass = [cv2.imread(file) for file in glob.glob("templates2/*.png")]
	
#declare the types of files we want and also where we will store them
photoType = ['*.jpg','*.png','*.JPG','*.PNG']
images = []

#iterate each file type to find all desired files
for end in photoType:
	for file in glob.glob(end):
		images.append(file)

#Sort the list alphabetically
images.sort()


for image in images:
	#print the image name 
	print(image,)
	
	#read in each image
	bare_images = diamondDetect(cv2.imread(image))
	
	#resizing the images to all be the same
	bare_images = cv2.resize(bare_images, (500, 500)) 

	#convert images to HSV for colour detection
	img_hsv = cv2.cvtColor(bare_images, cv2.COLOR_BGR2HSV)
	
	#colour for top and bottom
	colour(img_hsv)
	
	#OCR for word detection
	ocrText = ocr(bare_images)

	#template matching with symbols and class differentiated by the 3rd parameter
	match(bare_images, templatesClass, 'class')
	match(bare_images, templatesSymbol, 'Symbol')
	
	#print a blank space
	print()


	
