#!/usr/bin/env python3

import mysql.connector
from datetime import datetime
banco = mysql.connector.connect(
    host="localhost",
    user='dietrich',
    password='',
    database='clinica'
)
cursor = banco.cursor()

cursor.execute('select * from agenda')
response = cursor.fetchall()
horarios = []
for horario in response:
    horarios.append(list(horario))


dias = []
for x in horarios:
    dias.append(datetime.strftime(x[3], '%Y-%m-%d %H:%M:%S')[8:10])
dias = list(dict.fromkeys(dias))

#AGRUPA AS CONSULTAS POR DIA (CADA DIA EM UMA ARRAY)
consultasA = []
for i in dias:
    dia = []
    for x in horarios:
        if(datetime.strftime(x[3], '%Y-%m-%d %H:%M:%S')[8:10] == i):
            dia.append(x)
    consultasA.append(dia)
for dia in consultasA:
    print()
    for consulta in dia:
        print(consulta[3], consulta[4])
