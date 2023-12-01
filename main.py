import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def print_menu():
    print("----------------------------欢迎来到博客园自动爬虫及数据分析程序------------------------------")
    print("-     本程序依靠scrapy框架、sqlite3实现，能够对博客园的前200页上传博客内容进行爬取与保存     -")
    print("-                        本程序功能如下，请输入对应数字执行对应功能                          -")
    print("-                                   1.爬取博客园网站                                         -")
    print("-                              2.导出数据库数据为csv文件                                     -")
    print("-                                    3.快速数据分析                                          -")
    print("----------------------------------------------------------------------------------------------")

def crawl_blog():
    print("正在执行爬取博客园网站的操作...")
    
    import subprocess
    exe_path = "crawl.exe"
    print("爬虫执行与爬取需要等待一段时间，请耐心等待")
    print("为避免网站并发限制与ip封锁，已采取随机延时处理，爬取200页数据预计20分钟，您可以选择更少的页数来体验功能")
    process = subprocess.Popen(exe_path, shell=True)
    process.wait()
    print("已爬取完成")


def export_to_csv():
    print("正在执行导出数据为csv文件的操作...")
    query = "SELECT Id, title, title_url, pubtime,support,comments,view from news"
    conn = sqlite3.connect('scrapy.db')
    c = conn.cursor()
    result = pd.read_sql_query(query, conn)
    result.to_csv('output.csv',sep=';', index=False,encoding='utf_8_sig')

    print("数据已成功导出到 output.csv 文件。")
    conn.close()
    # Add your code for exporting to CSV here

def quick_data_analysis():
    
    print("请输入你想要绘制的数据图：")
    print("1.浏览数，评论数，支持数的热力图")
    print("2.浏览数，评论数，支持数的折线图")
    print("3.博客最热关键词的词云图")
    print("4.浏览数，评论数，支持数的增长趋势图")
    print("5.浏览数为大小，支持数为x，评论数为y的气泡图")
    print("6.浏览数的散点图")
    print("7.支持数的散点图")
    print("8.评论数的散点图")
    choice = input()


    if choice == '1':
        conn = sqlite3.connect('scrapy.db')
        c = conn.cursor()
        query = "SELECT support,comments,view from news"
        result = pd.read_sql_query(query, conn)
        correlation_matrix = result[['view', 'support', 'comments']].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.savefig('heat.png', bbox_inches='tight')
        plt.show()
        conn.close()


    elif choice == '2':
        conn = sqlite3.connect('scrapy.db')
        c = conn.cursor()
        # 折线图
        query = "SELECT pubtime,view from news"
        view = pd.read_sql_query(query, conn)
        query = "SELECT pubtime,support from news"
        support = pd.read_sql_query(query, conn)
        query = "SELECT pubtime,comments from news"
        comments = pd.read_sql_query(query, conn)

        view['pubtime'] = pd.to_datetime(view['pubtime'])
        support['pubtime'] = pd.to_datetime(support['pubtime'])
        comments['pubtime'] = pd.to_datetime(comments['pubtime'])

        view = view.resample('D', on='pubtime').sum()
        support = support.resample('D', on='pubtime').sum()
        comments = comments.resample('D', on='pubtime').sum()

        plt.figure(figsize=(10, 6))
        sns.lineplot(x='pubtime', y='view', data=view, label='Views')
        plt.xlabel('Publish Time')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.savefig('views.png', bbox_inches='tight')
        plt.show()

        sns.lineplot(x='pubtime', y='support', data=support, label='Supports')
        plt.xlabel('Publish Time')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.savefig('supports.png', bbox_inches='tight')
        plt.show()

        sns.lineplot(x='pubtime', y='comments', data=comments, label='Comments')
        plt.xlabel('Publish Time')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.savefig('comments.png', bbox_inches='tight')
        plt.show()
        conn.close()

    #词云图 
    elif choice == '3':
        import jieba
        conn = sqlite3.connect('scrapy.db')
        c = conn.cursor()
        def process_chinese_text(text):
            words = jieba.cut(text)
            words = [word for word in words if len(word) > 1]
            return ' '.join(words)

        query = "SELECT title from news"
        result = pd.read_sql_query(query, conn)
        result['processed_title'] = result['title'].apply(process_chinese_text)

        from wordcloud import WordCloud
        all_text = ' '.join(result['processed_title'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='C:\\Windows\\Fonts\\SimHei.ttf').generate(all_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('wordcloud.png', bbox_inches='tight')
        plt.show()
        conn.close()
    #增长趋势图
    elif choice == '4':
        conn = sqlite3.connect('scrapy.db')
        c = conn.cursor()
        query = "SELECT pubtime,view from news"
        view = pd.read_sql_query(query, conn)
        query = "SELECT pubtime,support from news"
        support = pd.read_sql_query(query, conn)
        query = "SELECT pubtime,comments from news"
        comments = pd.read_sql_query(query, conn)

        view['pubtime'] = pd.to_datetime(view['pubtime'])
        support['pubtime'] = pd.to_datetime(support['pubtime'])
        comments['pubtime'] = pd.to_datetime(comments['pubtime'])

        view = view.resample('D', on='pubtime').mean()
        support = support.resample('D', on='pubtime').mean()
        comments = comments.resample('D', on='pubtime').mean()

        view['cumulative_views'] = view['view'].cumsum()
        support['cumulative_supports'] = support['support'].cumsum()
        comments['cumulative_comments'] = comments['comments'].cumsum()

        plt.figure(figsize=(10, 6))
        plt.bar(view.index, view['view'], color='blue', alpha=0.7, label='Daily Views')
        plt.plot(view.index, view['cumulative_views'], color='orange', marker='o', label='Cumulative Views', linestyle='--')
        plt.xlabel('Date')
        plt.ylabel('Views')
        plt.title('Daily and Cumulative Views')
        plt.legend()
        plt.savefig('incre_views.png', bbox_inches='tight')
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.bar(support.index, support['support'], color='blue', alpha=0.7, label='Daily Supports')
        plt.plot(support.index, support['cumulative_supports'], color='orange', marker='o', label='Cumulative Supports', linestyle='--')
        plt.xlabel('Date')
        plt.ylabel('Supports')
        plt.title('Daily and Cumulative Supports')
        plt.legend()
        plt.savefig('incre_supports.png', bbox_inches='tight')
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.bar(comments.index, comments['comments'], color='blue', alpha=0.7, label='Daily Comments')
        plt.plot(comments.index, comments['cumulative_comments'], color='orange', marker='o', label='Cumulative Comments', linestyle='--')
        plt.xlabel('Date')
        plt.ylabel('Comments')
        plt.title('Daily and Cumulative Comments')
        plt.legend()
        plt.savefig('incre_comments.png', bbox_inches='tight')
        plt.show()
        conn.close()
    #绘制气泡图  
    elif choice == '5':
        conn = sqlite3.connect('scrapy.db')
        c = conn.cursor()
        query = "SELECT support,comments,view,pubtime from news"
        result = pd.read_sql_query(query, conn)
        result['pubtime'] = pd.to_datetime(result['pubtime'])
        result = result.resample('D', on='pubtime').sum()
        x = result['support']
        y = result['comments']
        size = result['view']

        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=x, y=y, size=size, sizes=(20, 500), alpha=0.7)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Bubble Chart')
        plt.savefig('bubble.png', bbox_inches='tight')
        plt.show()
        conn.close()

    elif choice == '6':
        conn = sqlite3.connect('scrapy.db')
        c = conn.cursor()
        # 散点图
        query = "SELECT pubtime,view from news"
        view = pd.read_sql_query(query, conn)
        view['pubtime'] = pd.to_datetime(view['pubtime'])
        view = view.resample('D', on='pubtime').sum()
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='pubtime', y='view', data=view)
        plt.xlabel('time')
        plt.ylabel('views')
        plt.savefig('scatter_view.png', bbox_inches='tight')
        plt.title('Scatter Plot of Views')
        plt.show()
        conn.close()
    elif choice == '7':
        conn = sqlite3.connect('scrapy.db')
        c = conn.cursor()
        # 散点图
        query = "SELECT pubtime,support from news"
        support = pd.read_sql_query(query, conn)
        support['pubtime'] = pd.to_datetime(support['pubtime'])
        support = support.resample('D', on='pubtime').sum()
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='pubtime', y='support', data=support)
        plt.xlabel('time')
        plt.ylabel('supports')
        plt.savefig('scatter_supports.png', bbox_inches='tight')
        plt.title('Scatter Plot of Supports')
        plt.show()
        conn.close()
    elif choice == '8':
        conn = sqlite3.connect('scrapy.db')
        c = conn.cursor()
        # 散点图
        query = "SELECT pubtime,comments from news"
        comments = pd.read_sql_query(query, conn)
        comments['pubtime'] = pd.to_datetime(comments['pubtime'])
        comments = comments.resample('D', on='pubtime').sum()
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='pubtime', y='comments', data=comments)
        plt.xlabel('time')
        plt.ylabel('comments')
        plt.savefig('scatter_comments.png', bbox_inches='tight')
        plt.title('Scatter Plot of Comments')
        plt.show()
        conn.close()



    else:
        print("无效的输入，请重新输入。")


if __name__ == "__main__":
    while True:
        print_menu()
        choice = input("请输入数字执行相应操作 (输入 'q' 退出程序): ")

        if choice == '1':
            crawl_blog()
        elif choice == '2':
            export_to_csv()
        elif choice == '3':
            quick_data_analysis()
        elif choice.lower() == 'q':
            print("感谢使用，程序已退出。")
            break
        else:
            print("无效的输入，请重新输入。")
        input("按 Enter 键继续...")
        os.system('cls' if os.name == 'nt' else 'clear')

# # cursor = c.execute("SELECT Id, title, title_url, pubtime,support,comments,view from news")
