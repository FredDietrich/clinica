from modulos import *
from time import sleep

# função que busca o menu e exibe
while True:
    resposta = menu(['Cadastros','Agendar','Consultar','Arquivos','Sair']) #lista das opçoes do menu principal
    if resposta == 1:
        while True:
            resposta = cadastro(['Editar','Excluir','Sair']) # listas as opções do submenu de cadastro
            if resposta == 1:
                header('Editando...')
            elif resposta ==2:
                header('Excluindo...')
            elif resposta == 3:
                header('Saindo...')            
            else:
                header('Opção Invalida')                                   

    elif resposta == 2:
        resposta = agenda(['Agendar','Listar','Editar','Excluir','Sair']) # listas as opções do submenu da agenda
        if resposta == 1:
            header('Agendando...')
        elif resposta == 2:
            header('Listando...')
        elif resposta == 3:
            header('Editando...')
        elif resposta == 4:
            header('Excluindo')
        elif resposta == 5:
            header('Saindo..')
        else:
            header('Opção Invalida!')              

    elif resposta == 3:
        resposta = consultar(['Consultar', 'Sair']) # listas as opções do submenu consultar
        if resposta == 1:
            header('Consultando...')
        elif resposta == 2:
            header('Saindo...')
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
        else:
            header('Opção Invalida!')           
        
    elif resposta == 5:
        header('Saindo... Good Bye!')
        exit()
    else:
        header('Digite uma opção valida!')
    sleep(2)        
