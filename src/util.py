import re
def isInt(string):
    return True if re.match(r'^[\d]+$',string) else False
def getListedItems(objsListFun,descripter,otherItems=[],otherBeforeObjs=True):
    print objsListFun()
    reList=[]
    if otherBeforeObjs:
        reList.extend(otherItems)
        reList.extend(map(descripter,objsListFun()))
    else:
        reList.extend(map(descripter,objsListFun()))
        reList.extend(otherItems)
    return '\n'.join(map(lambda (index,item): '%d - %s'% (index,item),enumerate(reList)))

