    程序入口为main.py，crawl.exe并不是main.py的可执行文件，而是打包好爬虫功能的exe文件，若想单独运行爬虫即可只打开该crawl.exe

    scrapy.cfg是scrapy的配置文件，请不要修改或移动
    scrapy.db是SQLite数据库
    bokeyuan下所属文件夹是爬虫的具体配置文件，由于scrapy即使打包也不能单独存在，因此请保留该文件夹不要移动，如果想增加或修改功能请按照官方文档修改，以免造成不必要的错误。

    数据库内已提前爬取好了3999条内容，可直接处理（如果想节约时间），因此建议使用数据分析与导出功能后，再自行使用爬虫功能获取最新的博客信息

    git页面：https://github.com/LunarMar3/Bokeyuan_crawl.git