#!/usr/bin/env python

import fire

import subprocess
import sys
import os

from lib import util


#####################################

import logging

from logging.config import dictConfig

import yaml
import json
import csv

logConf = util.relPath('./resources/config/logging.yaml',__file__)
with open(logConf) as file:
    logConf = yaml.load(file)
    logConf['handlers']['file']['filename'] = 'logs/Able_Glooming_Pasture.log'

dictConfig(logConf)

fl = logging.getLogger('base_file')
cl = logging.getLogger('base_console')

def processField(data,field,function):
    result = []
    for row in data:
        row[field] = function(row[field])
        result.append(row)
    return(result)

def pipeProcessText():
    

#####################################

class pipes():
    def __init__(self,field = 'body'):
        '''
        Accepts data in .json format
        '''

        self.data = json.load(sys.stdin)
        self.field = field

    def charsOnly(self): #FIXME
        script = util.relPath('./pipes/cleaner.py',__file__)

        p = util.pipeProcess('python',script,
                             logger = fl,
                             input = self.data.encode())

        sys.stdout.write(p.stdout.decode())

    def stem(self):
        script = util.relPath('./pipes/stemmer.py',__file__)

        p = util.pipeProcess('python',script,
                             logger = fl,
                             input = self.data.encode())

        sys.stdout.write(p.stdout.decode())

    def ner(self):

        script = util.relPath('./pipes/simpleNer.py',__file__)
        dataPath = util.relPath('./resources/data/names.csv',__file__)
        dataPath = os.path.abspath(dataPath)

        def nerProcess(text):
            p = util.pipeProcess('python',script,
                                 logger = fl,
                                 input = text.encode(),
                                 arguments = [dataPath])
            return(p.stdout.decode())

        result = processField(self.data,self.field,nerProcess)
        json.dump(result,sys.stdout)

    def synonyms(self): #FIXME
        pass


#####################################

if __name__ == '__main__':
    fire.Fire(pipes)
