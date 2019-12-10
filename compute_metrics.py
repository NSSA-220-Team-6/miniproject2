def compute(parserOutput, IP):
   print ('called compute function in compute_metrics.py')
   #Time Metrics
   pingTimes = []
   replyDelay = 0
   #Distance Metrics
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
         requests.append(packet)
         times.append(float(packet[1]))
         if "rep" == packet[6][12:15]:
               echoRepSent += 1
         if "req" == packet[6][12:15]:
               echoReqSent += 1
               totalReqBytesSent += int(packet[5])
               payloadSent += (int(packet[5]) - 42)
      elif IP == packet[3]:
         times.append(float(packet[1]))
         if "rep" == packet[6][12:15]:
               echoRepRecieved += 1
         if "req" == packet[6][12:15]:
               echoReqRecieved += 1
               totalReqBytesRecieved += int(packet[5])
               payloadRecieved += (int(packet[5]) - 42)
      else:
         continue

   time_sum = int()
   for i in range(0, len(times) - 1, 2):
      time_sum += (times[i + 1] - times[i])
   avgPingRTT = (time_sum / (len(times) / 2)) * 1000

   throughput = int()
   goodput = int()

   pingTime = (float(requests[-1][1])) - (float(requests[0][1]))
   throughput = ((totalReqBytesRecieved + totalReqBytesSent)/pingTime)/1000
   goodput = ((payloadRecieved + payloadSent)/pingTime)/1000

   delaySum = int()
   for i in range(0, len(times) - 1, 2): #While i has not iterated through the entire list
      delaySum += times[i + 1] - times[i]

   avgTimes = delaySum /(len(times)/2) #in miliseconds
   replyDelay = avgTimes*1000 #Convert to microseconds

   fileName = "output.csv"
   f = open(fileName, "a")
   f.write("")
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
   f.write("Average Echo Request Hop Count," + str(avgHops) + "\n\n")
