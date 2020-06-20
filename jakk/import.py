import sqlite3, csv, pandas

conn = sqlite3.connect('students_v1.db')
c = conn.cursor()

df = pandas.read_csv('./student_salary_data-v1-Jan27-19.csv')
df.to_sql('students', conn, if_exists='append', index=False)

c.execute("select * from students")

print(c.fetchall())