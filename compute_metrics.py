
def compute(parserOutput, file, IP):
   print('called compute function in compute_metrics.py')
   packetCounter = 0
   #Time Metrics
   pingTimes = []
   replyDelaySum = 0
   replyDelay = 0
   #Distance Metrics
   totalHops = 0
   avgHops = 0 

   echoReqSent = int()
   echoRepSent = int()
   echoReqRecieved = int()
   echoRepRecieved = int()
   totalReqBytesSent = int()
   totalReqBytesRecieved = int()
   payloadRecieved = int() 
   payloadSent = int()
   times = list()
   requests = list()

   for packet in parserOutput:
      if IP == packet[2]:
         #Its the source IP
         #append to a list of requests
         requests.append(packet)
         #Append the a list of times
         times.append(float(packet[1]))
         if "rep" == packet[6][12:15]:
               echoRepSent += 1
         if "req" == packet[6][12:15]:
               echoReqSent += 1
               totalReqBytesSent += int(packet[5])
               payloadSent += (int(packet[5]) - 42)
         packetCounter += 1
      elif IP == packet[3]:
         #Its the destination IP
         #append to a list of times
         times.append(float(packet[1]))
         if "rep" == packet[6][12:15]:
               echoRepRecieved += 1
               totalHops += 129 - int(packet[6].split(",")[2].split("=")[1].split(" ")[0])
         if "req" == packet[6][12:15]:
               echoReqRecieved += 1
               totalReqBytesRecieved += int(packet[5])
               payloadRecieved += (int(packet[5]) - 42)
               # Average reply delay
               replyDelaySum += float(parserOutput[packetCounter + 1][1]) - float(packet[1])
         packetCounter += 1
      else:
         continue
 

   #Find average ping RTT
   time_sum = int()
   every_sum = int()
   loopCount = 0
   for i in range(0, len(times) - 1, 2):
      if parserOutput[i][2] == IP:
         time_sum += (times[i + 1] - times[i]) #This sum adds only packets that match IP
         loopCount += 1
      
      every_sum += (times[i + 1] - times[i]) #This sum adds times for every packet
   avgPingRTT = (time_sum/loopCount) * 1000

   throughput = int()
   goodput = int()
   #Find Throughput and Goodput
   pingTime = (float(requests[-1][1])) - (float(requests[0][1]))
   throughput = ((totalReqBytesSent)/time_sum)/1000
   goodput = ((payloadSent)/time_sum)/1000

   #Find Delay Time in microseconds
   loopCount = 0
   delaySum = int()
   for i in range(1, len(times) - 1, 2): #While i has not iterated through the entire list
      if parserOutput[i][2] == IP: #Check if the source IP matches the node IP
         delaySum += times[i + 1] - times[i]
         loopCount += 1

   avgTimes = delaySum /(len(times)/2) 
   replyDelay = (replyDelaySum / echoReqRecieved) * 1000000
   avgHops = totalHops / (echoRepRecieved)   

   fileName = "output.csv"
   f = open(fileName, "a")
   f.write(file.split(".")[0])
   f.write("\n\n")
   f.write("Echo Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received\n")
   f.write(str(echoReqSent) + "," + str(echoReqRecieved) + "," +  str(echoRepSent) + "," + str(echoRepRecieved) + "\n")
   f.write("Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)\n")
   f.write(str(totalReqBytesSent) + "," + str(payloadSent) + "\n")
   f.write("Echo Request Bytes Received (bytes),Echo Request Data Received (bytes)\n")
   f.write(str(totalReqBytesRecieved) + "," + str(payloadRecieved) + "\n")
   f.write("Average RTT (milliseconds)," + str(avgPingRTT) + "\n")
   f.write("Echo Request Throughput (kB/sec)," + str(throughput) + "\n")
   f.write("Echo Request Goodput (kB/sec)," + str(goodput) + "\n")
   f.write("Average Reply Delay (microseconds)," + str(replyDelay) + "\n")
   f.write("Average Echo Reply Hop Count," + str(avgHops) + "\n\n")
