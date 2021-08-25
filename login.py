import getpass
def main():
    print('FACA LOGIN OU DEIXE OS CAMPOS EM BRANCO PARA RETORNAR AO MENU INICIAL')
    email = input('EMAIL: ')
    senha = getpass.getpass(prompt = 'SENHA:')
    if(email != '' and senha != ''):
        print('deu')
    else:
        print('de novo')