import string

from flask import render_template, request, redirect, url_for, flash
from sitecomunidade import app, database, bcrypt
from sitecomunidade.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from sitecomunidade.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
from datetime import timedelta
import secrets
import os
from PIL import Image


redirects_seguros = ['/', '/contato', '/usuarios', '/login', '/sair', '/perfil', '/post/criar']


@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
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
            login_user(usuario, remember=form_login.lembrar_dados.data, duration=timedelta(days=365))
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
    ''' # Implementei uma versão que utiliza o email como nome de arquivo,
    # para substituir o arquivo toda vez que trocar a foto e ocupar menos espaço no server.
    # Assim cada usuário só terá uma foto no server.
    # As linhas comentadas são a solução original

    # codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    # nome_arquivo = nome + codigo + extensao
    mail = str(current_user.email)
    nome2 = ''
    for i, l in enumerate(mail):
        nome2 += chr(ord(l) + (10 - i))
    mail = ''
    for l in nome2:
        if l in string.punctuation:
            mail += 'z'
        else:
            mail += l
    '''

    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = codigo + extensao
    # nome_arquivo = mail + extensao
    print(nome_arquivo)
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    imagem_reduzida.save(caminho_completo)

    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if campo.name.startswith('curso_') and campo.data:
            lista_cursos.append(campo.label.text)

    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editarperfil = FormEditarPerfil()

    if 'botao_submit_editarperfil' in request.form:
        if form_editarperfil.validate_on_submit():
            current_user.username = form_editarperfil.username_editarperfil.data
            current_user.email = form_editarperfil.email_editarperfil.data

            if form_editarperfil.foto_perfil.data:
                foto_antiga = current_user.foto_perfil

                # Excluir foto antiga
                if foto_antiga != 'default.jpg':
                    arquivo_antigo = os.path.join(app.root_path, 'static/fotos_perfil', foto_antiga)
                    if os.path.isfile(arquivo_antigo):
                        os.remove(arquivo_antigo)

                nome_imagem = salvar_imagem(form_editarperfil.foto_perfil.data)
                current_user.foto_perfil = nome_imagem

            current_user.cursos = atualizar_cursos(form_editarperfil)

            database.session.commit()
            flash(f'Perfil atualizado com sucesso', 'alert-success')
            return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form_editarperfil.username_editarperfil.data = current_user.username
        form_editarperfil.email_editarperfil.data = current_user.email

        # Utilizei essa lógica para carregar os dados de cursos na atualização de perfil
        for campo in form_editarperfil:
            if campo.name.startswith('curso_') and campo.label.text in current_user.cursos:
                campo.data = True

    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form_editarperfil=form_editarperfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criarpost = FormCriarPost()

    if 'botao_submit_criarpost' in request.form:
        if form_criarpost.validate_on_submit():
            post = Post(autor=current_user, titulo=form_criarpost.titulo.data, corpo=form_criarpost.corpo.data)
            database.session.add(post)
            database.session.commit()
            flash('Post criado com sucesso', 'alert-success')
            return redirect(url_for('home'))

    return render_template('criarpost.html', form_criarpost=form_criarpost)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form_editarpost = FormCriarPost()

        if request.method == 'GET':
            form_editarpost.titulo.data = post.titulo
            form_editarpost.corpo.data = post.corpo
        elif 'botao_submit_criarpost' in request.form:
            if form_editarpost.validate_on_submit():
                post.titulo = form_editarpost.titulo.data
                post.corpo = form_editarpost.corpo.data
                database.session.commit()
                flash('Post atualizado com sucesso', 'alert-success')
                return redirect(url_for('home'))

    else:
        form_editarpost = None
    return render_template('post.html', post=post, form_editarpost=form_editarpost)
