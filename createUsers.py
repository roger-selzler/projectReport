import backend
import pandas as pd
import flask_bcrypt
from main import app
import re
bcrypt = flask_bcrypt.Bcrypt(app)
a=pd.read_excel('SYSC3010A Fall 2019 Grades.xlsx')

def createUsers(a):
	for index,row in a.iterrows():
		backend.createUser(
			bcrypt,
			a.iloc[index]['First name'],
			a.iloc[index]['Surname'],
			a.iloc[index]['Email address'],
			str(a.iloc[index]['Student ID'])
			)
		print("Creating user " +  re.sub('[^a-zA-Z]+','',a.iloc[index]['First name'] + a.iloc[index].Surname ).lower())
		# print(a.iloc[index].Surname + '  ' + a.iloc[index]['First name'])

def deleteUsers(a):
	for index,row in a.iterrows():
		backend.deleteUser(
			re.sub('[^a-zA-Z]+','',a.iloc[index]['First name'] + a.iloc[index]['Surname']).lower())
		print ("User " + re.sub('[^a-zA-Z]+','',a.iloc[index]['First name'] + a.iloc[index]['Surname']).lower() + " deleted.")

def deleteAllUsersBut(username):
	users = backend.getUser()
	for user in users:
		if user['username'] != username:
			backend.deleteUser(user['username'])

def printUsernamesIDs(a):
	for index,row in a.iterrows():
		print(re.sub('[^a-zA-Z]+','',a.iloc[index]['First name'] + a.iloc[index]['Surname']).lower() +
			" " + str(a.iloc[index]['Student ID']))
		