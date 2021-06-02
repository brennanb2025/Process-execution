import sys
import signal

from . import *


def sigINT_handler(sig, frame):
    print('\nShell Exiting...')
    sys.exit()


if __name__ == '__main__':
    del sys.argv[0]
    signal.signal(signal.SIGINT, sigINT_handler)

    endProgram = False
    while not endProgram:
        print('> ', end='', flush=True)
        cmdStr = sys.stdin.readline()
    
        if len(cmdStr) == 0:
            break

        try:
            processes = parseProcesses(cmdStr)
            """for proc in enumerate(processes):
                print('----------------')
                print('Process {}'.format(proc[0]))
                print('----------------')
                print(proc[1])"""

            executeProcesses(processes)
        except Exception as e:
            print('Error:', e)
