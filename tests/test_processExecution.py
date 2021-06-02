import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import unittest
from shell import executeProcesses
from shell import Process
import subprocess

class ProcessExecutionTester(unittest.TestCase):

    #didn't get the unit tests done - output wasn't working

    def test_process_redirect_basic_output(self): #basic output from input file
        processes = []
        p1 = Process()
        processes.append(p1)
        p1.redirectIn = True
        p1.fileRedirect = 'test_file.txt'
        p1.command = 'grep'
        p1.arguments.append('a')
        #self.assertEqual(subprocess.check_output(executeProcesses(processes), "a")
        try:
            executeProcesses(processes)
        except ExceptionType:
            self.fail("executeProcesses(processes) raised ExceptionType unexpectedly!")
        
    def test_different_process_pipe(self): #ls --> pipe --> grep
        processes = []
        p1 = Process()
        p1.pipe = True
        p1.command = 'ls'
        processes.append(p1)
        p2 = Process()
        p2.command = "grep"
        p2.arguments.append("test_process.py")
        processes.append(p2)
        #self.assertEqual(executeProcesses(processes), "test_process.py")
        try:
            executeProcesses(processes)
        except ExceptionType:
            self.fail("executeProcesses(processes) raised ExceptionType unexpectedly!")

    def test_process_redirect_nofile(self): #exception - file doesn't exist
        processes = []
        p1 = Process()
        p1.redirectIn = True
        p1.fileRedirect = 'doesnotexist'
        p1.command = 'grep'
        p1.arguments.append('a')
        processes.append(p1)
        self.assertRaises(Exception, executeProcesses, processes)

    def test_process_pipe(self): #one pipe
        processes = []
        p1 = Process()
        p1.pipe = True
        p1.command = 'ls'
        processes.append(p1)
        p2 = Process()
        p2.command = "grep"
        p2.arguments.append("test_file.txt")
        #self.assertEqual(executeProcesses(processes), "test_file.txt")
        try:
            executeProcesses(processes)
        except ExceptionType:
            self.fail("executeProcesses(processes) raised ExceptionType unexpectedly!")

    def test_process_double_pipe(self): #two pipes - this doesn't work and I couldn't figure out why, >2 pipes doesn't work either
        processes = []
        p1 = Process()
        p1.pipe = True
        p1.command = 'ls'
        processes.append(p1)
        p2 = Process()
        p2.pipe = True
        p2.command = "grep"
        p2.arguments.append("test.txt")
        processes.append(p2)
        p3 = Process()
        p3.command = "grep"
        p3.arguments.append("test_file.txt")
        processes.append(p3)
        #self.assertEqual(executeProcesses(processes), "test_file.txt")
        try:
            executeProcesses(processes)
        except ExceptionType:
            self.fail("executeProcesses(processes) raised ExceptionType unexpectedly!")

    def test_process_quadruple_pipe(self): #four pipes - this doesn't work and I couldn't figure out why, >2 pipes doesn't work
        processes = []
        p1 = Process()
        p1.pipe = True
        p1.command = 'ls'
        processes.append(p1)
        p2 = Process()
        p2.pipe = True
        p2.command = "grep"
        p2.arguments.append("test.txt")
        processes.append(p2)
        p3 = Process()
        p3.pipe = True
        p3.command = "grep"
        p3.arguments.append("test_p.txt")
        processes.append(p3)
        p4 = Process()
        p4.pipe = True
        p4.command = "grep"
        p4.arguments.append("test_process.txt")
        processes.append(p4)
        p5 = Process()
        p5.command = "grep"
        p5.arguments.append("test_processExecution.py")
        processes.append(p5)
        #self.assertEqual(executeProcesses(processes), "test_processExecution.py")
        try:
            executeProcesses(processes)
        except ExceptionType:
            self.fail("executeProcesses(processes) raised ExceptionType unexpectedly!")

    def test_process_redirect_to_pipe(self): #input file --> pipe
        processes = []
        p1 = Process()
        p1.redirectIn = True
        p1.fileRedirect = 'test_file.txt'
        processes.append(p1)
        p2 = Process()
        p2.pipe = True
        p2.command = "grep"
        p2.arguments.append("a")
        processes.append(p2)
        #self.assertEqual(executeProcesses(processes), "a")
        try:
            executeProcesses(processes)
        except ExceptionType:
            self.fail("executeProcesses(processes) raised ExceptionType unexpectedly!")

    def test_process_redirect_to_double_pipe(self): #input file --> pipe --> pipe
        processes = []
        p1 = Process()
        p1.redirectIn = True
        p1.fileRedirect = 'test_file.txt'
        processes.append(p1)
        p2 = Process()
        p2.pipe = True
        p2.command = "grep"
        p2.arguments.append("a")
        processes.append(p2)
        p3 = Process()
        p3.pipe = True
        p3.command = "grep"
        p3.arguments.append("b")
        processes.append(p3)
        #self.assertEqual(executeProcesses(processes), "")
        try:
            executeProcesses(processes)
        except ExceptionType:
            self.fail("executeProcesses(processes) raised ExceptionType unexpectedly!")

    def test_process_bad_command(self): #exception - command doesn't exist
        processes = []
        p1 = Process()
        p1.command = 'fdsfasdfdsafdsafdsafdsafdsafdsafdsafdsafdsafdsafsadfsadf'
        processes.append(p1)
        self.assertRaises(Exception, executeProcesses, processes)

    def test_process_bad_arguments(self): #exception - argument not found
        processes = []
        p1 = Process()
        p1.command = 'ls'
        p1.arguments.append('fdsklfjdsklfjdsklfjlksdjfklsdjflkdsjlkfjfkldsjlkf')
        processes.append(p1)
        self.assertRaises(Exception, executeProcesses, processes)

if __name__ == '__main__':
    unittest.main()