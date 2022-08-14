from flask import render_template, request, redirect, url_for, flash
from sitecomunidade import app, database, bcrypt
from sitecomunidade.forms import FormLogin, FormCriarConta
from sitecomunidade.models import Usuario
from flask_login import login_user

lista_usuarios = ['Lira', 'João', 'Alon', 'Alessandra', 'Amanda']


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if 'botao_submit_login' in request.form:
        if form_login.validate_on_submit():
            usuario = Usuario.query.filter_by(email=form_login.email_login.data).first()
            if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'), form_login.senha.data):
                login_user(usuario, remember=form_login.lembrar_dados.data)
                # Fez login com sucesso
                flash(f'Login feito com sucesso no e-mail: {form_login.email_login.data}', 'alert-success')
                return redirect(url_for('home'))
            else:
                flash(f'Falha no login. E-mail ou senha incorretos.', 'alert-danger')

    if 'botao_submit_criarconta' in request.form:
        if form_criarconta.validate_on_submit():
            senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
            usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email_criarconta.data,
                              senha=senha_cript)
            database.session.add(usuario)
            database.session.commit()
            # Criou conta com sucesso
            flash(f'Conta criada com sucesso para o e-mail: {form_criarconta.email_criarconta.data}', 'alert-success')
            return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)
