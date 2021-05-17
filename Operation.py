import firebaseDao
import Crawling
import Sentiment_analysis
import gc
from time import sleep

def article_saver(category, category_ko, category_en,Category_url):
    titles, contents = Crawling.split(Crawling.news_link(category,Category_url), category_ko)
    for title, content,in zip(titles, contents):
        try:
            if(len(content)<3000):
                summary, keyword, sentiment = Sentiment_analysis.data(content)
                firebaseDao.aritcle_dbsaver(title, content, category_en,summary, keyword, sentiment)
        except:
            print ("error skip /n")
    gc.collect()
    del summary, keyword, sentiment, titles, contents