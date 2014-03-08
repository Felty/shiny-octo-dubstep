from PIL import Image
from PIL import ImageDraw

im = Image.new("RGB", (100, 100), "white")
draw = ImageDraw.Draw(im)

colors = {'red':'red', 'blue':'blue','green':'green'}
xcount = 0
ycount = 0

for i in range(0,100):
	#iterates through the rows
	xcount = 0
	for i in range(0,100):
		#draws a pixerl at each coord along the row
		for pixel in colors:
			draw.point((xcount,ycount), fill=str(colors[pixel]))
			xcount += 1
	ycount += 1	

im.save("resultv2.png")