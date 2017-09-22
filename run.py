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

def runModel(length):
    # input file:
    inputFilePath = os.path.join(os.getcwd(), "D:\VS\HTMTest\Data\Test.csv")
    # output file:
    outputPath = os.path.join(os.getcwd(), "D:\VS\HTMTest\Data\Test_Output.csv")
  
    detectObject = anomaly_detect(
            pointCount = length)

    with open(outputPath,'wb') as outfile:
        writeFile = csv.writer(outfile)
        columnsName = ["timestamp", "value", "prediction","anomalyScore","likelihoodScore"]
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
            
                writeFile.writerow([timestamp, actualValue, prediction,anomalyScore,finalScore])
           #print "a value = %s prediction = %s anomalyScore = %s" % (str(actualValue), str(prediction),str(anomalyScore))

def getDataLength():
    inputFilePath = os.path.join(os.getcwd(), "D:\VS\HTMTest\Data\Test.csv")
    length=0
    with open(inputFilePath,'rb') as input:
        csvReader = csv.reader(input)
        csvReader.next()
        csvReader.next()
        
        for row in csvReader:            
            length+=1
    return length
    
def runTest():
    length = getDataLength()
    runModel(length)

if __name__ == "__main__":
    runTest()