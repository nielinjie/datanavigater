class ExitRequest(Exception):
    pass
from control.commands import CommandException
class Context(object):
    def _setPromoter(self):
        if self._promoter==None:
            if self._parent!=None:
                if self._parent._promoter!=None:
                    self._promoter='%s>>'% self._parent._promoter
            else:
                self._promoter='>>'
    def __init__(self,commands,parent=None):
        self._parent=parent
        self._commands=commands
        self._commands._context=self
        self._promoter=None
        self._setPromoter()
    def __enter__(self):
        self._run()
        return self
    def __exit__(self,exc_type, exc_val, exc_tb):
        pass
    def _run(self):
        commands=self._commands
        self._commands._context=self
        while True:
            try:
                commands.react(self._promoter)
            except ExitRequest,er:
                print er.message
                break
            except CommandException, bc:
                print 'Command exception -- %s' % bc
            #except BaseException,e :    
             #   print 'Non-handlable exception -- %s'% e 
        
    
class QuestionContext(Context):
    def __init__(self,question,commands,parent=None):
        super(QuestionContext,self).__init__(commands,parent)
        self.question=question
    def __enter__(self):
        print self._promoter+self.question+'...'
        return super(QuestionContext,self).__enter__()
