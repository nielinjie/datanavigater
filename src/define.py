from control.context import StepsContext
class DefineContext(StepsContext):
    def __init__(self,parent):
                super(DefineContext,self).__init__(ifInConnectionContext,promoter='--Defining an entity--')
def getDefineContext(parentContext):





    chooseConnectionContext=QuestionContext('Please chose a connection, or create one.\n',lambda:util.getListedItems(lambda:parentContext.connections,lambda conn:conn.description,['Create one']))
            ChoseCommands(range(0,len(connections)),multiple=False))
    createConnectionContext=None#TODO
    nameEntityContext=QuestionContext('Input a name for your Entity.',TextInputCommands())
    choseEnteranceContext=QuestionContext('Input a table\'s name as start poin.',TextInputCommands())
    noSuchTableContext=DisplayContext(lambda:'No such table, please input a existed table\'s name.')
    choseLinkContext=QuestionContext('Please chose a reference to add to creating entity',ChoseCommands)

        nameEntityContext.getNextStepContext=lambda choseLinkContext
    chooseConnectContext.getNextStepContext=lambda :createConnectionContext if chooseConnectContext.result=[len(connections)] else nameEntityContext


