from flask import Markup, request, redirect, render_template, url_for, g, Blueprint

import statistics
from jakk import data

main = Blueprint('main', __name__)

def calc_average(list):
  x = statistics.mean(list)
  average = round(x,3)
  return average

def calc_retention(list):
  rate = (sum(list) / len(list)) * 100
  return rate

@main.route('/')
def home():
  return redirect(url_for('main.major'))

@main.route('/major', methods=['GET','POST'])
def major():
  c = data.get_db()
  major_rows = data.select_major(c)
  major_rows.sort()

  major = ""
  major_salary_byyear = []
  loansByYear = []
  if request.method == 'POST':
    major = request.form['major']
    major_salary_byyear = data.get_major_salary_year(c, major)
    grad = data.get_graduated(c, major)
    loansByYear = data.get_loans_by_year(c, major)
  major_salary_byyear.sort(reverse=True)
  loansByYear.sort(reverse=True)
  major_sorted_gradyear = []
  major_sorted_salary = []
  major_sorted_loans = []
  retention = 0
  for x in major_salary_byyear:
    major_sorted_gradyear.append(((x[0])))
    major_sorted_salary.append(((x[1])))
  for x in loansByYear:
    major_sorted_loans.append(((x[1])))
    
  if len(major_sorted_salary) == 0:
    average = 0
  else:

    average = float(calc_average(major_sorted_salary)) * 1000 # PGT to get into thousands
    average = "{0:,g}".format(average)  # PGT to add comma
    retention = str(round(calc_retention(grad),2)) + '%'


  return render_template("major.html", major_rows = major_rows, major = major, major_loans = major_sorted_loans, major_salary = major_sorted_salary, major_gradyear = major_sorted_gradyear,retention = retention)

@main.route('/salaryvsdept', methods=['GET','POST'])
def salaryvsdept():
  c = data.get_db()
  major_rows = data.select_major(c)
  major_rows.sort()

  major = ""
  major_salary = [0]
  major_loans = [0]
  if request.method == 'POST':
    major = request.form['major']
    major_salary = data.get_major_salary(c, major)
    major_loans = data.get_major_loans(c, major)

  majors = []
  majors.append('Salary')
  majors.append('Loan Debt')

  average_salary = calc_average(major_salary)
  average_loans = calc_average(major_loans)
  averages = []
  averages.append(average_salary)
  averages.append(average_loans)
  return render_template("salaryvsdept.html", major_rows = major_rows, majors = majors, averages = averages, major = major, major_loans = major_loans)

@main.route('/compare', methods=['GET','POST'])
def compare():
  c = data.get_db()
  major_rows = data.select_major(c)
  major_rows.sort()

  majorF = ""
  majorS = ""
  major_salaryF = [0]
  major_salaryS = [0]
  if request.method == 'POST':
    majorF = request.form['majorF']
    majorS = request.form['majorS']
    major_salaryF = data.get_major_salary(c, majorF)
    major_salaryS = data.get_major_salary(c, majorS)

  majors = []
  majors.append(majorF)
  majors.append(majorS)

  averageF = calc_average(major_salaryF)
  averageS = calc_average(major_salaryS)
  averages = []
  averages.append(averageF)
  averages.append(averageS)
  return render_template("compare.html", major_rows = major_rows, majors = majors, averages = averages, majorF = majorF, majorS = majorS)

@main.route('/minor', methods=['GET','POST'])
def minor():
  c = data.get_db()
  major_rows = data.select_major(c)
  minor_rows = data.select_minor(c)
  major_rows.sort()
  minor_rows.sort()

  major = ""
  minor = ""
  major_salary = [0]
  minor_salary = [0]
  if request.method == 'POST':
    major = request.form['major']
    minor = request.form['minor']
    major_salary = data.get_major_salary(c, major)
    minor_salary = data.get_major_minor_salary(c, major, minor)

  major_minor = []
  major_minor.append(major)
  tuple_maj_min = []
  tuple_maj_min.append((major,minor))
  major_minor.append(', '.join(str(x) + ' and ' + str(y) + ' minor' for x, y in tuple_maj_min))

  averages = []
  average_major = calc_average(major_salary)
  averages.append(average_major)
  if len(minor_salary) != 0:
    average_minor = calc_average(minor_salary)
    averages.append(average_minor)

  return render_template("minor.html", major_rows = major_rows, minor_rows = minor_rows, major = major, minor = minor, major_minor = major_minor, averages = averages)

@main.route('/gender', methods=['GET','POST'])
def gender():
  c = data.get_db()
  genderM = "M"
  genderF = "F"
  genderM_salary = data.get_gender_salary(c, genderM)
  genderF_salary = data.get_gender_salary(c, genderF)
  averageM = calc_average(genderM_salary)
  averageM = str(averageM)
  averageM = averageM.replace('.',',')
  averageF = calc_average(genderF_salary)
  averageF = str(averageF)
  averageF = averageF.replace('.',',')

  genders = []
  nums = []
  nums.append(len(genderM_salary))
  nums.append(len(genderF_salary))
  genders.append(genderM)
  genders.append(genderF)
  colors = ["#546b00", "#b8e44e"]

  return render_template("gender.html", genderM = genderM, genderF = genderF, averageM = averageM, averageF = averageF, set=zip(nums, genders, colors))


