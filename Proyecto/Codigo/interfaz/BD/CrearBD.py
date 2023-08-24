import sqlite3

conn = sqlite3.connect('CURSO.db')
cursor_sql= conn.cursor()
#sql = "CREATE TABLE Estudiantes (USUARIO TEXT,MATEMATICAS REAL,ESPANOL REAL,ESTUDIOS REAL,CIENCIAS REAL,CONDUCTA REAL)"
#sql = "CREATE TABLE Docentes(NOMBRE TEXT, MATERIA TEXT)"
sql = "CREATE TABLE Director(NOMBRE TEXT)"
cursor_sql.execute(sql)

conn.commit()
conn.close()