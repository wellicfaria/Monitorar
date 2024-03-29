# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if request.is_local:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.db')
else:
    #/Quando o sistema esta no servidor do pythonanywhere, o mesmo utiliza mysql
    db = DAL('mysql://monitorar:ar123@monitorar.mysql.pythonanywhere-services.com/monitorar$monitorar',migrate=False,fake_migrate=False)





## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager



auth = Auth(db)
service = Service()
plugins = PluginManager()

#Campos extras do usuário
auth.settings.extra_fields['auth_user']= [
  Field('cidade', 'reference cidades')
  ]

#Tabela para armazenar as estados que possem o harware instalado
db.define_table('estados',
    Field('nome_estado', type='string'),
    Field('abreviacao', type='string'), 
    format='%(nome_estado)s'
    )

#Tabela para armazenar as cidades que possem o harware instalado
db.define_table('cidades',
    Field('nome_cidade', type='string'),
    Field('estado', 'reference estados'),
    format='%(nome_cidade)s'
    )



## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
T.force('pt-br')

db.define_table('sensor',
    Field('tipo_sensor', type='string'),
    Field('unidade', type='string'),
    format='%(tipo_sensor)s'
    )

db.sensor.tipo_sensor.requires = IS_IN_SET(['METANO','MONOXIDO DE CARBONO','ALERTA'],error_message='Escolha um tipo para a autoridade!')

db.define_table('hardwares',
    Field('descricao', type='string'),
    Field('cidade', 'reference cidades'),
    Field('latitude', type='string'),
    Field('longitude', type='string'),
    Field('sensores', 'list:reference sensor'),
    Field('senha', 'string'),
    format='%(descricao)s'
    )

db.define_table('leituras',
    Field('hardware', 'reference hardwares'),
    Field('sensor', 'reference sensor'),
    Field('valor', 'double'),
    Field('data_leitura', 'date'),
    Field('hora_leitura', 'time'),
    format='%(sensor)s'
    )

db.define_table('autoridades',
     Field('nome', type='string'),
     Field('email', type='string'),
     Field('telefone', type='string'),
     Field('cidade', 'reference cidades'),
     Field('tipo',type='string'),
     format='%(nome)s'
    )

db.autoridades.nome.requires = IS_IN_SET(['Municipal', 'Estadual', 'Federal','Internacional'],error_message='Escolha um tipo para a autoridade!')