import re
def isInt(string):
    return True if re.match(r'^[\d]+$',string) else False
def getListedItems(objsListFun,descripter,fixedItems=None):
    reList=[]
    if fixedItems!=None:
        reList.extend(fixedItems)
    reList.extend(map(descripter,objsListFun()))
    return '\n'.join(map(lambda (index,item): '%d - %s'% (index,item),enumerate(reList)))

