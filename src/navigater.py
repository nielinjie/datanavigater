from __future__ import with_statement
from control.commands import BasicCommands,YesNoCommands,MethodesCommands,ChoseCommands
command=MethodesCommands.command
from control.context import QuestionContext,ExitRequest

class DefineContext(Context):
    def __init__(self,parent=None):
        super(DefineContext,self).__init__(DefineCommands(),parent)
class RootCommands(MethodesCommands):
    @command()
    def exit(self):
        raise ExitRequest('Exit Navigate...')
    @command()
    def define(self):
        with DefineContext():pass
    @command()    
    def go(self,*arg):
        if arg==None or arg==():
            with QuestionContext('Please chose one or more',ChoseCommands([1,2,3]),self._context) as context :
                print 'You want go: %s' % context.result
        else:
            print 'You want to go: %s' % arg[0]
    @command()
    def refresh(self):
        class RefreshCommands(YesNoCommands):pass
        with QuestionContext('Are you sure?',RefreshCommands(),self._context):pass
    @command()
    def echo(self,str):
        print str
