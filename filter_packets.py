# Parameters: File name to parse, protocol to search for (ex. "ICMP")
def filter(inputFileName, protocol):
   print 'called filter function in filter_packets.py'
   
   # Create an output file based on the input filename
   outputFileName = inputFileName.split(".")[0] + "_filtered.txt"
   print(outputFileName)

   # Open the input and output files
   fIn = open(inputFileName, 'r')
   fOut = open(outputFileName, 'w')
   
   a = str()
   b = list()

   for line in fIn:
      if line[0] == 'N':
         b += [a]
         a = line
      else:
         a += line

   for packet in b:
      if packet.find('ICMP') != -1:
         fOut.write(packet)
      else:
         continue

   fIn.close()
   fOut.close()
