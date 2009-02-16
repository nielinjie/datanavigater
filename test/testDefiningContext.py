from __future__ import with_statement
if __name__=='__main__':
    import sys
    import pprint
    sys.path.append('../src')
    import logging
    logging.basicConfig(level=logging.INFO,format='%(levelname)s\t%(message)s')
    import data 
    from data.link import Link
    #engine=data.DataDescripter.getDescripter('postgres')(**{'host':'localhost','port':5432,
    #                                                        'userName':'postgres',
    #                                                        'passwd':'790127','dbname':'hipergate4'}).getEngine()
    engine=data.DataDescripter.getDescripter('sqlite')(**{'path':'testdata.text'}).getEngine()
    #print engine
    import sqlalchemy
    meta=sqlalchemy.MetaData()
    meta.bind=engine
    meta.reflect()
    from data import Data
    da=Data()
    from data.link import LinkNode
    for (name,table) in meta.tables.items():
#        print 'table - %s'% table.name
#        print 'pk - %s' % table.primary_key.columns
#        for fk in table.foreign_keys:
#            print 'fk - %s'% fk.target_fullname
#        for column in table.c:
#            print 'column - %s' % column.name
#        
        da.tables[name.encode('ascii')]=table
        for fk in table.foreign_keys:
            da.links.setdefault(fk.column.table.name.encode('ascii'),[]).append(LinkNode(fk.column.table.name,fk.column.name,table.name,fk.parent.name))
            da.links.setdefault(table.name.encode('ascii'),[]).append(LinkNode(table.name,fk.parent.name,fk.column.table.name,fk.column.name,'fk'))
    logging.info('da.links - %s',pprint.pformat(da.links))
    logging.info('da.tables.keys() - %s',pprint.pformat(da.tables.keys()))

    import define
    define.data=da
    con=define.getDefineContext(None)
    with con :pass
