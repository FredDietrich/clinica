#!/usr/bin/env python3

from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
#PRIMEIRA ENTRADA, ANO E MES PARA CRIAR A AGENDA
#ano = int(input('Insira o ano para fazer a criacao da agenda: '))
#mes = int(input('Insira o mes (1-12) para fazer a criacao da agenda: '))
ano = 2021
mes = 10
#GERANDO O CALENDARIO/DIAS

diass = []
calendario = calendar.Calendar(firstweekday=0)
cal = calendario.itermonthdates(ano, mes)
while True:
    try:
        diass.append(next(cal))
    except:
        break
#REMOVENDO FIM DE SEMANA
for x in diass:
    if(x.strftime('%a') == 'Sun'):
        diass.remove(x)
for x in diass:
    if(x.strftime('%a') == 'Sat'):
        diass.remove(x)
#REMOVE DIAS QUE NAO SAO DO MES QUE O MEDICO PEDIU, JA QUE O METODO DE CRIAR O CALENDARIO CRIA ALGUNS DIAS DE OUTROS MESES
def apaga(lista):
    listanova = lista
    for x in lista:
        if(x.strftime('%m') == str(mes) or x.strftime('%m') == '0' + str(mes)):
            continue
        else:
            listanova.remove(x)
            apaga(listanova)
    return lista

diass = apaga(diass)
#CRIA UMA LISTA COM OS DIAS UTEIS DO MES, JA SEM FIM DE SEMANA (NAO REMOVE FERIADOS)
week = []
for x in diass:
    week.append(int(x.strftime('%d')))

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)
horarios = []
#CRIA OS HORARIOS
dayOfWeek = 0
while dayOfWeek < len(week):
    startDate = datetime(2021, mes, week[dayOfWeek], 9, 00, 00)
    endDate = datetime(2021, mes, week[dayOfWeek], 17, 30, 00)
    thirtyminutes = relativedelta(minutes=+30)
    delta = relativedelta(startDate, endDate)
    horainicio = startDate
    while horainicio <= endDate:
        horafim = horainicio + thirtyminutes
        horarios.append(str(horainicio))
        horarios.append(str(horafim))
        horainicio = horainicio + thirtyminutes
    consultas = list(pairwise(horarios))
    dayOfWeek = dayOfWeek + 1

for x in range(len(consultas)):
    consultas[x] = list(consultas[x])
#APAGA HORARIO DE ALMOCO DO MEDICO, DEFINIDO EM REGRA DE NEGOCIO NO PRIMEIRO PI
def apagaConsultas(consultasE):
    consultasNovas = consultasE
    for x in consultasE:
        if(x[0][11:] == '11:30:00' or x[0][11:] == '12:00:00' or x[0][11:] == '12:30:00' or x[0][11:] == '13:00:00'):
            consultasNovas.remove(x)
            apagaConsultas(consultasNovas)
        else:
            continue
        return consultasNovas
#CHAMA A FUNCAO DE APAGAR AS CONSULTAS
consultas = apagaConsultas(consultas)

#DIAS DO MES AGENDADOS
dias = []
for x in consultas:
    dias.append(x[0][8:10])
dias = list(dict.fromkeys(dias))

#AGRUPA AS CONSULTAS POR DIA (CADA DIA EM UMA ARRAY)
consultasA = []
for i in dias:
    dia = []
    for x in consultas:
        if(str(x[0][8:10]) == i):
            dia.append(x)
    consultasA.append(dia)

#FUNCAO PARA CHECAR SE O HORARIO INSERIDO NA EDICAO POSSUI CONFLITOS 
def checaProximoDia(inicio, fim, iConsultas, opcaoEdit, firstTime=True):
    if(not inicio - relativedelta(inicio, fim) > inicio - relativedelta(inicio, datetime.strptime(consultasA[iConsultas][opcaoEdit][0], '%Y-%m-%d %H:%M:%S'))):
        return True
    else:
        if(firstTime):
            consultasA[iConsultas][opcaoEdit-1] = [novoComeco.strftime('%Y-%m-%d %H:%M:%S'), novoFim.strftime('%Y-%m-%d %H:%M:%S')]
        consultasA[iConsultas].pop(opcaoEdit)
        return checaProximoDia(inicio, fim, iConsultas, opcaoEdit + 1, False)

def apagaHorariosConflito(horariosEntrada, inicio, fim, opcaoEdit):
    horariosInterno = horariosEntrada[opcaoEdit:]
    print(horariosInterno)
    print(inicio - relativedelta(inicio, fim))
    for horario in horariosInterno:
        print(horario)
        print(inicio - relativedelta(inicio, datetime.strptime(horario[0], '%Y-%m-%d %H:%M:%S')))
        if(inicio - relativedelta(inicio, fim) > inicio - relativedelta(inicio, datetime.strptime(horario[0], '%Y-%m-%d %H:%M:%S'))):
            horariosInterno.remove(horario)
            return apagaHorariosConflito(horariosInterno, inicio, fim, opcaoEdit)
        else: 
            return horariosEntrada

print('\n')
#AQUI COMECA A PARTE QUE O MEDICO ENXERGA
while True:
    try:
        print(f"""
---------------------------------------------------
-- CRIANDO AGENDA PARA O MES {mes} DO ANO {ano} ---
---------------------------------------------------
-- INSIRA O DIA PARA CONFERIR OS HORARIOS/EDITAR --
---------------------------------------------------
-- DIGITE SAIR PARA SAIR DA CRIACAO DE AGENDA -----
---------------------------------------------------
        {problema}
            """)      
    except:
        print(f"""
---------------------------------------------------
-- CRIANDO AGENDA PARA O MES {mes} DO ANO {ano} ---
---------------------------------------------------
-- INSIRA O DIA PARA CONFERIR/EDITAR OS HORARIOS --
---------------------------------------------------
-- DIGITE SAIR PARA SAIR DA CRIACAO DE AGENDA -----
---------------------------------------------------
            """)   
#EXIBE O CALENDARIO PARA O MEDICO TER UMA NOCAO DOS DIAS   
    print(calendar.month(theyear=ano, themonth=mes))
    problema = ''
    try:
        opcao = input('$ ')
    except:
        continue
    if(opcao == 'sair' or opcao == 'SAIR'):
        print('saindo')
        break
    elif(opcao in dias or '0' + opcao in dias):
        for x in consultasA:
            if(str(x[0][0][8:10]) == str(opcao)):
                ili = 0
                for i in x:
                    print(f'{ili + 1}: Inicio: {i[0]}; Fim: {i[1]};')
                    ili+=1
            elif(str(x[0][0][8:10]) == '0' + str(opcao)):
                ili = 0
                for i in x:
                    print(f'{ili + 1}: Inicio: {i[0]}; Fim: {i[1]};')
                    ili+=1
        #SUBMENU COM HORARIOS GERADOS
        while True:
            try:
                if prob != '':
                    opcaoEdit = input(f'Insira o {prob} do horario para editar ou "SAIR" para voltar a lista de horarios do mes: ')
                else:
                    opcaoEdit = input(f'Insira o numero do horario para editar ou "SAIR" para voltar a lista de horarios do mes: ')
            except:
                opcaoEdit = input(f'Insira o numero do horario para editar ou "SAIR" para voltar a lista de horarios do mes: ')
            prob = ''
            if(opcaoEdit == 'sair' or opcaoEdit == 'SAIR'):
                break
            try:
                opcaoEdit = int(opcaoEdit)
            except:
                prob = 'NUMERO'
                continue
            if(opcaoEdit >= 1 and opcaoEdit <= ili):
                iConsultas = 0
                for x in consultasA:
                    if(str(x[0][0][8:10]) == str(opcao) or str(x[0][0][8:10]) == '0' + str(opcao)):
                        ili = 0
                        for i in x:
                            if(ili == int(opcaoEdit)):
                              #SUBMENU "CRUD" DOS HORARIOS
                                while True:
                                    try:
                                        print("""
1 - Apagar este horario
2 - Editar este horario
3 - Voltar
                                        """)
                                        opcaoDentroDeEdit = input('Opcao: ')
                                    except:
                                        continue
                                    if(opcaoDentroDeEdit == '3'):
                                        break
                                    elif(opcaoDentroDeEdit == '1'):
                                        consultasA[iConsultas].pop(opcaoEdit-1)
                                        break
                                    elif(opcaoDentroDeEdit == '2'):
                                      #SUBMENU EDITA HORARIOS
                                        while True:
                                            try: 
                                                #novoComeco = input('Insira o novo horario do comeco no formato correto(aaaa-mm-dd hh:mm:ss): ')
                                                #novoFim = input('Insira o novo horario do fim no formato correto(aaaa-mm-dd hh:mm:ss): ')
                                                novoComeco = '2021-10-01 09:00:00'
                                                novoFim = '2021-10-01 11:30:00'
                                            except:
                                                continue
                                            try:
                                                if(not (novoComeco[4] == '-' and novoComeco[7] == '-' and novoComeco[13] == ':' and novoComeco[16] == ':') or not (novoFim[4] == '-' and novoFim[7] == '-' and novoFim[13] == ':' and novoFim[16] == ':')):
                                                    print('Insira os horarios no formato correto, com 0 em caso de digito simples.')
                                                    continue
                                                else: 
                                                    novoComeco = datetime.strptime(novoComeco, '%Y-%m-%d %H:%M:%S')
                                                    novoFim = datetime.strptime(novoFim, '%Y-%m-%d %H:%M:%S')
                                                    #validacao 1: if(novoComeco - relativedelta(novoComeco, novoFim) >= novoComeco - relativedelta(novoComeco, inicioproxima))
                                                    print(apagaHorariosConflito(consultasA[iConsultas], novoComeco, novoFim, opcaoEdit))
                                                    break
                                            except:
                                                continue
                            ili+=1
                    iConsultas += 1
                break
    else:
        problema = 'Insira um dia que esta agendado.'