import sys
import os
from .process import Process

def parseProcesses(cmdStr):

    # We depend upon the command string ending with a newline.
    # So, verify that it exists.
    if cmdStr[-1] != '\n':
        cmdStr += '\n'

    processes = []
    currProcess = Process()
    endProcess = False

    pipes = []
    fileProc = (-1, "")

    startCopy = 0
    index = 0
    inSingleQuotes = -1
    inDoubleQuotes = -1
    i = 0
    for letter in cmdStr:
        
        if letter == '\"' and inSingleQuotes < 0:
            inDoubleQuotes *= -2

        if letter == '\'' and inDoubleQuotes < 0:
            inSingleQuotes *= -2
        
        if inSingleQuotes < 0 and inDoubleQuotes < 0:
            if letter == '|' or letter == '<' or letter == '>':
                endProcess = True
                if letter == '|':
                    pipes.append(i) #pipe from process i to process i+1

                elif letter == '<':
                    processes.append(currProcess)
                    currProcess = Process()
                    if fileProc[0] != -1: #can only be one > or < in a line
                        raise Exception('Too many file redirects')
                    fileProc = (i+1, "in")
                    #relative path name
                    #set currProcess in to file --> read it now. It will be the last thing

                elif letter == '>':
                    processes.append(currProcess)
                    currProcess = Process()
                    if fileProc[0] != -1: #can only be one > or < in a line
                        raise Exception('Too many file redirects')
                    fileProc = (i+1, "out")
                    #relative path name
                    #set currProcess out to file --> read it now. It will be the last thing
                
            
            if endProcess or letter == ' ' or letter == '\n':
                argStr = cmdStr[startCopy:index].strip()
                startCopy = index+1
                
                if inSingleQuotes < -1 or inDoubleQuotes < -1:  
                    argStr = argStr[1:len(argStr)-1]
                    inSingleQuotes = inDoubleQuotes = -1

                if len(argStr) > 0:
                    if currProcess.command == '':
                        currProcess.command = argStr
                    else:
                        currProcess.arguments.append(argStr)

            if endProcess:
                if len(currProcess.command) > 0:
                    processes.append(currProcess)
                    i+=1
                    currProcess = Process()
                endProcess = False

        index += 1

    if not endProcess and len(currProcess.command) > 0:
        if inDoubleQuotes < 0 and inSingleQuotes < 0:
            processes.append(currProcess)
            i+=1
        else:
            raise Exception('Mismatched Quotes')


    #establish relationships between processes

    # pipe to other process or redirect file
    # currProcess out --> points to next process in. 
    for i in range(len(processes)):
        if i != fileProc[0]:
            processes[i].pipe = True
    if fileProc[0] != -1:
        if fileProc[0] >= len(processes):
            raise Exception('No file input')
        if fileProc[0] == 1:
            raise Exception('Input a process along with the file')
        if fileProc[1] == "out": #send file to the last process' out
            processes[len(processes)-2].fileRedirect = processes[fileProc[0]].command
            processes[len(processes)-2].redirectOut = True
        else: #send file to the first process in
            processes[0].fileRedirect = processes[fileProc[0]].command
            processes[0].redirectIn = True
        
        del processes[fileProc[0]] #remove the file - not a real process

    
    return processes

def executeProcesses(processes):
    fds = []
    #create all pipes --> [(3,4), (5,6), etc]
    for i in range(len(processes)):
        r, w = os.pipe()
        temp = []
        temp.append(r) #need it to be array, tuples are immutable
        temp.append(w)
        fds.append(temp)

    for i in range(len(processes)):
        np = os.fork()

        if np == 0: #child process

            if processes[i].redirectIn: #get input from a file
                try:
                    f = open(processes[i].fileRedirect, 'r') 
                    fds[i][0] = f.fileno() #set read to file descriptor of input file
                    os.dup2(fds[i][0], sys.stdin.fileno()) #set input to ^
                except FileNotFoundError as e:
                    print(e)
                    os._exit(2)
            elif processes[i].redirectOut: #print to output file 
                f = open(processes[i].fileRedirect, 'w') 
                fds[i][1] = f.fileno() #set write to file descriptor of input file
                os.dup2(fds[i][1], sys.stdout.fileno()) #set output to ^

            if i != 0: #not first process
                os.dup2(fds[i-1][0], sys.stdin.fileno()) #get input from previous process
            
            elif i != len(processes)-1: #not last process
                os.dup2(fds[i][1], sys.stdout.fileno()) #output to next process

            for p in range(len(fds)): #close all pipes before executing process
                os.close(fds[p][0])
                os.close(fds[p][1])
            
            #execute the process
            args = processes[i].arguments
            args.insert(0, processes[i].command)
            try:
                os.execvp(args[0], args)
            except OSError as error:
                print(error)
                os._exit(2)
        
    #parent close all pipes
    for p in range(len(fds)):
        os.close(fds[p][0])
        os.close(fds[p][1])
    
    for p in range(len(fds)):
        os.wait()
    
            
