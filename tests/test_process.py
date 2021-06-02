import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import unittest
from shell import Process

class ProcessTester(unittest.TestCase):

    # Verify Correct Number of Processes Parsed
    def test_process_init_default(self):
        process = Process()
        self.assertEqual(process.command, '')
        self.assertAlmostEqual(len(process.arguments), 0)

    def test_process_command(self):
        process = Process('command')
        self.assertEqual(process.command, 'command')
        self.assertEqual(len(process.arguments), 0)

    def test_process_oneArg(self):
        process = Process('command', ['argument'])
        self.assertEqual(len(process.arguments), 1)
        self.assertEqual(process.arguments[0], 'argument')

    def test_process_twoArg(self):
        process = Process('command', ['argument', 'argument1'])
        self.assertEqual(len(process.arguments), 2)
        self.assertEqual(process.arguments[0], 'argument')
        self.assertEqual(process.arguments[1], 'argument1')

    def test_process_namedArg(self):
        process = Process(args=['argument', 'argument1'])
        self.assertEqual(process.command, '');
        self.assertEqual(len(process.arguments), 2)
        self.assertEqual(process.arguments[0], 'argument')
        self.assertEqual(process.arguments[1], 'argument1')

    def test_process_oneArgString(self):
        process = Process('command', 'arg')
        self.assertEqual(process.command, 'command', 'Command Incorrect')
        self.assertEqual(len(process.arguments), 1, 'Number of Arguments Incorrect')
        self.assertEqual(process.arguments[0], 'arg', 'String Not Handled')

    def test_process_stringCast(self):

        checkString = 'Command: command\nArguments:\n0: arg\n1: arg1\n'

        process = Process('command', ['arg', 'arg1'])
        self.assertEqual(str(process), checkString)

    def test_process_stringCast_noArgs(self):

        checkString = 'Command: command\nArguments:\n'

        process = Process('command', [])
        self.assertEqual(str(process), checkString)

if __name__ == '__main__':
    unittest.main()