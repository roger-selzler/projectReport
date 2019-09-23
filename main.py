from flask import Flask, render_template, render_template_string, request, url_for, redirect
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin,current_user, roles_required
import os 
import backend

# Need to start the mongo server 
#os.system('sudo service mongod Start')

dbUsers = 'projectReport'
#userData = backend.userMng()

class ConfigClass(object):
    """ Flask application config """
    # Flask settings
    SECRET_KEY = 'This is an INSECUREsecret!!  DO NOT use this in production!!'
    # Flask-MongoEngine settings
    MONGODB_SETTINGS = {
        'db' : dbUsers,
        'host': 'mongodb://localhost:27017/projectReport'
    }
    # Flask-User settings
    USER_APP_NAME = "Project Progress Report"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False    # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    #USER_EMAIL_SENDER_EMAIL = 'rogerse18@gmail.com'
    USER_REQUIRE_RETYPE_PASSWORD = False   # Simplify register form

def create_app():
    
    """ Flask application factory """
    # Setup Flask and load app.config
    app1 = Flask('main')
    app1.config.from_object('main'+'.ConfigClass')
    # Setup Flask-MongoEngine
    db = MongoEngine(app1)


    # Define the User document.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Document, UserMixin):
        active = db.BooleanField(default=True)
        # User authentication information
        #email = db.StringField(default='')
        username = db.StringField(default='')
        password = db.StringField()
    #        email_confirmed_at = db.
        # User information
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')
        email = db.StringField(default='')
        # Relationships
        roles = db.ListField(db.StringField(), default=[])

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app1, db, User)
    @app1.route('/',methods=['GET','POST'])
    def root_page():
        if current_user.is_authenticated:
            return redirect(url_for('homePage'))
        else:
            # if request.method == 'POST':
            #     userName = request.form['username']
            #     password = request.form['password']
            #     # user = User.query.filter_by(username=request.form.username.data).first()
            #     print 'POST method ' , userName, password
            # if request.method =='POST':
            #     print request.form['username']
            #     print request.form['password']

            return redirect(url_for('user.login'))

    @app1.route('/Register') # TODO
    def registerPage():
        return render_template('register.html')

        # return redirect('/Home')

    # The Members page is only accessible to authenticated users via the @login_required decorator
    @app1.route('/Home') # TODO
    @login_required   
    def homePage():
        # print(current_user.username)
        return render_template('layout.html',isAdmin = backend.isAdmin(current_user.username))

    

    @app1.route('/registerActivity',methods=['GET', 'POST'])
    @login_required
    def registerActivityPage():
        activities = backend.getActivitiesByUsername(current_user.username)
        print(activities)
        if request.method == 'POST':
            author = current_user.username
            activity = request.form['activity']
            if activity == "Other":
                print('Activity is other')
                activity = request.form['activityOther']
            task = request.form['task']
            hours = request.form['hours']
            details = request.form['details']
            backend.insertActivity(author,activity,task,hours,details)
            print(type(hours))
            print(activity + task + hours + details)
            activities = backend.getActivitiesByUsername(current_user.username)
            render_template('registerActivity2.html',activities=activities,isAdmin = backend.isAdmin(current_user.username))
        return render_template('registerActivity2.html',activities=activities,isAdmin = backend.isAdmin(current_user.username))

    @app1.route('/admin')
    @login_required
    def adminPage():
        return redirect(url_for('viewGroupReportPage'))
        # return render_template('admin.html')
    
    @app1.route('/admin/createGroups',methods=['GET','POST'])
    @login_required
    def createGroups():
        groups = backend.getGroups()
        if request.method == 'POST':
            group = request.form['group']
            backend.insertGroup(group)
            groups = backend.getGroups()
            return render_template('createGroups.html',
                groups=groups,
                isAdmin = backend.isAdmin(current_user.username))
        return render_template('createGroups.html',
            groups = groups,
            isAdmin = backend.isAdmin(current_user.username))

    @app1.route('/admin/assignGroups',methods=['GET','POST'])
    @login_required
    def assignGroups():
        usernames = backend.getUsernames()
        groups = backend.getGroups()
        users = []
        for username in usernames:
            users.append(dict(username=username, group=backend.getAssignedGroupUser(username)))
        print(users)
        for userGroup in users:
            if userGroup['group'] not in groups:
                groups.append(userGroup['group'])
        print(users)
        #request.get_json()
        if request.method == 'POST':
            print("there was a post request")
            username = request.form['username']
            group = request.form['group']
            print(username + "  " + group)
            backend.assignGroup(username,group)
        return render_template('assignGroups.html',
            users = users,groups=groups,
            isAdmin = backend.isAdmin(current_user.username))

    @app1.route('/admin/viewGroupReport',methods=['GET','POST'])
    @login_required
    @roles_required('admin')
    def viewGroupReportPage():
        groups = backend.getGroups()
        if len(groups) > 0:
            selectedGroup = groups[0]
        else :
            selectedGroup = ""
        # reportOptions = ['Week','Username','Activity']
        reportOptions = ['Week']
        reportType = reportOptions[0]
        activities = backend.getActivitiesByGroup(selectedGroup)
        summary = backend.getSummaryReportDataByGroup(activities)
        activities = backend.organizeActivityForReport(activities,reportType)
        projectInfo = backend.getProjectInfo()
        print (projectInfo)
        print ("creating viewGroupReportPage")
        if request.method == 'POST':
            selectedGroup = request.form['selectedGroup']
            reportType = request.form['reportType']
            activities = backend.getActivitiesByGroup(selectedGroup)
            config = reportType
            summary = backend.getSummaryReportDataByGroup(activities)
            activities = backend.organizeActivityForReport(activities,config)
            print ("there was a post request in viewGroupReport",selectedGroup,reportType)
            return render_template( 'viewGroupReport.html',
                activities = activities,
                groups = groups,
                selectedGroup = selectedGroup,
                reportType = reportType,
                reportOptions=reportOptions,
                summary=summary,
                isAdmin = backend.isAdmin(current_user.username))
            # return redirect(url_for('viewGroupReportPage',selectedGroup))
        return render_template('viewGroupReport.html',
            activities = activities,
            groups = groups,
            selectedGroup = selectedGroup,
            reportType = reportType,
            reportOptions=reportOptions,
            summary=summary,
            isAdmin = backend.isAdmin(current_user.username))

    return app1

app = create_app()
# Start development web server
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True,ssl_context='adhoc')







