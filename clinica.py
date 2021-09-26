#!/usr/bin/env python3
from modulos import *
from time import sleep

# função que busca o menu e exibe
def clinica(logado=False):
    if not logado:
        login(clinica)
    else:
        while True:
            header(f'{term.green}Bem vindo a clínica, {logado[1]}!{term.normal}')
            resposta = menu(['Cadastros','Agendar','Consultar','Arquivos','Sair']) #lista das opçoes do menu principal
            if resposta == 1:
                cadastros()                                

            elif resposta == 2:
                resposta = menuAgenda(['Criar agenda','Listar','Editar','Sair']) # listas as opções do submenu da agenda
                if resposta == 1:
                    header('Acessando criação de agenda...')
                    agenda('criando')
                elif resposta == 2:
                    header('Listando...')
                    agenda('exibindo')
                    continue
                elif resposta == 3:
                    header('Acessando edição de agenda...')
                    agenda('editando')
                elif resposta == 4:
                    header(f'{term.red}Saindo.. {term.normal}')
                    continue
                else:
                    header('Opção Invalida!')              

            elif resposta == 3:
                resposta = consultar(['Consultar', 'Sair']) # listas as opções do submenu consultar
                if resposta == 1:
                    header('Consultando...')
                elif resposta == 2:
                    header('Saindo...')
                    break
                else:
                    header('Opção Invalida!')        

            elif resposta == 4:
                resposta = arquivos(['Anexar arquivos', 'Download de Arquivos','Sair']) # listas as opções do submenu de arquivos
                if resposta == 1:
                    header('Arquivando...')
                elif resposta == 2:
                    header('Fazendo downloading...')
                elif resposta == 3:
                    header('Saindo...')
                    break
                else:
                    header('Opção Invalida!')           
                
            elif resposta == 5:
                #header('Saindo... Good Bye!')
                respostaSaida = leiaInt('Quer sair do sistema ou do usuário? [1 - Usuario, 2 - Sistema]: ')
                if(respostaSaida == 1):
                    clinica()
                else:
                    exit()
            else:
                header('Digite uma opção valida!')
            sleep(2)        
clinica()