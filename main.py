from flask import Flask, render_template, url_for

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


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
