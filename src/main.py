from __future__ import with_statement
import sys
from control.context import Context
from browser import RootCommands
if __name__=='__main__':
    with Context(RootCommands()) as rc:
        pass
    
    
