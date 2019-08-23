from flask import Flask, render_template, render_template_string
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin,current_user
import os 

# Need to start the mongo server 
os.system('sudo service mongod start')

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """
    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    # Flask-MongoEngine settings
    MONGODB_SETTINGS = {
        'db': 'projectReport',
        'host': 'mongodb://localhost:27017/projectReport'
    }
    # Flask-User settings
    USER_APP_NAME = "Project Progress Report"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False     # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form


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
        username = db.StringField(default='')
        password = db.StringField()
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
        # String-based templates
    #    return 
        return render_template_string("""
            {% extends "layout.html" %}
            {% block content %}
                <h2>Home page</h2>
    #             <p><a href={{ url_for('user.register') }}>Register</a></p>
     #            <p><a href={{ url_for('user.login') }}>Sign in</a></p>
      #           <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
       #          <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
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
            {% block menuRegisteredUser  %}
            <a href="/registerActivity"> Register Activity </a>
            {% endblock %}

            {% block content %}
                <h2>Members page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """)

    return app


# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)



#app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello World from /'

#@app.route('/home')
#def home():
#    return render_template("index.html")
#app.add_url_rule('/home','home',render_template("index.html"))

#@app.route('/registerActivity')
#def registerActivity():
#    return render_template("registerActivity.html")

#if __name__ == '__main__':
#    app.run(debug=True)
