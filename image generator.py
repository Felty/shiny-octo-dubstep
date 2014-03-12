"""This is my attempt at creating a semi-random image generator.  The concept is shamelessly stolen from http://joco.name/2014/03/02/all-rgb-colors-in-one-image/
but lacking the constraints of the original challenge."""
from PIL import Image
from PIL import ImageDraw
from random import randint

xres = 720 		#resolution settings
yres = 480
break_out_max = 5000		#break outs are the dead-end avoidance function, more breakouts = more colored pixels
break_out_max_depth = 30	#maximum distance the break out will jump in search of blank space.  Not a complete search.
color_shift = 5		#maximum color shift between pixels.  RGB values are 0-255

im = Image.new("RGB", (xres, yres), "white")
draw = ImageDraw.Draw(im)

xmid = int(xres * 0.5)
ymid = int(yres * 0.5)
hubpixel = (xmid, ymid)

def spinner(hubpixel):
	"""Points to a pixel bordering the seed pixel"""
	spin = randint(0, 7)
	xpoint = hubpixel[0]
	ypoint = hubpixel[1]
	#The descriptions may seem off because PIL uses a coordinate system where (0,0) is the top left corner
	if spin == 0:
		#top left 
		xpoint -= 1
		ypoint -= 1

	elif spin == 1:
		#directly above
		ypoint -= 1

	elif spin == 2:
		#top right
		xpoint += 1
		ypoint -= 1

	elif spin == 3:
		#to the left
		xpoint -= 1

	elif spin == 4:
		#to the right
		xpoint += 1

	elif spin == 5:
		#bottom left
		ypoint += 1
		xpoint -= 1

	elif spin == 6:
		#directly below
		ypoint += 1

	elif spin == 7:
		#bottom right
		ypoint += 1
		xpoint += 1
	


	if xpoint in range(1, int(xres-1)) and ypoint in range(1, int(yres-1)):
		return (xpoint, ypoint)

	elif xpoint < 1:
		xpoint = 1
		return (xpoint, ypoint)
	elif xpoint >= xres-1:
		xpoint = xres-2
		return (xpoint, ypoint)
	elif ypoint < 1:
		ypoint = 1
		return (xpoint, ypoint)
	elif ypoint >= yres-1:
		ypoint = yres-2
		return (xpoint, ypoint)
	else: 
		return (xpoint, ypoint)


def choose_color(hubpixel):
	"""Generates color for new pixel and returns it as an RGB tuple"""
	RGBlst= list(im.getpixel(hubpixel)) 

	for i in range(0,3): 	
		if randint(0, 1) == 0 and RGBlst[i] <= (255 - color_shift) or RGBlst[i] <= (0 + color_shift) :     
			RGBlst[i] += randint(0, color_shift)
		else:
			RGBlst[i] -= randint(0, color_shift)
	return tuple(RGBlst)

def remaining_white(hubpixel):
	"""Cycles through each neighboring pixel and returns True if at least one is white.""" 
	xpoint = hubpixel[0]
	ypoint = hubpixel[1]
	checklist = [(xpoint-1, ypoint-1),(xpoint, ypoint-1),(xpoint+1, ypoint-1),(xpoint-1, ypoint),(xpoint+1, ypoint),(xpoint-1, ypoint+1),(xpoint, ypoint+1),
	(xpoint+1, ypoint+1)]
	checker = 8
	for i in range(0,8):
		if im.getpixel(checklist[i]) == (255, 255, 255):
			return True
			break
			checker -= 1		
	if checker == 8:
		return False

def breakout(hubpixel):
	newpixel = hubpixel
	for each in range(0, break_out_max_depth):
		newpixel = spinner(newpixel)
		if im.getpixel(newpixel) == (255, 255, 255):
			return newpixel
	else:
		for i in range(0,10):
			breakoutpixel = spinner(newpixel)
			if im.getpixel(breakoutpixel) == (255, 255, 255):
				return breakoutpixel
			else:
				return breakoutpixel


breakcount = 0
TrackingBeacon = 0
newpixel = spinner(hubpixel)

while breakcount < break_out_max:

	count = 0
	TrackingBeacon += 1
	if TrackingBeacon >= 20:
		print "Spinning around the vicinity of" + str(hubpixel)
		TrackingBeacon = 0
	
	while count < 40:
		if im.getpixel(newpixel) == (255, 255, 255): #Checking to see if the pixel is white/unpainted
			draw.point(newpixel, fill=choose_color(hubpixel)) #painting the pixel
		hubpixel = newpixel
		count += 1
	 	newpixel = spinner(hubpixel)
	 	if count % 6 == 0:
	 		for i in range(0,4):
	 			if im.getpixel(newpixel) == (255, 255, 255): 
					draw.point(newpixel, fill=choose_color(hubpixel))
				newpixel = spinner(hubpixel)
	if remaining_white(hubpixel) == False:
	 	newpixel = breakout(hubpixel)
		if breakcount % 10 == 0:
			print "BREAKOUT! " + str(breakcount) + "/" + str(break_out_max)
		breakcount += 1
	
		
	



im.save("result.png")