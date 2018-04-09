from os import listdir
from os.path import isfile, islink, join, realpath, relpath, getsize
import sqlite3
import hashlib
from manageDB import DBManager

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
        pass
        #print leader+'- '+''.join(directory.split('/')[-1])
    elif islink(directory):
        pass
        #print leader+'- '+tform(''.join(directory.split('/')[-1]), 'OKGREEN')
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

def addToDatabase(directory, cid, fid):
    fx = hashlib.md5()
    if islink(directory):
        d = 1
        f = ''.join(directory.split('/')[-1])
        index = [ i for i, word in enumerate(directory.split('/')) if word.startswith('squashfs-root') ][0]
        p = '/'.join(directory.split('/')[index:])
        rp = '/'.join(relpath(realpath(directory)).split('/')[index:])
        M.addLink(cid, fid, f, p, rp)
    elif isfile(directory):
        d = 1
        f = ''.join(directory.split('/')[-1])
        index = [ i for i, word in enumerate(directory.split('/')) if word.startswith('squashfs-root') ][0]
        p = '/'.join(directory.split('/')[index:])
        s = getsize(directory)
        try:
            with open(directory, 'rb') as f1:
                while 1:
                    buf = f1.read(256)
                    if not buf : break
                    a = hashlib.md5(buf).hexdigest()
                    fx.update(a)
        except:
            import traceback
            # Print the stack traceback
            traceback.print_exc()
            print tform("Hashing issue on "+directory, 'FAIL')
        M.addFile(cid, fid, f, p, s, str(fx.hexdigest()))
    else:
        d = ''.join(directory.split('/')[-1])
        index = [ i for i, word in enumerate(directory.split('/')) if word.startswith('squashfs-root') ][0]
        #print ' --- '+'/'.join(directory.split('/')[index:])
        cid = M.addDir(fid, cid, d, '/'.join(directory.split('/')[index:]), 'f18fb3bfaf8fe67e61aaa1a10d420135')
    return cid
    #print 'Added: '+''.join(directory.split('/')[-1])

fs_list = []

with open('sqfs.dump', 'r') as infile:
    lines = infile.readlines()
    for line in lines:
        fs_list.append(line[:-1])
    print 'Loaded '+str(len(fs_list))+' directories'

M = DBManager('X.db')

vendor = "X"

M.addVendor(vendor)
number = 1
for x in fs_list:
    directory = x
    device = x.split('/')[1].split('_')[1]
    print 'Processing '+tform(device, 'OKBLUE')
    M.addDevice(device, 1)
    print ' + Added device to database'
    M.addFirmware(number,1, x, 'X', 'X', 'X')
    print ' + Added firmware to database'
    functionWalk(x, addToDatabase, number, number)
    #recursiveList(x, ' - ')
    print ' | Walked '+ directory
    M.commit()
    print tform(' = All files for '+device+' committed', 'OKGREEN')
    number += 1

M.close()
