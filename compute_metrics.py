def compute(parserOutput, fileName) :
   print('called compute function in compute_metrics.py')

   #Total Packet count
   packetCount = 0
   
   #Count number of echo requests sent, echo requests recieved, echo replies sent, echo replies recieved
   echoReqSent = 0
   echoReqRecieved = 0
   echoRepSent = 0
   echoRepRecieved = 0

   #Count Total Data Recieved
   totalReqBytesSent = 0
   totalReqBytesRecieved = 0
   payloadSent = 0
   payloadRecieved = 0

   #Time Metrics
   request = True
   reply = False
   times = []
   pingTimes = []
   avgPingRRT = 0
   throughput = 0
   goodput = 0
   replyDelay = 0

   #Distance Metrics
   avgHops = 0
   totalHops = 0
   requestCounter = 0

   #Determine request or reply, and sent or recieved
   rep = 'reply'
   req = 'request'
   firstIP = "192.168.100.1"
   secondIP = "192.168.100.2"

   #Find Request and Replies Sent
   for packet in parserOutput:

      #Compute Data Metrics
      
      #Check if the packet is a reply
      if rep in (packet[6])[:20]:


         #Check if the packet was sent
         if firstIP in packet[2]:
            echoRepSent = echoRepSent + 1


         #Check if the packet was recieved
         if not firstIP in packet[2]:
            #print(packet[6])
            echoRepRecieved = echoRepRecieved + 1



      #Check if the packet is a request
      if req in (packet[6])[:20]:
         #Distance metrics for echo requests	  
         hops = 129 - int(packet[6].split(",")[2].split("=")[1].split(" ")[0])
         totalHops += int(hops)
         requestCounter += 1
         print("count " + str(requestCounter))
         print("hops for this packet " + str(hops))
         print("total hops " + str(totalHops))
         
         #Check if the packet was sent
         if firstIP in packet[2]:
            echoReqSent = echoReqSent + 1
            totalReqBytesSent = totalReqBytesSent + int(packet[5])
            payloadSent = payloadSent + (int(packet[5])-42) # -42 Bytes to remove headers.


         #Check if the packet was recieved
         if not firstIP in packet[2]:
            #print(packet[6])
            echoReqRecieved = echoReqRecieved + 1
            totalReqBytesRecieved = totalReqBytesRecieved + int(packet[5])
            payloadRecieved = payloadRecieved + (int(packet[5])-42) # -42 Bytes to remove headers.

      #Gather Times
      times.append(float(packet[1]))
      
   #Compute average hops
   avgHops = totalHops / requestCounter
   
   #Compute Time Metrics
   i = 0
   timeSum = 0
   while i < (len(times)): #While i has not iterated through the entire list
      request = times[i]
      reply = times[i + 1]
      timeBetween = reply - request
      timeSum = timeSum + timeBetween
      i = i + 2

   avgTimes = timeSum /(len(times)/2) #Divide by the number of RTTs
   avgPingRRT = avgTimes*1000 #Convert to Miliseconds

   #Compute Echo Request Throughput and Goodput
   packetNum= 0
   packetFull = 0
   packetPayload = 0
   while packetNum < len(parserOutput):
      #Request packets are even
      #Add up all the packets
      packetFull = packetFull + int(parserOutput[packetNum][5])
      packetSize = int(parserOutput[packetNum][5]) - 42 #ICMP Packet size after removing headers
      packetPayload = packetPayload + packetSize 
      packetNum = packetNum + 2 #Skip over the reply packets

   throughput = ((packetFull/sum(pingTimes))/1000) #Calculate and convert to kB/s
   goodput = ((packetPayload/sum(pingTimes))/1000) #Calculate and convert to kB/s
   
   
   
   j = 1
   delaySum = 0
   delayBetween = 0
   while j < (len(times)-1): #While i has not iterated through the entire list
      reply = times[j]
      request = times[j + 1]
      delayBetween = request - reply
      delaySum = delaySum + delayBetween
      j = j + 2

   avgTimes = delaySum /(len(times)/2) #in miliseconds
   replyDelay = avgTimes*1000 #Convert to microseconds
   
   print('Data Metrics')
   print('------------')
   print()
   print()      
   print('Number of requests sent: ',echoReqSent)
   print('Number of requests recieved: ',echoReqRecieved)
   print('Number of replies sent: ',echoRepSent)
   print('Number of replies recieved: ',echoRepRecieved)
   print()
   print()
   print('Number of request bytes sent: ',totalReqBytesSent)
   print('Number of request bytes recieved: ',totalReqBytesRecieved)
   print('Payload Size of sent bytes: ',payloadSent)
   print('Payload Size of recieved bytes: ',payloadRecieved)
   print()
   print()
   print('Time Metrics')
   print('------------')
   print()
   print()
   print('Average Ping RTT:',avgPingRRT)
   print('Echo Request Throughput',throughput,'kB/sec')
   print('Echo Request Goodput',goodput,'kB/sec')
   print('Average Reply Delay',replyDelay)
   print()
   print()
   print('Distance Metrics')
   print('----------------')
   print()
   print()
   print('Average number of Hops per echo request:',avgHops)

   f = open("output.csv", "a")
   f.write(fileName.split(".")[0])
   f.write("\n\n")
   f.write("Echo Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received\n")
   f.write(str(echoReqSent) + "," + str(echoReqRecieved) + "," +  str(echoRepSent) + "," + str(echoRepRecieved) + "\n")
   f.write("Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)\n")
   f.write(str(totalReqBytesSent) + "," + str(payloadSent) + "\n")
   f.write("Echo Request Bytes Received (bytes),Echo Request Data Received (bytes)\n")
   f.write(str(totalReqBytesRecieved) + "," + str(payloadRecieved) + "\n\n")
   f.write("Average RTT (milliseconds)," + str(avgPingRRT) + "\n")
   f.write("Echo Request Throughput (kB/sec)," + str(throughput) + "\n")
   f.write("Echo Request Goodput (kB/sec)," + str(goodput) + "\n")
   f.write("Average Reply Delay (microseconds)," + str(replyDelay) + "\n")
   f.write("Average Echo Request Hop Count," + str(avgHops) + "\n\n")
