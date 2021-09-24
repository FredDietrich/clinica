#importando dependencias dos modulos internos

from datetime import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar, sqlite3
from blessed import Terminal

#setando variaveis de uso de varios modulos
term = Terminal()
banco = sqlite3.connect('clinica.db')
cursor = banco.cursor()

# Verifica se o numero das opções é valido
def leiaInt(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            print('ERRO: por favor, digite um numero valido.')
            continue
        except (KeyboardInterrupt):
            print('Usuario preferiu não digitar esse numero.')
            return 0
        else:
            return n


# imprime as linhas nos menus principais
def linha(tam=50):
    return "="*tam


# imprime os cabeçalhos nos menus e submenus, ou onde essa função for chamada
def header(txt):
    print(linha())
    print(txt.center(50))
    print(linha())


# exibe o menu independente da quantidade de opções
def menu(lista):
    header('Bem vindo a Clinica Tech Connect!')
    c = 1
    for item in lista:
        print(f'{c} - {item}')
        c+= 1
    print(linha())
    opc = leiaInt('Digite sua Opção: ')
    return opc
    

# exibe o submenu de cadastros
def cadastro(lista):
    header('Deseja ajustar um cadastro! Selecione uma opção.')
    c = 1
    for item in lista:
        print(f'{c} - {item}')
        c+=1
    print(linha())
    opc = leiaInt('Digite sua Opção: ')
    return opc    

# exibe o submenu de agenda
def menuAgenda(lista):
    header('Bem vindo a sua Agenda')
    c = 1
    for item in lista:
        print(f'{c} - {item}')
        c+=1
    print(linha())
    opc = leiaInt('Digite sua Opção: ')
    return opc 


# exibe o submenu de consultar
def consultar(lista):
    header('Seja Bem vindo a video Consulta!')
    c = 1
    for item in lista:
        print(f'{c} - {item}')
        c+=1
    print(linha())
    opc = leiaInt('Digite sua Opção: ')
    return opc

# exibe o submenu de arquivos
def arquivos(lista):
    header('Seja Bem vindo a sua area de arquivos!')
    c = 1
    for item in lista:
        print(f'{c} - {item}')
        c+=1
    print(linha())
    opc = leiaInt('Digite sua Opção: ')
    return opc

# -- AGENDA A PARTIR DAQUI -- #

def leiaAnoMes(querMes = True):
    while True:
        try:
            ano = int(input('Insira o ano para fazer a criacao da agenda: '))
            if querMes:
                mes = int(input('Insira o mes (1-12) para fazer a criacao da agenda: '))
            else: 
                mes = ''
        except (ValueError, TypeError):
            print('ERRO: por favor, digite um ano e um mês válidos.')
            continue
        except (KeyboardInterrupt):
            print('Usuario preferiu não digitar esses dados.')
            exit()
        else:
            return ano, mes

def agenda(estado):
    #caso o médico esteja gerando uma nova agenda
    if(estado == 'criando'):
        consultasA = []
        ano, mes = leiaAnoMes()
        #ano = 2021
        #mes = 10
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
            startDate = datetime(ano, mes, week[dayOfWeek], 9, 00, 00)
            endDate = datetime(ano, mes, week[dayOfWeek], 17, 30, 00)
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
        for i in dias:
            dia = []
            for x in consultas:
                if(str(x[0][8:10]) == i):
                    dia.append(x)
            consultasA.append(dia)
        agendaCrud(consultasA, mes, ano, dias, estado) #Chama o CRUD da agenda com a agenda criada a partir do mês e ano inseridos

    #caso o médico esteja editando a sua agenda   
    elif(estado == 'editando' or estado == 'exibindo'):
        consultasA = []
        select = 'select * from agenda where id_medico = ?'
        value = 1,
        cursor.execute(select, value)
        response = cursor.fetchall()
        if len(response) == 0:
            header('''  
    Não foi encontrada nenhuma agenda!
''')
            return 0
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
        consultasA = agrupadas[:]
        while True:
            print(f"""
{estado.upper()} AGENDA
INSIRA UM DOS ANOS ABAIXO PARA ACESSAR A AGENDA
            """)
            i = 1
            for ano in anos:
                print(term.blue, f'{i}{term.lightblue}: {ano}', term.normal)
                i+=1
            print()
            qualAno = leiaInt('Insira a opção de um dos anos: ')
            anoAtual = int(anos[qualAno-1])
            print('Meses disponiveis: \n')
            mesesDisponiveis = []
            for mes in consultasA[qualAno - 1]:
                mesesDisponiveis.append(datetime.strftime(mes[0][0][3], '%m'))
            mesesDisponiveis = list(dict.fromkeys(mesesDisponiveis))
            iMes = 1
            for mes in mesesDisponiveis:
                print(f'{term.blue}{iMes}{term.lightblue}: {mes}', term.normal)
                iMes += 1
            print()
            qualMes = leiaInt('Insira uma opção de um mês dentre os disponíveis: ')
            mesAtual = int(mesesDisponiveis[qualMes - 1])
            consultasFormatada = []
            for dia in consultasA[qualAno-1][qualMes-1]:
                esseDia = []
                for pedaco in dia:
                    esseHorario = []
                    esseHorario.append(datetime.strftime(pedaco[3], '%Y-%m-%d %H:%M:%S'))
                    esseHorario.append(datetime.strftime(pedaco[4], '%Y-%m-%d %H:%M:%S'))
                    esseDia.append(esseHorario)
                consultasFormatada.append(esseDia)
            if(estado == 'exibindo'):
                return agendaCrud(consultasFormatada, mesAtual, anoAtual, dias, estado)
            print(f"""
{term.blue}1 {term.lightblue}- Editar esse mês
{term.blue}2 {term.lightblue}- Deletar esse mês
{term.blue}3 {term.lightblue}- Sair
            """, term.normal)   
            opcaoEditarAgenda = leiaInt('Insira uma opção dentre as listadas acima: ')
            if(opcaoEditarAgenda == 3):
                return 0
            elif(opcaoEditarAgenda == 1):
                return agendaCrud(consultasFormatada, mesAtual, anoAtual, dias, estado) #Chama o CRUD da agenda com a agenda a editar trazida do banco de dados
            elif(opcaoEditarAgenda == 2):
                sqlDeleteAgenda = 'delete from agenda where dataInicioConsulta like ?'
                valuesDeleteAgenda = (str(ano)+'-'+str(mes)+'%'), 
                cursor.execute(sqlDeleteAgenda, valuesDeleteAgenda)
                banco.commit()
                return 0
            else:
                print('Insira uma opção válida!')
                return agenda(estado)

#Função de métodos CRUD da agenda, aqui apenas leitura e edição
def agendaCrud(consultasA, mes, ano, dias, estado):
    while True:
        problema = ''
        print(f"""{term.green}
    ---------------------------------------------------
    -- {estado.upper()} AGENDA PARA O MES {mes} DO ANO {ano} ---
    ---------------------------------------------------
    -- INSIRA O DIA PARA ACESSAR OS HORARIOS        ---
    ---------------------------------------------------
    -- DIGITE SAIR PARA SAIR DA AGENDA ----------------
    ---------------------------------------------------
            {problema}{term.normal}
                """)      

    #EXIBE UM CALENDARIO PARA O MEDICO VER OS DIAS   
        print(term.lightblue , calendar.month(theyear=ano, themonth=mes))
        problema = ''
        try:
            opcao = input('$ ')
        except KeyboardInterrupt:
            break
        except:
            continue
        if(opcao == 'sair' or opcao == 'SAIR'):
            #SAI DO MODULO AGENDA E ENVIA A AGENDA GERADA PARA O BANCO DE DADOS (CASO ESTEJA CRIANDO)
            print(f'{term.red}\nSaindo da agenda...\n')
            print(term.normal)
            for dia in consultasA:
                for horario in dia:
                    if(estado == 'criando'):
                        sqlAgenda = 'INSERT INTO agenda VALUES(null, null, ?, ?, ?)'
                        valoresAgenda = (1, horario[0], horario[1])
                        cursor.execute(sqlAgenda, valoresAgenda)
                        banco.commit()
            break
        elif(opcao in dias or '0' + opcao in dias):
            print()
            for x in consultasA:
                if(str(x[0][0][8:10]) == str(opcao)):
                    ili = 0
                    for i in x:
                        print(f'{term.blue}{ili + 1}{term.lightblue}: Inicio: {i[0][11:]}; Fim: {i[1][11:]};')
                        ili+=1
                    print()
                elif(str(x[0][0][8:10]) == '0' + str(opcao)):
                    ili = 0
                    for i in x:
                        print(f'{term.blue}{ili + 1}{term.lightblue}: Inicio: {i[0][11:]}; Fim: {i[1][11:]};')
                        ili+=1
                    print()
            #SUBMENU COM HORARIOS
            if estado == 'editando' or estado == 'criando':
                prob = ''
                while True:
                    if prob != '':
                        opcaoEdit = input(f'Insira o {prob} do horario para editar ou "SAIR" para voltar a lista de horarios do mes: ')
                    else:
                        opcaoEdit = input(f'Insira o numero do horario para editar ou "SAIR" para voltar a lista de horarios do mes: ')
                
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
                                ili = 1
                                for i in x:
                                    if(ili == int(opcaoEdit)):
                                    #SUBMENU "CRUD" DOS HORARIOS
                                        while True:
                                            try:
                                                print(f"""
{term.green}Editando: {term.blue}Inicio: {consultasA[iConsultas][opcaoEdit-1][0]} Fim: {consultasA[iConsultas][opcaoEdit-1][1]}
{term.normal}
{term.blue}1{term.lightblue}- Apagar este horario
{term.blue}2{term.lightblue} - Editar este horario
{term.blue}3{term.lightblue}- Voltar
                                                """)
                                                opcaoDentroDeEdit = input('Opcao: ')
                                            except:
                                                continue
                                            if(opcaoDentroDeEdit == '3'):
                                                break
                                            elif(opcaoDentroDeEdit == '1'):
                                                sqlDelete = 'delete from agenda where dataInicioConsulta = ? and dataFimConsulta = ?'
                                                valuesDelete = tuple(consultasA[iConsultas].pop(opcaoEdit-1))
                                                cursor.execute(sqlDelete, valuesDelete)
                                                banco.commit()
                                                break
                                            elif(opcaoDentroDeEdit == '2'):
                                            #SUBMENU EDITA HORARIOS
                                                while True:
                                                    try: 
                                                        novoComeco = input('Insira o novo horario do comeco no formato correto(hh:mm): ')
                                                        novoFim = input('Insira o novo horario do fim no formato correto(hh:mm): ')
                                                    except:
                                                        continue
                                                    try:
                                                        if(novoComeco == '' or novoFim == ''):
                                                            break
                                                        elif(not (novoComeco[1] == ':' or novoComeco[2] == ':') or not (novoFim[1] == ':' or novoFim[2] == ':')):
                                                            print('Insira os horarios no formato correto.')
                                                            continue
                                                        else: 
                                                            novoComeco = datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0][:11] + novoComeco, '%Y-%m-%d %H:%M')
                                                            novoFim = datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0][:11] + novoFim, '%Y-%m-%d %H:%M')
                                                            #PROCURANDO PROBLEMAS NO NOVO HORARIO
                                                            if(opcaoEdit > 1):
                                                                if((novoComeco < datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0], '%Y-%m-%d %H:%M:%S') - relativedelta(minutes=+30) or novoComeco > datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0], '%Y-%m-%d %H:%M:%S') + relativedelta(minutes=+30)) or (novoFim > datetime.strptime(consultasA[iConsultas][opcaoEdit-1][1], '%Y-%m-%d %H:%M:%S') + relativedelta(minutes=+30) or novoFim < datetime.strptime(consultasA[iConsultas][opcaoEdit-1][1], '%Y-%m-%d %H:%M:%S') - relativedelta(minutes=+30))):
                                                                    print('Novo horario muito longe do horario inicial, não seria melhor editar outro horario, caso possível?')
                                                                    continue
                                                                elif(not novoComeco >= datetime.strptime(consultasA[iConsultas][opcaoEdit-2][1], '%Y-%m-%d %H:%M:%S')):
                                                                    print(f'Conflito com horario anterior ({consultasA[iConsultas][opcaoEdit-2][0][11:]} - {consultasA[iConsultas][opcaoEdit-2][1][11:]}), por favor apague-o ou confira o novo horário inserido.')
                                                                    continue
                                                                elif(not novoFim <= datetime.strptime(consultasA[iConsultas][opcaoEdit][0], '%Y-%m-%d %H:%M:%S')):
                                                                    print(f'Conflito com o próximo horário ({consultasA[iConsultas][opcaoEdit][0][11:]} - {consultasA[iConsultas][opcaoEdit][1][11:]}), por favor apague-o ou confira o novo horário inserido.')
                                                                    continue
                                                                elif(not novoComeco.time() >= dt.time(9, 0) or not novoFim.time() >= dt.time(9, 0)):
                                                                    print(f'Horario antes do começo do expediente da clínica!')
                                                                    continue
                                                                elif(not novoFim.time() <= dt.time(18, 0)):
                                                                    print(f'Horario após o fim do expediente da clinica!')
                                                                    continue
                                                                elif not(novoComeco.time() <= dt.time(11, 15) and novoFim.time() <= dt.time(11,30) or novoComeco.time() >= dt.time(13, 30) and novoFim.time() >= dt.time(13,45)):
                                                                    print('Consulta no horário de almoço! Revise o horário.')
                                                                    continue
                                                                else:
                                                                    consultasA[iConsultas][opcaoEdit-1] = [datetime.strftime(novoComeco, '%Y-%m-%d %H:%M:%S'), datetime.strftime(novoFim, '%Y-%m-%d %H:%M:%S')]
                                                                    print(f'\nHorário editado com sucesso, {datetime.strftime(novoComeco, "%Y-%m-%d %H:%M:%S")} até {datetime.strftime(novoFim, "%Y-%m-%d %H:%M:%S")}.')
                                                                    break
                                                            else:
                                                                if((novoComeco < datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0], '%Y-%m-%d %H:%M:%S') - relativedelta(minutes=+30) or novoComeco > datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0], '%Y-%m-%d %H:%M:%S') + relativedelta(minutes=+30)) or (novoFim > datetime.strptime(consultasA[iConsultas][opcaoEdit-1][1], '%Y-%m-%d %H:%M:%S') + relativedelta(minutes=+30) or novoFim < datetime.strptime(consultasA[iConsultas][opcaoEdit-1][1], '%Y-%m-%d %H:%M:%S') - relativedelta(minutes=+30))):
                                                                    print('Novo horario muito longe do horario inicial, não seria melhor editar outro horario, caso possível?')
                                                                    continue
                                                                elif(not novoFim <= datetime.strptime(consultasA[iConsultas][opcaoEdit][0], '%Y-%m-%d %H:%M:%S')):
                                                                    print(f'Conflito com o próximo horário ({consultasA[iConsultas][opcaoEdit][0][11:]} - {consultasA[iConsultas][opcaoEdit][1][11:]}), por favor apague-o ou confira o novo horário inserido.')
                                                                    continue
                                                                elif(not novoComeco.time() >= dt.time(9, 0) or not novoFim.time() >= dt.time(9, 0)):
                                                                    print(f'Horario antes do começo do expediente da clínica!')
                                                                    continue
                                                                elif(not novoFim.time() <= dt.time(18, 0) or not novoComeco.time() < dt.time(18, 0)):
                                                                    print(f'Horario após o fim do expediente da clinica!')
                                                                    continue
                                                                elif not(novoComeco.time() <= dt.time(11, 15) and novoFim.time() <= dt.time(11,30) or novoComeco.time() >= dt.time(13, 30) and novoFim.time() >= dt.time(13,45)):
                                                                    print('Consulta no horário de almoço! Revise o horário.')
                                                                    continue
                                                                else:
                                                                    if(estado == 'editando'):
                                                                        sqlUpdate = 'update agenda set dataInicioConsulta = ?, dataFimConsulta = ? where dataInicioConsulta = ?'     
                                                                        valuesUpdate = (datetime.strftime(novoComeco, '%Y-%m-%d %H:%M:%S'), datetime.strftime(novoFim, '%Y-%m-%d %H:%M:%S'), consultasA[iConsultas][opcaoEdit-1][0])
                                                                        cursor.execute(sqlUpdate, valuesUpdate)
                                                                        banco.commit()                                                               
                                                                    consultasA[iConsultas][opcaoEdit-1] = [datetime.strftime(novoComeco, '%Y-%m-%d %H:%M:%S'), datetime.strftime(novoFim, '%Y-%m-%d %H:%M:%S')]
                                                                    print(f'\nHorário editado com sucesso, {datetime.strftime(novoComeco, "%Y-%m-%d %H:%M:%S")} até {datetime.strftime(novoFim, "%Y-%m-%d %H:%M:%S")}.')
                                                                    break
                                                    except:
                                                        continue
                                    ili+=1
                            iConsultas += 1
                        break
                    else: 
                        print('Insira um horário dentre os listados.')
                        continue
            else: 
                input('Pressione qualquer tecla para continuar...')
        else:
            problema = 'Insira um dia que esta agendado.'

# -- FIM AGENDA -- #

if __name__ == '__main__':
    print('Por favor execute a partir do arquivo "clinica.py".')
    exit()