
from itemadapter import ItemAdapter

import sqlite3
class sqliteNewsPipeline(object):
    def __init__(self):
        db_name = 'scrapy.db'
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        insert_sql="""
            DROP TABLE news
        """
        self.cursor.execute(insert_sql)
        insert_sql="""
            CREATE TABLE "news" (
	            "Id"	INTEGER NOT NULL UNIQUE,
	            "title"	TEXT NOT NULL,
	            "title_url"	TEXT NOT NULL,
	            "author"	TEXT NOT NULL,
	            "pubtime"	TEXT NOT NULL,
	            "support"	INTEGER NOT NULL,
	            "comments"	INTEGER NOT NULL,
	            "view"	INTEGER NOT NULL,
	            PRIMARY KEY("Id" AUTOINCREMENT)
            );
        """
        self.cursor.execute(insert_sql)
        self.conn.commit()
    def process_item(self,item,spider):
        insert_sql="""
            INSERT INTO news(title,title_url,author,pubtime,support,comments,view)
                VALUES(?,?,?,?,?,?,?)
        """
        params=[
            item.get("title","")[0],
            item.get("title_url","")[0],
            item.get("author","")[0],
            item.get("pubtime","")[0],
            item.get("support","0")[0],
            item.get("comments","0")[0],
            item.get("view","0")[0],
        ]
        self.cursor.execute(insert_sql,tuple(params))
        self.conn.commit()
        return item
class BokeyuanPipeline:
    def process_item(self, item,spider):
        return item
