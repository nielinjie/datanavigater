import util
import logging
from control.context import ExitRequest
class CommandRuntimeException(Exception):
    pass
class CommandValidateException(Exception):
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
            raise CommandValidateException('Command not found :-(')
        
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
        raise ExitRequest('exited')
    @MethodesCommands.command(['no','n','NO','No'])
    def no(self):
        self._context.result='no'
        raise ExitRequest('exited.')
class ChoseCommands(BasicCommands):
    format='1,3-7'
    def __init__(self,optionsCreateFun,multiple=False):
        self._optionsCreateFun=optionsCreateFun
        self._multiple=multiple
    def _dispatch(self,commandName,*args):
        rs=[]
        commands=commandName.split(',')
        for command in commands:
            parts=command.split('-')
            if len(parts)==1:
                if not util.isInt(parts[0]):
                    raise CommandValidateException('Input wrong format, input like this - %s' % self.format)
                rs.append(int(parts[0]))
            if len(parts)==2:
                if not util.isInt(parts[1]):
                    raise CommandValidateException('Input wrong format, input like this - %s' % self.format)
                rs.extend(range(int(parts[0]),int(parts[1])+1))
        if len(rs)>1 and not self._multiple:
            raise CommandValidateException('Only one chose allowed.')
        options=self._optionsCreateFun()
        for c in rs:
            if not c in range(0,len(options)):
                raise CommandValidateException("'%s' is not in options." % c)
        result=[]
        for r in rs:
            result.append(options[r])
        self._context.result=result
        raise ExitRequest('')
class TextInputCommands(BasicCommands):
    def __init__(self,validatingRe=None):
        self._validatingRe=validatingRe
    def _dispatch(self,commandName,*arg):
        text=commandName+('' if len(arg)==0 else (' '+' '.join(arg)))
        if self._validatingRe!=None:
            if not re.match(self._validaterFun,text):
                raise CommandValidateException("Validate failed, please input %s" % self._validatingRe)
        self._context.result=text
        raise ExitRequest('')
class ChainCommands(BasicCommands):
    def __init__(self,commandzs):
        self._commandzs=commandzs
    def setContext(self,context):
        for commands in self._commandzs:
            commands._context=context
    def getContext(self):
        return self._context
    _context=property(getContext,setContext)
    def _dispatch(self,commandName,*arg):
        self._handled=False
        for commands in self._commandzs:
            try:
                commands._dispatch(commandName,*arg)
                logging.debug('no exception')
                self._handled=True
            except Exception,e:
                logging.debug(e)
                logging.debug(e.__class__)
                if isinstance(e,ExitRequest):
                    self._handled=True
                    raise e
                elif isinstance(e,CommandValidateException):
                    continue
                else:
                    self._handled=True
                    raise CommandRuntimeException(e)
                    break
        if not self._handled:
            raise CommandValidateException("Input is not handleable - '%s'" % (commandName+' '+' '.join(arg)))
class ComboCommands(ChainCommands):
    def __init__(self,options,multiple=False,validatingRe=None):
        super(ComboCommands,self).__init__([ChoseCommands(options,multiple),TextInputCommands(validatingRe)])
