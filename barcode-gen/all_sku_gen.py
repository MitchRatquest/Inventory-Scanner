from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import datetime, time, sys
'''
			USAGE:
			python all_sku_gen.py 
'''
with open('all_barcodes.txt','r+') as a:
	lines = a.readlines()
for x in range(len(lines)):
	lines[x] = lines[x].strip('\n')
	lines[x] = lines[x].split(',')
#now lines is an array len(lines) [138] long, with [0 1 2] as barcode, color, title

c = canvas.Canvas("all_skus.pdf")
c.setPageSize((216*mm,280*mm))			 #US-letter dimensions

bardata = lines[0][0]
barsize = [30*mm,.5*mm]

pagesize = [216*mm, 280*mm]
barlocationcol1 = [pagesize[0]/10, pagesize[1]*.8]
barlocationcol2 = [pagesize[0]/1.8, pagesize[1]*.8]
positionarray = [.7, .5, .3, .1]

currentbarcode = 0
pagecounter = 1
for x in range(len(lines)/8):
	if(currentbarcode%8==0): #barcode mod 4 will be 0 1 2 3 0 for mod 0 1 2 3 4 
		while(currentbarcode%8 <= 3):
			for x in range(4):
				###############################################################
				bardata = lines[currentbarcode][0]
				#generate a barcode of specific size
				barcode = code128.Code128(bardata,barHeight=barsize[0],barWidth=barsize[1])
				#draw the barcode on page somewhere
				barlocation = barlocationcol1[0], pagesize[1]*positionarray[currentbarcode%4]
				c.line(0,barlocation[1]+35*mm, pagesize[0], barlocation[1]+35*mm)	#horizontal line above
				c.line(0,barlocation[1]-12*mm, pagesize[0], barlocation[1]-12*mm)	#horizontal line below
				barcode.drawOn(c, barlocation[0], barlocation[1]) 		#x then y, origin bottom left
				#put the string on the page under the barcode
				c.setFont('Helvetica-Bold',12)
				c.drawString(barlocation[0]+5*mm,barlocation[1]-5*mm, bardata)
				c.drawString(barlocation[0]+5*mm,barlocation[1]-9*mm, lines[currentbarcode][2]+"-"+lines[currentbarcode][1]) #pallet number
				currentbarcode = currentbarcode + 1
				#print currentbarcode
				################################################################
		for x in range(4):
			###############################################################
			bardata = lines[currentbarcode][0]
			#generate a barcode of specific size
			barcode = code128.Code128(bardata,barHeight=barsize[0],barWidth=barsize[1])
			#draw the barcode on page somewhere
			barlocation = barlocationcol2[0], pagesize[1]*positionarray[currentbarcode%4]
			c.line(0,barlocation[1]+35*mm, pagesize[0], barlocation[1]+35*mm)	#horizontal line above
			c.line(0,barlocation[1]-12*mm, pagesize[0], barlocation[1]-12*mm)	#horizontal line below
			barcode.drawOn(c, barlocation[0], barlocation[1]) 		#x then y, origin bottom left
			#put the string on the page under the barcode
			c.setFont('Helvetica-Bold',12)
			c.drawString(barlocation[0]+5*mm,barlocation[1]-5*mm, bardata)
			c.drawString(barlocation[0]+5*mm,barlocation[1]-9*mm, lines[currentbarcode][2]+"-"+lines[currentbarcode][1]) #pallet number
			currentbarcode = currentbarcode + 1
			################################################################

		#close this page
	#print currentbarcode
	c.drawString(pagesize[0]*.90,pagesize[1]*.03, "page " + str(pagecounter))
	c.line(pagesize[0]/2, pagesize[1], pagesize[0]/2, 0)	#vertical bar
	c.showPage() 							#causes canvas to stop drawing, any further operations on subsquent page
	pagecounter = pagecounter + 1
c.save()								#generates pdf doc
