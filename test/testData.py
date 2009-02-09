if __name__=='__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG,format='%(levelname)s\t%(asctime)s\t%(message)s')
    import data 
    from data.link import Link
    engine=data.DataDescripter.getDescripter('postgres')(**{'host':'localhost','port':5432,
                                                            'userName':'postgres',
                                                            'passwd':'790127','dbname':'hipergate4'}).getEngine()
    print engine
    import sqlalchemy
    meta=sqlalchemy.MetaData()
    meta.bind=engine
    meta.reflect()
    from data import Data
    da=Data()
    for (name,table) in meta.tables.items():
#        print 'table - %s'% table.name
#        print 'pk - %s' % table.primary_key.columns
#        for fk in table.foreign_keys:
#            print 'fk - %s'% fk.target_fullname
#        for column in table.c:
#            print 'column - %s' % column.name
#        
        da.tables[name]=table
    Link.explore(da,'k_users')
    for link in da.links:
        print link
        print id(link)
    