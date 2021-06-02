class Process:

    def __init__(self, command = '', args = None, pipe = None, redirectIn = None, redirectOut = None, fileRedirect = None):    
        self.command = command
        self.pipe = pipe
        self.fileRedirect = fileRedirect
        self.redirectIn = redirectIn
        self.redirectOut = redirectOut
        
        if args is None:
            args = []
        elif isinstance(args, str):
            args = [args]
            
        self.arguments = args

    def __str__(self):
        rtn = "Command: {}\n".format(self.command)
        rtn += "Arguments:\n"
        for arg in enumerate(self.arguments):
            rtn += "{}: {}\n".format(arg[0], arg[1])
        return rtn