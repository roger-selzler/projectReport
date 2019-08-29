from pymongo import MongoClient
import datetime
import itertools
# import numpy as np

client = MongoClient('localhost',27017)

createMinimalData = True
resetDB = False
resetDB = True
if resetDB == True:
    client.drop_database('prjMngRpt')

prjdb = client['prjMngRpt']
dbUsers = client['projectReport']

# functions to deal with users 
def isAdmin(self,username):
    return True #TODO 
    
def getUsernames():
    usersCollection = dbUsers.user
    users = []
    for userX in usersCollection.find():
        users.append(userX['username'])
    for userX in users:
        print(userX)
    return users


# functions to deal with the activities
#prjdb.activities.drop()
def insertActivity(author,activityName,task,hours,details):
    activities = prjdb.activities
    group = getAssignedGroupUser(author)
    activity = dict(author=author,
            group=group,
            activity = activityName,
            task = task,
            hours = hours,
            details = details,
            date = datetime.datetime.now())
    print(activity)
    post_id = activities.insert_one(activity).inserted_id
    print(post_id)

def insertActivityWithDate(author,activityName,task,hours,details,date):
    activities = prjdb.activities
    group = getAssignedGroupUser(author)
    activity = dict(author=author,
            group=group,
            activity = activityName,
            task = task,
            hours = hours,
            details = details,
            date = date)
    print(activity)
    post_id = activities.insert_one(activity).inserted_id
    print(post_id)

def getActivities():
    activities = prjdb.activities
    listOfActivities = activities.find().sort("date",-1)
    print('Activities')
    for i in listOfActivities:
        if "author" in i:
            print(i["author"])
        if "group" in i:
            print(str(i['date']) + ' ' + i["group"])
            print(i['activity'])
        print (" " )
    return listOfActivities

def getActivitiesByUsername(username):
    activities = prjdb.activities
    listOfActivities = activities.find(dict(author=username)).sort("date",-1)
    act = []
    print('Activities by username')
    for i in listOfActivities:
        act.append(i)
        if "author" in i:
            print(i["author"])
        if "group" in i:
            print(str(i['date']) + ' ' + i["group"])
            print(i['activity'])
        print (" ")
    return act

def getActivitiesByGroup(groupX):
    activities = prjdb.activities
    listOfActivities = activities.find(dict(group=groupX)).sort("date",-1)
    act = []
    print("Group selected is: \"" + groupX +"\"")
    print('Activities by group')
    for i in listOfActivities:
        print("got activity")
        act.append(i)
    return act

def organizeActivityForReport(activities,config):
    pinfo = getProjectInfo();
    startDate = pinfo['startDate']
    seq =[activity['date'] for activity in activities]
    weeks = [(seqN-startDate).days/7+1 for seqN in seq]
    uniqueWeeks = []
    organizedActivities = dict()
    for week in weeks:
        if week not in uniqueWeeks:
            uniqueWeeks.append(week)
    uniqueWeeks.sort(reverse=True)
    for uniqueWeek in uniqueWeeks:
        for (week,activity) in itertools.izip(weeks,activities):
            if week == uniqueWeek:
                if 'week'+str(week) not in organizedActivities:
                    organizedActivities['week'+str(week)]=list()
                organizedActivities['week'+str(week)].append(activity)
    # for week in list(organizedActivities):
    #     organizedActivities[week] = sorted(organizedActivities[week])
    return organizedActivities

def getSummaryReportDataByGroup(activities):
    # activities = getActivitiesByGroup(group)
    summary = dict()
    summary['extraInfo']=dict(hours=0)
    uniqueActivities = []
    uniqueAuthors =[]
    for activity in activities:
        if activity['activity'] not in uniqueActivities:
            uniqueActivities.append(activity['activity'])
        if activity['author'] not in uniqueAuthors:
            uniqueAuthors.append(activity['author'])
    # build the structure
    for uniqueActivity in uniqueActivities:
        if uniqueActivity not in summary:
            summary[uniqueActivity] = dict(hours=0)
        for uniqueAuthor in uniqueAuthors:
            summary[uniqueActivity][uniqueAuthor]=dict(hours=0)
            summary['extraInfo'][uniqueAuthor]=dict(hours=0)
    # Compute total hours per author
    for activity in activities:
        summary[activity['activity']][activity['author']]['hours'] += activity['hours']
        summary[activity['activity']]['hours'] += activity['hours']
        summary['extraInfo']['hours'] += activity['hours']
        summary['extraInfo'][activity['author']]['hours'] += activity['hours']

    return summary

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
    g = []
    for i in groups:
        g.append(i['group'])
        print(i['group'])
    return g

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
    if aGrp == None:
        assignedGroups.insert_one(dict(username=username,group=group))
    else:
        assignedGroups.update_one(dict(_id=aGrp['_id']),{"$set":dict(username=username,group=group)},upsert=False)
    aGrp = assignedGroups.find_one(dict(username=username))
    updateGroupActivity(username,group)
    print(aGrp)

def listAssignedGroups():
    assignedGroups=prjdb.assignedGroups
    assignedGroups = assignedGroups.find().sort('username')
    for i in assignedGroups:
        print(i['username'] + ' ' + i['group'])

def ProjectInfo(startDate):
    pinfo = prjdb.projectInfo
    info = pinfo.find_one()
    if info == None:
        infoId = pinfo.insert_one(dict(startDate=startDate))
    else:
        pinfo.update_one(dict(_id=info['_id']),{"$set":dict(startDate=startDate)},upsert=False)

def getProjectInfo():
    pinfo = prjdb.projectInfo
    info = pinfo.find_one()
    return info

# ------ Tests
if resetDB and createMinimalData:
    ProjectInfo(datetime.datetime(2019,8,1,0,0,0))
    insertGroup('G1')
    insertGroup('G2')
    insertGroup('G3')
    getGroups()
    
    listAssignedGroups()
    assignGroup('rogerselzler','G1')
    assignGroup('carlosselzler','G1')
    assignGroup('giovannigiacommo','G2')
    assignGroup('franksinatra','G1')
    listAssignedGroups()
    assignGroup('rogerselzler','G2')
    assignGroup('rogerselzler','G1')
    listAssignedGroups()
    
    insertActivityWithDate("rogerselzler","management","editing papers",4,"details1",datetime.datetime(2019,8,15,15,35,0))    
    insertActivityWithDate("carlosselzler","management","editing papers",2,"details1",datetime.datetime(2019,8,17,15,35,0))    
    insertActivityWithDate("carlosselzler","Business","editing papers",3,"details1",datetime.datetime(2019,8,13,15,35,0))    
    insertActivityWithDate("franksinatra","control","editing papers",5,"details1",datetime.datetime(2019,8,12,15,35,0))    
    insertActivity("franksinatra","Business","editing papers one more time",1.5,"details2")
    insertActivity("giovannigiacommo","Business","editing papers one more time",1.22,"details2")
    insertActivity("carlosselzler","Business","Selling to xxx",3.4,"details3")
    getActivities()
    
    
    
    updateGroupActivity('rogerselzler',getAssignedGroupUser('rogerselzler'))
    getActivities()




