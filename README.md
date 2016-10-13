# Inventory-Scanner

Wireless barcode scanner used for manifesting pallets of wholesale lamps, but can be extended to just about anything. 

It runs on a small single board computer with integrated wifi (Orange Pi Lite), a portable USB battery bank, and a USB barcode scanner.
Initially I tried to use USB over IP, but the results were lackluster.

There are scripts for generating manifests in CSV format, with our without hyperlinks, and they rely on lookups. I created a few scripts to generate the lookup tables, but they mostly used the Mechanize package and were trivial. 

The barcode generation scripts are for either pallet identification or for when a barcode on an item wont scan. 

The user has to log in to the board by scanning the username and password barcode, and finally the rawinput_on_pi.py script. From then on they are in the main loop, which appends each scanned input to a file. There is a delete function, but it merely saves the text "deleteprevious", which is parsed by the manifest builder. It was important to make the actual scanning as simple as possible. Finally, scanning "imfinished" uploads the newly scanned inventory to an FTP server on our local network. 

I've given each board a static IP and can `watch "tail -n 50 10.14.30_AM.txt && wc 10.14.30_AM.txt"` via ssh to make sure nothing weird is happenning. 

The entire setup looks like this (static IP written on tape):
![alt text](https://github.com/MitchRatquest/Inventory-Scanner/blob/master/Hardware/together.JPG "Hardware Setup")
