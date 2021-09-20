import sqlite3

banco = sqlite3.connect('clinica.db')
cursor = banco.cursor()
cursor.execute('drop table if exists agenda;')
cursor.execute('''
CREATE TABLE IF NOT EXISTS agenda(
  id_agenda integer primary key AUTOINCREMENT NOT NULL ,
  id_paciente integer NULL,
  id_medico integer NULL,
  dataInicioConsulta DATETIME NULL,
  dataFimConsulta DATETIME NULL);
''')
banco.commit()
