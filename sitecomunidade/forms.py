from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sitecomunidade.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email_criarconta = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    # A função 'validate_on_submit' do FlaskForm executa automaticamente qualquer função que começa com 'validate_'
    # O nome da função tem que começar com 'validate_' + o nome da variável para validar
    # Estava tentando usar a função com o nome 'validate_email' e estava dando erro
    def validate_email_criarconta(self, email_criarconta):
        usuario = Usuario.query.filter_by(email=email_criarconta.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastra-se com outro e-mail ou faça login para continuar.')


class FormLogin(FlaskForm):
    email_login = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Manter-me conectado')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username_editarperfil = StringField('Nome de Usuário', validators=[DataRequired()])
    email_editarperfil = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    curso_excel = BooleanField('Excel')
    curso_powerbi = BooleanField('PowerBI')
    curso_python = BooleanField('Python')
    curso_htmlcss = BooleanField('HTML/CSS')
    curso_javascript = BooleanField('Javascript')
    curso_sql = BooleanField('SQL')
    curso_cienciadedados = BooleanField('Ciência de Dados')

    botao_submit_editarperfil = SubmitField('Salvar')

    def validate_email_editarperfil(self, email_editarperfil):
        # Só faz validação se ele mudou o email
        if current_user.email != email_editarperfil.data:
            usuario_editarperfil = Usuario.query.filter_by(email=email_editarperfil.data).first()
            if usuario_editarperfil:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail.')
