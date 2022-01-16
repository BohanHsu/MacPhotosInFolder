#!/usr/bin/env python3

import sys
import platform
from os import listdir
from os import path
from os import stat

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

filePath = sys.argv[1]

files = listdir(filePath)

print(files)

file = files[0]

#newPath = os.path.join(filePath, file)
newPath = path.join(filePath, file)

print(newPath)

isFileDir = path.isdir(newPath)

print(isFileDir)

photoFiles = listdir(newPath)

print(photoFiles)

class Folder:
  def __init__(self, folderName, fileNames):
    self.folderName
    self.fileNames

def checkPath(strPath):
  files = []
  dirs = []
  dotDSStore = ".DS_Store"
  files = listdir(filePath)
  for fileName in files:
    if fileNames != dotDSStore:
      fileAbsoltePath = path.join(filePath, file)
      isFileDir = path.isdir(fileAbsoltePath)
      if isFileDir:
        dirs.append(fileAbsoltePath)
      else:
        files.append(fileAbsoltePath)

  return Folder(dirs, files)


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return path.getctime(path_to_file)
    else:
        filestat = stat(path_to_file)
        try:
            return filestat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return filestat.st_mtime

def main():
  testFilePath = ""

  print(creation_date(testFilePath))

main()




