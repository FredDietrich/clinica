import sqlite3

banco = sqlite3.connect('clinica.db')
cursor = banco.cursor()
cursor.execute('drop table if exists agenda;')
cursor.execute('drop table if exists paciente;')
cursor.execute('drop table if exists medico;')
cursor.execute('''
CREATE TABLE IF NOT EXISTS agenda(
  id_agenda integer primary key AUTOINCREMENT NOT NULL ,
  id_paciente integer NULL,
  id_medico integer NULL,
  dataInicioConsulta DATETIME NULL,
  dataFimConsulta DATETIME NULL);
''')

cursor.execute('''
CREATE TABLE if not exists paciente (
    id_paciente integer primary key AUTOINCREMENT NOT NULL,
    nome varchar(255) not null,
    cpf nchar(11) not null unique,
    telefone char(20),
    email varchar(255) not null,
    senha varchar(16)
);
''')
cursor.execute('''
CREATE TABLE if not exists medico(
  id_medico integer primary key AUTOINCREMENT NOT NULL, 
  nome varchar(255) not null,
  crm varchar(20),
  telefone varchar(20),
  email varchar(255),
  senha varchar(16)
);
''')
banco.commit()
