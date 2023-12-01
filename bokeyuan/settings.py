BOT_NAME = "bokeyuan"
SQLITE_DB_NAME = 'scrapy.db'
SPIDER_MODULES = ["bokeyuan.spiders"]
NEWSPIDER_MODULE = "bokeyuan.spiders"
ITEM_PIPELINES={
    'bokeyuan.pipelines.sqliteNewsPipeline':400,
}
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
ROBOTSTXT_OBEY = True
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
FEED_EXPORT_ENCODING = "utf-8"
