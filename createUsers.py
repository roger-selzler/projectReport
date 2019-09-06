import backend
import pandas as pd
a=pd.read_excel('SYSC3010A Fall 2019 Grades.xlsx')

for index,row in a.iterrows():
	backend.createUser(
		a.iloc[index]['First name'],
		a.iloc[index]['Surname'],
		a.iloc[index]['Email address'],
		str(a.iloc[index]['Student ID'])
		)
	# print(a.iloc[index].Surname + '  ' + a.iloc[index]['First name'])

def deleteUsers():
	for index,row in a.iterrows:
		backend.deleteUsers(a.iloc[index]['First name'] + a.iloc[index]['Surname'])
