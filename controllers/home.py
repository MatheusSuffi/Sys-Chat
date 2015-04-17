# -*- coding: utf-8 -*-
from gluon.contrib.websocket_messaging import websocket_send
import datetime
@auth.requires_login()
def index():
	db(db.amigos.nome == auth.user.first_name).update(status='Disponivel')
	user_amigos = db(db.amigos.nome == auth.user.first_name).select().as_list()
	if user_amigos == []:
		db.amigos.insert(id_user=auth.user.id,nome=auth.user.first_name,status='Disponivel')

	session.usuario_logado = []
	session.usuario_logado = [auth.user.first_name]
	session.usuario_logado += [auth.user.id]
	tipoMsg = 'atualizaUsuario'
	socketAtualizaUsuario(tipoMsg)
	return response.render('home/index.html')

@auth.requires_login()
def atualiza():
	user_amigos = db(db.amigos.nome == auth.user.first_name).select().as_list()
	if user_amigos == []:
		db.amigos.insert(id_user=auth.user.id,nome=auth.user.first_name,status='Disponivel')
	tipoMsg = 'atualizaUsuario'
	socketAtualizaUsuario()

	return response.render('home/index.html')

def login():
	if auth.user is None:
		form = auth.login()
		form.element(_name='email')['_class'] = "form-control"
		form.element(_name='password')['_class'] = "form-control"
		form.element(_name='email')['_placeholder'] = 'E-mail'
		form.element(_name='password')['_placeholder'] = 'Senha'
		form.element(_type='submit')['_class'] = "btn btn-outline btn-primary btn-lg btn-block"
		return response.render('home/login.html', form=form)
	else:
		return redirect(URL('index'))

def registro():
	return auth.register()

@auth.requires_login()
def usuarios_online():
	amigos = db(db.amigos.nome != auth.user.first_name).select()
	estado = db(db.amigos.id_user == auth.user.id).select('status')
	return response.render('sub_view/usuarios_online.html',ativos=amigos,status=estado)

@auth.requires_login()
def get_chat():
	chat = db(db.chat.id_user == auth.user.id).select()
	return response.render('sub_view/chat.html',chat=chat)

@auth.requires_login()
def logout():
	db(db.amigos.id_user == auth.user.id).update(status = 'Offline')
	tipoMsg = 'atualizaUsuario'
	socketAtualizaUsuario(tipoMsg)
	auth.logout()

@auth.requires_login()
def retira_usuario():
	query = (db.amigos.nome == auth.user.first_name)
	db(db.amigos.id_user == auth.user.id).update(status = 'Offline')
	tipoMsg = 'atualizaUsuario'
	socketAtualizaUsuario(tipoMsg)
	return redirect(URL('index'))

@auth.requires_login()
def trocar_status():
	db(db.amigos.id_user == auth.user.id).update(status = request.vars['status'])
	tipoMsg = 'atualizaUsuario'
	socketAtualizaUsuario(tipoMsg)
	return True

#Funções Sockets
#Função socketAtualizaUsuario para atualizar o frame de Usuarios Logados
@auth.requires_login()	
def socketAtualizaUsuario(tipoMsg=""):
	websocket_send('http://127.0.0.1:8888',tipoMsg,'chat','conversa')

@auth.requires_login()
def abrir_conversa():
	id_envio = request.vars['id']
	usuario_envio = db(db.auth_user.id ==  id_envio).select()
	if usuario_envio.as_list() != []:
		session.id_envio = id_envio
		session.usuario_envio=usuario_envio
	mensagens = db(((db.chat.id_user == session.id_envio) | (db.chat.id_recebido == session.id_envio)) & ((db.chat.id_user == auth.user.id) | (db.chat.id_recebido == auth.user.id))).select(orderby=db.chat.data_envio)
	return response.render('sub_view/chat.html',mensagens=mensagens,usuario_envio=session.usuario_envio)
@auth.requires_login()
def envia_mensagem():
	mensagem = request.vars['mensagem']
	id_envio = request.vars['id_envio']
	db.chat.insert(nome=auth.user.first_name,mensagem=mensagem,id_user=auth.user.id,id_recebido=id_envio,data_envio=datetime.datetime.now())
	tipoMsg = 'atualizaChat'
	socketAtualizaUsuario(tipoMsg)

@auth.requires_login()
def recebe_mensagem():
	dados = db(db.mensagem).select(orderby=~db.mensagem.data_envio)
	return response.render('sub_view/linha_tempo.html',dados=dados)

@auth.requires_login()
def nova_publicacao():
	dados = request.vars['mensagem']
	db.mensagem.insert(mensagem = dados,nome = auth.user.first_name, id_user = auth.user.id, data_envio = datetime.datetime.now())
	tipoMsg = 'atualizaLinhadoTempo'
	socketAtualizaUsuario(tipoMsg)
