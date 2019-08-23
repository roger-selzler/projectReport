from pymongo import MongoClient
import datetime

client = MongoClient('localhost',27017)

prjdb = client['prjMngRpt']


def insertActivity(username,activityName,task,hours):
    activities = prjdb.activities
    activity = dict(author=username,
            activity = activityName,
            task = task,
            hours = hours,
            date = datetime.datetime.utcnow())
    print(activity)
    post_id = activities.insert_one(activity).inserted_id
    print(post_id)

# Tests
insertActivity("rogerselzler","management","editing papers",2)    
insertActivity("rogerselzler","management","editing papers one more time",3)    


