import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate('oss-project-f6fb6-firebase-adminsdk-9vwfe-27b8f530ff.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://oss-project-f6fb6-default-rtdb.firebaseio.com/'
})

def aritcle_dbsaver(title,content,category,summary, keyword, sentiment):
    num=0
    ref = db.reference('news/%s'%(category))
    snapshot = ref.get()
    for key in snapshot:
        num+=1
    dir = db.reference('news/%s/%s'% (category,num))
    dir.update({'title':'%s'%(title)})
    dir.update({'content':'%s'%(content)})
    dir.update({'summary': '%s' % (summary)})
    dir.update({'keyword': '%s' % (','.join(keyword))})
    dir.update({'sentiment': '%s' % (sentiment)})
