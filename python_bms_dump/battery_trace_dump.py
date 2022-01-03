#!/bin/python
import datetime
import csv
import sys

def extractIntFrom55BitField(bitfield, startbit, nbits):
    if startbit<0:
        startbit=55+startbit
    if (startbit+nbits)>55:
        return 0
    rightPad=55-(startbit+nbits)
    if rightPad<0:
        return 0
    mask = ((pow(2,nbits)-1)<<rightPad)
    return((bitfield & mask) >> rightPad)

def extractAllFieldsFrom55BitField(bitfield, listOfLengths):
    startpos=0
    returnVal=[]
    for l in listOfLengths:
        returnVal.append(extractIntFrom55BitField(bitfield, startpos, l))
        startpos=startpos+l
    return returnVal

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)
filtered = filter(lambda p: '261' == p[4], reader)
for row in filtered:
    millis = int(row[2])/1000
    mux = int(row[7],16)
    data = row[8:15]
    dataVal = int(''.join(data),16)
    dataVal = dataVal << 1
    vals = extractAllFieldsFrom55BitField(dataVal, [11]*5)
    vals = [v*2 for v in vals]

    hours, minutes  = (millis/1000) // 3600, (millis/1000) %3600//60 
    seconds = (millis/1000) - hours*3600 - minutes*60

    writer.writerow([int(hours)] + [int(minutes)] + [int(seconds)] + [mux] + vals)

#    hours, remainder = divmod(millis/1000, 3600)
#    minutes, seconds = divmod(remainder, 60)

#    writer.writerow([int(millis/1000)] + [mux] + vals)

