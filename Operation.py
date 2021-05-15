import firebaseDao
import Crawling
import Sentiment_analysis
society= []
sports= []
politics= []
economic= []
foreign= []
culture= []
entertain= []
digital= []
editorial= []
press = []
Category = [society, sports,politics,economic,foreign,culture,entertain,digital,editorial,press]
Category_ko = ['사회', '스포츠','정치','경제','국제','문화','연예','IT','칼럼','보도자료']
Category_En = ['Society', 'Sports', 'Politics', 'Economic', 'Foreign', 'Culture', 'Entertain', 'Digital', 'Editorial',
               'Press']
Category_urls= ['society','sports','politics','economic','foreign', 'culture','entertain','digital', 'editorial','press']

def article_saver():
    for category, category_ko, category_en,Category_url in zip(Category, Category_ko, Category_En,Category_urls):
        titles, contents = Crawling.split(Crawling.news_link(category,Category_url), category_ko)
        summaries, keywords,sentiments = Sentiment_analysis.data(contents)
        for title, content, summary, keyword, sentiment in zip(titles, contents, summaries, keywords,sentiments):
            firebaseDao.aritcle_dbsaver(title, content, category_en,summary, keyword, sentiment)

article_saver()