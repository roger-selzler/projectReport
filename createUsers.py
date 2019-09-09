import backend
import pandas as pd
import flask_bcrypt
from main import app

bcrypt = flask_bcrypt.Bcrypt(app)

a=pd.read_excel('SYSC3010A Fall 2019 Grades.xlsx')

for index,row in a.iterrows():
	backend.createUser(
		bcrypt,
		a.iloc[index]['First name'],
		a.iloc[index]['Surname'],
		a.iloc[index]['Email address'],
		str(a.iloc[index]['Student ID'])
		)
	print("Creeating user " +  a.iloc[index]['First name'] + a.iloc[index].Surname )
	# print(a.iloc[index].Surname + '  ' + a.iloc[index]['First name'])

def deleteUsers(a):
	for index,row in a.iterrows():
		backend.deleteUser(a.iloc[index]['First name'] + a.iloc[index]['Surname'])
