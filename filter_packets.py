# Parameters: File name to parse, protocol to search for (ex. "ICMP")
def filter(inputFileName, protocol):
   print ('called filter function in filter_packets.py')
   
   # Create an output file based on the input filename
   outputFileName = inputFileName.split(".")[0] + "_filtered.txt"

   # Open the input and output files
   fIn = open(inputFileName, 'r')
   fOut = open(outputFileName, 'w')

   # Variables to store information   
   a = str()
   b = list()

   # Iterate through input file to separate packets into a list
   for line in fIn:
      if line[0] == 'N':
         b += [a] # Store the current line
         a = line # set a to current line
      else:
         a += line # append packet information to string

   # Indentify and filter packets by specified protocol
   for packet in b:
      # Check if list index contains protocol in string (!= -1 meaning it has been found) 
      # Also check if the packet does not contain "unreachable" as part of an error message (== -1 meaning it has not been found)
      if packet.find(protocol) != -1 and packet.find("unreachable") == -1:
         # Write packet to output file if found
         fOut.write(packet)

   # Close files
   fIn.close()
   fOut.close()
