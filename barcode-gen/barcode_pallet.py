from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import datetime, time, sys
'''
			USE LIKE
			python barcode_pallet.py PALLETNAME NUMBEROFPALLETS
'''
bardata = str(sys.argv[1])
barsize = [50*mm,.7*mm]

pagesize = [216*mm, 280*mm]
barlocation = [pagesize[0]/4, pagesize[1]*.7]
count = 1
#instantiate a new canvas
c = canvas.Canvas(str(sys.argv[1])+".pdf")
c.setPageSize((216*mm,280*mm))			 #US-letter dimensions

for x in range(int(sys.argv[2])):
	#generate a barcode of specific size
	barcode = code128.Code128(bardata+"-"+str(count),barHeight=barsize[0],barWidth=barsize[1])
	#draw the barcode on page somewhere
	barcode.drawOn(c, barlocation[0], barlocation[1]) 		#x then y, origin bottom left
	#put the string on the page under the barcode
	c.setFont('Helvetica-Bold',70)
	c.drawString(barlocation[0]-25*mm,barlocation[1]-45*mm, bardata+"-"+str(count)) #pallet number
	#luminara tag just for safe keeping
	c.setFont('Helvetica-Bold', 35)
	c.drawString(barlocation[0]+10*mm, barlocation[1]-70*mm, "LUMINARA")

	c.setFont('Helvetica-Bold', 14)
	c.drawString(barlocation[0]+30*mm, barlocation[1]-80*mm,datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d') )
	count = count + 1
	#close this page
	c.showPage() 							#causes canvas to stop drawing, any further operations on subsquent page
c.save()								#generates pdf doc
