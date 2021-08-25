#!/usr/bin/env python3
import getpass
import login, cadastro
print("""
**********************************************************************
**                                                                  **
**      BEM VINDO AO SISTEMA DE CLINICA MEDICA POR TECH CONNECT     **
**                                                                  **
**********************************************************************
""")
print("""
OPCOES:
(1) LOGIN
(2) CADASTRO
(3) SAIR
""")
escolhaLogin = int(input('Insira a opcao:'))
if(escolhaLogin == 1):
    login.main()
elif(escolhaLogin == 2):
    cadastro.main()
elif(escolhaLogin == 3):
    exit()
