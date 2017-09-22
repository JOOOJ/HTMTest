#! /usr/bin/python

import json
import datetime
import numpy as np
import math

from nupic.frameworks.opf.model_factory import ModelFactory
from nupic.frameworks.opf.common_models.cluster_params import getScalarMetricWithTimeOfDayAnomalyParams
from nupic.algorithms.anomaly_likelihood import AnomalyLikelihood
from Test_model_params import MODEL_PARAMS

class anomaly_detect():
    """
    stream data anomaly detect for one field.
    """
    
    def __init__(self, pointCount):
        
        self.timestamp = None
        self.actualValue = None
        self.predictValue = None
        self.anomalyScore = None
        self.modelResult = None
        self.output = None
        
        probationaryPercent = 0.15
        probationaryPeriod = self.getProbationPeriod(probationaryPercent,pointCount)
        numentaLearningPeriod = int(math.floor(probationaryPeriod / 2.0))
        self.anomalyLikelihood = AnomalyLikelihood(
            learningPeriod=numentaLearningPeriod,
            estimationSamples=probationaryPeriod-numentaLearningPeriod,
            reestimationPeriod=100
        )
        self.model = ModelFactory.create(MODEL_PARAMS)
        self.model.enableInference({"predictedField": "value"})

    def anomalyDetect(self, timestamp, actualValue):
        # anomaly detect method for one field.
        self.timestamp = timestamp
        self.actualValue = actualValue

        # convert the timestamp/actualValue into proper type.
        # the string of input timestamp should be like this: 2017-2-18 0:00:00
        #self.timestamp = datetime.datetime.strptime(self.timestamp, "%Y-%m-%dT%H:%M:%SZ")
        self.timestamp = datetime.datetime.strptime(self.timestamp, "%m/%d/%Y %H:%M")
        self.actualValue = float(self.actualValue)
        
        self.modelResult = self.model.run({
            "timestamp": self.timestamp,
            "value": self.actualValue
        })
        print self.modelResult
        self.predictValue = self.modelResult.inferences["multiStepBestPredictions"][1]
        if self.modelResult.inferences["anomalyScore"] is not None:
            self.anomalyScore = float(self.modelResult.inferences["anomalyScore"])
        else:
            self.anomalyScore = -1
        
        probScrore = self.anomalyLikelihood.anomalyProbability(
            self.actualValue, self.anomalyScore, self.timestamp)
        finalScore = self.anomalyLikelihood.computeLogLikelihood(probScrore)
        self.output = {
            "timestamp": self.timestamp,
            "actualValue": self.actualValue,
            "predictValue": self.predictValue,
            "anomalyScore": self.anomalyScore,
            "likelihoodScore":finalScore
        }
        return self.output
        
    def getProbationPeriod(self,probationPercent, pointCount):
        """Return the probationary period index."""
        return min(
            math.floor(probationPercent * pointCount),
            probationPercent * 5000)