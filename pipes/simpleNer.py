#!/usr/bin/env python
import sys
import re
import csv

import logging

def nerTokenize(line,data):
    def reIfy(name):
        # General format = firstName_name_sirName_
        #name = name.replace('_',r'[\-\.\'\´ ]*')
        name = name.replace('_',r'[\-\.\'\´ ^$]+')
        name = r'(^| )' + name + r'($| )'
        if '|' in name:
            name = '(%s)'%name
        return(name)

    sLine = re.sub('[^a-z]','_',line.lower())
    sLine = re.sub('__+','_',sLine)
    sLine = '_' + sLine

    for entry in data:

        if '|' not in entry:
            found = entry in sLine
        else:
            for e in entry.split('|'):
                found |= e in sLine

        if found and entry != '':
            pattern = reIfy(entry)
            pattern = re.compile(pattern,flags = re.IGNORECASE)
            match = re.search(pattern,line)
            if match:
                sys.stderr.write(match[0] + ' to ' + data[entry] + '\n')
                sys.stderr.write(line + '\n')
                line = re.sub(pattern,' '+data[entry]+' ',line)

    return(line)

#####################################################
if __name__ == '__main__':

    dataPath = sys.argv[1]
    with open(dataPath) as file:
        r = csv.reader(file)
        peopleData = {}

        headers = next(r)
        for line in r:
            lineValues = {line[headers.index('name')]:line[headers.index('title')]}
            peopleData.update(lineValues)

    line = 'init'
    while line != '':
        line = sys.stdin.readline()
        if line != '':
            line = nerTokenize(line,peopleData)
            sys.stdout.write(line)
        else:
            pass
