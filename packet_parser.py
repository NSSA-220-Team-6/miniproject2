def parse(inputFileName) :
   print ('called parse function in packet_parser.py')

   # Take input file to parse
   fIn = open(inputFileName, 'r')

   # Create a list to store information, to be returned
   L = list()

   # Parse the file into a list of lists
   for line in fIn:
      # Parse only the line with metrics and information
      # (=! -1 means that the line does contain 'ICMP' and therefore is the metrics/info line)
      if line.find('ICMP') != -1:
         # Parse it
         L += [' '.join(line.strip().split()).split(' ', 6)]

   # Return the parsed list of list
   return L
