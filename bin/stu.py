#!/usr/bin/env python3
# Python script to help with recursive git actions
import getopt, sys
import argparse
import os
import glob
import platform
import pickle

helpText = 'stu is a wrapper utility to help use git with many submodules. Try stu help for more info'

devDir = os.environ.get('DEVDIR')

parser = argparse.ArgumentParser(description=helpText)

parser.add_argument(dest='command', nargs="?", type=str, help="command to execute")

parser.add_argument("-V", "--version", help="show program version", action="store_true")
parser.add_argument("-b", help="short status", action="store_true")
parser.add_argument("-A", help="add all status", action="store_true")
parser.add_argument("-v", help="verbose", action="store_true")

parser.add_argument(dest='parameter1', nargs="?", type=str, help="branch to checkout", default="working")

# Read arguments from the command line
args = parser.parse_args()


def findFile(name, path):
	resList = []
	for root, dirs, files in os.walk(path):
		if name in files:
			res = os.path.join(root, name)
			resList.append(res)
	return resList

def findDir(dirName, path):
	resList = []
	for root, dirs, files in os.walk(path):
		for name in dirs:
			if dirName.upper() in name.upper():
				res = os.path.join(root, name)
				resList.append(res)
	return resList

def findSubDirs(dirName):
	resList = []
	for file in os.listdir(dirName):
		d = os.path.join(dirName, file)
		if os.path.isdir(d):
			resList.append(file)
	return resList

def doVortexGenerate():
	commonCppDir=min(findDir("CommonCppDartCode", vortexDir), key=len)
	print(commonCppDir)
	os.chdir(commonCppDir)
	os.system("Generate.bat")


class WorkSpace:
	projectDirs = None
	matrixDir = None
	vortexDir = None
	backChannelDir = None
	workingDir = None
	def __init__(self, _projectDirs, _matrixDir, _vortexDir, _workingDir):
		self.projectDirs = _projectDirs
		self.matrixDir = _matrixDir
		self.vortexDir = _vortexDir
		self.workingDir = _workingDir
	def scan(self):
		global devDir
		print("Scanning {}".format(devDir))
		self.projectDirs=findSubDirs(devDir)
		self.matrixDir=min(findDir("Matrix", devDir), key=len, default="EMPTY")
		self.vortexDir=min(findDir("Vortex", devDir), key=len, default="EMPTY")
		self.backChannelDir=min(findDir("backChannel", devDir), key=len, default="EMPTY")
		self.workingDir = self.vortexDir
	def printAll(self):
		print("Project dirs {}".format(self.projectDirs))
		print("Matrix dir {}".format(self.matrixDir))
		print("Vortex dir {}".format(self.vortexDir))
		print("Working dir {}".format(self.workingDir))
	def load(self):
		pickleFile = os.path.join(devDir, "pickleFile")
		if os.path.exists(pickleFile):
			with open(pickleFile, 'rb') as f:
				WS = pickle.load(f)
				self.__init__(WS.projectDirs, WS.matrixDir, WS.vortexDir, WS.workingDir)

	def save(self):
		pickleFile = os.path.join(devDir, "pickleFile")
		with open(pickleFile, 'wb') as f:
			pickle.dump(self, f)
	def setup(self):
		self.load()
		if not self.projectDirs:
			self.scan()
			self.save()

workSpace = WorkSpace(None, None, None, None)

def setup():
	global workSpace
	workSpace.setup()
		

# -------------------------------------------------------------------------

setup()

# -------------------------------------------------------------------------

# Check for --version or -V
if args.version:
    print("This is stu git assistant version 1.0")

def doPrintHelp():
	print("\nusage: stu [-h] [-V] [command] [parameter]")
	print("")
	print(helpText)
	print("")
	print("  stu requires the environment variable DEVDIR to be set to the root development directory")
	print("  It is expected the project directories such as Matrix are set under this.")
	print("  So if DEVDIR is 'C:\Dev', then it is expected that the matrix project is in 'C:\dev\Matrix'. ")
	print("")
	print("  NOTE it is important that the workspace is set by doing 'stu workspace <project dir> at least once.")
	print("    Eg. 'stu workspace Matrix'")
	print("")
	print("\ncommands:			recursive actions on this and all submodules")
	print("   status <-b>                                           <-b> for brief")
	print("   checkout  <branchName>")
	print("   pull							current branch")
	print("   pullVortex					pull current branch and run generate")
	print("   push							current branch")
	print("   add -A						git add -A")
	print("   branch -v						git branch -v")
	print("   remote -v						git remote -v")
	print("   commit <message>					git commit <message>")
	print("   workspace <dirName>			set workspace. E.g stu workspace Vortex")

def doGitSubmodules(commandLine):
#	print('git submodule foreach --recursive "{} || :"'.format(commandLine))
	print('----------- for each submodule -----------')
	os.system('git submodule foreach --recursive "{} || :"'.format(commandLine))

def doGitMainDir(commandLine):
	print("Project {}".format(workSpace.workingDir))
	print("{}".format(commandLine))
	os.chdir(workSpace.workingDir)
	os.system(commandLine)

def doGit(commandLine):
	doGitMainDir(commandLine)
	doGitSubmodules(commandLine);

if len(sys.argv)==1:
	doPrintHelp()

if args.command == "help":
	doPrintHelp()

if args.command == "status":
	if (args.b):
		doGit("git status -s -b")
	else:
		doGit("git status")

if args.command == "checkout":
	doGit("git checkout {}".format(args.parameter1))

if args.command == "push":
	doGit("git push")

if args.command == "pull":
	doGit("git pull")

if args.command == "pullVortex":
	doGit("git pull")
	os.chdir(workSpace.workingDir)
	os.system("cd .\\lib\\ftlTools\\network\\CommonCppDartCode & Generate.bat")

if args.command == "fetch":
	doGit("git fetch {}".format(args.parameter1))

if args.command == "add":
	if (args.A):
		doGit("git add -A")
	else:
		print("Invalid option");

if args.command == "branch":
	if (args.v):
		doGit("git branch -v")
	else:
		print("Invalid option");

if args.command == "remote":
	if (args.v):
		doGit("git remote -v")
	else:
		print("Invalid option");

if args.command == "commit":
	if (args.parameter1):
		doGitMainDir("git commit -m \"{}\"".format(args.parameter1))
		doGitSubmodules("git commit -m '{}'".format(args.parameter1))
	else:
		print("Invalid option");

if args.command == "workspace":
	if args.parameter1 in workSpace.projectDirs:
		workSpace.workingDir = os.path.join(devDir, args.parameter1)
		print("Set working dir to {}".format(workSpace.workingDir))
		os.chdir(workSpace.workingDir)
		workSpace.save()
		#if platform.system()=="Windows":
			#os.system("cmd")
		#if platform.system()=="Linux":
			#os.system("/bin/bash")
	else:
		print("ERROR - Unknown workspace {} - check capitalization".format(args.parameter1))

if args.command == "test":
	#doVortexGenerate()
	setup()
