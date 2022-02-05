#!/usr/bin/env python3

from os import listdir
from os import path
from os import stat
from datetime import datetime
import sys
import platform
import subprocess
import collections


class Folder:
  def __init__(self, folderPaths, filePaths):
    self.folderPaths = folderPaths
    self.filePaths = filePaths


def readFileAndFolderInPath(filePath):
  """
  Read a foler file path, return files and sub-folders in the given folder
  """
  files = []
  dirs = []
  dotDSStore = ".DS_Store"
  fileAndDirInFolder = listdir(filePath)
  for fileName in fileAndDirInFolder:
    if fileName != dotDSStore:
      fileAbsoltePath = path.join(filePath, fileName)
      isFileDir = path.isdir(fileAbsoltePath)
      if isFileDir:
        dirs.append(fileAbsoltePath)
      else:
        files.append(fileAbsoltePath)

  return Folder(dirs, files)


def creationTime(pathToFile):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return path.getctime(pathToFile)
    else:
        filestat = stat(pathToFile)
        try:
            return filestat.st_birthtime
        except AttributeError:
            return filestat.st_mtime


def suggestDestinationForFile(pathToFile, dest):
  """
  Suggest a file name base on the given file's creation time.
  If there is naming collision in the destination folder, suggest a non-colliding
  name by suffixing number.
  """
  fileCreationTimeUnixtimestamp = creationTime(pathToFile)
  fileCreationDateObj = datetime.fromtimestamp(fileCreationTimeUnixtimestamp);
  creationTimeString = fileCreationDateObj.strftime("%m-%d-%Y_%H-%M-%S")
  suffix = pathToFile.split(".")[-1]
  suggestName = creationTimeString + "." + suffix

  suggestedPath = path.join(dest, suggestName)
  fileExists = path.exists(suggestedPath)
  suggestCount = 0
  while fileExists:
    suggestName = creationTimeString + "_" + str(suggestCount) + "." + suffix
    suggestCount = suggestCount + 1
    suggestedPath = path.join(dest, suggestName)
    fileExists = path.exists(suggestedPath)

  return suggestedPath


def copyFile(source, target):
  """
  Copy a file, need absolute source and target path.
  """
  print ("Copy file\n{0}\n{1}\n".format(source, target))
  result = subprocess.run(["cp", source, target])


def moveFileOutOfMacPhotoFolder(macPhotoFolder, dest):
  folderQueue = collections.deque([macPhotoFolder])
  fileQueue = collections.deque([])

  while len(folderQueue) > 0 or len(fileQueue) > 0:
    while len(fileQueue) > 0:
      filePath = fileQueue.popleft()
      suggestedPath = suggestDestinationForFile(filePath, dest)
      copyFile(filePath, suggestedPath)

    while len(folderQueue) > 0:
      folderPath = folderQueue.popleft()
      folder = readFileAndFolderInPath(folderPath)
      folderQueue.extend(folder.folderPaths)
      fileQueue.extend(folder.filePaths)


def main():
  absoluteSourcePath = path.abspath(sys.argv[1])
  absoluteDestPath = path.abspath(sys.argv[2])
  print(absoluteSourcePath)
  print(absoluteDestPath)
  if not path.isdir(absoluteSourcePath):
    print("Source path is not a directory")

  if not path.isdir(absoluteDestPath):
    print("Destination path is not a directory")

  moveFileOutOfMacPhotoFolder(absoluteSourcePath, absoluteDestPath)

main()




