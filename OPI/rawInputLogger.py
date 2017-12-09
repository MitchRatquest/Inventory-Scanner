import subprocess, datetime, time, os

scannedItemsArray = []

timestamp = '%s.txt' % datetime.datetime.now().strftime('%I.%M.%S%p') #only once, filename ultimately
daystamp = datetime.datetime.now().strftime('%m-%d-%Y') #name of folder to put files for today in

opj = os.path.join
folderWithTodaysDate = opj(os.getcwd(), daystamp) # folder to place all todays scans in. OS PATH JOIN = for windows and linux compatibility

def blinky(color):
	try:
		subprocess.call(['echo 1 > /sys/class/leds/%s_led/brightness' % color])
		time.sleep(1)
		subprocess.call(['echo 1 > /sys/class/leds/%s_led/brightness' % color])
		time.sleep(1)

 	except OSError:
		pass

def removeLastInput():
	try:
		del scannedItemsArray[-1]
	except IndexError as e: # When -1 index doesn't exist.
		print e

def makeFolder():
	if os.path.exists(folderWithTodaysDate) == True: #If file w/ today's date exists, then continue the script.
		pass
	else:
		os.makedirs(folderWithTodaysDate, 0666) #read/write permissions for creating files inside python created folder. For Win & Linux.
		#os.chmod(folderWithTodaysDate, 0777)

def writeFile(rawInput):
	createFileInDateDirectory = str(opj(folderWithTodaysDate, timestamp)) #current file in progress, based on timestamp above

	with open(createFileInDateDirectory, 'a') as final:  #append that file every time you scan in case of system failure somewhere (batteries die)
		final.write(rawInput + '\n') #write the latest input
		final.close() #close it

	with open('%s/ArrayLog - %s.txt' % (folderWithTodaysDate, timestamp), 'w+') as arrayLog:
		arrayLog.write(str(scannedItemsArray))

def getInput(rawInput):

	makeFolder()
			
	if rawInput == 'deleteprevious':
		removeLastInput()
		writeFile('deleteprevious')

	else:
		scannedItemsArray.append(rawInput)
		writeFile(rawInput)

	blinky('green')
	print '\n%s' % scannedItemsArray

while True:
	print "\nScan Something....."
	getInput(raw_input())
