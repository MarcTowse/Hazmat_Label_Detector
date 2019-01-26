import numpy as np
import numpy as np
import cv2

def colour(image):
	#boundaries for the colours
	boundaries = [([10,50,50],[19,256,256]),
		([100,50, 50],[120,256,256]),
		([19,50,50],[30,256,256]),
		([170,50,50],[181,256,256]),
		([0,50,50],[10,256,256]),
		([70,50,50],[90,256,256]),
		([-1,-1,230],[181,10,256]),
		([-1,-1,-1],[181,50,50])
	]
	
	#names of the colorus
	colours = ['orange', 'blue', 'yellow', 'red2', 'red', 'green', 'white', 'black']

	def execute(image):
		i = 0
		red = 0
		for (lower,upper) in boundaries:
			lower = np.array(lower)
			upper = np.array(upper)
			
			#mask the required region then count how many of that colour range was found
			mask = cv2.inRange(image, lower, upper)
			output = cv2.bitwise_and(image, image, mask = mask)
			match = cv2.countNonZero(mask)
			#conver to a percent of the diamond size/2
			percent = match/62500
			
			#red contains 2 boundaries so i == 3 and i == 4 sorts this
			if i == 3:
				red2 = percent
				percent = 0
			if i == 4:
				percent = percent + red2
			#since the background is black simply removing 100% from it will counteract this
			if i == 7:
				percent = percent - 1 
			if percent > 0.6:
				return(colours[i])
			i = i + 1

	#calculate the top half colour then the bottom half
	colour_top = execute(image[0:image.shape[0]//2])
	colour_bot = execute(image[image.shape[0]//2:image.shape[0]])
	
	#print the colours
	print ('top:', colour_top)
	print ('bot:', colour_bot)
