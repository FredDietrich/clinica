def cadastros():

    lista_de_regioes_crm = ['/AC','/AL','/AP','/AM','/BA','/CE','/DF',
                            '/ES','/GO','/MA','/MT','/MS','/MG','/PA',
                            '/PB','/PR','/PE','/PI','/RJ','/RN','/RS',
                            '/RO','/RR','/SC','/SP','/SE','/TO']

    banco_de_dados_pacientes = [] #Dados dos clientes
    nome_paciente = None
    email_paciente = None
    cpf = None
    telefone_paciente = None
    """
                    Banco de dados Paciente
     _________ _________ _________ _____________ _________
    | Médico1 | Médico2 | Médico3 | .......     | Médico4 |
    |_________|_________|_________|_____________|_________|
   0| Nome    | Nome    | Nome    | .......     | Nome    |
    |_________|_________|_________|_____________|_________|
   1| CPF     | CPF     | CPF     | .......     | CPF     |
    |_________|_________|_________|_____________|_________|
   2|Telefone |Telefone |Telefone | .......     |Telefone |
    |_________|_________|_________|_____________|_________|
   3|Email    |Email    |Email    | .......     |Email    |
    |_________|_________|_________|_____________|_________|
    tabela de confecção da lista para orientação..."""

    banco_de_dados_medicos = [] #Dados dos Médicos
    nome_medico = None
    email_medico = None
    crm = None
    telefone_medico = None
    """
                    Banco de dados Médico
     _________ _________ _________ _____________ _________
    | Médico1 | Médico2 | Médico3 | .......     | Médico4 |
    |_________|_________|_________|_____________|_________|
   0| Nome    | Nome    | Nome    | .......     | Nome    |
    |_________|_________|_________|_____________|_________|
   1| CRM     | CRM     | CRM     | .......     | CRM     |
    |_________|_________|_________|_____________|_________|
   2|Telefone |Telefone |Telefone | .......     |Telefone |
    |_________|_________|_________|_____________|_________|
   3|Email    |Email    |Email    | .......     |Email    |
    |_________|_________|_________|_____________|_________|
    tabela de confecção da lista para orientação..."""
    

    crm_referência = "00000000/PP"
    cpf_referencia = "000.000.000-00"
    telefone_referencia = "(51)988888888"

    def entradaDeDados():
        condicao = str(input('\nOlá deseja realizar um cadastro? ')).strip().upper()[0]
        if condicao == "S":
            medico_paciente = str(input("\nVocê é médico ou paciente? ")).strip().upper()[0]
            if medico_paciente == "M":
                cadastroMedico()
            elif medico_paciente == "P":
                cadastroPaciente()

    def cadastroMedico(): # funcional
        condicao = 0
        #Nome do Médico
        while condicao == 0:
            nome_medico = str(input('\nDigite o seu nome completo:   \nOu deixe em branco para sair... '))
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
            crm = str(input('\nDigite seu CRM! "Exemplo 00000000/RS"  \nOu deixe em branco para sair... ')).strip().upper()
            if crm == "":
                condicao = 1
                break
            if crm.isdigit() == True:# verifica se o CRM não é apenas uma sequência de numeros
                erro_crm()
            if crm[-3:] in lista_de_regioes_crm: # pega os ultimos 3 digitos e busca na lista (lista_de_regioes_crm)
                if len(crm[:-3]) <= len(crm_referência[:-3]): # pega todos digitos antes dos 3 ultimos e faz a comparacao com a quantidade de valores existentes no crm_referência
                    if crm[:-3].isdigit() == True : #verifica se os valores antes do 3 ultimos sao numeros
                        print('\nCRM ACEITO!')
                        #segue com cadastro de médico
                        break
                    erro_crm()
                erro_crm()
            erro_crm()

        #Telefone do Médico
        while condicao == 0:
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
            break

        # Email do Médico
        while condicao == 0:
            email_medico = str(input('\nDigite seu email: "Exemplo: nome@domínio.com.br"\nOu deixe em branco para sair... '))
            if email_medico == "":
                condicao = 1
                break
            if "@" in email_medico: #Verifica se tem "@" no email digitado
                print('deu certo email')
                break
            else:
                erroEmail()

        #Salvando os dados do cadastro no banco de dados dos medicos
        while condicao == 0:
            banco_de_dados_medicos.append([nome_medico,crm,telefone_medico,email_medico])
            for i in range(len(banco_de_dados_medicos)):
                print(banco_de_dados_medicos[i])
            break
        entradaDeDados()

    def cadastroPaciente(): # Funcional
        condicao = 0
        #Nome do Paciente
        while condicao == 0:
            nome_paciente = str(input('\nDigite o seu nome completo:   \nOu deixe em branco para sair... '))
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
                    #print(cpf)
            if len(cpf) != 11:
                erroCPF()
                #print('1')
                continue
            """------------Abaixo os calculos de validação do CPF--------------"""
            for i in range(len(cpf[:-2])):
                produto1_cpf += int(cpf[i])*(10-i) 
                #print(produto1_cpf)
            produto1_cpf = 11 - (produto1_cpf % 11)
            #print(produto1_cpf)
            for i in range(len(cpf[:-2])):
                produto2_cpf += int(cpf[i])*(11-i)
                #print(produto2_cpf)
            produto2_cpf = 11 -((produto2_cpf+(produto1_cpf*2)) % 11)
            #print(produto2_cpf)
            if produto2_cpf > 9:
                produto2_cpf = 0
                #print('produto = 0')
            #print(produto2_cpf)
            if str(cpf[-2:]) == (str(produto1_cpf) + str(produto2_cpf)):
                #print('CPF valido!!!')
                break
            continue



        #Telefone do Paciente
        while condicao == 0:
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
            break

        # Email do Paciente
        while condicao == 0:
            email_paciente = str(input('\nDigite seu email: "Exemplo: nome@domínio.com.br"\nOu deixe em branco para sair... '))
            if email_paciente == "":
                condicao = 1
                break
            if "@" in email_paciente: #Verifica se tem "@" no email digitado
                print('deu certo email')
                break
            else:
                erroEmail()
        #Salvando os dados do cadastro no banco de dados dos Pacientes
        while condicao == 0:
            banco_de_dados_pacientes.append([nome_paciente,cpf,telefone_paciente,email_paciente])
            for i in range(len(banco_de_dados_pacientes)):
                print(banco_de_dados_pacientes[i])
            break
        entradaDeDados()
    """ -------------------Def's de erro!!!------------------------"""
    def erroNome():
        print('\nDigite um nome válido!')

    def erroCPF():
        print('\nDigite um CPF valido!')
    
    def erro_crm():
        print('\nDigite um CRM válido!')
        
    def erroTelefone():
        print('\nDigite um telefone Válido!')

    def erroEmail():
        print('\nDigite um E-Mail Válido!')


    entradaDeDados()

cadastros()

#atualização 19/09 | 22:55