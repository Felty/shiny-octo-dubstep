"""Making an image with every RGB color used once, the dumb way."""
from PIL import Image
from PIL import ImageDraw
from random import randint
import time

xres = 400
yres = 400
startPos = (int(xres*.5), int(yres *.5))


im = Image.new("RGBA", (xres, yres), (0,0,0,0))
draw = ImageDraw.Draw(im)

unusedCoords = []
for x in range(0, xres):
	for y in range(0, yres):
		unusedCoords.append((x, y))
quickc = int(.3*xres)
unusedColors = []
#dont forget to change back to 256 after debug
for r in range(0,256): #just making a list of 1.67 million tuples, I'm sure it'll only take a couple of seconds
	print "color list at " +str(r)+"/255"
	for g in range(0,256):
		for b in range (0, 256):
			unusedColors.append((r,g,b, 255))


def bordering_unused(hubpixel):


	"""Cycles through each neighboring pixel and returns a list (potentialNew) of the ones that are unused or False if each one is used.""" 
	global potentialNew
	potentialNew = []
	xpoint = hubpixel[0]
	ypoint = hubpixel[1]
	checklist = [(xpoint-1, ypoint-1),(xpoint, ypoint-1),(xpoint+1, ypoint-1),(xpoint-1, ypoint),(xpoint+1, ypoint),(xpoint-1, ypoint+1),(xpoint, ypoint+1),
	(xpoint+1, ypoint+1)]
	for i in range(0,8):
		if checklist[i][0] in range(0, xres-1) and checklist[i][1] in range(0,yres-1):
			if im.getpixel(checklist[i]) == (0,0,0,0):
				potentialNew.append(checklist[i])
	if len(potentialNew) > 0:
		return potentialNew
	else:
		return False



hubpixel = startPos
draw.point(hubpixel, fill=unusedColors[len(unusedColors)-1])
unusedColors.remove(unusedColors[len(unusedColors)-1])
unusedCoords.remove(hubpixel)

trackingBeacon = 0
timeInWhile = 0
timeInElse = 0
timeInMainWhileCheck = 0
timeInPrinter = 0
timeInElse1 = 0
timeInElserand = 0
timeInElseDraw = 0

timerstart = time.time()
mainwhilecheckstart = time.time()
whiletimerstart = time.time()
mainLooptimerstart = time.time()
while unusedCoords:
	mainwhilecheckstop = time.time()
	timeInMainWhileCheck += (mainwhilecheckstop-mainwhilecheckstart)
	printertimerstart = time.time()
	trackingBeacon += 1
	if trackingBeacon > 20:
		print len(unusedCoords)
		timerstop = time.time()
		trackingBeacon = 0
		print str(timerstop-timerstart) + " elapsed"
		timerstart = time.time()
	printertimestop = time.time()
	timeInPrinter += printertimestop - printertimerstart
	whiletimerstart = time.time()	
	while bordering_unused(hubpixel):
		while potentialNew:
			newpixel = potentialNew[randint(0, len(potentialNew)-1)]
			draw.point(newpixel, fill=unusedColors[len(unusedColors)-1])
			unusedColors.remove(unusedColors[len(unusedColors)-1])
			unusedCoords.remove(newpixel)
			potentialNew.remove(newpixel)
		hubpixel = newpixel
	

	else:
		whiletimerstop = time.time()
		timeInWhile += whiletimerstop-whiletimerstart
		elsetimerstart = time.time()
		else1start = time.time()
		if len(unusedCoords) == 0:
			break
		else1stop = time.time()
		timeInElse1 += else1stop - else1start
		elserandstart = time.time()
		hubpixel = unusedCoords[randint(0, len(unusedCoords)-1)]
		elserandstop = time.time()
		timeInElserand += elserandstop - elserandstart
		#somehow most of the processing time is between this and the next # main culprit is the while loop ending prematurely
		elsedrawstart = time.time()
		draw.point(hubpixel, fill=unusedColors[len(unusedColors)-1])
		unusedColors.remove(unusedColors[len(unusedColors)-1])
		unusedCoords.remove(hubpixel)
		elsedrawstop = time.time()
		#
		elsetimerstop = time.time()
		timeInElseDraw += elsedrawstop - elsedrawstart
		timeInElse += (elsetimerstop-elsetimerstart)
		mainwhilecheckstart = time.time()
mainLooptimerstop = time.time()
print "seconds in main loop: " + str(mainLooptimerstop - mainLooptimerstart)
print "seconds in else: " +str(timeInElse)
print "seconds in else1: "+str(timeInElse1)
print "seconds in elserand: "+str(timeInElserand)
print "seconds in elseDraw: "+str(timeInElseDraw)
print "seconds in in while: "+ str(timeInWhile)
print "seconds in main while check: "+str(timeInMainWhileCheck)
print "seconds in printer: "+str(timeInPrinter)
im.save("result.png")