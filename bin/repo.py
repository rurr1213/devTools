# Python script to help with recursive git actions
import getopt, sys
import argparse
import os

helpText = 'repo is a wrapper utility to help use git with many submodules. Try repo help for more info'

parser = argparse.ArgumentParser(description=helpText)

parser.add_argument("-V", "--version", help="show program version", action="store_true")
parser.add_argument("-b", help="short status", action="store_true")
parser.add_argument("-A", help="add all status", action="store_true")
parser.add_argument("-v", help="add all status", action="store_true")

parser.add_argument(dest='command', nargs="?", type=str, help="command to execute")
parser.add_argument(dest='parameter1', nargs="?", type=str, help="branch to checkout", default="working")

# Read arguments from the command line
args = parser.parse_args()

# Check for --version or -V
if args.version:
    print("This is repo git assistant version 1.0")

def doPrintHelp():
	print("\nusage: repo [-h] [-V] [command] [parameter]")
	print("")
	print(helpText)
	print("\ncommands:			recursive actions on this and all submodules")
	print("   status")
	print("   checkout  <branchName>")
	print("   pull				current branch")
	print("   push				current branch")
	print("   add -A			git add -A")
	print("   branch -v			git branch -v")

def doGit(commandLine):
	os.system(commandLine)
	os.system('git submodule foreach --recursive {}'.format(commandLine))

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

if args.command == "commit":
	#print("git commit -m '{}'".format(args.parameter1))
	doGit("git commit -m '{}'".format(args.parameter1))
