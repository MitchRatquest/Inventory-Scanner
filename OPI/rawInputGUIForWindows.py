import Tkinter as tk
import os, datetime, time

scannedItemsArray = []
timestamp =  str(datetime.datetime.now().strftime('%I.%M.%S_%p')) + '.txt' #only once, filename ultimately
daystamp = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%y') #name of folder to put files for today in
cwd = os.getcwd() #current working directory
opj = os.path.join #more magic - OS PATH JOIN = opj, for windows and linux compatibility
folderWithTodaysDate = opj(cwd, daystamp)  # folder to place all todays scans in

def center(toplevel): # Function for centering root tKinter Window
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth() 
    h = toplevel.winfo_screenheight() 
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2 
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
        	
class mainApp(tk.Tk): # The core class for creating tkinter GUI
    def __init__(self):
        tk.Tk.__init__(self)
        def getInput():
            skuInput = SkuEntry.get()
            scannedItemsArray.append(skuInput)
            
            if os.path.exists(folderWithTodaysDate) == True: #If file w/ today's date exists, then continue the script.
                pass
            else: #else create the directory with read/write/exe permissions.
                os.makedirs(folderWithTodaysDate, 0666) #read/write permissions for creating files inside python created folder. For Win & Linux.
				#os.chmod(folderWithTodaysDate, 0777)
            createFileInDateDirectory = str(opj(folderWithTodaysDate, timestamp)) #current file in progress, based on timestamp above
            with open(createFileInDateDirectory, 'a') as final:  #append that file every time you scan in case of system failure somewhere (batteries die)
                final.write(skuInput + '\n') #write the latest input
                final.close() #close it
            print skuInput
            print scannedItemsArray
            SkuEntry.delete(0, 'end')

            if skuInput == 'deleteprevious':
            	del scannedItemsArray[-1]
            	del scannedItemsArray[-1]

            try:
                lastScannedOne = tk.Label(width=41, anchor='n', relief='ridge', text=str(scannedItemsArray[-1]))
                lastScannedOne.place(relx=.35, rely=.31)
                try:
                    lastScannedTwo = tk.Label(width=41, anchor='n', relief='ridge', text=str(scannedItemsArray[-2]))
                    lastScannedTwo.place(relx=.35, rely=.51)
                    try:
                        lastScannedThree = tk.Label(width=41, anchor='n', relief='ridge', text=str(scannedItemsArray[-3]))
                        lastScannedThree.place(relx=.35, rely=.71)
                    except IndexError:
                        print 'error3'
                except IndexError:
                    print 'error2'
            except IndexError:
                print 'error3'

        scanaUPC = tk.Label(width=20, anchor='n', relief='ridge', text='Scan a barcode:')#, background='orange')
        scanaUPC.place(relx=.01, rely=.05)

        SkuEntry = tk.Entry(width=48)#, background='orange')
        SkuEntry.place(relx=.35, rely=.059)
        SkuEntry.focus_set()

        EnterButton = tk.Button(text="Continue", width=19, height=5, background='orange', command=lambda: getInput())
        EnterButton.place(relx=.016, rely=.3)
        self.bind('<Return>', (lambda event: getInput()))

        lastScannedOne = tk.Label(width=41, anchor='n', relief='ridge', text='')
        lastScannedOne.place(relx=.35, rely=.31)
        lastScannedTwo = tk.Label(width=41, anchor='n', relief='ridge', text='')
        lastScannedTwo.place(relx=.35, rely=.51)
        lastScannedThree = tk.Label(width=41, anchor='n', relief='ridge', text='')
        lastScannedThree.place(relx=.35, rely=.71)

        lineCanvas = tk.Canvas(height=1, width=460, bg='gray')
        lineCanvas.place(relx=.0, rely=.23)

if __name__ == "__main__":
    root = mainApp()
    root.resizable(0,0) # Not resizeable
    root.geometry("465x150") # Static width/height of tkinter GUI
    center(root) # call Center function on entire frame, so each run is displayed on same monitors coordinates
    root.title('Inventory-Scanner') # Name GUI Window
    root.mainloop()
