from __future__ import with_statement
import sys
sys.path.append('../src')
import control.context
from control.context import QuestionContext,DisplayContext,StepsContext
from control.commands import YesNoCommands
if __name__=='__main__':
    first=QuestionContext('Do you want a mm?',YesNoCommands())
    yes=DisplayContext(lambda:'Yes, you want.')
    no=DisplayContext(lambda:'No? I don\'t beleive!')
    control.context.join(first,control.context.ifElse(lambda:first.result=='yes',yes,no))
    control.context.join(no,first)
    sc=StepsContext(first)
    with sc:pass
