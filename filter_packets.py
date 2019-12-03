# Parameters: File name to parse, protocol to search for (ex. "ICMP")
def filter(inputFileName, protocol):
	print 'called filter function in filter_packets.py'
	outputFileName = inputFileName.split(".")[0] + "_filtered.txt"
	print outputFileName
	
	fIn = open(inputFileName, 'r')
	fOut = open(outputFileName, 'w')
	line = fIn.readline()
	
	while line:
                lineSplit = line.split()
                for a in lineSplit:
                        if(a == protocol):
                                for x in lineSplit:
                                        fOut.write(x.replace(",", "") + ";")
                                fOut.write("\n")
                line = fIn.readline()
