#importando dependências

from datetime import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar, sqlite3
from blessed import Terminal
import getpass
import time

#variáveis usadas por vários módulos
term = Terminal()
banco = sqlite3.connect('clinica.db')
cursor = banco.cursor()

def leiaInt(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            print('ERRO: por favor, digite um número valido.')
            continue
        except (KeyboardInterrupt):
            print('Usuário preferiu não digitar esse número.')
            return 0
        else:
            return n

#imprime uma linha
def linha(tam=75):
    return "="*tam

# imprime os cabeçalhos nos menus e submenus, ou onde essa função for chamada
def header(txt):
    print(linha())
    print(txt.center(75))
    print(linha())

#menu inicial do login
def login(clinica):
    header('Bem vindo à Clínica Tech Connect!')
    loginOpcao = input('Digite 1 para login.\n\nDigite 2 para Cadastro.\n\nInforme sua opção: ')
    while True:
            if loginOpcao == '1':
                logado(clinica)
                break
            elif loginOpcao == '2':
                cadastros(clinica)
            else:
                print(term.clear, 'Opção Inválida! Tente novamente')
                login(clinica)
                break

#função de login
def logado(clinica):
    while True:
        header('Fazendo login na clinica!')
        try:
            info = input('Informe seu CRM ou CPF: ')
            senha = getpass.getpass('Informe sua senha:')
        except:
            continue
        if info == '' and senha == '':
            print(term.clear)
            login(clinica)
            break
        if '/' in info:
            selectCRM = 'select * from medico where crm = ?'
            valCRM = info, 
            cursor.execute(selectCRM, valCRM)
        else: 
            selectCPF = 'select * from paciente where cpf = ?'
            valCPF = info,
            cursor.execute(selectCPF, valCPF)
        resposta = cursor.fetchall()
        print(resposta)
        if(len(resposta) == 0):
            print(term.clear)
            print(f'{term.red}Nenhum usuário com esse CPF/CRM!{term.normal}')
            time.sleep(3)
            print(term.clear)
            continue
        else:
            if(senha == resposta[0][5]):
                clinica(resposta[0])
            else: 
                print(term.clear)
                print(f'{term.red}Você digitou a senha incorreta!{term.normal}')
                time.sleep(3)
                print(term.clear)
                print('Usuário ou senha inválidos!')   

# exibe o menu independente da quantidade de opções
def menu(lista):
    header('Menu Principal Clínica Tech Connect!')
    c = 1
    for item in lista:
        print(f'{c} - {item}')
        c+= 1
    print(linha())
    opc = leiaInt('Digite uma Opção: ')
    return opc
    
# exibe o submenu de agenda
def menuAgenda(lista):
    header('Bem vindo à sua Agenda')
    c = 1
    for item in lista:
        print(f'{c} - {item}')
        c+=1
    print(linha())
    opc = leiaInt('Digite uma Opção: ')
    return opc 


# exibe o submenu de consultas
def consultar(lista):
    header('Seja Bem vindo à video Consulta!')
    c = 1
    for item in lista:
        print(f'{c} - {item}')
        c+=1
    print(linha())
    opc = leiaInt('Digite uma Opção: ')
    return opc

# exibe o submenu de arquivos
def arquivos(lista):
    header('Seja Bem vindo à sua área de arquivos! (não funcional)')
    c = 1
    for item in lista:
        print(f'{c} - {item}')
        c+=1
    print(linha())
    opc = leiaInt('Digite sua Opção: ')
    return opc

# -- CADASTROS A PARTIR DAQUI -- #

def cadastros(clinica): #26092021

    lista_de_regioes_crm = ['/AC','/AL','/AP','/AM','/BA','/CE','/DF',
                            '/ES','/GO','/MA','/MT','/MS','/MG','/PA',
                            '/PB','/PR','/PE','/PI','/RJ','/RN','/RS',
                            '/RO','/RR','/SC','/SP','/SE','/TO']

    banco_de_dados_pacientes = [] #Dados dos clientes
    banco_de_dados_medicos = [] #Dados dos Médicos
    crm_referência = "00000000/PP"

    def entradaDeDados():
        condicao = str(input(f'\nOlá deseja realizar um cadastro? {term.blue}[s = Sim ou n = Não]: {term.normal}')).strip().upper()[0]
        print(term.clear)
        if condicao == "S":
            medico_paciente = str(input(f"\nVocê é médico ou paciente?{term.blue} [m = Médico ou p = Paciente]: {term.normal}")).strip().upper()[0]
            print(term.clear)
            if medico_paciente == "M":
                cadastroMedico()
            elif medico_paciente == "P":
                cadastroPaciente()
            else:
                return login(clinica)
        if condicao == "N":
            return login()        

    def cadastroMedico(): # funcional
        condicao = 0
        #Nome do Médico
        while condicao == 0:
            print(term.clear)
            nome_medico = str(input(f'{term.lightblue}\nDigite o seu nome completo:   \nOu deixe em branco para sair... '))
            if nome_medico == "" or nome_medico == " ":
                condicao = 1
                break
            for i in range(len(nome_medico[:])): # Verifica se não ha numeros no nome
                if nome_medico[i].isdigit() == True:
                    erroNome()
                    cadastroMedico()
            break

        #CRM do Médico
        while condicao == 0:
            print(term.clear)
            crm = str(input('\nDigite seu CRM! "Exemplo 00000000/RS"  \nOu deixe em branco para sair... ')).strip().upper()
            if crm == "":
                condicao = 1
                break
            if crm.isdigit() == True:# verifica se o CRM não é apenas uma sequência de numeros
                erro_crm()
            if crm[-3:] in lista_de_regioes_crm: # pega os ultimos 3 digitos e busca na lista (lista_de_regioes_crm)
                if len(crm[:-3]) <= len(crm_referência[:-3]): # pega todos digitos antes dos 3 ultimos e faz a comparacao com a quantidade de valores existentes no crm_referência
                    if crm[:-3].isdigit() == True : #verifica se os valores antes do 3 ultimos sao numeros
                        sqlTestaCRM = 'SELECT crm FROM medico WHERE crm = ?'
                        valCRM = crm,
                        cursor.execute(sqlTestaCRM, valCRM)
                        if (len(cursor.fetchall()) == 0):
                            print(f'{term.green}\nCRM ACEITO!{term.lightblue}')
                            time.sleep(3)
                            #segue com cadastro de médico
                            break
                        else:
                            print(f'{term.green}\nCRM Já cadastrado no sistema.{term.lightblue}')
                            time.sleep(3)
            erro_crm()

        #Telefone do Médico
        while condicao == 0:
            print(term.clear)
            telefone_medico = ""
            telefone_medico_ref = str(input('\nDigite seu telefone: "Exemplo: (51) 98888 8888"\nOu deixe em branco para sair... ')).strip().upper()
            if telefone_medico_ref == "":
                condicao = 1
                break
            for i in range(len(telefone_medico_ref)):
                if telefone_medico_ref[i].isdigit() == True: # Se o valor no índice [i] for numero intera na str telefone_medico
                    telefone_medico = telefone_medico + telefone_medico_ref[i]
            if len(telefone_medico) != 11: # Se o telefone formatado não tiver 11 digitose da erro
                erroTelefone()
                continue
            print(f'{term.green}\nTelefone cadastrado!{term.lightblue}') 
            time.sleep(3)
            break

        # Email do Médico
        while condicao == 0:
            print(term.clear)
            email_medico = str(input('\nDigite seu email: "Exemplo: nome@domínio.com.br"\nOu deixe em branco para sair... '))
            if email_medico == "":
                condicao = 1
                break
            if "@" in email_medico: #Verifica se tem "@" no email digitado
                print(f'{term.green}\nE-mail cadastrado!!!{term.lightblue}')
                time.sleep(3)
                break
            else:
                erroEmail()
        
        #Solicitação da senha de login
        while condicao == 0:
            print(term.clear)
            senha_medico = str(input('\nDigite sua senha de login: \nOu deixe em branco para sair... '))
            if senha_medico == "":
                condicao = 1
                break
            confirmacao_senha = str(input("\nConfirme sua senha: \nOu deixe em branco para digitar novamente... "))
            if confirmacao_senha == "":
                continue
            if senha_medico == confirmacao_senha:
                print(term.clear)
                print(f'{term.green}\n\nSENHA CONFIRMADA!\n')
                print(f'\nUsuário cadastrado com sucesso!{term.lightblue}')
                time.sleep(4)
                print(term.clear)
                break
            erroSenha()

        #Salvando os dados do cadastro no banco de dados dos medicos
        while condicao == 0:
            banco_de_dados_medicos.append([nome_medico,crm,telefone_medico,email_medico,senha_medico])
            sqlInsereMedico = 'INSERT INTO medico VALUES (null, ?,?,?,?,?)'
            valoresMedico = (nome_medico,crm,telefone_medico,email_medico,senha_medico)
            cursor.execute(sqlInsereMedico, valoresMedico)
            banco.commit()
            print(term.normal,term.clear)
            break
        return login(clinica)

    def cadastroPaciente(): # Funcional
        condicao = 0
        #Nome do Paciente
        while condicao == 0:
            print(term.clear)
            nome_paciente = str(input(f'{term.lightblue}\nDigite o seu nome completo:   \nOu deixe em branco para sair... '))
            if nome_paciente == "" or nome_paciente == " ":
                condicao = 1
                break
            for i in range(len(nome_paciente[:])):
                if nome_paciente[i].isdigit() == True:# Verifica se não ha numeros no nome
                    erroNome()
                    cadastroPaciente()
            break

        #CPF do Paciente
        while condicao == 0:
            print(term.clear)
            produto1_cpf = 0 # variavel para comparar o penultimo digito do CPF
            produto2_cpf = 0 # variavel para comparar o ultimo digito do CPF
            cpf = "" 
            cpf_string = str(input('\nDigite seu CPF! "Exemplo 000.000.000-00"  \nOu deixe em branco para sair... ')).strip()
            if cpf_string == "":
                condicao = 1
                break
            for i in range(len(cpf_string)):
                if cpf_string[i].isdigit() == True:# Se o valor no índice [i] for numero intera na str CPF
                    cpf = cpf + cpf_string[i]
            if len(cpf) != 11:
                erroCPF()
                continue
            """------------Abaixo os calculos de validação do CPF--------------"""
            for i in range(len(cpf[:-2])):
                produto1_cpf += int(cpf[i])*(10-i) 
            produto1_cpf = 11 - (produto1_cpf % 11)
            for i in range(len(cpf[:-2])):
                produto2_cpf += int(cpf[i])*(11-i)
            produto2_cpf = 11 -((produto2_cpf+(produto1_cpf*2)) % 11)
            if produto2_cpf > 9:
                produto2_cpf = 0
            if str(cpf[-2:]) == (str(produto1_cpf) + str(produto2_cpf)):
                sqlTestaCPF = 'SELECT cpf from paciente WHERE cpf = ?'
                valCPF = cpf, 
                cursor.execute(sqlTestaCPF, valCPF)
                if(len(cursor.fetchall()) == 0):
                    print(f'{term.green}\nCPF confirmado!!!{term.lightblue}')
                    time.sleep(3)
                    break
                else:
                    print(term.clear)
                    print(f'{term.red}\nCPF Já cadastrado!{term.lightblue}')
                    time.sleep(3)
            erroCPF()
            continue

        #Telefone do Paciente
        while condicao == 0:
            print(term.clear)
            telefone_paciente = ""
            telefone_paciente_ref = str(input('\nDigite seu telefone: "Exemplo: (51) 98888 8888"\nOu deixe em branco para sair... ')).strip().upper()
            if telefone_paciente_ref == "":
                condicao = 1
                break
            for i in range(len(telefone_paciente_ref)):
                if telefone_paciente_ref[i].isdigit() == True:# Se o valor no índice [i] for numero intera na str telefone_paciente
                    telefone_paciente = telefone_paciente + telefone_paciente_ref[i]
            if len(telefone_paciente) != 11:
                erroTelefone()
                continue
            print(f'{term.green}\nTelefone cadastrado!{term.lightblue}') 
            time.sleep(3)
            break

        # Email do Paciente
        while condicao == 0:
            print(term.clear)
            email_paciente = str(input('\nDigite seu email: "Exemplo: nome@domínio.com.br"\nOu deixe em branco para sair... '))
            if email_paciente == "":
                condicao = 1
                break
            if "@" in email_paciente: #Verifica se tem "@" no email digitado
                print(f'{term.green}\nE-mail cadastrado!!!{term.lightblue}')
                time.sleep(3)
                break
            else:
                erroEmail()

        #Solicitação da senha de login
        while condicao == 0:
            print(term.clear)
            senha_paciente = str(input('\nDigite sua senha de login: \nOu deixe em branco para sair... '))
            if senha_paciente == "":
                condicao = 1
                break
            confirmacao_senha = str(input("\nConfirme sua senha: \nOu deixe em branco para digitar novamente... "))
            if confirmacao_senha == "":
                continue
            if senha_paciente == confirmacao_senha:
                print(term.clear)
                print(f'{term.green}\n\nSENHA CONFIRMADA!\n')
                print(f'\nUsuário cadastrado com sucesso!{term.lightblue}')
                time.sleep(4)
                break
            erroSenha()

        #Salvando os dados do cadastro no banco de dados dos Pacientes
        while condicao == 0:
            banco_de_dados_pacientes.append([nome_paciente,cpf,telefone_paciente,email_paciente,senha_paciente])
            try:
                sqlInserePaciente = 'INSERT INTO paciente VALUES (null, ?,?,?,?,?)'
                valoresPaciente = (nome_paciente,cpf,telefone_paciente,email_paciente,senha_paciente)
                cursor.execute(sqlInserePaciente, valoresPaciente)
                banco.commit()
            except:
                print(f'{term.green}\nCPF Inválido ou já cadastado no sistema!{term.lightblue}')
                time.sleep(4)
                print(term.clear)
                entradaDeDados()
                break         
            break
        print(term.normal,term.clear)
        return login(clinica)
    """ -------------------Def's de erro!!!------------------------"""
    def erroNome():
        print(term.clear)
        print(f'{term.red}\nDigite um nome válido!{term.lightblue}')
        time.sleep(3)

    def erroCPF():
        print(term.clear)
        print(f'{term.red}\nDigite um CPF válido!{term.lightblue}')
        time.sleep(3)
    
    def erro_crm():
        print(term.clear)
        print(f'{term.red}\nDigite um CRM válido!{term.lightblue}')
        time.sleep(3)
        
    def erroTelefone():
        print(term.clear)
        print(f'{term.red}\nDigite um telefone válido!{term.lightblue}')
        time.sleep(3)

    def erroEmail():
        print(term.clear)
        print(f'{term.red}\nDigite um E-Mail Válido!{term.lightblue}')
        time.sleep(3)
    
    def erroSenha():
        print(term.clear)
        print(f'{term.red}\nAs senhas não coincidem!\nDigite novamente...{term.lightblue}')
        time.sleep(3)

    entradaDeDados()
# -- FIM CADASTROS -- #

# -- AGENDA A PARTIR DAQUI -- #

#função para requisitar ano e mês para o médico
def leiaAnoMes(querMes = True):
    while True:
        try:
            ano = int(input('Insira o ano para fazer a criação da agenda: '))
            if querMes:
                mes = int(input('Insira o mês (1-12) para fazer a criação da agenda: '))
            else: 
                mes = ''
        except (ValueError, TypeError):
            print('ERRO: por favor, digite um ano e um mês válidos.')
            continue
        except (KeyboardInterrupt):
            print('Usuário preferiu não digitar esses dados.')
            return 0
        else:
            return ano, mes

#função que puxa as consultas do banco de dados e agrupa elas nas camadas: 
"""
|-----------------------------------------|
|                 Médico                  |
|   |---------------------------------|   |                        
|   |              Ano                |   |       
|   |   |-------------------------|   |   | 
|   |   |          Mês            |   |   |       
|   |   |  |------------------|   |   |   |
|   |   |  |       Dia        |   |   |   |         
|   |   |  |  |------------|  |   |   |   |
|   |   |  |  |  Consulta  |  |   |   |   |              
|   |   |  |  |------------|  |   |   |   |
|   |   |  |                  |   |   |   |
|   |   |  |------------------|   |   |   |
|   |   |                         |   |   |
|   |   |-------------------------|   |   |
|   |                                 |   |
|   |---------------------------------|   |
|                                         | 
|-----------------------------------------|
"""
def agrupaConsultas(medico):
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
    return (agrupadas, anos, dias)

#também puxa agendas do banco
def puxaAgendaBanco(usuarioLogado, estado):
    sqlIdsMedico = 'select distinct id_medico from agenda;'
    cursor.execute(sqlIdsMedico)
    idsMedico = [id[0] for id in cursor.fetchall()]
    if(len(idsMedico)==0):
        header('Não foram encontradas agendas!')
        time.sleep(2)
        return 0
    if estado == 'marcando':
        nomesMedico = []
        agendasMedicos = []
        quantosLivreMedicos = []
        anosDias = []
        sqlQuantosLivre = 'select count(id_agenda) from agenda where id_paciente is null and id_medico = ?;'
        sqlMedico = 'select nome from medico where id_medico = ?'
        for medico in idsMedico:
            esseMedicoAnosDias = []
            cursor.execute(sqlMedico, (medico,))
            nomesMedico.append(cursor.fetchall()[0][0])
            cursor.execute(sqlQuantosLivre, (medico,))
            quantosLivreMedicos.append(cursor.fetchall()[0][0])
            agenda, anos, dias = agrupaConsultas(medico) 
            esseMedicoAnosDias.append(anos)
            esseMedicoAnosDias.append(dias)
            agendasMedicos.append(agenda)
            anosDias.append(esseMedicoAnosDias)
        consultasA = agendasMedicos[:]
        indisponiveis = []
        while True:
            indice = 1
            header(f'Escolha de médico: ')
            for nome in nomesMedico:
                print(f'{term.blue}{indice}{term.normal}: {term.green}{nome}; Este médico possui horários livres.' if quantosLivreMedicos[indice-1] > 0 else f'{term.red}{indice}: {nome};{term.grey} Este médico {term.red}não{term.gray} possui horários livres.', term.normal)
                if quantosLivreMedicos[indice-1] > 0:
                    indisponiveis.append(indice-1)
                indice += 1
            id_medico = leiaInt('Insira uma opção de médico: ')
            if(id_medico in indisponiveis):
                print(term.clear)
                print(term.red, 'Por favor insira um médico que tenha pelo menos um horário disponível!', term.normal)
                continue
            break
        consultasA = consultasA[id_medico-1]
        anos = anosDias[id_medico-1][0]
        dias = anosDias[id_medico-1][1]
    else:
        consultasA, anos, dias = agrupaConsultas(usuarioLogado[0])
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
        print('Meses disponíveis: \n')
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
        id_medico = consultasA[qualAno-1][qualMes-1][0][0][2]
        return (consultasFormatada, mesAtual, anoAtual, dias, id_medico)

def agenda(estado, usuarioLogado):
    #caso o médico esteja gerando uma nova agenda
    if(estado == 'criando'):
        consultasA = []
        try:
            ano, mes = leiaAnoMes()
        except:
            return 0
        sqlChecaInsere = 'select * from agenda where dataInicioConsulta like ? and id_medico = ?;'
        valChecaInsere = str(ano)+'-'+str(mes)+'%', usuarioLogado[0]
        cursor.execute(sqlChecaInsere, valChecaInsere)
        resposta = cursor.fetchall()
        if not(len(resposta) == 0):
            header('Você já possui uma agenda cadastrada para este mês!')
            return 0
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
        sqlAgenda = 'INSERT INTO agenda VALUES(null, null, ?, ?, ?)'
        for dia in consultasA:
                for horario in dia:
                        valoresAgenda = (usuarioLogado[0], horario[0], horario[1])
                        cursor.execute(sqlAgenda, valoresAgenda)
                        banco.commit()
                        header(f'{term.clear}Salvando alterações...')
                        print()
        while True:
            desejaEditar = input('Deseja editar a agenda criada? [s = Sim ou n = Não]: ')
            if(desejaEditar[0].upper() == 'S'):
                agendaCrud(consultasA, mes, ano, dias, 'editando', usuarioLogado) #Chama o CRUD da agenda com a agenda criada a partir do mês e ano inseridos
                break
            elif(desejaEditar[0].upper() == 'N'):
                return 0
  
    #caso o médico esteja editando a sua agenda   
    elif(estado == 'editando' or estado == 'exibindo' or estado == 'marcando'): 
        try:
            consultasFormatada, mesAtual, anoAtual, dias, id_medico = puxaAgendaBanco(usuarioLogado, estado)
        except:
            return 0
        #caso estiver exibindo ou marcando não precisa exibir menu de editar e deletar
        if(estado == 'exibindo' or estado == 'marcando'):
            return agendaCrud(consultasFormatada, mesAtual, anoAtual, dias, estado, usuarioLogado, id_medico)
        
        print(f"""
{term.blue}1 {term.lightblue}- Editar esse mês
{term.blue}2 {term.lightblue}- Apagar esse mês
{term.blue}3 {term.lightblue}- Sair
        """, term.normal)   
        opcaoEditarAgenda = leiaInt('Insira uma opção dentre as listadas acima: ')
        if(opcaoEditarAgenda == 3):
            return 0
        elif(opcaoEditarAgenda == 1):
            return agendaCrud(consultasFormatada, mesAtual, anoAtual, dias, estado, usuarioLogado) #Chama o CRUD da agenda com a agenda a editar trazida do banco de dados
        elif(opcaoEditarAgenda == 2):
            sqlChecaAgendadas = 'select * from agenda where id_medico = ? and id_paciente is not null and id_paciente <> 0 and dataInicioConsulta like ?;'
            valuesChecaAgendada = usuarioLogado[0], str(anoAtual)+'-'+str(mesAtual)+'%' 
            cursor.execute(sqlChecaAgendadas, valuesChecaAgendada)
            resposta = cursor.fetchall()
            if(len(resposta) == 0):
                sqlDeleteAgenda = 'delete from agenda where dataInicioConsulta like ? and id_medico = ?'
                valuesDeleteAgenda = (str(anoAtual)+'-'+str(mesAtual)+'%'), usuarioLogado[0]
                print(term.clear)
                header(f'{term.red}Apagando...')
                cursor.execute(sqlDeleteAgenda, valuesDeleteAgenda)
                banco.commit()
                return 0
            else:
                print(term.clear)
                header('Há pacientes agendados para este mês!')
                header('Saindo...')
                return 0
        else:
            print('Insira uma opção válida!')
            return agenda(estado, usuarioLogado)

    elif estado == 'editandoPaciente' or estado == 'exibindoPaciente':
        sqlProcuraAgendadas = 'select * from agenda where id_paciente = ?'
        sqlNomeMedico = 'select nome from medico where id_medico = ?'
        valProcuraAgendadas = usuarioLogado[0],
        cursor.execute(sqlProcuraAgendadas, valProcuraAgendadas)
        resposta = cursor.fetchall()
        if(len(resposta) == 0):
            header('Você não possui consultas agendadas ainda!')
        else:
            header('CONSULTAS AGENDADAS')
            indexAtual = 1
            print()
            for agendaResposta in resposta:
                valNomeMedico = resposta[indexAtual-1][2],
                cursor.execute(sqlNomeMedico, valNomeMedico)
                nomeMedico = cursor.fetchone()
                print(f'{term.blue}{indexAtual}{term.lightblue}: {agendaResposta[3][:16]} - {agendaResposta[4][11:16]}; Com o médico: {nomeMedico[0]}')
                indexAtual+=1
            if estado == 'editandoPaciente':
                print()
                opcaoEditaAgendada = leiaInt('Insira a opção de uma consulta acima para desmarcá-la ou 0 para sair: ')
                if(opcaoEditaAgendada == 0):
                    return 0
                sqlDeletaAgendada = 'delete from agenda where id_agenda = ?'
                cursor.execute(sqlDeletaAgendada, (resposta[opcaoEditaAgendada-1][0],))
                banco.commit()       
            elif estado == 'exibindoPaciente':   
                input('Pressione qualquer tecla para sair...') #@Gabriel Goulart pode ver se coloca algo aqui nesse ponto  

#Função de métodos CRUD da agenda, aqui apenas leitura e edição
def agendaCrud(consultasA, mes, ano, dias, estado, usuarioLogado, id_medico=None):
    while True:
        print(term.clear)
        problema = ''    
        header(f'{term.green}{estado.upper()} AGENDA PARA O MÊS {mes} DO ANO {ano}')
        header(f'INSIRA O DIA PARA ACESSAR OS HORÁRIOS')
        header('DIGITE SAIR PARA SAIR DA AGENDA')
        header(f'{problema}{term.normal}')
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
                        valoresAgenda = (usuarioLogado[0], horario[0], horario[1])
                        cursor.execute(sqlAgenda, valoresAgenda)
                        banco.commit()
                        header(f'{term.clear}Salvando alterações...')
                        print()
            break
        elif(opcao in dias or '0' + opcao in dias):
            if(estado == 'marcando'):
                print(term.yellow, '\nAs consultas costumam durar 30 min, podendo se estender até o início do próximo horário.', term.normal)
            elif(estado == 'editando'):
                print(term.yellow, '\nCaso alguma consulta esteja como não editável, quer dizer que há um paciente agendado nela, ou foi inativado.')
            for x in consultasA:
                if(str(x[0][0][8:10]) == str(opcao) or str(x[0][0][8:10]) == '0' + str(opcao)):
                    ili = 0
                    disponiveis = []
                    indisponiveis = []
                    horariosConsulta = (0, 2, 4, 5, 7, 9, 11, 13)
                    print('')
                    for i in x:
                        if estado == 'marcando':
                            if(ili in horariosConsulta):
                                indexAtual = horariosConsulta.index(ili)
                                sqlLivre = 'select id_paciente from agenda where dataInicioConsulta = ? and dataFimConsulta = ? and id_medico = ?'
                                valLivre = i[0], i[1], id_medico
                                cursor.execute(sqlLivre, valLivre)
                                temPaciente = cursor.fetchall()[0][0]
                                if(temPaciente == None):
                                    disponiveis.append(indexAtual+1)
                                    print(f'{term.blue}{indexAtual + 1}{term.lightblue}: {i[0][11:]} - {i[1][11:]}; Disponível;')
                                else:
                                    indisponiveis.append(indexAtual+1)
                                    print(f'{term.blue}{indexAtual + 1}{term.gray}: {i[0][11:]} - {i[1][11:]}; Indisponível;')
                        elif estado == 'editando' or estado == 'exibindo':
                            sqlProcuraPaciente = 'select id_paciente from agenda where id_medico = ? and dataInicioConsulta = ? and dataFimConsulta = ?'
                            valProcuraPaciente = usuarioLogado[0], i[0], i[1]
                            cursor.execute(sqlProcuraPaciente, valProcuraPaciente)
                            resposta = cursor.fetchall()
                            if(resposta[0][0] == None):
                                print(f'{term.blue}{ili + 1}{term.lightblue}: Início: {i[0][11:]}; Fim: {i[1][11:]}; Editável;')
                                disponiveis.append(ili+1)
                            elif(resposta[0][0] == 0):
                                print(f'{term.blue}{ili + 1}{term.gray}: Início: {i[0][11:]}; Fim: {i[1][11:]}; Inativado;')
                                indisponiveis.append(ili+1)
                            else:
                                print(f'{term.blue}{ili + 1}{term.gray}: Início: {i[0][11:]}; Fim: {i[1][11:]}; Não editável;')
                                indisponiveis.append(ili+1)
                        else:
                            print(f'{term.blue}{ili + 1}{term.lightblue}: Início: {i[0][11:]}; Fim: {i[1][11:]};')
                        ili+=1
                    print(term.normal)
            #SUBMENU COM HORARIOS
            if estado == 'editando':
                prob = ''
                while True:
                    if prob != '':
                        opcaoEdit = input(f'Insira o {prob} do horário para editar ou "sair" para voltar a lista de horários do mes: ')
                    else:
                        opcaoEdit = input(f'Insira o número do horário para editar ou "sair" para voltar a lista de horários do mes: ')
                    if(opcaoEdit.upper() == 'SAIR'):
                        break
                    try:
                        opcaoEdit = int(opcaoEdit)
                    except:
                        prob = 'NÚMERO'
                        continue
                    if(opcaoEdit in disponiveis):
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
{term.green}Editando: {term.blue}Início: {consultasA[iConsultas][opcaoEdit-1][0]} Fim: {consultasA[iConsultas][opcaoEdit-1][1]}
{term.normal}
{term.blue}1{term.lightblue}- Inativar este horário
{term.blue}2{term.lightblue}- Editar este horário
{term.blue}3{term.lightblue}- Voltar
                                                    """)
                                                    opcaoDentroDeEdit = input('Opção: ')
                                                except:
                                                    continue
                                                if(opcaoDentroDeEdit == '3'):
                                                    break
                                                elif(opcaoDentroDeEdit == '1'):
                                                    sqlDelete = 'update agenda set id_paciente = 0 where dataInicioConsulta = ? and dataFimConsulta = ? and id_medico = ?'
                                                    valuesDelete = consultasA[iConsultas].pop(opcaoEdit-1)
                                                    valuesDelete.append(usuarioLogado[0])
                                                    cursor.execute(sqlDelete, tuple(valuesDelete))
                                                    banco.commit()
                                                    break
                                                elif(opcaoDentroDeEdit == '2'):
                                                #SUBMENU EDITA HORARIOS
                                                    sqlProcuraInativado = 'select id_paciente from agenda where id_medico = ? and dataInicioConsulta = ?'
                                                    cursor.execute(sqlProcuraInativado, (usuarioLogado[0], datetime.strptime(consultasA[iConsultas][opcaoEdit][0], '%Y-%m-%d %H:%M:%S')))
                                                    temInativadoDepois = True if cursor.fetchone()[0] == 0 else False
                                                    while True:
                                                        try: 
                                                            novoComeco = input('Insira o novo horário do começo no formato correto(hh:mm): ')
                                                            novoFim = input('Insira o novo horário do fim no formato correto(hh:mm): ')
                                                        except:
                                                            continue
                                                        try:
                                                            if(novoComeco == '' or novoFim == ''):
                                                                break
                                                            elif(not (novoComeco[1] == ':' or novoComeco[2] == ':') or not (novoFim[1] == ':' or novoFim[2] == ':')):
                                                                print('Insira os horários no formato correto.')
                                                                continue
                                                            else: 
                                                                novoComeco = datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0][:11] + novoComeco, '%Y-%m-%d %H:%M')
                                                                novoFim = datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0][:11] + novoFim, '%Y-%m-%d %H:%M')
                                                                #PROCURANDO PROBLEMAS NO NOVO HORARIO
                                                                if(opcaoEdit > 1):
                                                                    cursor.execute(sqlProcuraInativado, (usuarioLogado[0], datetime.strptime(consultasA[iConsultas][opcaoEdit-2][0], '%Y-%m-%d %H:%M:%S')))
                                                                    temInativadoAntes = True if cursor.fetchone()[0] == 0 else False
                                                                    if((novoComeco < datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0], '%Y-%m-%d %H:%M:%S') - relativedelta(minutes=+30) or novoComeco > datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0], '%Y-%m-%d %H:%M:%S') + relativedelta(minutes=+30)) or (novoFim > datetime.strptime(consultasA[iConsultas][opcaoEdit-1][1], '%Y-%m-%d %H:%M:%S') + relativedelta(minutes=+30) or novoFim < datetime.strptime(consultasA[iConsultas][opcaoEdit-1][1], '%Y-%m-%d %H:%M:%S') - relativedelta(minutes=+30))):
                                                                        print('Novo horário muito longe do horário inicial, não seria melhor editar outro, caso possível?')
                                                                        continue
                                                                    elif(not novoComeco >= datetime.strptime(consultasA[iConsultas][opcaoEdit-2][1], '%Y-%m-%d %H:%M:%S') and (not temInativadoAntes)):
                                                                        print(f'Conflito com horário anterior ({consultasA[iConsultas][opcaoEdit-2][0][11:]} - {consultasA[iConsultas][opcaoEdit-2][1][11:]}), por favor apague-o ou confira o novo horário inserido.')
                                                                        continue
                                                                    elif(not novoFim <= datetime.strptime(consultasA[iConsultas][opcaoEdit][0], '%Y-%m-%d %H:%M:%S') and (not temInativadoDepois)):
                                                                        print(f'Conflito com o próximo horário ({consultasA[iConsultas][opcaoEdit][0][11:]} - {consultasA[iConsultas][opcaoEdit][1][11:]}), por favor apague-o ou confira o novo horário inserido.')
                                                                        continue
                                                                    elif(not novoComeco.time() >= dt.time(9, 0) or not novoFim.time() >= dt.time(9, 0)):
                                                                        print(f'Horário antes do começo do expediente da clínica!')
                                                                        continue
                                                                    elif(not novoFim.time() <= dt.time(18, 0)):
                                                                        print(f'Horário após o fim do expediente da clinica!')
                                                                        continue
                                                                    elif not(novoComeco.time() <= dt.time(11, 15) and novoFim.time() <= dt.time(11,30) or novoComeco.time() >= dt.time(13, 30) and novoFim.time() >= dt.time(13,45)):
                                                                        print('Consulta no horário de almoço! Revise-o.')
                                                                        continue
                                                                    else:
                                                                        sqlUpdate = 'update agenda set dataInicioConsulta = ?, dataFimConsulta = ? where dataInicioConsulta = ? and id_medico = ?'     
                                                                        valuesUpdate = (datetime.strftime(novoComeco, '%Y-%m-%d %H:%M:%S'), datetime.strftime(novoFim, '%Y-%m-%d %H:%M:%S'), consultasA[iConsultas][opcaoEdit-1][0], usuarioLogado[0])
                                                                        cursor.execute(sqlUpdate, valuesUpdate)
                                                                        banco.commit()   
                                                                        consultasA[iConsultas][opcaoEdit-1] = [datetime.strftime(novoComeco, '%Y-%m-%d %H:%M:%S'), datetime.strftime(novoFim, '%Y-%m-%d %H:%M:%S')]
                                                                        print(f'\nHorário editado com sucesso, {datetime.strftime(novoComeco, "%Y-%m-%d %H:%M:%S")} até {datetime.strftime(novoFim, "%Y-%m-%d %H:%M:%S")}.')
                                                                        break
                                                                else:
                                                                    if((novoComeco < datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0], '%Y-%m-%d %H:%M:%S') - relativedelta(minutes=+30) or novoComeco > datetime.strptime(consultasA[iConsultas][opcaoEdit-1][0], '%Y-%m-%d %H:%M:%S') + relativedelta(minutes=+30)) or (novoFim > datetime.strptime(consultasA[iConsultas][opcaoEdit-1][1], '%Y-%m-%d %H:%M:%S') + relativedelta(minutes=+30) or novoFim < datetime.strptime(consultasA[iConsultas][opcaoEdit-1][1], '%Y-%m-%d %H:%M:%S') - relativedelta(minutes=+30))):
                                                                        print('Novo horário muito longe do horário inicial, não seria melhor editar outro, caso possível?')
                                                                        continue
                                                                    elif(not novoFim <= datetime.strptime(consultasA[iConsultas][opcaoEdit][0], '%Y-%m-%d %H:%M:%S') and (not temInativadoDepois)):
                                                                        print(f'Conflito com o próximo horário ({consultasA[iConsultas][opcaoEdit][0][11:]} - {consultasA[iConsultas][opcaoEdit][1][11:]}), por favor apague-o ou confira o novo horário inserido.')
                                                                        continue
                                                                    elif(not novoComeco.time() >= dt.time(9, 0) or not novoFim.time() >= dt.time(9, 0)):
                                                                        print(f'Horário antes do começo do expediente da clínica!')
                                                                        continue
                                                                    elif(not novoFim.time() <= dt.time(18, 0) or not novoComeco.time() < dt.time(18, 0)):
                                                                        print(f'Horário após o fim do expediente da clinica!')
                                                                        continue
                                                                    elif not(novoComeco.time() <= dt.time(11, 15) and novoFim.time() <= dt.time(11,30) or novoComeco.time() >= dt.time(13, 30) and novoFim.time() >= dt.time(13,45)):
                                                                        print('Consulta no horário de almoço! Revise o horário.')
                                                                        continue
                                                                    else:
                                                                        sqlUpdate = 'update agenda set dataInicioConsulta = ?, dataFimConsulta = ? where dataInicioConsulta = ? and id_medico = ?'     
                                                                        valuesUpdate = (datetime.strftime(novoComeco, '%Y-%m-%d %H:%M:%S'), datetime.strftime(novoFim, '%Y-%m-%d %H:%M:%S'), consultasA[iConsultas][opcaoEdit-1][0], usuarioLogado[0])
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
                        print()
                        header('Este horário já possui um paciente agendado, ou foi inativado, então não pode ser editado.')
                        print()
                        continue
            elif estado == 'exibindo': 
                input('Pressione qualquer tecla para continuar...')
            elif estado == 'marcando': 
                print()
                horarioEscolhido = leiaInt('Insira um dos horários listados para consultar, ou 0 para sair: ')
                sqlAgendaPaciente = 'update agenda set id_paciente = ? where dataInicioConsulta = ? and id_medico = ?'
                if(horarioEscolhido == 0):
                    continue
                if(horarioEscolhido in disponiveis):
                    for dia in consultasA: #itera os dias das consultas para encontrar a que tem o dia que o paciente selecionou lá no calendário (opcao)
                        if(str(dia[0][0][8:10]) == str(opcao) or str(dia[0][0][8:10]) == '0' + str(opcao)):
                            valuesAgendaPaciente = usuarioLogado[0], dia[horariosConsulta[horarioEscolhido-1]][0], id_medico
                            cursor.execute(sqlAgendaPaciente, valuesAgendaPaciente)
                            banco.commit()
                    print(term.clear)
                    header('Consulta agendada com sucesso!')
                    break

        else:
            problema = 'Insira um dia que está agendado.'

# -- FIM AGENDA -- #

if __name__ == '__main__':
    print('Por favor execute a partir do arquivo "clinica.py".')
    exit()