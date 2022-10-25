from importlib.metadata import files
import os
import shutil
import tarfile

folderKeyCount = 3
fileStatusSymbol = 's'
folderKeyValues = ['SUMMARY', 'Raw_data_dumps', 'Raw_data_files']

# funkcija direktoriju trynimui
def folderDeletion(path):
    listDir = os.listdir(path)
    for filename in listDir:
        filePath = os.path.join(path, filename)
        if os.path.isfile(filePath) or os.path.islink(filePath):
            os.unlink(filePath)
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath)
    os.rmdir(path)

# funkcija .tar.gz failu ikelimui
def troubleshootFileExtraction(tempdir, troubleshootFiles, index, fileStatus):
    extractElementCounter  = 0
    movingForward = False
    file = tarfile.open(troubleshootFiles[index])   
    file.extractall(os.path.join(tempdir))

    for i in folderKeyValues:
        arr = os.listdir(os.path.join(tempdir + '/' + 'diagnose'))
        if i in arr:
            extractElementCounter  += 1

    if extractElementCounter  == folderKeyCount:
        os.chdir(os.path.join(tempdir))
        os.rename('diagnose', newName)
        file.close()
        os.chdir(tempdir)
        if fileStatus == fileStatusSymbol:
            print('\nFile *** ' + troubleshootFiles[index] + ' *** uploaded successfully\n')
        movingForward = True
        return newName, movingForward
    
    elif extractElementCounter  != folderKeyCount:
        os.rename('diagnose', newName)
        if len(troubleshootFiles) == 1:
            print('\nSelected file (' + newName + ".tar.gz" + ') is not appropriate for troubleshoot diagnostics\n')
            folderDeletion(newName)
            tmpnewName = ''
        os.remove(newName + ".tar.gz")
        newName = tmpnewName
        return newName, movingForward

# funkcija .tar.gz failu extractinimui ir pervadinimui
def troubleshootFileContentExtract(tempdir, troubleshootFiles, index, fileStatus):
    newName = ''
    newName = troubleshootFiles[index].replace('.tar.gz','')

    if (os.path.isdir(tempdir + '/' + newName)) is False:
        os.chdir(os.path.join(tempdir))

        try:
            newName, movingForward = troubleshootFileExtraction(tempdir, troubleshootFiles, index, fileStatus)
        except:
            if len(troubleshootFiles) == 1:
                print('\nSelected file (' + newName + ".tar.gz" + ') can not be opened\n')
                tmpnewName = ''
            os.remove(newName + ".tar.gz")
            newName = tmpnewName
            return newName, movingForward

    else: 
        arr = os.listdir(os.path.join(tempdir + '/' + newName))
        for i in folderKeyValues:
            if i in arr:
                extractElementCounter  += 1

        if extractElementCounter  == folderKeyCount:
            movingForward = True
            return newName, movingForward

        elif extractElementCounter   != folderKeyCount:

            if len(troubleshootFiles) == 1:
                print('\nSelected file (' + newName + ".tar.gz" + ') is not appropriate for troubleshoot diagnostics\n')
                
            os.remove(newName + ".tar.gz")
            folderDeletion(newName)
            newName = ''

            return newName, movingForward
