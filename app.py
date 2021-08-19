from flask import Flask, render_template, request, url_for, redirect, session
import pymongo, os, bcrypt, mysql.connector
#crypto
salt = bcrypt.gensalt()

#mysql setup
mysqlDB = mysql.connector.connect(
    host='localhost',
    user='',
    password='',
    database='clinica'
)
cursor = mysqlDB.cursor()


#functions
def authUser(email, password):
    userSelect = "SELECT * FROM usuario WHERE email = %s"
    val = (email,)
    cursor.execute(userSelect, val)
    res = cursor.fetchone()
    if(res != None):
        sqlPessoa = 'SELECT * FROM paciente where id_usuario = %s'
        valPessoa = (res[0],)
        cursor.execute(sqlPessoa,valPessoa)
        resPessoa = cursor.fetchone()
        if(resPessoa != None):
            session['profissao'] = 'paciente'
            session['loggeduser'] = resPessoa
        else:
            sqlMedico = 'SELECT * FROM medico where id_usuario = %s'
            valMedico = (res[0],)
            cursor.execute(sqlMedico,valMedico)
            resMedico = cursor.fetchone()
            session['profissao'] = 'medico'
            session['loggeduser'] = resMedico
            print(resMedico)
        if(bcrypt.checkpw(password.encode(), res[3].encode())):
            return redirect('/')
        else:
            return redirect('/login?error=checkpassword')
    else:
        return redirect('/login?error=userdoesntexist')
#flask routing
app = Flask(__name__)
app.secret_key = b'\xca\x88\x1fTmh!\xd4\xd8\xb5\x02D7j\xb4G'
@app.route('/')
def index():
    try:
        return render_template('index.jinja', user=session['loggeduser'], profissao=session['profissao'])
    except:
        return render_template('index.jinja')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return authUser(request.form['email'], request.form['password'])
    else:
        if(request.args.get('error','') != ''): 
            return render_template('login.jinja', error=request.args.get('error', ''))
        else:
            return render_template('login.jinja')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        encPass = bcrypt.hashpw(request.form['password'].encode(), salt).decode('utf-8')
        insertsUsuario = 'INSERT INTO usuario VALUES(null, %s, %s, %s)'
        valUser = (request.form['name'], request.form['email'], encPass)
        print(valUser)
        cursor.execute(insertsUsuario, valUser)
        print(cursor.statement)
        if(request.form['crm'] == ''):
            insertsPaciente = 'INSERT INTO paciente VALUES(null, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            valuesPaciente = (request.form['name'], request.form['cpf'], request.form['email'], request.form['rua'], request.form['ncasa'], request.form['cep'], request.form['bairro'], request.form['telefone'], cursor.lastrowid)
            cursor.execute(insertsPaciente, valuesPaciente)
        else:
            insertsMedico = 'INSERT INTO medico VALUES(null, %s, %s, %s, %s, %s, %s)'
            valuesMedico = (request.form['name'], request.form['cpf'], request.form['crm'], request.form['email'], request.form['telefone'], cursor.lastrowid)
            cursor.execute(insertsMedico, valuesMedico)
        mysqlDB.commit()
        return redirect('/login')
    else:
        return render_template('register.jinja')
@app.route('/logout')
def logout():
    session.pop('loggeduser', None)
    session.pop('profissao', None)
    return redirect('/')