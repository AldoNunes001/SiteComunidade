from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return '''<h1>Hello, world!</h1>
            <p>O site está no ar!</p>'''


@app.route('/contato')
def contato():
    return 'Qualquer dúvida mande um e-mail para aldonunes001@gmail.com'


if __name__ == '__main__':
    app.run(debug=True)
