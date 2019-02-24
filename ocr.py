import cv2
import numpy as np
from PIL import Image 
import os
import pytesseract
import string
from difflib import SequenceMatcher

#list of the possible texts found on the hazmat labels
words = ['CORROSIVE','RADIOACTIVE I','RADIOACTIVE II', 'RADIOACTIVE III', 'RADIOACTIVE',
	'INHALATION HAZARD', 'POISON', 'ORGANIC PEROXIDE', 'OXIDZER', 'EXPLOSIVE', 'POISONOUS GAS',
	'BLASTING AGENT', 'FLAMMABLE GAS', 'NON FLAMMABLE GAS', 'FLAMMABLE LIQUID', 'DANGEROUS WHEN WET',
	'SPONTANEOUSLY COMBUSTIBLE', 'COMBUSTIBLE', 'FLAMMABLE', 'FUEL OIL', 'GASOLINE', 'TOXIC']

def ocr(image):
	#preprocessing to help tesseract with OCR
	grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	grey = cv2.threshold(grey, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	grey = cv2.medianBlur(grey, 3)
	
	#create a new image for tesseract to use
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, image)
	
	#run tesseract with a restriction on whitelisted charcters
	text = pytesseract.image_to_string(Image.open(filename), config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 6")
	
	#remove the new file
	os.remove(filename)

	#remove new line characters
	text = text.replace('\n',' ')
	
	#compare each of the OCR'd words with the database 
	newText = text
	bestMatch = 0
	for word in words:
		match = SequenceMatcher(a=text,b=word).ratio()
		if match > bestMatch:
			bestMatch = match
			newText = word
	if bestMatch > 0.2:
		print ('text:',newText)
	else:
		print('text: None')

