import os
import json
from os import listdir
import os

def inspectSummary(tempdir, newName):
    os.chdir(os.path.join(tempdir + '/' + newName))

    openRead = open('SUMMARY', 'r')
    wantedValues = ['BOARD', 'FIRMUX', 'BUILD', 'LOAD', 'RAM', 'print', 'UPTIME']
    summaryFileContent = []

    for line in openRead:
        for value in wantedValues:

            if value in line:
                summaryFileContent.append(line)   
    
    dict = {}
    
    size = len(summaryFileContent)
    for i in range(size):

        partitionedString = summaryFileContent[i].partition('=')

        dict[partitionedString[0]] = partitionedString[2]
        if partitionedString[0] == 'LOAD':
            dict['CPU LOAD'] = dict.pop('LOAD')

    for j in dict:
        if j == 'RAM':
            ramKB =  dict[j].partition(' ')
        if j == 'CPU LOAD':
            cpuLoad = dict[j].split(' ')
    
    with open("SUMMARY", "r") as f:
        content = f.read()
   
    return dict, ramKB, cpuLoad, content


def inspectHangedProcesses(tempdir, newName):

    os.chdir(os.path.join(tempdir + '/' + newName + '/Raw_data_dumps'))

    if os.path.isfile('ps'):
        openRead = open('ps', 'r')

        statContent = [] 

        unwantedStates = ['D', 'X', 'T', 'Z', 't']
        commonStatCounter = 0

        for possition, line in enumerate(openRead):
            
            if possition == 0:
                stat = line.split('STAT')[0]
                command = line.split('COMMAND')[0]
                statContent.append(line)
                
            if possition != 0:
                partitionedState = line[len(stat):len(command)]
                
                partitionedState = partitionedState.replace(" ", "")

                for i in unwantedStates:
                    if i in partitionedState:
                        
                        commonStatCounter += 1
                        statContent.append(line)

        os.chdir(os.path.join(tempdir + '/' + newName))

        commonStatCounter += 1
        statContent.append("  17 root         0 D   [watchdog/2]")

        if commonStatCounter == 0:
            statContentText='No hanged processes detected'
            statContent.pop(0)
            return statContent, statContentText 
        else:
            statContentText='Number of detected hanged processes: ' + str(commonStatCounter)
            return statContent, statContentText  
    
    else:
        os.chdir(os.path.join(tempdir + '/' + newName))
        statContentText='ps file is not found'
        commonStatCounter = 0
        statContent = []
        return statContent, statContentText 


def pstore(tempdir, newName):
    
    os.chdir(os.path.join(tempdir + '/' + newName))

    searchValues = ['Oops:', 'oom-killer']
    list_of_results = []
    line_number = 0
      
    if len(os.listdir(tempdir + '/' + newName + '/Raw_data_dumps/pstore') ) == 0: 
        pstore_text = "Pstore folder is empty"

    else:    
                       
        for filename in listdir(tempdir + '/' + newName + '/Raw_data_dumps/pstore'): 
                 
            with open(tempdir + '/' + newName + '/Raw_data_dumps/pstore' + '/' + filename, 'r') as read_obj: 

                line_number = 0

                for line in read_obj:

                    line_number += 1 

                    for i in searchValues: 

                        if i in line:
                            list_of_results.append((line_number, line.rstrip()))
                            
                list_of_results.append("labas")
                if list_of_results:
                    pstore_text = 'Anomality detected in Pstore file: ' + filename 
                else:
                    pstore_text="No craches or OOMs detected"

    return pstore_text, list_of_results
