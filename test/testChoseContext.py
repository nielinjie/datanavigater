from __future__ import with_statement
import sys
sys.path.append('../src')
import control.context
from control.context import QuestionContext,InternalContext,StepsContext,ChoseQuestionContext
from control.commands import ChoseCommands
import util
total=10
if __name__=='__main__':
    def setTotal(value):
        global total
        print 'setting total - %d' % value
        total=value
        print total
    #chose=QuestionContext('Chose a item\n',ChoseCommands(lambda:range(0,total)),lambda:util.getListedItems(lambda:range(0,total),lambda obj:'Item No. %d'%obj))
    chose=ChoseQuestionContext('Chose a item',lambda:map(lambda i:'Item No. %d'%i,range(0,total)))
    setTotalc=InternalContext()
    setTotalc._run=lambda:setTotal(chose.result[0]) or setTotalc
    control.context.join(chose,setTotalc)
    control.context.join(setTotalc,chose)
    sc=StepsContext(chose)
    with sc:pass
