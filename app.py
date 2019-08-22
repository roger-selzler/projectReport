from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World from /'

@app.route('/home')
def home():
    return render_template("index.html")
#app.add_url_rule('/home','home',render_template("index.html"))

@app.route('/registerActivity')
def registerActivity():
    return render_template("registerActivity.html")

if __name__ == '__main__':
   app.run(debug=True)
