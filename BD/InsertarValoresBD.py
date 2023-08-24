import sqlite3

conn = sqlite3.connect('CURSO.db')
cursor_sql = conn.cursor()

#many_data = [
#    ('', 90.2, 80.5, 90.5, 85.5, 100),
#    ('Jain2', 80.5, 70.8, 90.2, 80.3, 100),
#    ('Amanda', 50.5, 60.3, 80.2, 75.2, 80.1),
#    ('Esra', 88.8, 90.5, 97.8, 80.7, 100),
#    ('Lucian', 60.5, 50.3, 40.5, 80.3, 60.4)
#]


#sql = "INSERT INTO Estudiantes VALUES (?, ?, ?, ?, ?, ?)"
#cursor_sql.executemany(sql,many_data)

#many_data = [
#   ('Rogelio', 'Matematicas'),
#   ('Rocio', 'Espanol'),
#   ('Mateo', 'Ciencias'),
#   ('Rosaura', 'Estudios'),
#   ('Steve', 'Guia'),
#   ]

#sql = "INSERT INTO Docentes VALUES (?, ?)"
#cursor_sql.executemany(sql,many_data)

many_data = [
   ('Francisco',),
   ]

sql = "INSERT INTO Director VALUES (?)"
cursor_sql.executemany(sql,many_data)

conn.commit()
conn.close()