from __future__ import with_statement
import logging
logging.basicConfig(level=logging.INFO,format='%(levelname)s\t%(message)s')
if __name__=='__main__':
    import sys
    import pprint
    sys.path.append('../src')
    from control.context import StepsContext,QuestionContext
    from control.commands import YesNoCommands,ComboCommands
    first=QuestionContext('I am the first Question, please answer yes/no',YesNoCommands(),'-first-')
    second=QuestionContext('I am the second Question, please chose in [1,2,3] or input your text',ComboCommands([1,2,3],True,None),'-second-')
    first.getNextStepContext=lambda :second
    second.getNextStepContext=lambda :None
    sc=StepsContext(first,'>>testing steps>>')
    first._parent=sc
    second._parent=sc
    with sc:pass
    logging.info(first.result)
    logging.info(second.result)
    
