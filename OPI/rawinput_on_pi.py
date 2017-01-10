import os, re, datetime, time, subprocess
yam = [] #init var
timestamp =  str(datetime.datetime.now().strftime('%I.%M.%S_%p')) + '.txt' #only once, filename ultimately
daystamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d') #name of folder to put files for today in

#CHANGE THIS
with open('Credz.txt') as f:
	ftpPass = f.readline() # Line 1 of "Credz" file corresponds to main server pass
	ftpUserIPDirectory = f.readline() # Line 2 of credential file is the username and directory of where the rsynced file is sent
	f.close()

cwd = os.getcwd() #current working directory
opj = os.path.join #more magic - OS PATH JOIN = opj, for windows and linux compatibility

folderWithTodaysDate = opj(cwd, daystamp)  # folder to place all todays scans in

if os.path.exists(folderWithTodaysDate) == True: #If file w/ today's date exists, then continue the script.
	pass
else: #else create the directory with read/write/exe permissions.
	os.makedirs(folderWithTodaysDate, 0666) #read/write permissions for creating files inside python created folder. For Win & Linux.
	os.chmod(folderWithTodaysDate, 0777)
while True:
	yam.append(raw_input()) #stream input to append
	#if(yam[-1]) == 'deleteprevious':
	#	del(yam[-2])
	#	del(yam[-1])#delete control word
	#NOW u gotta save the deleteprevious line for your parser, dummy
	if(yam[-1]) == 'imfinished':
		del(yam[-1]) #dont print the imfinished bit
		currentfile = daystamp +'/'+timestamp #just put it in today's folder
		#change line below to fit your setup
		command = 'sshpass -p %s rsync -a %s %s' % ftpPass, currentfile, ftpUserIPDirectory
		#I know this is a total hack
		subprocess.call(command, shell=True)  #run the dumb thing
		quit()
		
	createFileInDateDirectory = str(opj(folderWithTodaysDate, timestamp)) #current file in progress, based on timestamp above
	with open(createFileInDateDirectory, 'a') as final:  #append that file every time you scan in case of system failure somewhere (batteries die)
		final.write(yam[-1] + '\n') #write the latest input
		final.close() #close it