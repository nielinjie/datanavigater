import data
import logging
import copy
class ResuriceFKException(BaseException):pass
class LinkNode(object):
    def __init__(self,fromTable,fromColumn,toTable,toColumn,linkType="vfk"):
        self.fromTable=fromTable
        self.fromColumn=fromColumn
        self.toTable=toTable
        self.toColumn=toColumn
        assert linkType in ('vfk','fk')
        self.linkType=linkType
    def __str__(self):
        return '%s(%s)--%s-->(%s)%s' % (self.fromTable,self.fromColumn,self.linkType,self.toColumn,self.toTable)
    __repr__=__str__
    def __eq__(self,other):
        return self.__class__==other.__class__ and self.__str__() == other.__str__()
    def __ne__(self,other):
        return not self.__ge__(other)
class Link(object):    
    def append(self,fromTable,fromColumn,toTable,toColumn):
        if self.items!=[]:
            #pass
            assert self.items[-1].toTable==fromTable
        linkNode=LinkNode(fromTable,fromColumn,toTable,toColumn)
        if linkNode in self.items:
            raise ResuriceFKException('resurice refrence found, link=%s, refrence will not be added - %s'%(self,str(linkNode)))
        logging.debug('adding refrence - %s',linkNode )
        self.items.append(linkNode)
    def __init__(self):
        self.items=[]
        pass
    
    def clone(self):
        link=Link()
        link.items=copy.copy(self.items)
        return link
    @staticmethod
    def explore(datA,tableName,link=None):
        if link==None:
            link=Link()
            datA.links.append(link)
        fkindex=0
        for fk in datA.tables[tableName].foreign_keys:
            
            fkindex+=1            
            if fkindex>1:
                link=link.clone()
                datA.links.append(link)
                logging.debug('link cloned - %s when fromTable - %s',link,tableName)
            toTable,toColumn=fk.target_fullname.split('.')
            tl=link.clone()
            try:
                link.append(tableName, fk.parent.name, toTable,toColumn)
            except ResuriceFKException,e:
                link=tl
                logging.warning(e.message)
                continue
            else:
                Link.explore(datA,toTable,link)
                link=tl
        logging.debug('link is - %s',link)
    def __str__(self):
        return ','.join(map(str,self.items))
    __repr__=__str__
        