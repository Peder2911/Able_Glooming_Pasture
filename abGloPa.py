#!/usr/bin/env python

import fire

import subprocess
import sys

from fun import util


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

#####################################

class pipes():
    def clean(self):
        pass
    def stem(self):
        script = util.relPath('./pipes/stemmer.py',__file__)
        p = util.pipeProcess('python',script,
                             logger = fl,input = sys.stdin.read().encode())
        sys.stdout.write(p.stdout.decode())
    def ner_tokenize(self):
        pass
    def synonyms(self):
        pass


#####################################

if __name__ == '__main__':
    fire.Fire(pipes)
