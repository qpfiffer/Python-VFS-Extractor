#!/usr/bin/python
'''
The following was taken from here:
http://forum.xentax.com/viewtopic.php?f=21&t=3517

This is the VFS file format:
long 0x0 = fileheader = "LP2C"
long 0x4 = total folders in Archive (probably :D)
long 0x8 = files in current folder
byte 0xC = length of filename
string 0xC + lof = filename
long 0xC + lof = filesize
long 0xC + lof + 4 = offset of file in archive
long 0xC + lof + 4 + 12 = next file
'''

import sys
import os.path

def readInChunk(fileHandle, chunkSize):
	data = fileHandle.read(chunkSize)
	data = data[::-1] # reverse it because we're dealing with hex
	data = long(data.encode("hex"), 16) #convert it
	return data

if __name__ == "__main__":
	EXTRACT_SPOT = "extract/"

	# Test to see if the file is there and not a directory
	if os.path.exists(sys.argv[1]) == False or os.path.isfile(sys.argv[1]) == False:
		print "Given file does not exist or is not a file."
		quit(-1)

	# Open the file
	print "Opening " + sys.argv[1] + "..."
	file = open(sys.argv[1], "r")

	# Read off the file header:
	fileHeader = file.read(4)
	print "File header is " + fileHeader
	if fileHeader != "LP2C":
		print "File is not a VFS file. Exiting."
		quit(-1)
	else:
		print "File is a VFS file."

	totalFolders = readInChunk(file,4)
	print "Total folders in archive:", totalFolders

	totalCurrentFiles = readInChunk(file,4)
	print "Total files in current folder:", totalCurrentFiles

	for i in range(totalCurrentFiles):
		print "\nFile (" + str(i+1) + "/" + str(totalCurrentFiles) + ")"
		filenameLength = readInChunk(file,1)
		print "Filename length:", filenameLength

		filename = file.read(filenameLength)
		print "File name is: " + filename

		filesize = readInChunk(file,4)
		print "File size in bytes:", filesize

		junkData = file.read(4)

		fileAddress = file.read(4)
		print "File address in VFS file: 0x"+fileAddress.encode("hex")

		# For some reason there is a chunk of zeroes.
		zeroes = file.seek(4, 1) # I forget the enum for it. I know its 1 for current offset.

		timestamp = readInChunk(file,8)
		print "Timestamp is:", timestamp

		print "Dumping " + filename + "..."
		preSeekSpot = file.tell()

		# Go to where the file is
		file.seek(long(fileAddress.encode("hex"), 16))

		extractedFile = open(EXTRACT_SPOT + filename, "w")
		extractedFile.write(file.read(filesize))
		extractedFile.close()

		# Go back to where we were
		file.seek(preSeekSpot)


	file.close()
