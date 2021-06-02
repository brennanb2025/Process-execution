Semester 2 lab 1\n
Description: Execute the processes that were parsed in the previous lab.\n
Use pipes to redirect the output of one process into theinput of the next with the last process’s output being the terminal (or a file)\n
The following symbols indicate special behaviour:\n
–proc1 | proc2 – send the output of proc1 into the input of proc2\n
–proc1 < file – redirect the contents of a file to the input of proc1\n
–proc1 > file – direct the output of proc1 to (and overwrite) file\n
Note: there can be only one < or > in a line, but there can be an unlimited number of |.\n
How to run: navigate to brennanb_processExecution folder and type python3 -m shell (linux).\n
Run tests individually: navigate to tests folder and type python3 -m {the test file you want to run} (linux).
