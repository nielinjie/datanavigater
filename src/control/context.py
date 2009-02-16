from __future__ import with_statement
import logging
import types
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
        assert promoter==None or type(promoter) in types.StringTypes
        assert parent==None or isinstance(parent,Context)
        self._parent=parent
        self._promoter=promoter
        self._resultConsumer=None
        self._result=None
    def __exit__(self,exc_type, exc_val, exc_tb):
        pass
    def __enter__(self):
        raise NotImplementedError()
    def getNextStepContext(self):
        return None
    def _setResult(self,result):
        self._result=result
        if self._resultConsumer!=None:
            self._resultConsumer(self._result)
    def _getResult(self):
        return self._result
    result=property(fget=_getResult,fset=_setResult)
class InternalContext(Context):
    def __enter__(self):
        return self._run()
    def _run(self):
        return self
class DisplayContext(InternalContext):
    def __init__(self,textFun,promoter=None,parent=None):
        super(DisplayContext,self).__init__(promoter=promoter,parent=parent)
        self.textFun=textFun
    def _run(self):
        print self._getPromoter()+self.textFun()
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
def join(fromContext, toContext):
    fromContext.getNextStepContext=lambda : toContext
def ifElse(conditionFun,trueNextContext,falseNextContext):
    assert trueNextContext._parent==falseNextContext._parent
    internal=InternalContext(parent=trueNextContext._parent)
    internal.__enter__=lambda : trueNextContext.__enter__() if conditionFun() else falseNextContext.__enter__()
    internal.getNextStepContext=lambda: trueNextContext.getNextStepContext() if conditionFun() else falseNextContext.getNextStepContext()
    return internal

            
class QuestionContext(CommandContext):
    def __init__(self,question,commands,dynQuesionCreaterFun=None,promoter=None,parent=None):
        assert dynQuesionCreaterFun==None or type(dynQuesionCreaterFun)==types.FunctionType
        super(QuestionContext,self).__init__(commands,promoter,parent)
        self.question=question
        self._dynQuesionCreaterFun=dynQuesionCreaterFun
    def __enter__(self):
        print self._getPromoter()+self.question+(self._dynQuesionCreaterFun() if self._dynQuesionCreaterFun!=None else '')
        return super(QuestionContext,self).__enter__()
from control.commands import ChoseCommands
import util
class ChoseQuestionContext(QuestionContext):
    def __init__(self,question,optionsCreaterFun,optionsDescriptorFun,fixedItems,promoter=None,parent=None):
        super(ChoseQuestionContext,self).__init__(question+'\n',ChoseCommands(lambda:fixedItems+optionsCreaterFun()),lambda:util.getListedItems(optionsCreaterFun,optionsDescriptorFun,fixedItems),promoter,parent)
