from os import listdir
from os.path import isfile, islink, join
import sqlite3
import hashlib
from manageDB import DBManager
import zipfile

firmwares = []

count = 0

#--------------------------------------------------------------------------------------------------

terminalFormats = {
'HEADER': '\033[95m',
'OKBLUE': '\033[94m',
'OKGREEN': '\033[92m',
'WARNING': '\033[93m',
'FAIL': '\033[91m',
'ENDC': '\033[0m',
'BOLD': '\033[1m',
'ITALIC': '\033[3m',
'UNDERLINE': '\033[4m'}

def tform(string, format):
    return str(terminalFormats[format]+string+terminalFormats['ENDC'])

#--------------------------------------------------------------------------------------------------

def ls(directory, lead=''):
    contents = sorted(listdir(directory))
    l = []
    for item in contents:
        if isfile(join(directory, item)):
            l.append(lead+item)
        else:
            l.append(lead+tform(item, 'OKBLUE'))
    print '\n'.join(l)

#--------------------------------------------------------------------------------------------------

def getContents(directory):
    l = []
    if isfile(directory):
        return l
    else:
        contents = sorted(listdir(directory))
        for item in contents:
            l.append(item)
        return (directory.split('/')[-1], l)

#--------------------------------------------------------------------------------------------------

def recursiveList(directory, leader=' '):
    if isfile(directory):
        print leader+'- '+''.join(directory.split('/')[-1])
    elif islink(directory):
        print leader+'- '+tform(''.join(directory.split('/')[-1]), 'OKGREEN')
    else:
        print leader+' '+tform(''.join(directory.split('/')[-1]), 'OKBLUE')
        contents = sorted(listdir(directory))

        for item in contents:
            recursiveList(join(directory, item), leader+' |')

#--------------------------------------------------------------------------------------------------

def functionWalk(directory, function, cid, fid):
        nid = function(directory, cid, fid)
        if not isfile(directory) and not islink(directory):
            contents = sorted(listdir(directory))
            for item in contents:
                functionWalk(join(directory, item), function, nid, fid)


#--------------------------------------------------------------------------------------------------

def makeFirmwareList(directory, leader=' '):
    global count
    global firmwares
    if (isfile(directory)):
        if ('.ZIP' in directory.upper()) and ('FIRMWARE' in ''.join(directory.split('/')[-1])):
            #print leader+'- '+''.join(directory.split('/')[-1])#+" - "+fx.hexdigest()
            firmwares.append(directory)
            count += 1
    elif islink(directory):
        pass
        #print leader+'- '+tform(''.join(directory.split('/')[-1]), 'OKGREEN')
    else:
        #print leader+' '+tform(''.join(directory.split('/')[-1]), 'OKBLUE')
        contents = sorted(listdir(directory))

        for item in contents:
            makeFirmwareList(join(directory, item), leader+' |')

#---------------------------------------------------------------------------------------------------
import os, shutil

makeFirmwareList('firmware')

fmeta = []

for firmware in firmwares:
    zip_ref = zipfile.ZipFile(firmwares[0], 'r')
    zip_ref.extractall('tmp')
    zip_ref.close()

    path = firmware
    extracted = os.listdir('tmp')
    size = os.path.getsize(path)

    fmeta.append((path, extracted))

    print "@"+path
    print "#"+str(size)
    for x in extracted:
        print " - "+x+" ^ "+str(os.path.getsize('tmp/'+x))

    for the_file in os.listdir('tmp'):
        file_path = os.path.join('tmp', the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
