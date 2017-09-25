import os

swarmConfig = {
  "includedFields": [
    {
      "fieldName": "timestamp", 
      "fieldType": "datetime"
    }, 
    {
      "fieldName": "value", 
      "fieldType": "float"
    }
  ], 
  "streamDef": {
    "info": "test", 
    "version": 1, 
    "streams": [
      {
        "info": "Test.csv", 
        "source": "file://Data\\Test.csv", 
        "columns": [
          "*"
        ]
      }
    ]   
  }, 
  "inferenceType": "TemporalAnomaly", 
  "inferenceArgs": {
    "predictionSteps": [
      1
    ], 
    "predictedField": "value"
  }, 
  "iterationCount": -1, 
  "swarmSize": "medium"
}
