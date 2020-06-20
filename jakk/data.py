import sqlite3
from flask import current_app as app

def get_db():
  #conn = sqlite3.connect('students_v1.db')
  conn = sqlite3.connect(app.config['DB_PATH'])
  c = conn.cursor()
  return c

def select_major(db):
  list = []
  for row in db.execute("select distinct Major1 from students"):
    list.append(str(row[0]))
  return list

def select_minor(db):
  list = []
  for row in db.execute("select distinct Minor1 from students"):
    list.append(str(row[0]))
  return list

def get_major_salary_year(db, m):
  list = []
  #for row in db.execute("select [Grad year],Salary from students where Major1 = '{}'".format(m)): # TODO: use ? rather than format
  for row in db.execute("select [Grad year],AVG(Salary) from students where Major1 = '{}' GROUP BY [Grad year]".format(m)): # TODO: use ? rather than format
    list.append((int(row[0]),float(row[1])))
  return list

def get_major_salary(db, m):
  list = []
  for row in db.execute("select Salary from students where Major1 = '{}'".format(m)):  # TODO: use ? rather than format
    list.append(int(row[0]))
  return list

def get_graduated(db, m):
  list = []
  for row in db.execute("select GraduatedAtUindy from students where Major1 = '{}'".format(m)):  # TODO: use ? rather than format
    list.append(int(row[0]))
  return list

def get_major_minor_salary(db, m, mi):
  list = []
  for row in db.execute("select Salary from students where Major1 = '{}' and Minor1 = '{}'".format(m,mi)):  # TODO: use ? rather than format
    list.append(int(row[0]))
  return list

def get_gender_salary(db, g):
  list = []
  for row in db.execute("select Salary from students where Sex = '{}'".format(g)):  # TODO: use ? rather than format
      list.append(int(row[0]))
  return list

def get_major_loans(db,m):
  list = []
  for row in db.execute("select Loans from students where Major1 = '{}'".format(m)):  # TODO: use ? rather than format
    list.append(int(row[0]))
  return list

def get_loans_by_year(db, m):
  list = []
  #for row in db.execute("select [Grad year],Salary from students where Major1 = '{}'".format(m)): # TODO: use ? rather than format
  for row in db.execute("select [Grad year],AVG(Loans) from students where Major1 = '{}' GROUP BY [Grad year]".format(m)): # TODO: use ? rather than format
    list.append((int(row[0]),int(row[1])))
  return list