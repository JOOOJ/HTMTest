#! /usr/bin/python

import csv
import os
import datetime
from nupic.frameworks.opf.common_models.cluster_params import (
  getScalarMetricWithTimeOfDayAnomalyParams)
from nupic.frameworks.opf.model_factory import ModelFactory
from anomalyDetect import anomaly_detect
#from algorithm.multiStreamAnomalyDetect import multi_stream_anomaly_detect
#import nupic

csvfile = "D:\VS\HTMTest\Data\Test.csv"

def runModel(length,rawdata):
    # input file:
    inputFilePath = os.path.join(os.getcwd(), csvfile)
    # output file:
    outputPath = os.path.join(os.getcwd(), "D:\VS\HTMTest\Data\Test_Output3.csv")
  
    detectObject = anomaly_detect(
            pointCount = length,
            rawData = rawdata)

    with open(outputPath,'wb') as outfile:
        writeFile = csv.writer(outfile)
        columnsName = ["timestamp", "value", "prediction","anomalyScore","likelihoodScore","anomalyLabel"]
        writeFile.writerow(columnsName)
        #for key,value in dataPoints.iteritems():
        with open(inputFilePath,'rb') as input:
            csvReader = csv.reader(input)
            csvReader.next()
            csvReader.next()
            csvReader.next()
            for row in csvReader:
                # format the timestamp.
                timestamp = row[0]
                # get the target value: actualValue.
                actualValue = row[1]
                # put the timestamp and the target value into the model.
                output = detectObject.anomalyDetect(timestamp,actualValue)
                prediction = output["predictValue"]
                anomalyScore = output["anomalyScore"]
                finalScore = output["likelihoodScore"]
                anomalylabel = output["anomalylabel"]
                writeFile.writerow([timestamp, actualValue, prediction,anomalyScore,finalScore,anomalylabel])
           #print "a value = %s prediction = %s anomalyScore = %s" % (str(actualValue), str(prediction),str(anomalyScore))

def getDataLength():
    inputFilePath = os.path.join(os.getcwd(), csvfile)
    length=0
    rawdata=[]
    with open(inputFilePath,'rb') as input:
        csvReader = csv.reader(input)
        csvReader.next()
        csvReader.next()
        csvReader.next()
        for row in csvReader:  
            length+=1
            rawdata.append(float(row[1]))
    return length,rawdata
    
def runTest():
    (length,rawdata) = getDataLength()
    runModel(length,rawdata)

if __name__ == "__main__":
    runTest()