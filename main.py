from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormLogin, FormCriarConta

app = Flask(__name__)

lista_usuarios = ['Lira', 'João', 'Alon', 'Alessandra', 'Amanda']

app.config['SECRET_KEY'] = '67049ce9faacc9f10c352d4bfb70cdbb'  # utilizei o secrets.token_hex(16)


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
            # Fez login com sucesso
            flash(f'Login feito com sucesso no e-mail: {form_login.email_login.data}', 'alert-success')
            return redirect(url_for('home'))

    if 'botao_submit_criarconta' in request.form:
        if form_criarconta.validate_on_submit():
            # Criou conta com sucesso
            flash(f'Conta criada com sucesso para o e-mail: {form_criarconta.email_criarconta.data}', 'alert-success')
            return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


if __name__ == '__main__':
    app.run(debug=True)
