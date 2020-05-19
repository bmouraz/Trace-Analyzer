import sys
import re
import os
import matplotlib.pyplot as plt
import pandas as pd

def analyzer(filename):

    lines = open(filename).readlines()
    lines=[x.split() for x in lines]

    dirName = "csvfiles"
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    csvfile = open("csvfiles/parameters.csv","w+")
    csvfile.write("Node,Lambda(\u03BB),E[N],E[W],E[W]*lambda,Throughput,Goodput,Dropped Packets,Data Sent(kB),JitterSum\n")

    completecsvfile = open("csvfiles/complete.csv","w+")
    completecsvfile.write("Time,Node,Lambda(\u03BB),E[N],E[W],E[W]*lambda,Throughput,Goodput,Dropped Packets,Data Sent(kB),Jitter,JitterSum\n")


    tmpSimu = lines[len(lines)-1][1]
    sentsizetemp = re.findall(r'\d+', lines[1][38])
    sentsize = int(sentsizetemp[0])

    #PacketSize
    totallength = lines[1][27]
    sizelength = lines[1][33]



    pcktloss = 0
    jitterrec = 0
    nodelist = []
    listrec = []
    sentdatarec = []
    jitter = []
    jitterrec = []
    jitterSum = []


    for i in range (len(lines)):


        if lines[i][0] == "+":
            timep = float(lines[i][1])

            if pcktloss > 0:

                rtimes = 0


        elif lines[i][0] == "-":
            timem = float(lines[i][1])
            queuedelay = timem - timep
        else:
            #Received time
            timerec = float(lines[i][1])

            #node
            temp = re.findall(r'\d+', lines[i][2])
            res = list(map(int, temp))
            node = res[0]


            if not node in nodelist:

                nodelist.append(int(node))
                listrec.append(1)
                if (int(node)) != 0 and (len(jitter)) < (int(node))+1:
                    for i in range (int(node)+1):
                        jitter.append(0)
                        jitterSum.append(0)
                        jitterrec.append(0)
                if (len(jitter)) == (int(node))+1 or (int(node)) == 0 :
                    jitter[int(node)] = timerec


                if lines[i][31] == "ns3::UdpHeader":
                    sentdatarec.append(int(lines[i][33]))
                else:
                    sentdatarec.append(int(lines[i][27]))
            else:

                listrec[int(node)-1] = listrec[int(node)-1] + 1
                if lines[i][31] == "ns3::UdpHeader":
                    # print ("node{}: sent {}" .format(node,lines[i][33]) )
                    sentdatarec[int(node)] = sentdatarec[int(node)] + int(lines[i][33])
                else:
                    # print ("node{}: sent {}" .format(node,lines[i][27]) )
                    sentdatarec[int(node)] = sentdatarec[int(node)] + int(lines[i][27])

                # print(jitter, timerec, node)
                jitter[int(node)] = - (jitter[int(node)] - timerec)
                jitterSum[int(node)] = jitterSum[int(node)] + jitter[int(node)]
                jitterrec[int(node)] = jitter[int(node)]
                jitter[int(node)] = timerec

            #Propagation delay
            propdelay = timerec - timem
            if i+1 < len(lines):
                temp = re.findall(r'\d+', lines[i+1][2])
                res = list(map(int, temp))
                nodenext = res[0]
                #if >1 has packet loss
                if nodenext == node and lines[i+1][0] == lines[i][0]:
                    pcktloss += 1
                    # print(pcktloss)

            try:

                lambdacalc = ((float(sentdatarec[int(node)]))/float(sizelength))/(float(tmpSimu))
                en = 0
                ew = 0
                throughput = lambdacalc*(float(totallength)+2)
                goodput = lambdacalc*((float(sentdatarec[node]))/listrec[node])
                droppedpackets = pcktloss
                stringcsv =("{},{},{},{},{},{},{},{},{},{},{},{}\n" .format(timerec,nodelist[int(node)],lambdacalc,en,ew,en*lambdacalc,throughput,goodput,droppedpackets,sentdatarec[int(node)]/1000,jitterrec[int(node)],jitterSum[node]))
                completecsvfile.write(stringcsv)
            except:

                lambdacalc = ((float(sentdatarec[int(0)]))/float(sizelength))/(float(tmpSimu))
                en = 0
                ew = 0
                throughput = lambdacalc*(float(totallength)+2)
                goodput = lambdacalc*((float(sentdatarec[int(0)]))/listrec[0])
                droppedpackets = pcktloss
                stringcsv =("{},{},{},{},{},{},{},{},{},{},{},{}\n" .format(timerec,nodelist[0],lambdacalc,en,ew,en*lambdacalc,throughput,goodput,droppedpackets,sentdatarec[0]/1000,jitterrec[0],jitterSum[0]))
                completecsvfile.write(stringcsv)

    for i in range (len(nodelist)):
        lambdacalc = ((float(sentdatarec[i]))/float(sizelength))/(float(tmpSimu))
        en = 0
        ew = 0
        throughput = lambdacalc*(float(totallength)+2)
        goodput = lambdacalc*(float(sentdatarec[i]/listrec[i]))
        droppedpackets = pcktloss
        stringcsv =("{},{},{},{},{},{},{},{},{},{}\n" .format(nodelist[i],lambdacalc,en,ew,en*lambdacalc,throughput,goodput,droppedpackets,sentdatarec[i]/1000,jitterSum[i]))
        # print(stringcsv)
        csvfile.write(stringcsv)
