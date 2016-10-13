from collections import Counter 
import pdb, re, sys
from copy import deepcopy

print "Make sure you have lookup.txt in this directory"
print "and pass your new scan as argv"
print "output.csv will be your manifest\n"

with open('lookup.txt','r+') as b:	#open your lookup table
	lookups = b.readlines()
headers = 'Load,'					#insert Load to beginning
headers += lookups[0]				#First row of lookup is headers

for x in range(len(lookups)):
	lookups[x] = lookups[x].strip('\n') #strip the dumb things

try:
	with open(sys.argv[1],'r+') as f:	#user has to pass value
		rawlines = f.readlines()
except:
	print "------------------------------------------------"
	print "--YOU DIDNT PASS THE NEW SHEET TO THE PROGRAM---"
	print "------------------------------------------------"
	quit()								#quit gracefully? not sure Optimal Way

for x in range(len(rawlines)):
	rawlines[x]=rawlines[x].strip('\r\n') #unneccesary?
                   #assuming pallet# first thing scanned
currentload   = rawlines[0].split('-')[0]      #split it on hypen
currentpallet = rawlines[0].split('-')[1]	   #number of current pallet

x= 0
sizeofrawlines = len(rawlines)
while x < (sizeofrawlines -1): #define your own loop
	try:
		if rawlines[x] == 'deleteprevious':
			del(rawlines[x]) #delete current cell
			x = x -1
			del(rawlines[x]) #delete this one too, the actual item to be deleted
			x = x -1
			sizeofrawlines = len(rawlines) #recalc the length of the listc
		else:
			x = x + 1 #step forward one
	except:
		pass

palletsplit = []
for x in range(len(rawlines)):
		if rawlines[x].split('-')[0] == currentload:
			#print "found a new pallet: %s" %rawlines[x].split('-')[1] #pallet delimeters?
			palletsplit.append(x) #now you know where the pallets end
			numberofpallets = len(palletsplit)
palletsplit.append(len(rawlines)) #end of the entire file

finaloutput = ''
finaloutput += headers
for palletrange in range(len(palletsplit)+1):
	try:
		currentpallet = rawlines[palletsplit[palletrange]].split('-')[1]	   #number of current pallet
	except:
		print finaloutput
		with open('manifest.csv', 'w+') as dango: #this runs wher your list index is out of range(end of pallet list)
			dango.write(finaloutput)
			dango.close()
		break #should maybe be quit()?
	temppallet = []
	for x in range(palletsplit[palletrange]+1, palletsplit[palletrange+1]): #for range of new pallet
		temppallet.append(deepcopy(rawlines[x]))      #just append to new list

	tempcount =  Counter(temppallet)
	almostthere = [[[]]for i in range(len(sorted(tempcount.iteritems())))] #only the range of unique values
	x = 0
	for key,value in sorted(tempcount.iteritems()):		#turn dict into 3d array
		if key == '': #if you hit a nothing spot, just skip this one
			pass
		else:
			almostthere[x] = [key,value,currentload + '-' + currentpallet] #add pallet number to thing
			x = x+1
	#print almostthere
	#print "^^^^ those are our items, count, and pallet numbers"
	#pdb.set_trace()
	#print "length of 3d array " 
	#print  len((almostthere))
	for x in range(len(almostthere)):   #pallet information 3d array
		loadpallet  = almostthere[x][2]	#combined load number (load plus pallet number)
		sku			= almostthere[x][0]	#long sku from vendor
		quantity	= almostthere[x][1]	#total quantity on pallet
		regexflag = 0 					#keep track of whether or not the sku is in the lookup table
		for findsku in range(len(lookups)):
			s = re.search(sku+'.*', lookups[findsku])	#find sku in lookup, include everything after
			if s:
				otherdata = s.group()[14:]				#sku is 13, comma is 1, strip them out
				regexflag = 1							#send flag for found
		if regexflag == 1:
			finaloutput += "%s,%s,%s%s\n" %(loadpallet,sku,otherdata,quantity) #you have the full list here
		else:
			finaloutput += "%s,%s,YOU DO NOT HAVE THIS SKU IN YOUR LOOKUP TABLE,%s\n" %(loadpallet,sku,quantity)

