from flask import Flask, render_template, render_template_string, request, url_for, redirect
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin,current_user
import os 
import backend

# Need to start the mongo server 
os.system('sudo service mongod Start')

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
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')
    # Setup Flask-MongoEngine
    db = MongoEngine(app)


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
        # Relationships
        roles = db.ListField(db.StringField(), default=[])
    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)
    
    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        if current_user.is_authenticated:
            return redirect('/members')
        else:
            return render_template_string("""
                {% extends "layout.html" %}
                {% block content %}
                     <h2>Home page</h2>
                         <p><a href={{ url_for('user.register') }}>Register</a></p>
                         <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                         <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
                         <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                         <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
                {% endblock %}
            """)

    # The Members page is only accessible to authenticated users via the @login_required decorator
    @app.route('/members')
    @login_required    # User must be authenticated
    def member_page():
        print(current_user.username)
        # String-based templates
        return render_template_string("""
            {% extends "layout.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """)

    @app.route('/registerActivity',methods=['GET', 'POST'])
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
            render_template('registerActivity2.html',activities=activities)
        return render_template('registerActivity2.html',activities=activities)

    @app.route('/admin')
    @login_required
    def adminPage():
        return render_template('admin.html')
    
    @app.route('/admin/createGroups',methods=['GET','POST'])
    @login_required
    def createGroups():
        groups = backend.getGroups()
        if request.method == 'POST':
            group = request.form['group']
            backend.insertGroup(group)
            groups = backend.getGroups()
            return render_template('createGroups.html',groups=groups)
        return render_template('createGroups.html',groups = groups)

    @app.route('/admin/assignGroups',methods=['GET','POST'])
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
        return render_template('assignGroups.html',users = users,groups=groups)

    @app.route('/admin/viewGroupReport',methods=['GET','POST'])
    @login_required
    def viewGroupReportPage():
        groups = backend.getGroups()
        if len(groups)>0:
            selectedGroup = groups[0]
        activities = backend.getActivitiesByGroup(selectedGroup)
        if request.method == 'POST':
            selectedGroup = request.form['selectedGroup']
            activities = backend.getActivitiesByGroup(selectedGroup)
            activities = backend.getActivitiesByUsername(current_user.username)
            print "there was a post request in viewGroupReport",selectedGroup
            for activity in activities:
                print(activity)
            return render_template('viewGroupReport.html',activities = activities,groups = groups,selectedGroup = selectedGroup)
        return render_template('viewGroupReport.html',activities = activities,groups = groups,selectedGroup = selectedGroup)

    return app

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)







