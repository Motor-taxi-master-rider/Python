# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json

from scrapy import log
from scrapy.http import Request
from twisted.enterprise import adbapi


class DoubanmoviePipeline(object):
    def __init__(self):
        '''self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db = 'python',
                user = 'root',
                passwd = 'root',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )'''
        self.file=open(r'G:\Learn\Python\doubanmovie\moviejson.json','wb')
    def process_item(self, item, spider):
        '''query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)'''
        line=json.dumps(dict(item))+'\n'
        self.file.write(line+' a ')
        return item

    def _conditional_insert(self,tx,item):
        tx.execute("select * from doubanmoive where m_name= %s",(item['name'][0],))
        result=tx.fetchone()
        log.msg(result,level=log.DEBUG)
        print(result)
        if result:
            log.msg("Item already stored in db:%s" % item,level=log.DEBUG)
        else:
            classification=actor=''
            lenClassification=len(item['classification'])
            lenActor=len(item['actor'])
            for n in xrange(lenClassification):
                classification+=item['classification'][n]
                if n<lenClassification-1:
                    classification+='/'
            for n in xrange(lenActor):
                actor+=item['actor'][n]
                if n<lenActor-1:
                    actor+='/'

            tx.execute(\
                "insert into doubanmoive (m_name,m_year,m_score,m_director,m_classification,m_actor) values (%s,%s,%s,%s,%s,%s)",\
                (item['name'][0],item['year'][0],item['score'][0],item['director'][0],classification,actor))
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)
