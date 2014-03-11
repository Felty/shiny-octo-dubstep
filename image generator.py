"""This is my attempt at creating a semi-random image generator.  The concept is shamelessly stolen from http://joco.name/2014/03/02/all-rgb-colors-in-one-image/
but lacking the constraints of the original challenge."""
from PIL import Image
from PIL import ImageDraw
from random import randint

xres = 720
yres = 480

im = Image.new("RGB", (xres, yres), "white")
draw = ImageDraw.Draw(im)

xmid = int(xres * 0.5)
ymid = int(yres * 0.5)
hubpixel = (xmid, ymid)

def Spinner(hubpixel):
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
	else:
		print "DANGER DANGER, ERROR IN THE SPINNER" #fun with debugging
		print "SPIN VALUE OF:" + str(spin)

	if xpoint in range(1, int(xres-1)) and ypoint in range(1, int(yres-1)):
		return (xpoint, ypoint)

	else: 
		print "Looks like the wall has been hit"
		print (xpoint, ypoint)
		return "Wall"


def ChooseColor(hubpixel):
	"""Generates color for new pixel and returns it as an RGB tuple"""
	RGBlst= list(im.getpixel(hubpixel)) 

	for i in range(0,3): 	
		if randint(0, 1) == 0 and RGBlst[i] <= 245 or RGBlst[i] <= 10:     
			RGBlst[i] += randint(0, 10)
		else:
			RGBlst[i] -= randint(0, 10)
	return tuple(RGBlst)

def RemainingWhite(hubpixel):
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


TrackingBeacon = 0
newpixel = Spinner(hubpixel)
while newpixel != "Wall":
	count = 0

	if TrackingBeacon >= 500:
		print "Spinning around the vicinity of" + str(hubpixel)
		TrackingBeacon = 0
	while count < 4 and newpixel != "Wall":
		if im.getpixel(newpixel) == (255, 255, 255): #Checking to see if the pixel is white/unpainted
			draw.point(newpixel, fill=ChooseColor(hubpixel)) #painting the pixel
		hubpixel = newpixel
		count += 1
	 	newpixel = Spinner(hubpixel)

	else:
		TrackingBeacon += 1
	while RemainingWhite(hubpixel) and newpixel != "Wall":
		if im.getpixel(newpixel) == (255, 255, 255): 
			draw.point(newpixel, fill=ChooseColor(hubpixel))
		newpixel = Spinner(hubpixel)
	else:
		hubpixel = newpixel #Don't delete/move this or it'll probably enter an infinite loop.
		if hubpixel != "Wall":
			newpixel = Spinner(hubpixel)
			
		else:
			break



im.save("result.png")