# *********************************************************************
# This file illustrates how to execute a command and get it's output
# *********************************************************************
# import commands

# # Run ls command, get output, and print it
# for line in commands.getstatusoutput('ls -l'):
# 	print(line)

import subprocess

for line in subprocess.call(["ls", "-l"]):
    print(line)