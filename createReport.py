import backend
import datetime
import collections
import io 

act = backend.getActivities();
users = backend.getUser();

def createReport(act,users):
    datestr = datetime.datetime.now().strftime("%Y_%d_%m_%H_%M")   
    f = open("report_" + datestr + ".txt","w+");
    f.write(generalInfo(act,users))
    f.write(generateActivityHours(act))   
    f.write(generateUsersWithoutActivity(users))
    f.close();

def generalInfo(act,users):
    buf = io.StringIO()
    buf.write("General informamtion:\n")
    buf.write("Number of activities: {}\n".format(len(act)))
    buf.write("Number of users: {}\n".format(len(users)))
    groups=backend.getGroups()
    buf.write("\n{:<12}{:<12}{:<12}\n".format("Group","Nr act","hours"))
    for g in groups:
        nact=0
        hact=0
        for a in act:
            if a['group'] == g:
                nact=nact+1
                hact=hact+float(a['hours'])
        buf.write("{:<12}{:<12}{:<12}\n".format(g,str(nact),str(hact)))
#    print(buf.getvalue())
    return buf.getvalue()

def generateActivityHours(activities):
    buf = io.StringIO()
    summ = dict();
    for a in activities:
        if a['activity'] in summ:
            summ[a['activity']]=summ[a['activity']] + float(a['hours'])
        else:
            summ[a['activity']] = float(a['hours'])
    buf.write("\n\nSummary of time spent per activity:\n")
    for s in sorted(summ,key=summ.get,reverse=True):
        buf.write("%s: %.2f\n" %(s,summ[s]))
    return buf.getvalue()

def generateUsersWithoutActivity(users):
    buf = io.StringIO()
    buf.write("\n\nList of users without activities:\n")
    buf.write("{:<20}{:<20}{:<20}{:<40}\n".format("Group","First name","Last name","email"))
    for u in users:
        a1=backend.getActivitiesByUsername(u['username'])
        if len(a1) ==0:
            buf.write("{:<20}{:<20}{:<20}{:<40}\n".format(backend.getAssignedGroupUser(u['username']),u['first_name'],u['last_name'],u['email']))
            #buf.write("%s %s %s %s\n" %(backend.getAssignedGroupUser(u['username']),u['first_name'],u['last_name'],u['email']))
    return buf.getvalue()        

createReport(act,users)
print(generateActivityHours(act))
print(generateUsersWithoutActivity(users))
