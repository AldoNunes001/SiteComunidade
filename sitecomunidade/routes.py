from flask import render_template, request, redirect, url_for, flash
from sitecomunidade import app, database, bcrypt
from sitecomunidade.forms import FormLogin, FormCriarConta, FormEditarPerfil
from sitecomunidade.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required
from datetime import timedelta
import secrets
import os
from PIL import Image

lista_usuarios = ['Lira', 'João', 'Alon', 'Alessandra', 'Amanda']
redirects_seguros = ['/', '/contato', '/usuarios', '/login', '/sair', '/perfil', '/post/criar']


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if 'botao_submit_login' in request.form:

        # print(form_login.email_login.data)
        if form_login.validate_on_submit():
            usuario = Usuario.query.filter_by(email=form_login.email_login.data).first()
            # print(f'Usuário: {usuario}')

            # Essas condições às vezes funcionam e às vezes não
            if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'), form_login.senha.data):  # encode('utf-8')
                login_user(usuario, remember=form_login.lembrar_dados.data, duration=timedelta(days=365))
                # Fez login com sucesso
                flash(f'Login feito com sucesso no e-mail: {form_login.email_login.data}', 'alert-success')

                par_next = request.args.get('next')
                if par_next in redirects_seguros:
                    return redirect(par_next)
                else:
                    return redirect(url_for('home'))

            elif not usuario:
                # print('Usuário não encontrado')
                flash(f'Falha no login. E-mail não cadastrado.', 'alert-danger')

            else:
                # print('Senha incorreta')
                flash(f'Falha no login. Senha incorreta.', 'alert-danger')

    if 'botao_submit_criarconta' in request.form:
        if form_criarconta.validate_on_submit():
            senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')  # .decode('utf-8')
            usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email_criarconta.data,
                              senha=senha_cript)
            database.session.add(usuario)
            database.session.commit()
            # Criou conta com sucesso
            flash(f'Conta criada com sucesso para o e-mail: {form_criarconta.email_criarconta.data}', 'alert-success')
            return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    imagem_reduzida.save(caminho_completo)

    return nome_arquivo


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editarperfil = FormEditarPerfil()

    if 'botao_submit_editarperfil' in request.form:
        if form_editarperfil.validate_on_submit():
            current_user.username = form_editarperfil.username_editarperfil.data
            current_user.email = form_editarperfil.email_editarperfil.data

            if form_editarperfil.foto_perfil.data:
                nome_imagem = salvar_imagem(form_editarperfil.foto_perfil.data)
                current_user.foto_perfil = nome_imagem

            database.session.commit()
            flash(f'Perfil atualizado com sucesso', 'alert-success')
            return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form_editarperfil.username_editarperfil.data = current_user.username
        form_editarperfil.email_editarperfil.data = current_user.email

    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form_editarperfil=form_editarperfil)


@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')
