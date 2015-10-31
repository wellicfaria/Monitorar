# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

#Importação de Bibliotecas
from datetime import date #Manipulação de datas

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if auth.user:
        redirect(URL(c='default', f='portal'))


    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

@auth.requires_login()
def portal():
    #formulário para setar o filto para aprententar os dados
    atual = date.today()
    final = date.fromordinal(atual.toordinal()-7) 
    leituras=db((db.leituras.data_leitura<=atual) & (db.leituras.data_leitura>=final) & (db.leituras.hardware.cidade==auth.user.cidade)).select()
    form = SQLFORM.factory(
        Field('date_atual', default=atual ,requires=[IS_NOT_EMPTY(),IS_DATE()]),
        Field('date_final', default=final ,requires=[IS_NOT_EMPTY(),IS_DATE()])
        )

    #Grafico de linha
    dados_do_grafico_metano=[]
    dados_do_grafico_monoxido_de_carbono=[]
    for dado in leituras:
        aux = []
        aux.append(dado.hora_leitura)
        aux.append(dado.valor)
        if dado.sensor.tipo_sensor.upper() =='METANO':
            dados_do_grafico_metano.append(aux)
        if dado.sensor.tipo_sensor.upper() =='MONOXIDO DE CARBONO':
            dados_do_grafico_monoxido_de_carbono.append(aux)

    grafico_metano=XML(dados_do_grafico_metano)
    grafico_monoxido_de_carbono=XML(dados_do_grafico_monoxido_de_carbono)

    if form.process().accepted:
        response.flash = 'form accepted'
        leituras=db((db.leituras.data_leitura<=form.vars.date_atual) & (db.leituras.data_leitura>=form.vars.date_final)).select()
    elif form.errors:
        response.flash = 'form has errors'



    nome=db(db.auth_user.id==auth.user).select().last()

    #retorno
    
    return {'nome':nome.first_name,'form':form,'leituras':leituras,'grafico_metano':grafico_metano,'grafico_monoxido_de_carbono':grafico_monoxido_de_carbono}



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    form=auth()
    #form.custom.widget.email.update(_placeholder="E-mail...")
    #form.custom.widget.password.update(_placeholder="Senha...")
   
    return {'form':form}


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def salvar_dados():
    # Padrão da URL: 
    #               /monitorart/default/salvar_dados?senha=1584as&idh=1&ids=2&valor=98&data=25/12/2015&hora=15:25
    # Respostas:
    #   0 - Erro não determinado
    #   1 - Hardware não encontrado no banco de dados
    #   2 - Parâmetro via URL estão incorretos
    #   3 - Senha do Hardware será incorreta
    #   4 - Inseriu no banco
    #   5 - Erro ao inserir no banco


    resposta=HTML(BODY('<erro>', XML('<p>0</p>')))
    dados=request.vars
    print(dados.keys())
    hardware=db(db.hardwares.id==dados['idh']).select().first()
    if(hardware):
        if(['hora', 'senha', 'idh', 'valor', 'data', 'ids']==dados.keys()):
            if(dados['senha']==hardware.senha):
                insersao=db.leituras.insert(
                    hardware=dados['idh'],
                    sensor=dados['ids'],
                    valor=dados['valor'],
                    data_leitura=dados['data'],
                    hora_leitura=dados['hora']
                    )
                if(insersao>0):
                    resposta=HTML(BODY('<ok>', XML('<p>4</p>')))
                else:
                    resposta=HTML(BODY('<erro>', XML('<p>5</p>')))
            else:
                resposta=HTML(BODY('<erro>', XML('<p>3</p>')))
        else:
            resposta=HTML(BODY('<erro>', XML('<p>2</p>'))) 
    else:
         resposta=HTML(BODY('<erro>', XML('<p>1</p>')))

    return resposta







