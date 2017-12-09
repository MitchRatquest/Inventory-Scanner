from collections import Counter
import json

tempArray = []

with open('secondLookup.json') as lookup:
	jsonContents = json.load(lookup)

with open('scanned.txt', 'r') as scanned:
	for each in scanned:
		tempArray.append(each.strip('\n'))

print tempArray

for scannedSKU in tempArray:
	for lookupSKU in jsonContents:
		if scannedSKU == lookupSKU['SKU']:
			print scannedSKU, lookupSKU['SKU'], lookupSKU['Title']
