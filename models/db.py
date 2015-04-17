# -*- coding: utf-8 -*-
from gluon.storage import Storage

config = Storage(
    db=Storage(),
)

#Conexão com o Banco de Dados
config.db.uri = "postgres:pg8000://matheus:123456@localhost/sys_chat"
db = DAL(**config.db)

from gluon.tools import Auth

#Configuração Auth
auth = Auth(db, controller="home",function="login")
auth.settings.formstyle = "divs"
auth.settings.login_next = URL(a='teste_chat', c='home', f='index')
auth.settings.remember_me_form = False
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False

#Mensagens de Erro 
auth.messages.logged_in = 'Bem Vindo' 
auth.messages.access_denied = 'Acesso negado! Contate o administrador'
auth.messages.invalid_username = 'Usuario Inválido '
auth.messages.invalid_login = 'Usuario ou Senha Inválidos'
auth.messages.invalid_password = 'Senha Inválida'
auth.messages.login_button = "Entrar"
auth.messages.label_email = 'E-mail'
auth.messages.label_password = 'Password'


