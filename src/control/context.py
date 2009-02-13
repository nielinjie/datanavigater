from __future__ import with_statement
import logging

class ExitRequest(Exception):
    pass
from control.commands import CommandValidateException,CommandRuntimeException
defaultPromoter='>>'
class Context(object):
    def _getPromoter(self):
        logging.debug('entered _setPromoter')
        if self._promoter==None:
            if self._parent!=None:
                if self._parent._promoter!=None:
                    self._promoter='%s%s'% (self._parent._promoter,defaultPromoter)
            else:
                self._promoter=defaultPromoter
        return self._promoter
    def __init__(self,promoter=None, parent=None):
        self._parent=parent
        self._promoter=promoter
    def __exit__(self,exc_type, exc_val, exc_tb):
        pass
    def __enter__(self):
        raise NotImplementedError()
class CommandContext(Context):
    def __init__(self,commands,promoter=None,parent=None):
        super(CommandContext,self).__init__(promoter,parent)
        self._commands=commands
        self._commands._context=self
        
    def __enter__(self):
        self._run()
        return self
    
    def _run(self):
        commands=self._commands
        self._commands._context=self
        while True:
            try:
                commands.react(self._getPromoter())
            except ExitRequest,er:
                logging.debug( er.message)
                break
            except CommandValidateException, cve:
                print 'Command validate exception -- %s' % cve
            except CommandRuntimeException, cre:
                print 'Command runtime exception -- %s' % cre
class StepsContext(Context):
    def __init__(self,firstStepContext,promoter=None,parent=None):
        super(StepsContext,self).__init__(promoter,parent)
        self._firstStepContext=firstStepContext
    def __enter__(self):
        currentStep=self._firstStepContext
        while currentStep!=None:
            logging.debug(currentStep)
            with currentStep:pass
            logging.debug('out from step context')
            currentStep=currentStep.getNextStepContext()
            
class QuestionContext(CommandContext):
    def __init__(self,question,commands,promoter=None,parent=None):
        super(QuestionContext,self).__init__(commands,promoter,parent)
        self.question=question
    def __enter__(self):
        print self._getPromoter()+self.question+'...'
        return super(QuestionContext,self).__enter__()
