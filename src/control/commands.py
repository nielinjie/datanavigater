from control.context import ExitRequest
class CommandException(Exception):
    pass
class Commands(object):
    def _input(self,str):
        parts=str.split()
        self._dispatch(parts[0],*parts[1:])
    def react(self,promoter):
        inputStr=raw_input(promoter)
        self._input(inputStr)
class BasicCommands(Commands):
    _commands={}
    def _dispatch(self,commandName,*args):
        if commandName in self._commands.keys():
            self._commands[commandName](self,*args)
        else:
            raise CommandException('Command not found :-(')
        
import functools
class MethodesCommands(BasicCommands):
    @staticmethod
    def __command(func,commandName):
        MethodesCommands._commands.update([(commandName,func)])
    @staticmethod
    def _command(func,alias):
        for arg in alias:
            MethodesCommands.__command(func,arg)
        MethodesCommands.__command(func,func.__name__)
        return func
    @staticmethod
    def command(alias=None):
        if alias==None:
            return functools.partial(MethodesCommands._command, alias=[])
        return functools.partial(MethodesCommands._command,alias=alias)
class YesNoCommands(MethodesCommands):
    @MethodesCommands.command(['yes','y','YES','Yes'])
    def yes(self):
        self._context.result='yes'
        raise ExitRequest('Refresh exited')
    @MethodesCommands.command(['no','n','NO','No'])
    def no(self):
        self._context.result='no'
        raise ExitRequest('Refresh exited.')
class ChoseCommands(BasicCommands):
    def __init__(self,options,multiple=False):
        self.options=options
        self.multiple=multiple
    def _dispatch(self,commandName,*args):
        rs=[]
        commands=commandName.split(',')
        for command in commands:
            parts=command.split('-')
            if len(parts)==1:
                rs.append(int(parts[0]))
            if len(parts)==2:
                rs.extend(range(int(parts[0]),int(parts[1])+1))
        self._context.result=rs
        raise ExitRequest('')
    #_commands={'y':yes,'n':no,'yes':yes,'no':no}