import subprocess
import os

#####################################

def relPath(filePath,fileVar):
    selfPath = os.path.dirname(fileVar)
    relPath = os.path.join(selfPath,filePath)
    return(relPath)

def pipeProcess(interpreter,file,arguments=[],logger=None,**kwargs):
        script = [interpreter,file]
        script += arguments

        if not logger is None:
            logger.debug('running ' + os.path.abspath(script[1]))

        p = subprocess.run(script,
                           stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE,
                           **kwargs)

        try:
            p.check_returncode()
        except subprocess.CalledProcessError:
            if not logger is None:
                logger.critical(p.stderr.decode())
            raise subprocess.CalledProcessError

        stderr = p.stderr.decode()
        logger.debug(stderr)

        return(p)

#####################################

def stringToStdFormat(string):
    
    '''
    Converts a csv. formatted string into the list-of-dictionaries format
    used by Diverse_Folio_Isle and Able_Glooming_Pasture
    '''

    fauxFile = StringIO(string)

    with fauxFile as csvFile:
        reader = csv.reader(csvFile)
        names = next(reader)

        result = []
        for line in reader:

            lineResult = {}
            for n,entry in enumerate(line):
                lineResult.update({names[n]:entry})

            result.append(lineResult)

    return(result)
