import control.context
import functools
from control.context import StepsContext,ChoseQuestionContext,QuestionContext,DisplayContext
from control.commands import TextInputCommands
from data.link import LinkNode
currentTable=None
def getDefineContext(parentContext):
#create steps
    #chooseConnectionContext=QuestionContext('Please chose a connection, or create one.\n',lambda:util.getListedItems(lambda:data.connections,lambda conn:conn.description,['Create one']))
#            ChoseCommands(range(0,len(connections)),multiple=False))
    chooseConnectionContext=ChoseQuestionContext('Please chose a connection',lambda:data.connections,lambda obj:obj,['Create one'])
    #TODO nest this to chooseConnectionContext
    #createConnectionContext=None
    nameEntityContext=QuestionContext('Input a name for your Entity.',TextInputCommands())
    choseEnteranceContext=QuestionContext('Input a table\'s name as start poin.',TextInputCommands())
    #TODO nest this to choseEnteranceContext
    #noSuchTableContext=DisplayContext(lambda:'No such table, please input a existed table\'s name.')
    choseLinkContext=ChoseQuestionContext('Please chose a reference to add to creating entity',lambda:data.listLinks(choseEnteranceContext.result if currentTable==None else currentTable),str,['Stop','Search in database'])
    def setCurrentTable(link):
        global currentTable
        currentTable=link.toTable
    choseLinkContext._resultConsumer=lambda result:(setCurrentTable(result[0]) if result[0].__class__==LinkNode else None)
    #choseLinkContext._resultConsumer=lambda result:printTrue(result)
    #searchPathContext=_getSearchPathContext()
    successContext =DisplayContext(lambda:'Entity defining successed. Entityname = %s'% nameEntityContext.result)
#connect contexts togethor
    control.context.join(chooseConnectionContext,nameEntityContext)
    control.context.join(nameEntityContext,choseEnteranceContext)
    control.context.join(choseEnteranceContext,choseLinkContext)
    control.context.join(choseLinkContext,control.context.ifElse(lambda: choseLinkContext.result[0]=='Stop',successContext,choseLinkContext))
#create define context
    defineContext=StepsContext(chooseConnectionContext,promoter='--Defining an entity--',parent=parentContext)
    return defineContext

def printTrue(s):
    print str(s)
    return True
def _getSearchPathContext(parentContext=None):#TODO
    choseTargetTableNameContext=QuestionContext()
    reContext=StepsContext()

