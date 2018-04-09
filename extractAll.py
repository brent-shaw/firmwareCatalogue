from os import listdir
from os.path import isfile, islink, join
import sqlite3
import hashlib
from manageDB import DBManager

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

def printItems(directory):
    if isfile(directory):
        print ''.join(directory.split('/')[-1])
    elif islink(directory):
        print tform(''.join(directory.split('/')[-1]), 'OKGREEN')
    else:
        print tform(''.join(directory.split('/')[-1]), 'OKBLUE')

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

print "Looking for firmware"

makeFirmwareList('firmware')

print "Found "+str(count)+" valid firmwares"

M = DBManager()

vendor = "X"

M.addVendor(vendor)

#---------------------------------------------------------------------------------------------------

import sys
import binwalk

M.commit()

for z in firmwares:
    path = z.split('/')[-1]
    dev = path.split('_')[0]
    print dev
    M.addDevice(dev, 1)
    M.commit()
        
    for module in binwalk.scan(z, matryoshka=True, signature=True, extract=True, quiet=True, directory='extracted'):
        for result in module.results:
            if module.extractor.output.has_key(result.file.path):
                if module.extractor.output[result.file.path].carved.has_key(result.offset):
                    pass
                if module.extractor.output[result.file.path].extracted.has_key(result.offset):
                    pass

    M.commit()
    print ("%s extracted" % z)

M.commit()
M.close()
