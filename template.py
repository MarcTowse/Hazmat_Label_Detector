# import the necessary packages
import numpy as np
import glob
import cv2
 
def match(image, templates, templateType):
	#default variables
	bestMatch = 0
	bestMatchName = ''

	#depending on what type required they had different properties needed for calculation
	if templateType == 'Symbol':
		crop_img = image[20:250, 120:380]
		names = ['Skull and Crossbones on Black Diamond', '1.6','Explosion','1.4',
			'Gas cylinder','1.5','Corrosive','Radioactive',
			'Oxidiser','Skull and Crossbones','flame']
		minus = 0
		threshold = 10000000
		print('Symbol:', end = ' ')
	else:
		crop_img = image[325:480, 120:380]
		names = ['4','3','5.1','7','2','5.2','8','1','6']
		minus = 1500000
		threshold = 5000000		
		print('Class:', end = ' ')
		
	a=0
	#iterate the tempaltes
	for template in templates:
		#grey and canny the tempaltes
		template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
		template = cv2.Canny(template, 50, 200)
		(tH, tW) = template.shape[:2]

		#grey the image
		grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
		found = None
	 
		# loop over the scales of the image
		for scale in np.linspace(0.2, 1.5, 30)[::-1]:
			# resize the image according to the scale, and keep track
			# of the ratio of the resizing
			resized = cv2.resize(grey, (0,0), fx = scale, fy = scale)
			r = grey.shape[1] / float(resized.shape[1])
		 
			# if the resized image is smaller than the template, then break
			# from the loop
			if resized.shape[0] < tH or resized.shape[1] < tW:
				break


			# detect edges in the resized, grayscale image and apply template
			# matching to find the template in the image
			edged = cv2.Canny(resized, 50, 200)
			result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
			(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
		 

			# if we have found a new maximum correlation value, then ipdate
			# the bookkeeping variable
			if found is None or maxVal > found[0]:
				found = (maxVal, maxLoc, r)
		
		#if this was the first template set it as the best match
		if a == 0:
			bestMatch = found[0]
			bestMatchName = names[a]
		#for classes a buffer is needed on 5.1 to stop it identifying as 1
		elif a == 2:
			temp = found[0]
			moderated = temp - minus
			if bestMatch < moderated:
				bestMatch = moderated
				bestMatchName = names[a]
		#for classes a buffer is needed on 5.2 to stop it identifying as 2
		elif a == 5:
			temp = found[0]
			moderated = temp - minus
			if bestMatch < moderated:
				bestMatch = moderated
				bestMatchName = names[a]
		else:
			if bestMatch < found[0]:
				bestMatch = found[0]
				bestMatchName = names[a]
		a = a + 1

	if bestMatch > threshold:
		print(bestMatchName)
	else:
		print('None')
