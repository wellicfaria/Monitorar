# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if auth.user:
        print("tem usuario")


    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


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
    print(form.vars)
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







