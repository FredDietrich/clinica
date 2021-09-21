#modulos.py
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
def agenda(lista):
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
