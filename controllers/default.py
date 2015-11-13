# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

#Importação de Bibliotecas
from datetime import date
from datetime import datetime #Manipulação de datas

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
    
    usuario=db(db.auth_user.id==auth.user).select().last()
    
    if len(request.args)==0:
        atual = date.today()
        final = date.fromordinal(atual.toordinal()-7)
    else:

        atual = datetime.strptime(request.args[0], '%Y-%m-%d').date()
        final = datetime.strptime(request.args[1], '%Y-%m-%d').date() #Convertendo para data

    leituras=db((db.leituras.data_leitura<=atual) & (db.leituras.data_leitura>=final) ).select()
    datas_de_leituras= db((db.leituras.data_leitura<=atual) & (db.leituras.data_leitura>=final) ).select(db.leituras.data_leitura, distinct=True)

    
  
    form = SQLFORM.factory(
        Field('date_atual', type='date'  ,default=atual ,requires=[IS_NOT_EMPTY(),IS_DATE(format=T('%d/%m/%Y'))]),
        Field('date_final', type='date' ,default=final ,requires=[IS_NOT_EMPTY(),IS_DATE(format=T('%d/%m/%Y'))])
        )

    #Grafico de linha
    dados_do_grafico_metano=[]
    dados_do_grafico_metano.append(['Hora','Valor'])
    
    dados_do_grafico_monoxido_de_carbono=[] 
    dados_do_grafico_monoxido_de_carbono.append(['Hora','Valor'])


    for dado in leituras:
        aux = []
        aux.append(dado.data_leitura.strftime("%d/%m/%y")+" "+dado.hora_leitura.strftime("%H:%M:%S"))
        aux.append(dado.valor)
        if dado.sensor.tipo_sensor.upper() =='METANO':
            dados_do_grafico_metano.append(aux)
        if dado.sensor.tipo_sensor.upper() =='MONOXIDO DE CARBONO':
            dados_do_grafico_monoxido_de_carbono.append(aux)

    grafico_metano=XML(dados_do_grafico_metano)
    grafico_monoxido_de_carbono=XML(dados_do_grafico_monoxido_de_carbono)


    #Tabela de maximo e minino
    
    #Formato: [ ['Data',Maximo, Minino], ['Data',Maximo, Minino] ...]

    #Tabela de Metano
    tabela_metano=[]
    grafico_max_min_metano=[]
    grafico_max_min_metano.append(["Data","Maximo","Minimo"])

    for data in datas_de_leituras:
        leituras_diarias=db((db.leituras.data_leitura==data.data_leitura)&(db.leituras.sensor==db.sensor.id)&(db.sensor.tipo_sensor=='METANO')).select(db.leituras.valor)
        if len(leituras_diarias)>0:
            aux = []
          
            aux.append(data.data_leitura.strftime('%d/%m/%y'))
            valor_maximo= max(leituras_diarias)
            valor_minimo= min(leituras_diarias)
            aux.append(valor_maximo.valor)
            aux.append(valor_minimo.valor)
            tabela_metano.append(aux)
            grafico_max_min_metano.append(aux)
        
    aux2=grafico_max_min_metano
    grafico_max_min_metano=XML(aux2)

    #Tabela de Monoxido de Carbono
    tabela_monoxido_de_carbono=[]
    grafico_max_min_monoxido=[]
    grafico_max_min_monoxido.append(["Data","Maximo","Minimo"])
    for data in datas_de_leituras:

        leituras_diarias=db((db.leituras.data_leitura==data.data_leitura)&(db.leituras.sensor==db.sensor.id)&(db.sensor.tipo_sensor=='MONOXIDO DE CARBONO')).select(db.leituras.valor)
        if len(leituras_diarias)>0:
            aux = []
          
            aux.append(data.data_leitura.strftime('%d/%m/%y'))
            valor_maximo= max(leituras_diarias)
            valor_minimo= min(leituras_diarias)
            aux.append(valor_maximo.valor)
            aux.append(valor_minimo.valor)
            tabela_monoxido_de_carbono.append(aux)
            grafico_max_min_monoxido.append(aux)
        
    aux2=grafico_max_min_monoxido
    grafico_max_min_monoxido=XML(aux2)

    #Formulário de entrada de datas para filtro. 
    if form.process().accepted:
        response.flash = 'Filtrando os dados ....'
        args = []
        args.append(str(form.vars.date_atual))
        args.append(str(form.vars.date_final))
        redirect(URL('portal', args=tuple(args)))
    elif form.errors:
        response.flash = 'Datas inválidas'
    
    #Parametros de Retorno da função para gerar a portal
    retorno = {}
    retorno.update({'nome':usuario.first_name}) #Nome do Usuário Logado
    retorno.update({'form':form}) #Formulário para setar a data para filtro de leituras
    retorno.update({'leituras':leituras}) #Leituras filtradas para apresentar na view
    retorno.update({'grafico_metano':grafico_metano}) #Dados para construção do gráfico de metano
    retorno.update({'grafico_monoxido_de_carbono':grafico_monoxido_de_carbono}) #Dados para construção do gráfico de Monixido de Carbono
    retorno.update({'tabela_metano':tabela_metano}) #Dados de Maxima e minimo sensor de metano
    retorno.update({'tabela_monoxido_de_carbono':tabela_monoxido_de_carbono}) #Dados de Maxima e minimo sensor de Monoxido de carbono 
    retorno.update({'grafico_max_min_metano':grafico_max_min_metano})
    retorno.update({'grafico_max_min_monoxido':grafico_max_min_monoxido})
    
    #Retorna os dados para View
    return retorno



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
    hardware=db(db.hardwares.id==dados['idh']).select().first()
    if(hardware):
        if(['hora', 'senha', 'idh', 'valor', 'data', 'ids']==dados.keys()):
            if(dados['senha']==hardware.senha):
                insersao=db.leituras.insert(
                    hardware=dados['idh'],
                    sensor=dados['ids'],
                    valor=dados['valor'],
                    data_leitura=date.today(),
                    hora_leitura=datetime.now().time()
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







