#!/usr/bin/env python3

#UNIT TESTS edicao da agenda, tudo isso esta/sera incluido no modulo principal 'agenda.py'

import sqlite3
from datetime import datetime
banco = sqlite3.connect('clinica.db')
cursor = banco.cursor()
sqlIdsMedico = 'select distinct id_medico from agenda;'
cursor.execute(sqlIdsMedico)
idsMedico = [id[0] for id in cursor.fetchall()]
agendasMedicos = []
for medico in idsMedico:
    print(medico)
    select = 'select * from agenda where id_medico = ?'
    value = medico,
    cursor.execute(select, value)
    response = cursor.fetchall()
    horarios = []
    for horario in response:
        horarios.append(list(horario))
    for horario in range(len(horarios)):
        horarios[horario][3] = datetime.strptime(horarios[horario][3], '%Y-%m-%d %H:%M:%S')
        horarios[horario][4] = datetime.strptime(horarios[horario][4], '%Y-%m-%d %H:%M:%S')

    anos = []
    for horario in horarios:
        anos.append(datetime.strftime(horario[3], '%Y'))
    anos = list(dict.fromkeys(anos))
    consultasA = []
    for anoI in anos:
        ano = []
        for horario in horarios:
            if(datetime.strftime(horario[3], '%Y') == anoI):
                ano.append(horario)
        consultasA.append(ano)

    agrupadas = []
    for anoI in consultasA:
        meses = []
        for horario in anoI:
            meses.append(datetime.strftime(horario[3], '%m'))
        meses = list(dict.fromkeys(meses))
        meses.sort()
        mesess = []
        for mes in meses:
            esseMes = []
            dias = []
            for horario in anoI:
                if(datetime.strftime(horario[3], '%m') == mes):
                    dias.append(datetime.strftime(horario[3], '%d'))
            dias = list(dict.fromkeys(dias))
            dias.sort()
            for diaI in dias:
                dia = []
                for horario in horarios:
                    if(datetime.strftime(horario[3], '%d') == diaI and datetime.strftime(horario[3], '%m') == mes):
                        dia.append(horario)
                esseMes.append(dia)
            mesess.append(esseMes)
        agrupadas.append(mesess)
    agendasMedicos.append(agrupadas)
consultasA = agendasMedicos[:]






                

