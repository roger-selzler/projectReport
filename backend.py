from pymongo import MongoClient
import datetime

client = MongoClient('localhost',27017)

resetDB = False
resetDB = True
if resetDB == True:
    client.drop_database('prjMngRpt')

prjdb = client['prjMngRpt']

#prjdb.activities.drop()
def insertActivity(author,group,activityName,task,hours):
    activities = prjdb.activities
    activity = dict(author=author,
            group=group,
            activity = activityName,
            task = task,
            hours = hours,
            date = datetime.datetime.now())
    print(activity)
    post_id = activities.insert_one(activity).inserted_id
    print(post_id)

def getActivities():
    activities = prjdb.activities
    listOfActivities = activities.find().sort("date")
    print('Activities')
    for i in listOfActivities:
        if "author" in i:
            print(i["author"])
        if "group" in i:
            print(str(i['date']) + ' ' + i["group"])
            print(i['activity'])
        print (" " )
    return listOfActivities

def updateGroupActivity(username,group):
    activities = prjdb.activities
    listOfActivities = activities.find(dict(author=username))
    print('Updating activity')
    print(listOfActivities)
    for act in listOfActivities:
        print(act)
        activities.update_one(dict(_id=act['_id']),{"$set":dict(group=group)},upsert=False)

def insertGroup(group):
    groups = prjdb.groups
    grp = groups.find_one(dict(group=group))
    if grp == None:
        group_id = groups.insert_one(dict(group=group))
        print("Inserted group " + group + " with id " + str(group_id))
    else:
        print("Group " + group + " already exist")

def getGroups():
    groups = prjdb.groups 
    groups = groups.find().sort("group")
    print ('Available Groups:')
    for i in groups:
        print(i['group'])
    return groups

def getAssignedGroupUser(username):
    assignGroups = prjdb.assignedGroups
    assignedGroup = assignGroups.find_one(dict(username=username))
    print(assignedGroup)
    if assignedGroup == None:
        return ''
    else:
        print(assignedGroup['group'])
        return assignedGroup['group']

def assignGroup(username,group):
    assignedGroups = prjdb.assignedGroups
    aGrp = assignedGroups.find_one(dict(username=username))
    #print(aGrp['_id'])
    print(aGrp)
    if aGrp == None:
        assignedGroups.insert_one(dict(username=username,group=group))
    else:
        assignedGroups.update_one(dict(_id=aGrp['_id']),{"$set":dict(username=username,group=group)},upsert=False)

def listAssignedGroups():
    assignedGroups=prjdb.assignedGroups
    assignedGroups = assignedGroups.find().sort('username')
    for i in assignedGroups:
        print(i['username'] + ' ' + i['group'])



# ------ Tests
insertActivity("rogerselzler","G1","management","editing papers",4)    
insertActivity("rogerselzler","G2","management","editing papers one more time",22)
insertActivity("CarlosSelzler","G4","Business","Selling to xxx",3.4)
getActivities()



insertGroup('Ggg1')
insertGroup('Ggg22')
insertGroup('Ggg22')
getGroups()

listAssignedGroups()
assignGroup('rogerselzler','Ggg1')
assignGroup('CarlosSelzler','Ggg21')
listAssignedGroups()
assignGroup('rogerselzler','Ggg12')
assignGroup('rogerselzler','Ggg221')
listAssignedGroups()

updateGroupActivity('rogerselzler',getAssignedGroupUser('rogerselzler'))
getActivities()
