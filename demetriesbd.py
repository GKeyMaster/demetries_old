#demetriasbd 0.00 22/10/2018
#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import webapp2
import os
import datetime
import MySQLdb
from google.appengine.api import users
from google.appengine.ext.webapp import template
#from datetime import timedelta


# BASE DE DATOS
################################

# These environment variables are configured in app.yaml
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_DATABASE= os.environ.get('CLOUDSQL_DATABASE')

def connect_to_cloudsql():
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):

        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD,
            db=CLOUDSQL_DATABASE,
            charset='utf8')

    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db



def get_db():
    conn = connect_to_cloudsql()
    return conn

#INICI APLICACIO
class MainPage(webapp2.RequestHandler):
    def get(self):
            self.redirect("/Inicio") #Redirecciona a Inicio
            


# FUNCIONS GENERALS
################################           
#-- FUNCIO DATA FORMAT
#-- Convertix una data al format 2016-09-26
def dataFormat(data):
    try:
        dataF= data.strftime("%Y-%m-%d") # data amb format 
    except:
        dataF= ""
    return dataF

def novar(variable):
    if variable is not None and variable != '':
        variable = variable
    else:
        variable = None
    return variable

def noimp(variable):
    if variable is not None and variable != '':
        variable = variable
    else:
        variable = ""
    return variable


def comandaSeguent(comanda):
    an = comanda[1:3]
    num = comanda[4:7]
    total = an+num
    total = int(total)
    seguent = total+1
    seguent = str(seguent)
    segNum = seguent[2:6]
    comS = "C"+an+"/"+segNum
    return comS

def fcompraSeguent(fcompra):
    an = fcompra[2:4]
    num = fcompra[5:8]
    total = an+num
    total = int(total)
    seguent = total+1
    seguent = str(seguent)
    segNum = seguent[2:6]
    comS = "FC"+an+"/"+segNum
    return comS

def factSimpliSeguent(factSimpli):
    an = factSimpli[2:4]
    num = factSimpli[5:8]
    total = an+num
    total = int(total)
    seguent = total+1
    seguent = str(seguent)
    segNum = seguent[2:6]
    comS = "FS"+an+"/"+segNum
    return comS
            
###########################################################################################################################################################
# CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES     
########################################################################################################################################################### 
    
def autentificacio(self, users):
    user = users.get_current_user()
    lista = treballadorsNivell()
    dernierePos = len(lista)-1
    idTreballador= -1
    
    
    if user:
        
        i=0
        while(i<=dernierePos):
            treballador=lista[i]
            if user.nickname() ==treballador.mailTreballador:           
                idTreballador= treballador.idTreballador
                i=dernierePos+1
                
            else :
                idTreballador=-1
                i+=1
    if(idTreballador == -1):
        self.redirect(users.create_login_url(self.request.uri,))
                          
    return idTreballador

def treballadorsNivell():
    db= get_db()
    cursor = db.cursor()
    lista= tablaTreballadorsNivell(cursor)
    db.commit()
    db.close()
    return lista






        
###########################################################################################################################################################
# INICI     INICI    INICI     INICI    INICI     INICI    INICI     INICI    INICI     INICI    INICI     INICI    INICI     
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariInicio (usuari):

    #conectar a la bd
    db= connect_to_cloudsql()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    #desconectar de la bd
    db.commit()
    db.close()
    
    

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class Inicio(webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):   
            self.redirect("/Index") 


class Index(webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #obtenim valors per al html
            values = formulariInicio(usuari)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'index.html') 
            self.response.out.write(template.render(path, values,))
            



###########################################################################################################################################################
# TREBALLADOR          TREBALLADOR          TREBALLADOR          TREBALLADOR          TREBALLADOR          TREBALLADOR          TREBALLADOR         
###########################################################################################################################################################


def tablaTreballadorSelect(cursor, idTreballador):
    cursor.execute('SELECT idTreballador, claveTreballador, nomTreballador, enActiu, nivell, ordre, mailTreballador FROM treballadors WHERE idTreballador=%s',(idTreballador,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        lista = Treballador(i[0],i[1],i[2],i[3],i[4],i[5],i[6]) #Modificar si anyadim columna
    return lista        


def tablaTreballadorTots(cursor):   
    cursor.execute('SELECT idTreballador, claveTreballador, nomTreballador, enActiu, nivell, ordre, mailTreballador FROM treballadors  ORDER BY enActiu DESC, nivell DESC, idTreballador')
    expedients = cursor.fetchall()
    conta=0
    indice=0
    for i in expedients: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in expedients: #cada fila es converteix en un objecte de lista
        lista[indice] = Treballador(i[0],i[1],i[2],i[3],i[4],i[5],i[6]) #Modificar si anyadim columna
        indice=indice+1   
    return lista

def tablaTreballadorsNivell(cursor):   
    cursor.execute('SELECT idTreballador, claveTreballador, nomTreballador, enActiu, nivell, ordre, mailTreballador FROM treballadors WHERE nivell>%s',(0,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Treballador(i[0],i[1],i[2],i[3],i[4],i[5],i[6]) #Modificar si anyadim columna
        indice=indice+1   
    return lista

def tablaTreballadorAct(cursor):   
    cursor.execute('SELECT idTreballador, claveTreballador, nomTreballador, enActiu, nivell, ordre, mailTreballador FROM treballadors WHERE enActiu=%s ORDER BY ordre',(1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Treballador(i[0],i[1],i[2],i[3],i[4],i[5],i[6]) #Modificar si anyadim columna
        indice=indice+1   
    return lista 
           
class Treballador: 
    def __init__(self, idTreballador, claveTreballador, nomTreballador,enActiu, nivell, ordre, mailTreballador):
        self.idTreballador = idTreballador
        self.claveTreballador = claveTreballador
        self.nomTreballador = nomTreballador
        self.enActiu = enActiu
        self.nivell = nivell
        self.ordre = ordre    
        self.mailTreballador = mailTreballador       

###########################################################################################################################################################
# CONTROL             CONTROL             CONTROL             CONTROL             CONTROL             CONTROL             CONTROL             
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariUsuari (usuari, idTreballador):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    
    if idTreballador == -1: #sense seleccio
        usuariSelect = ''
        treballadorTots = tablaTreballadorTots(cursor)
        
    elif idTreballador == -2: #treballador en blanc
        usuariSelect = ''
        treballadorTots = ''
        
    else: #treballador select
        usuariSelect = tablaTreballadorSelect(cursor,idTreballador)
        treballadorTots = ''
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'idTreballador': idTreballador,
             'treballadorSelect': treballadorSelect,
             'usuariSelect': usuariSelect,
             'treballadorTots': treballadorTots,
             
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class UsuariTots (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            nivell=nivellUsuari(usuari)
            if(nivell==2):   
                #parametres
                idTreballador = -1
            
                #obtenim valors per al html
                values = formulariUsuari(usuari, idTreballador)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'usuari.html') 
                self.response.out.write(template.render(path, values,))
            else:
                #obtenim valors per al html
                values = formulariInicio(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'accesDenegat.html') 
                self.response.out.write(template.render(path, values,))
            

class UsuariNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            nivell=nivellUsuari(usuari)
            if(nivell==2):   
                #parametres
                idTreballador = -2
            
                #obtenim valors per al html
                values = formulariUsuari(usuari, idTreballador)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'usuari.html') 
                self.response.out.write(template.render(path, values,))
            else:
                #obtenim valors per al html
                values = formulariInicio(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'accesDenegat.html') 
                self.response.out.write(template.render(path, values,))
            
class UsuariSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreballador= novar(self.request.get('idTreballador'))
            
            #parametres

            
            #obtenim valors per al html
            values = formulariUsuari(usuari, idTreballador)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'usuari.html') 
            self.response.out.write(template.render(path, values,))
            
class UsuariEdita (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTreballador= novar(self.request.get('idTreballador'))
            claveTreballador = novar(self.request.get('claveTreballador'))
            nomTreballador = novar(self.request.get('nomTreballador'))
            mailTreballador = novar(self.request.get('mailTreballador'))
            enActiu = novar(self.request.get('enActiu'))
            nivell = novar(self.request.get('nivell'))
            

            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('UPDATE treballadors SET claveTreballador=%s, nomTreballador=%s, mailTreballador=%s, enActiu=%s, nivell=%s WHERE idTreballador=%s', (claveTreballador, nomTreballador, mailTreballador, enActiu, nivell, idTreballador,))
            
            db.commit()
            db.close()
            
            #redirecciona
            self.redirect("/UsuariTots")

class UsuariCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            claveTreballador = novar(self.request.get('claveTreballador'))
            nomTreballador = novar(self.request.get('nomTreballador'))
            mailTreballador = novar(self.request.get('mailTreballador'))
            enActiu = novar(self.request.get('enActiu'))
            nivell = novar(self.request.get('nivell'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('INSERT INTO treballadors (claveTreballador, nomTreballador, mailTreballador, enActiu, nivell) VALUES (%s, %s, %s, %s, %s)', (claveTreballador, nomTreballador, mailTreballador, enActiu, nivell))
            cursor.execute('SELECT idTreballador FROM treballadors ORDER BY idTreballador DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idTreballador = lista[0][0]
            cursor.execute('UPDATE treballadors SET ordre=%s WHERE idTreballador=%s', (idTreballador, idTreballador,))
           
    
            
            db.commit()
            db.close()

            #redirecciona
            self.redirect("/UsuariTots")
            
# FUNCIONS SECUNDARIES DEL FORMULARI
####################################



def nivellUsuari(idTreballador):
    db= get_db()
    cursor = db.cursor()
    cursor.execute('SELECT  nivell FROM treballadors  WHERE idTreballador=%s', (idTreballador,))
    tabla = cursor.fetchall()
    idTreballador = tabla [0][0]
    db.commit()
    db.close()
    return idTreballador


###########################################################################################################################################################
# CLIENT              CLIENT                CLIENT               CLIENT               CLIENT               CLIENT               CLIENT               CLIENT          
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariClient (usuari, idClient):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    
    if idClient== -1: #tots intermediaris
        clientSelect = ''
        clientTots = tablaClientTots(cursor)
        
    elif idClient==-2:
        clientSelect = ''
        clientTots = ''
        
    else: # select
        clientSelect = tablaClientSelect(cursor,idClient)
        clientTots = tablaClientTots(cursor)
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idClient': idClient,
             'clientSelect': clientSelect,
             'clientTots': clientTots,          
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class ClientTots (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idClient = -1
            
                #obtenim valors per al html
                values = formulariClient(usuari, idClient)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'client.html') 
                self.response.out.write(template.render(path, values,))
                
class ClientNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idClient = -2
            
                #obtenim valors per al html
                values = formulariClient(usuari, idClient)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'client.html') 
                self.response.out.write(template.render(path, values,))

                
            
class ClientSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idClient= novar(self.request.get('idClient'))
            

            #obtenim valors per al html
            values = formulariClient(usuari, idClient)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'client.html') 
            self.response.out.write(template.render(path, values,))

            

class ClientEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idClient= novar(self.request.get('idClient'))
            nomClient = novar(self.request.get('nomClient'))
            direccioF = novar(self.request.get('direccioF'))
            direccioE = novar(self.request.get('direccioE'))
            cifClient = novar(self.request.get('cifClient'))
            telClient = novar(self.request.get('telClient'))
            contacte = novar(self.request.get('contacte'))
            mailClient = novar(self.request.get('mailClient'))
            direccioE2 = novar(self.request.get('direccioE2'))
            direccioE3 = novar(self.request.get('direccioE3'))
            nomComercial1 = novar(self.request.get('nomComercial1'))
            nomComercial2 = novar(self.request.get('nomComercial2'))
            nomComercial3 = novar(self.request.get('nomComercial3'))
            descripcio = novar(self.request.get('descripcio'))
            comunitari = novar(self.request.get('comunitari'))
            recarrec = novar(self.request.get('recarrec'))
          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT cifClient FROM clients WHERE idClient=%s',(idClient,))
            cifANT = cursor.fetchall()
            cifANT = cifANT [0][0]
            cifNOU = cifClient
            
            cursor.execute('SELECT cifClient FROM clients WHERE cifClient=%s',(cifClient,))
            cifs = cursor.fetchall()

            if cifs:
                if cifANT == cifNOU:
                    cursor.execute('UPDATE clients SET nomClient=%s, direccioF=%s, direccioE=%s, cifClient=%s, telClient=%s, contacte=%s, mailClient=%s, direccioE2=%s, direccioE3=%s, nomComercial1=%s, nomComercial2=%s, nomComercial3=%s, descripcio=%s, comunitari=%s, recarrec=%s WHERE idClient=%s', (nomClient, direccioF, direccioE, cifClient, telClient, contacte, mailClient, direccioE2, direccioE3, nomComercial1, nomComercial2, nomComercial3, descripcio, comunitari, recarrec, idClient,))          
                    db.commit()
                    db.close()
                else:                    
                    db.commit()
                    db.close()
                    values = formulariInicio(usuari)
                    path = os.path.join(os.path.dirname(__file__), 'clientDuplicat.html') 
                    self.response.out.write(template.render(path, values,))
            else:                       
                cursor.execute('UPDATE clients SET nomClient=%s, direccioF=%s, direccioE=%s, cifClient=%s, telClient=%s, contacte=%s, mailClient=%s, direccioE2=%s, direccioE3=%s, nomComercial1=%s, nomComercial2=%s, nomComercial3=%s, descripcio=%s, comunitari=%s, recarrec=%s WHERE idClient=%s', (nomClient, direccioF, direccioE, cifClient, telClient, contacte, mailClient, direccioE2, direccioE3, nomComercial1, nomComercial2, nomComercial3, descripcio, comunitari, recarrec, idClient,))          
                db.commit()
                db.close()
            

            
            #obtenim valors per al html
            values = formulariClient(usuari, idClient)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'client.html') 
            self.response.out.write(template.render(path, values,))

class ClientCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            nomClient = novar(self.request.get('nomClient'))
            direccioF = novar(self.request.get('direccioF'))
            direccioE = novar(self.request.get('direccioE'))
            cifClient = novar(self.request.get('cifClient'))
            telClient = novar(self.request.get('telClient'))
            contacte = novar(self.request.get('contacte'))
            mailClient = novar(self.request.get('mailClient'))
            direccioE2 = novar(self.request.get('direccioE2'))
            direccioE3 = novar(self.request.get('direccioE3'))
            nomComercial1 = novar(self.request.get('nomComercial1'))
            nomComercial2 = novar(self.request.get('nomComercial2'))
            nomComercial3 = novar(self.request.get('nomComercial3'))
            descripcio = novar(self.request.get('descripcio'))
            comunitari = novar(self.request.get('comunitari'))
            recarrec = novar(self.request.get('recarrec'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT cifClient FROM clients WHERE cifClient=%s',(cifClient,))
            cifs = cursor.fetchall()
            
            if cifs:
                db.commit()
                db.close()
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                db.commit()
                db.close()
                error = "Este CIF ja existeix"
                values = {
                             'treballadorSelect': treballadorSelect,
                             'error': error,         
                              }
                path = os.path.join(os.path.dirname(__file__), 'error.html') 
                self.response.out.write(template.render(path, values,))
            else:
                cursor.execute('INSERT INTO clients (nomClient, direccioF, direccioE, cifClient, telClient, contacte, mailClient, direccioE2, direccioE3, nomComercial1, nomComercial2, nomComercial3, descripcio, comunitari, recarrec) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nomClient, direccioF, direccioE, cifClient, telClient, contacte, mailClient,direccioE2, direccioE3, nomComercial1, nomComercial2, nomComercial3, descripcio, comunitari, recarrec))
                cursor.execute('SELECT idClient FROM clients ORDER BY idClient DESC LIMIT 0,1')
                lista = cursor.fetchall()
                idClient = lista[0][0]        
                db.commit()
                db.close()

                idClient = -1
                
                #obtenim valors per al html
                values = formulariClient(usuari, idClient)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'client.html') 
                self.response.out.write(template.render(path, values,))
            
class ClientElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idClient= novar(self.request.get('idClient'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('SELECT idClient FROM comandes WHERE idClient=%s',(idClient,))
            lista = cursor.fetchall()
            if lista:
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                db.commit()
                db.close()
                error = "Este client esta en alguna comanda"
                values = {
                             'treballadorSelect': treballadorSelect,
                             'error': error,         
                              }
                path = os.path.join(os.path.dirname(__file__), 'error.html') 
                self.response.out.write(template.render(path, values,))

            else:
                cursor.execute('DELETE FROM clients WHERE idClient=%s',(idClient,))

                db.commit()
                db.close()
                
                idClient=-1
            

                #obtenim valors per al html
                values = formulariClient(usuari, idClient)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'client.html') 
                self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaClientTots(cursor):   
    cursor.execute('SELECT idClient, nomClient, direccioF, direccioE, cifClient, telClient, contacte, mailClient, direccioE2, direccioE3, nomComercial1, nomComercial2, nomComercial3, descripcio, comunitari, recarrec FROM clients ORDER BY nomClient')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        cifClient=noimp(i[4])
        direccioF=noimp(i[2])
        lista[indice] = Client(i[0],i[1],direccioF,i[3],cifClient,i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaClientSelect(cursor, idClient):
    cursor.execute('SELECT idClient, nomClient, direccioF, direccioE, cifClient, telClient, contacte, mailClient, direccioE2, direccioE3, nomComercial1, nomComercial2, nomComercial3, descripcio, comunitari, recarrec  FROM clients WHERE idClient=%s',(idClient,))
    tabla = cursor.fetchall()
    
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = Client(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15]) #Modificar si anyadim columna 
    return lista 


class Client:
    def __init__(self, idClient, nomClient, direccioF, direccioE, cifClient, telClient, contacte, mailClient, direccioE2, direccioE3, nomComercial1, nomComercial2, nomComercial3, descripcio, comunitari, recarrec):
        self.idClient = idClient
        self.nomClient = nomClient
        self.direccioF = direccioF
        self.direccioE = direccioE
        self.cifClient = cifClient
        self.telClient = telClient
        self.contacte = contacte
        self.mailClient = mailClient
        self.direccioE2 = direccioE2
        self.direccioE3 = direccioE3
        self.nomComercial1 = nomComercial1
        self.nomComercial2 = nomComercial2
        self.nomComercial3 = nomComercial3
        self.descripcio = descripcio
        self.comunitari = comunitari
        self.recarrec = recarrec


###########################################################################################################################################################
# PRODUCTE      PRODUCTE       PRODUCTE      PRODUCTE      PRODUCTE      PRODUCTE      PRODUCTE      PRODUCTE      PRODUCTE      PRODUCTE         
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariProducte (usuari, idProducte):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    
    if idProducte== -1: #tots intermediaris
        producteSelect = ''
        producteTots = tablaProducteTots(cursor)
        
    elif idProducte==-2:
        producteSelect = ''
        producteTots = ''
        
    else: # select
        producteSelect = tablaProducteSelect(cursor,idProducte)
        producteTots = tablaProducteTots(cursor)
        
    tipoIvaTots= tablaTipoIvaTots(cursor)
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idProducte': idProducte,
             'producteSelect': producteSelect,
             'producteTots': producteTots,
             'tipoIvaTots': tipoIvaTots,        
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class ProducteTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idProducte = -1
            
                #obtenim valors per al html
                values = formulariProducte(usuari, idProducte)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'producte.html') 
                self.response.out.write(template.render(path, values,))
                
class ProducteNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idProducte = -2
            
                #obtenim valors per al html
                values = formulariProducte(usuari, idProducte)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'producte.html') 
                self.response.out.write(template.render(path, values,))

                
            
class ProducteSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idProducte= novar(self.request.get('idProducte'))
            

            #obtenim valors per al html
            values = formulariProducte(usuari, idProducte)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'producte.html') 
            self.response.out.write(template.render(path, values,))

            

class ProducteEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idProducte= novar(self.request.get('idProducte'))
            codiProducte = novar(self.request.get('codiProducte'))
            producte = novar(self.request.get('producte'))
            preuD = novar(self.request.get('preuD'))
            preuP = novar(self.request.get('preuP'))
            idTipoIva = novar(self.request.get('idTipoIva'))
            unitat = novar(self.request.get('unitat'))
            esFira = novar(self.request.get('esFira'))

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                     
            cursor.execute('UPDATE productes SET codiProducte=%s, producte=%s, preuD=%s, preuP=%s, idTipoIva=%s, unitat=%s, esFira=%s WHERE idProducte=%s', (codiProducte, producte, preuD, preuP, idTipoIva, unitat, esFira, idProducte,))          
            
            db.commit()
            db.close()
            

            
            #obtenim valors per al html
            values = formulariProducte(usuari, idProducte)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'producte.html') 
            self.response.out.write(template.render(path, values,))

class ProducteCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            codiProducte = novar(self.request.get('codiProducte'))
            producte = novar(self.request.get('producte'))
            preuD = novar(self.request.get('preuD'))
            preuP = novar(self.request.get('preuP'))
            unitat = novar(self.request.get('unitat'))
            idTipoIva = novar(self.request.get('idTipoIva'))
            esFira = novar(self.request.get('esFira'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            

            cursor.execute('INSERT INTO productes (codiProducte, producte, preuD, preuP, idTipoIva, unitat, esFira) VALUES (%s, %s, %s, %s, %s, %s, %s)', (codiProducte, producte, preuD, preuP, idTipoIva, unitat, esFira,))
            cursor.execute('SELECT idProducte FROM productes ORDER BY idProducte DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idProducte = lista[0][0]        
            db.commit()
            db.close()

            idProducte = -1
            
            #obtenim valors per al html
            values = formulariProducte(usuari, idProducte)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'producte.html') 
            self.response.out.write(template.render(path, values,))
            
class ProducteElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idProducte= novar(self.request.get('idProducte'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT idProducte FROM liniescomanda WHERE idProducte=%s',(idProducte,))
            lista = cursor.fetchall()
            if lista:
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                db.commit()
                db.close()
                error = "Este producte esta en alguna comanda"
                values = {
                             'treballadorSelect': treballadorSelect,
                             'error': error,         
                              }
                path = os.path.join(os.path.dirname(__file__), 'error.html') 
                self.response.out.write(template.render(path, values,))
            else:   
                cursor.execute('DELETE FROM productes WHERE idProducte=%s',(idProducte,))
    
                db.commit()
                db.close()
                
                idProducte = -1
    
                #obtenim valors per al html
                values = formulariProducte(usuari, idProducte)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'producte.html') 
                self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaProducteTots(cursor):   
    cursor.execute('SELECT pr.idProducte, pr.codiProducte, pr.producte, pr.preuP, pr.preuD, pr.idTipoIva, pr.unitat, pr.esFira, ti.percent FROM tipoiva ti INNER JOIN productes pr ON pr.idTipoIva = ti.idTipoIva ORDER BY producte')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = ProducteT(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaProducteSelect(cursor, idProducte):
    cursor.execute('SELECT idProducte, codiProducte, producte, preuP, preuD, idTipoIva, unitat, esFira FROM productes WHERE idProducte=%s',(idProducte,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = Producte(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]) #Modificar si anyadim columna 
    return lista 


class Producte:
    def __init__(self, idProducte, codiProducte, producte, preuP, preuD, idTipoIva, unitat, esFira):
        self.idProducte = idProducte
        self.codiProducte = codiProducte
        self.producte = producte
        self.preuP = preuP
        self.preuD = preuD
        self.idTipoIva = idTipoIva
        self.unitat = unitat
        self.esFira = esFira

class ProducteT:
    def __init__(self, idProducte, codiProducte, producte, preuP, preuD, idTipoIva, unitat, esFira, percent):
        self.idProducte = idProducte
        self.codiProducte = codiProducte
        self.producte = producte
        self.preuP = preuP
        self.preuD = preuD
        self.idTipoIva = idTipoIva
        self.unitat = unitat
        self.esFira = esFira
        self.percent = percent

def tablaTipoIvaTots(cursor):   
    cursor.execute('SELECT idTipoIva, tipoIva, percent FROM tipoiva ORDER BY tipoIva')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = TipoIva(i[0],i[1],i[2]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

class TipoIva:
    def __init__(self, idTipoIva, tipoIva, percent):
        self.idTipoIva = idTipoIva
        self.tipoIva = tipoIva
        self.percent = percent



###########################################################################################################################################################
# COMANDA         COMANDA            COMANDA            COMANDA            COMANDA            COMANDA            COMANDA            COMANDA         
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariComanda (usuari, idComanda):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    liniaComandaTots=''
    totalComanda=''
    pagamentTots=''
    totalPagament=''
    clientSelect=''
    
    if idComanda== -1: #tots intermediaris
        comandaSelect = ''
        comandaTots = tablaComandaTots(cursor)
        
        
    elif idComanda==-2:
        comandaSelect = ''
        comandaTots = ''
        
        
    else: # select
        comandaSelect = tablaComandaSelect(cursor,idComanda)
        comandaTots = tablaComandaTots(cursor)
        cursor.execute('SELECT idClient FROM comandes WHERE idComanda=%s',(idComanda,))
        vector = cursor.fetchall()
        idClient = vector[0][0]
        clientSelect = tablaClientSelect(cursor, idClient)
        
        cursor.execute('SELECT idLiniaComanda FROM liniescomanda WHERE idComanda=%s ORDER BY idLiniaComanda DESC LIMIT 0,1',(idComanda,))
        linies = cursor.fetchall()
        try:
            idLiniaComanda = linies[0][0]
        except:
            idLiniaComanda = 0
        if idLiniaComanda>0:
            liniaComandaTots = tablaLiniaComandaTots(cursor, idComanda)
            totalComanda = tablaTotalComanda(cursor, idComanda)
            
        cursor.execute('SELECT idPagament FROM pagaments WHERE idComanda=%s ORDER BY idPagament DESC LIMIT 0,1',(idComanda,))
        pagament = cursor.fetchall()
        try:
            idPagament = pagament[0][0]
        except:
            idPagament = 0
        if idPagament>0:
            pagamentTots = tablaPagamentTots(cursor, idComanda)
            totalPagament = tablaTotalPagament(cursor, idComanda)
    
            
    
    clientTots = tablaClientTots(cursor)
    lotTots=tablaLotTots(cursor)
    
    
    
    #ultima comanda
    cursor.execute('SELECT numComanda, dataComanda FROM comandes WHERE numComanda<>%s ORDER BY numComanda DESC LIMIT 0,1',('None',))
    comanda = cursor.fetchall()
    if comanda:
        ultNumComanda = comanda[0][0]
        ultDataComanda = dataFormat(comanda[0][1])
    else:
        ultNumComanda = 'C18/000'
        ultDataComanda = '2018-01-01'
    
    #comanda seguent
    comandaS=comandaSeguent(ultNumComanda)
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')
    
    #ultima factura
    cursor.execute('SELECT numFactura, dataFactura FROM comandes WHERE numFactura<>%s ORDER BY numFactura DESC LIMIT 0,1',('None',))
    factura = cursor.fetchall()
    if factura:
        ultNumFactura = factura[0][0]
        ultDataFactura = dataFormat(factura[0][1])
    else:
        ultNumFactura = '18/000'
        ultDataFactura = '2018-01-01'
        
        
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idComanda': idComanda,
             'comandaSelect': comandaSelect,
             'comandaTots': comandaTots,
             'clientTots': clientTots, 
             'clientSelect': clientSelect,
             'ultNumComanda': ultNumComanda,
             'ultDataComanda': ultDataComanda,
             'ultNumFactura': ultNumFactura,
             'ultDataFactura': ultDataFactura,
             'liniaComandaTots': liniaComandaTots,  
             'totalComanda': totalComanda, 
             'pagamentTots':  pagamentTots,  
             'totalPagament': totalPagament,
             'comandaS': comandaS,
             'dataHui': dataHui,
             'lotTots': lotTots,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class ComandaTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idComanda = -1
            
                #obtenim valors per al html
                values = formulariComanda(usuari, idComanda)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'comanda.html') 
                self.response.out.write(template.render(path, values,))
                
class ComandaNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idComanda = -2
            
                #obtenim valors per al html
                values = formulariComanda(usuari, idComanda)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'comanda.html') 
                self.response.out.write(template.render(path, values,))

                
            
class ComandaSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idComanda= novar(self.request.get('idComanda'))
            

            #obtenim valors per al html
            values = formulariComanda(usuari, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'comanda.html') 
            self.response.out.write(template.render(path, values,))

            

class ComandaEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idComanda= novar(self.request.get('idComanda'))
            numComanda = novar(self.request.get('numComanda'))
            dataComanda = novar(self.request.get('dataComanda'))
            numFactura = novar(self.request.get('numFactura'))
            dataFactura = novar(self.request.get('dataFactura'))
            entrega = novar(self.request.get('entrega'))
            preparat = novar(self.request.get('preparat'))
            idClient = novar(self.request.get('idClient'))
            descripcio = novar(self.request.get('descripcio'))


          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                     
            cursor.execute('UPDATE comandes SET numComanda=%s, dataComanda=%s, numFactura=%s, dataFactura=%s, entrega=%s, preparat=%s, idClient=%s, descripcio=%s WHERE idComanda=%s', (numComanda, dataComanda, numFactura, dataFactura, entrega, preparat, idClient, descripcio, idComanda,))          
            
            db.commit()
            db.close()
            

            
            #obtenim valors per al html
            values = formulariComanda(usuari, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'comanda.html') 
            self.response.out.write(template.render(path, values,))



class ComandaCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            numComanda = novar(self.request.get('numComanda'))
            dataComanda = novar(self.request.get('dataComanda'))
            idClient = novar(self.request.get('idClient'))
            numFactura = novar(self.request.get('numFactura'))
            dataFactura = novar(self.request.get('dataFactura'))
            preparat = novar(self.request.get('preparat'))
            descripcio = novar(self.request.get('descripcio'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            

            cursor.execute('INSERT INTO comandes (numComanda,idClient, numFactura, dataFactura, preparat, descripcio) VALUES (%s, %s, %s, %s, %s, %s)', (numComanda, idClient, numFactura, dataFactura, preparat, descripcio))
            cursor.execute('SELECT idComanda FROM comandes ORDER BY idComanda DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idComanda = lista[0][0]
                               
            if dataComanda:
                cursor.execute('UPDATE comandes SET dataComanda=%s WHERE idComanda=%s',(dataComanda,idComanda,))
                               
                                       
            db.commit()
            db.close()

            
            #obtenim valors per al html
            values = formulariComanda(usuari, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'comanda.html') 
            self.response.out.write(template.render(path, values,))
            
class ComandaElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idComanda= novar(self.request.get('idComanda'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT idComanda FROM liniescomanda WHERE idComanda=%s',(idComanda,))
            linia = cursor.fetchall()
            
            cursor.execute('SELECT idComanda FROM pagaments WHERE idComanda=%s',(idComanda,))
            pagament = cursor.fetchall()
            
            if linia:
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                db.commit()
                db.close()
                error = "Esta comanda te linies de comanda elimina abans"
                values = {
                             'treballadorSelect': treballadorSelect,
                             'error': error,         
                              }
                path = os.path.join(os.path.dirname(__file__), 'error.html') 
                self.response.out.write(template.render(path, values,))
                
            elif pagament:
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                db.commit()
                db.close()
                error = "Esta comanda te pagaments elimina abans"
                values = {
                             'treballadorSelect': treballadorSelect,
                             'error': error,         
                              }
                path = os.path.join(os.path.dirname(__file__), 'error.html') 
                self.response.out.write(template.render(path, values,))   
            
            else:
                
                cursor.execute('DELETE FROM comandes WHERE idComanda=%s',(idComanda,))
    
                db.commit()
                db.close()
                
                idComanda = -1
    
                #obtenim valors per al html
                values = formulariComanda(usuari, idComanda)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'comanda.html') 
                self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaComandaTots(cursor):   
    cursor.execute('SELECT co.idComanda, co.numComanda, co.dataComanda, co.idClient, co.numFactura, co.dataFactura, cl.nomClient, co.entrega, co.preparat, cl.comunitari, co.descripcio FROM clients cl INNER JOIN comandes co ON cl.idClient = co.idClient ORDER BY co.numComanda DESC LIMIT 500')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        idComanda=i[0]
        comunitari=i[9]
        descripcio=i[10]
        dataFactura=dataFormat(i[5])
        #obtenir total linies comanda
        if dataFactura>'2018-01-01':
            if comunitari == 1:
                cursor.execute('SELECT SUM(preuUnit*quantitat) AS preuC FROM liniescomanda  WHERE idComanda=%s',(idComanda,))
            else:
                cursor.execute('SELECT SUM(lc.preuUnit*lc.quantitat*(1+ti.tipoIva)) AS preuC FROM tipoiva ti INNER JOIN productes pr ON pr.idTipoIva=ti.idTipoIva INNER JOIN liniescomanda lc  ON lc.idProducte=pr.idProducte WHERE idComanda=%s',(idComanda,))
        else:
            cursor.execute('SELECT SUM(preuUnit*quantitat) AS preuC FROM liniescomanda  WHERE idComanda=%s',(idComanda,))
        
        vectorT = cursor.fetchall()
        try:
            preuC = vectorT [0] [0]
            preuCt = "%.2f" %preuC
        except:
            preuC = 0
            preuCt= '0.00'
        
        
        cursor.execute('SELECT SUM(quantitat) AS pagat FROM pagaments  WHERE idComanda=%s',(idComanda,))
        vectorT2 = cursor.fetchall() 
        try:
            pagatC = vectorT2 [0] [0]
            pagatCt = "%.2f" %pagatC
        except:
            pagatC = 0
            pagatCt= '0.00'
        
        pendentC = preuC - pagatC
        if pendentC>1:
            pendentCt = "%.2f" %pendentC
        else:
            pendentCt='0.00'
        
            
            
        dataComanda=dataFormat(i[2])
        lista[indice] = Comanda(i[0],i[1],dataComanda,i[3],i[4],dataFactura,i[6],i[7], i[8], preuCt, pagatCt, pendentCt, descripcio) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaComandaSelect(cursor, idComanda):
    cursor.execute('SELECT co.idComanda, co.numComanda, co.dataComanda, co.idClient, co.numFactura, co.dataFactura, cl.nomClient, co.entrega, co.preparat, co.descripcio FROM clients cl INNER JOIN comandes co ON cl.idClient = co.idClient WHERE co.idComanda=%s',(idComanda,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        dataComanda=dataFormat(i[2])
        dataFactura=dataFormat(i[5])
        lista = Comanda(i[0],i[1],dataComanda,i[3],i[4],dataFactura,i[6],i[7],i[8],"","","",i[9]) #Modificar si anyadim columna 
    return lista 


class Comanda:
    def __init__(self, idComanda, numComanda, dataComanda, idClient, numFactura, dataFactura, client,entrega, preparat, preuCt, pagatCt, pendentCt, descripcio):
        self.idComanda = idComanda
        self.numComanda = numComanda
        self.dataComanda = dataComanda
        self.idClient = idClient
        self.numFactura = numFactura
        self.dataFactura = dataFactura
        self.client = client
        self.entrega = entrega
        self.preparat = preparat
        self.preuCt = preuCt
        self.pagatCt = pagatCt
        self.pendentCt = pendentCt
        self.descripcio = descripcio
        

###########################################################################################################################################################
# LINIESCOMANDA          LINIESCOMANDA           LINIESCOMANDA           LINIESCOMANDA           LINIESCOMANDA           LINIESCOMANDA           LINIESCOMANDA         
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariLiniaComanda (usuari, idLiniaComanda, idComanda):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    
    if idLiniaComanda== -1: #tots 
        liniaComandaSelect = ''
        liniaComandaTots = tablaLiniaComandaTots(cursor, idComanda)
        
    else: # select
        liniaComandaSelect = tablaLiniaComandaSelect(cursor,idLiniaComanda)
        liniaComandaTots = tablaLiniaComandaTots(cursor, idComanda)
          
        
    producteTots= tablaProducteTots(cursor)
    lotTots=tablaLotTots(cursor)
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idComanda': idComanda,
             'idLiniaComanda': idLiniaComanda,
             'liniaComandaSelect': liniaComandaSelect,
             'liniaComandaTots': liniaComandaTots,  
             'producteTots': producteTots,
             'lotTots': lotTots,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
                
class LiniaComandaNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                idComanda= novar(self.request.get('idComanda'))
                #parametre
                idLiniaComanda = -1
            
                #obtenim valors per al html
                values = formulariLiniaComanda(usuari, idLiniaComanda, idComanda)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'liniacomanda.html') 
                self.response.out.write(template.render(path, values,))

                
            
class LiniaComandaSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idLiniaComanda = novar(self.request.get('idLiniaComanda'))
            idComanda= novar(self.request.get('idComanda'))
            

            #obtenim valors per al html
            values = formulariLiniaComanda(usuari, idLiniaComanda, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'liniacomanda.html') 
            self.response.out.write(template.render(path, values,))

            

class LiniaComandaEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idLiniaComanda = novar(self.request.get('idLiniaComanda'))
            idComanda= novar(self.request.get('idComanda'))
            idProducte =novar(self.request.get('idProducte'))
            preuUnit = novar(self.request.get('preuUnit'))
            quantitat = novar(self.request.get('quantitat'))
            idLot = novar(self.request.get('idLot'))
            

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                     
            cursor.execute('UPDATE liniescomanda SET idProducte=%s, preuUnit=%s, quantitat=%s, idLot=%s WHERE idLiniaComanda=%s', (idProducte, preuUnit, quantitat, idLot, idLiniaComanda,))          
            
            db.commit()
            db.close()
            

            
            #obtenim valors per al html
            values = formulariLiniaComanda(usuari, idLiniaComanda, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'liniacomanda.html') 
            self.response.out.write(template.render(path, values,))

class LiniaComandaCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idComanda= novar(self.request.get('idComanda'))
            idProducte =novar(self.request.get('idProducte'))
            preuUnit = novar(self.request.get('preuUnit'))
            quantitat = novar(self.request.get('quantitat'))
            idLot=-1
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            

            cursor.execute('INSERT INTO liniescomanda (idComanda, idProducte, preuUnit, quantitat, idLot) VALUES (%s, %s, %s, %s, %s)', (idComanda, idProducte, preuUnit, quantitat, idLot))
      
            db.commit()
            db.close()

            
            #obtenim valors per al html
            values = formulariComanda(usuari, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'comanda.html') 
            self.response.out.write(template.render(path, values,))
            
class LiniaComandaElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idComanda= novar(self.request.get('idComanda'))
            idLiniaComanda= novar(self.request.get('idLiniaComanda'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
                
            cursor.execute('DELETE FROM liniescomanda WHERE idLiniaComanda=%s',(idLiniaComanda,))

            db.commit()
            db.close()
            


            #obtenim valors per al html
            values = formulariComanda(usuari, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'comanda.html') 
            self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaLiniaComandaTots(cursor,idComanda):   
    cursor.execute('SELECT lc.idLiniaComanda, pr.idProducte, pr.codiProducte, pr.producte, lc.idComanda, lc.preuUnit, lc.quantitat, ti.tipoIva, ti.percent, pr.unitat, lc.idLot, ti.tipoRecarrec, ti.percentRecarrec FROM tipoiva ti INNER JOIN productes pr ON ti.idTipoIva=pr.idTipoIva INNER JOIN liniescomanda lc ON pr.idProducte = lc.idProducte WHERE lc.idComanda=%s',(idComanda,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        idLiniaComanda = i[0]
        idProducte = i[1]
        codiProducte = i[2]
        producte = i[3]
        idComanda = i[4]
        try:
            preuUnit=float(i[5])
        except:
            preuUnit=0
        try:
            quantitat = float(i[6])
        except:
            quantitat = 0
        try:
            tipoIva = float(i[7])
        except:
            tipoIva = 0
        try:
            tipoRecarrec = float(i[11])
        except:
            tipoRecarrec=0
        percent= i[8]
        percentRecarrec=i[12]
        unitat = i[9]
        idLot = i[10]
        preu = preuUnit*quantitat
        iva = preu*tipoIva
        preuTot= preu+iva
        recarrec= preu*tipoRecarrec
        preuTotRecarrec=preu+iva+recarrec
        
        preuUnitT = "%.2f" %preuUnit
        quantitatT = "%.3f" %quantitat
        preuT = "%.2f" %preu
        ivaT = "%.2f" %iva
        preuTotT = "%.2f" %preuTot
        recarrecT = "%.2f" %recarrec
        preuTotRecarrecT = "%.2f" %preuTotRecarrec
        
        
        
        lista[indice] = LiniaComanda(idLiniaComanda,idProducte,codiProducte,producte,idComanda,preuUnit,quantitat,tipoIva,percent,unitat, preu, iva, preuTot,preuUnitT, quantitatT, preuT, ivaT, preuTotT, idLot, recarrec, recarrecT, percentRecarrec, preuTotRecarrecT) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaLiniaComandaSelect(cursor, idLiniaComanda):
    cursor.execute('SELECT lc.idLiniaComanda, pr.idProducte, pr.codiProducte, pr.producte, lc.idComanda, lc.preuUnit, lc.quantitat, ti.tipoIva, ti.percent, pr.unitat, lc.idLot, ti.tipoRecarrec, ti.percentRecarrec FROM tipoiva ti INNER JOIN productes pr ON ti.idTipoIva=pr.idTipoIva INNER JOIN liniescomanda lc ON pr.idProducte = lc.idProducte WHERE lc.idLiniaComanda=%s',(idLiniaComanda,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        idLiniaComanda = i[0]
        idProducte = i[1]
        codiProducte = i[2]
        producte = i[3]
        idComanda = i[4]
        try:
            preuUnit=float(i[5])
        except:
            preuUnit=0
        try:
            quantitat = float(i[6])
        except:
            quantitat=0
        try:
            tipoIva = float(i[7])
        except:
            tipoIva=0
        try:
            tipoRecarrec = float(i[11])
        except:
            tipoRecarrec=0
        percent= i[8]
        percentRecarrec=i[12]
        unitat = i[9]
        idLot = i[10]
        preu = preuUnit*quantitat
        iva = preu*tipoIva
        preuTot= preu+iva
        recarrec= preu*tipoRecarrec
        preuTotRecarrec=preu+iva+recarrec
        
        preuUnitT = "%.2f" %preuUnit
        quantitatT = "%.3f" %quantitat
        preuT = "%.2f" %preu
        ivaT = "%.2f" %iva
        preuTotT = "%.2f" %preuTot
        recarrecT = "%.2f" %recarrec
        preuTotRecarrecT = "%.2f" %preuTotRecarrec

        
        
        lista = LiniaComanda(idLiniaComanda,idProducte,codiProducte,producte,idComanda,preuUnit,quantitat,tipoIva,percent,unitat, preu, iva, preuTot,preuUnitT, quantitatT, preuT, ivaT, preuTotT, idLot, recarrec, recarrecT, percentRecarrec, preuTotRecarrecT) #Modificar si anyadim columna 
    return lista 


class LiniaComanda:
    def __init__(self,idLiniaComanda,idProducte,codiProducte,producte,idComanda,preuUnit,quantitat,tipoIva,percent,unitat,preu, iva, preuTot,preuUnitT, quantitatT, preuT, ivaT, preuTotT, idLot, recarrec, recarrecT, percentRecarrec, preuTotRecarrecT):
        self.idLiniaComanda = idLiniaComanda
        self.idProducte = idProducte
        self.codiProducte = codiProducte
        self.producte = producte
        self.idComanda = idComanda
        self.preuUnit = preuUnit
        self.quantitat = quantitat
        self.tipoIva = tipoIva
        self.percent = percent
        self.unitat = unitat
        self.preu = preu
        self.iva = ivaT
        self.preuTot = preuTot
        self.preuUnitT = preuUnitT
        self.quantitatT = quantitatT
        self.preuT = preuT
        self.ivaT = ivaT
        self.preuTotT = preuTotT
        self.idLot = idLot
        self.recarrec = recarrec
        self.recarrecT = recarrecT
        self.percentRecarrec = percentRecarrec
        self.preuTotRecarrecT = preuTotRecarrecT
        
def tablaTotalComanda(cursor, idComanda):
    cursor.execute('SELECT  SUM(lc.preuUnit*lc.quantitat), SUM(ti.tipoIva*lc.preuUnit*lc.quantitat), SUM(ti.tipoRecarrec*lc.preuUnit*lc.quantitat) FROM tipoiva ti INNER JOIN productes pr ON pr.idTipoIva=ti.idTipoIva INNER JOIN liniescomanda lc ON pr.idProducte = lc.idProducte  WHERE lc.idComanda=%s',(idComanda,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        totalCom = i[0]
        ivaTotCom = i[1]
        recTotCom = i[2]
        try:
            totalCom = float(totalCom)
        except:
            totalCom =0
        try:
            ivaTotCom  = float(ivaTotCom)
        except:
            ivaTotCom = 0
        try:
            recTotCom  = float(recTotCom)
        except:
            recTotCom = 0
        
        totalFac = totalCom+ivaTotCom
        totalFacRec = totalCom+ivaTotCom+recTotCom

        
        totalSenseIva = "%.2f" %totalCom
        ivaTotComT = "%.2f" %ivaTotCom
        recTotComT = "%.2f" %recTotCom
        totalFactura = "%.2f" %totalFac
        totalFacturaRec = "%.2f" %totalFacRec
        
        
        lista = TotalComanda(idComanda,totalCom,ivaTotCom,totalFac,totalSenseIva,ivaTotComT,totalFactura,recTotCom, recTotComT, totalFacturaRec) #Modificar si anyadim columna 
    return lista  

class TotalComanda:
    def __init__(self,idComanda,totalCom,ivaTotCom,totalFac,totalSenseIva,ivaTotComT,totalFactura,recTotCom,recTotComT,totalFacturaRec):
        self.idComanda = idComanda  
        self.totalCom = totalCom
        self.ivaTotCom = ivaTotCom
        self.totalFac = totalFac
        self.totalSenseIva = totalSenseIva
        self.ivaTotComT = ivaTotComT
        self.totalFactura = totalFactura 
        self.recTotCom = recTotCom 
        self.recTotComT = recTotComT 
        self.totalFacturaRec = totalFacturaRec        


###########################################################################################################################################################
# PAGAMENT       PAGAMENT        PAGAMENT        PAGAMENT        PAGAMENT        PAGAMENT        PAGAMENT        PAGAMENT        PAGAMENT         
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariPagament (usuari, idPagament, idComanda):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    formaPagamentTots = tablaFormaPagamentTots(cursor)
    
    if idPagament == -1: #tots 
        pagamentSelect = ''
        pagamentTots = tablaPagamentTots(cursor, idComanda)
        
    else: # select
        pagamentSelect = tablaPagamentSelect(cursor,idPagament)
        pagamentTots = tablaPagamentTots(cursor, idComanda)
          
        
    producteTots= tablaProducteTots(cursor)
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idComanda': idComanda,
             'idPagament': idPagament,
             'pagamentSelect': pagamentSelect,
             'pagamentTots': pagamentTots,  
             'producteTots': producteTots, 
             'formaPagamentTots': formaPagamentTots 
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
                
class PagamentNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                idComanda= novar(self.request.get('idComanda'))
                #parametre
                idPagament = -1
            
                #obtenim valors per al html
                values = formulariPagament(usuari, idPagament, idComanda)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'pagament.html') 
                self.response.out.write(template.render(path, values,))

                
            
class PagamentSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idPagament = novar(self.request.get('idPagament'))
            idComanda= novar(self.request.get('idComanda'))
            

            #obtenim valors per al html
            values = formulariPagament(usuari, idPagament, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'pagament.html') 
            self.response.out.write(template.render(path, values,))

            

class PagamentEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idPagament = novar(self.request.get('idPagament'))
            idComanda= novar(self.request.get('idComanda'))
            dataPagament =novar(self.request.get('dataPagament'))
            quantitat = novar(self.request.get('quantitat'))
            idFormaPagament = novar(self.request.get('idFormaPagament'))
            descripcio = novar(self.request.get('descripcio'))
            
            

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                     
            cursor.execute('UPDATE pagaments SET idComanda=%s, dataPagament=%s, quantitat=%s, idFormaPagament=%s, descripcio=%s WHERE idPagament=%s', (idComanda, dataPagament, quantitat, idFormaPagament, descripcio, idPagament,))          
            
            db.commit()
            db.close()
            

            
            #obtenim valors per al html
            values = formulariPagament(usuari, idPagament, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'pagament.html') 
            self.response.out.write(template.render(path, values,))

class PagamentCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idComanda= novar(self.request.get('idComanda'))
            dataPagament =novar(self.request.get('dataPagament'))
            quantitat = novar(self.request.get('quantitat'))
            idFormaPagament = novar(self.request.get('idFormaPagament'))
            descripcio = novar(self.request.get('descripcio'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            

            cursor.execute('INSERT INTO pagaments (idComanda, dataPagament, quantitat, idFormaPagament, descripcio) VALUES (%s, %s, %s, %s, %s)', (idComanda, dataPagament, quantitat, idFormaPagament, descripcio))
      
            db.commit()
            db.close()

            
            #obtenim valors per al html
            values = formulariComanda(usuari, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'comanda.html') 
            self.response.out.write(template.render(path, values,))
            
class PagamentElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idComanda= novar(self.request.get('idComanda'))
            idPagament= novar(self.request.get('idPagament'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
                
            cursor.execute('DELETE FROM pagaments WHERE idPagament=%s',(idPagament,))

            db.commit()
            db.close()
            


            #obtenim valors per al html
            values = formulariComanda(usuari, idComanda)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'comanda.html') 
            self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaPagamentTots(cursor,idComanda):   
    cursor.execute('SELECT pa.idPagament, pa.idComanda, pa.dataPagament, pa.quantitat, pa.idFormaPagament, fp.formaPagament, pa.descripcio FROM formaPagament fp INNER JOIN pagaments pa ON fp.idFormaPagament = pa.idFormaPagament WHERE pa.idComanda=%s',(idComanda,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        idPagament = i[0]
        idComanda = i[1]
        dataPagament=dataFormat(i[2])
        try:
            quantitatN = float(i[3])
        except:
            quantitatN = 0
        idFormaPagament = i[4]
        formaPagament= i[5]
        descripcio = i[6]
            
        quantitat = "%.2f" %quantitatN
     
        lista[indice] = Pagament(idPagament,idComanda,dataPagament,quantitat, idFormaPagament, formaPagament, descripcio) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaPagamentSelect(cursor, idPagament):
    cursor.execute('SELECT pa.idPagament, pa.idComanda, pa.dataPagament, pa.quantitat, pa.idFormaPagament, fp.formaPagament, pa.descripcio FROM formaPagament fp INNER JOIN pagaments pa ON fp.idFormaPagament = pa.idFormaPagament WHERE pa.idPagament=%s',(idPagament,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        idPagament = i[0]
        idComanda = i[1]
        dataPagament=dataFormat(i[2])
        try:
            quantitatN = float(i[3])
        except:
            quantitatN = 0
        
        idFormaPagament = i[4]
        formaPagament= i[5]
        descripcio = i[6]
            
        quantitat = "%.2f" %quantitatN
        
        
        lista = Pagament(idPagament,idComanda,dataPagament,quantitat, idFormaPagament, formaPagament, descripcio)
        
        return lista 


class Pagament:
    def __init__(self,idPagament,idComanda,dataPagament,quantitat, idFormaPagament, formaPagament, descripcio):
        self.idPagament = idPagament
        self.idComanda = idComanda
        self.dataPagament = dataPagament
        self.quantitat = quantitat
        self.idFormaPagament = idFormaPagament
        self.formaPagament = formaPagament
        self.descripcio = descripcio
       
        
def tablaTotalPagament(cursor, idComanda):
    cursor.execute('SELECT  SUM(quantitat) FROM pagaments WHERE idComanda=%s',(idComanda,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        totalPagament = i[0]
        try:
            totalPagament = float(totalPagament)
        except:
            totalPagament =0

        
        totalPagament = "%.2f" %totalPagament

        
        return totalPagament  

def tablaFormaPagamentTots(cursor):   
    cursor.execute('SELECT idFormaPagament, formaPagament FROM formaPagament')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista    
        lista[indice] = FormaPagament(i[0],i[1]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

class FormaPagament:
    def __init__(self, idFormaPagament, formaPagament):
        self.idFormaPagament = idFormaPagament
        self.formaPagament = formaPagament
          

###########################################################################################################################################################
# IMP FACTURA          IMP FACTURA           IMP FACTURA          IMP FACTURA          IMP FACTURA          IMP FACTURA          IMP FACTURA          IMP FACTURA       
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariImpFactura (usuari, idComanda, esFactura):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    

    comandaSelect = tablaComandaSelect(cursor,idComanda)
    liniaComandaTots = tablaLiniaComandaTots(cursor, idComanda)
    
    clientTots = tablaClientTots(cursor)
    
    cursor.execute('SELECT idClient FROM comandes WHERE idComanda=%s',(idComanda,))
    lista = cursor.fetchall()
    idClient = lista[0][0]

        
    clientSelect=tablaClientSelect(cursor, idClient)
    
    totalComanda = tablaTotalComanda(cursor, idComanda)
    
    lotTots= tablaLotTots(cursor)
        
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idComanda': idComanda,
             'comandaSelect': comandaSelect,
             'clientTots': clientTots, 
             'liniaComandaTots': liniaComandaTots,  
             'esFactura': esFactura, 
             'totalComanda': totalComanda, 
             'clientSelect': clientSelect,
             'lotTots': lotTots, 
              }
    return values 

class ImpFactura (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                idComanda= novar(self.request.get('idComanda'))
                #parametre
                esFactura = 1
            
                #obtenim valors per al html
                values = formulariImpFactura(usuari, idComanda, esFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'facturaImp.html') 
                self.response.out.write(template.render(path, values,))
                
class ImpAlbara (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                idComanda= novar(self.request.get('idComanda'))
                #parametre
                esFactura = 0
            
                #obtenim valors per al html
                values = formulariImpFactura(usuari, idComanda, esFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'facturaImp.html') 
                self.response.out.write(template.render(path, values,))


class ImpFacturaRecarrec (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                idComanda= novar(self.request.get('idComanda'))
                #parametre
                esFactura = 1
            
                #obtenim valors per al html
                values = formulariImpFactura(usuari, idComanda, esFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'facturaImpRecarrec.html') 
                self.response.out.write(template.render(path, values,))

class ImpAlbaraRecarrec (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                idComanda= novar(self.request.get('idComanda'))
                #parametre
                esFactura = 0
            
                #obtenim valors per al html
                values = formulariImpFactura(usuari, idComanda, esFactura)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'facturaImpRecarrec.html') 
                self.response.out.write(template.render(path, values,))



###########################################################################################################################################################
# IMP ENVIAR           IMP ENVIAR              IMP ENVIAR           IMP ENVIAR           IMP ENVIAR           IMP ENVIAR           IMP ENVIAR      
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariImpEnviar (usuari, idComanda):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    

    comandaSelect = tablaComandaSelect(cursor,idComanda)
    
    
    cursor.execute('SELECT idClient FROM comandes WHERE idComanda=%s',(idComanda,))
    vector = cursor.fetchall()
    idClient = vector[0][0]
    clientSelect = tablaClientSelect(cursor, idClient)
    
    

        
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'comandaSelect': comandaSelect,
             'clientSelect': clientSelect,  
              }
    return values 

class ImpEnviar (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                idComanda= novar(self.request.get('idComanda'))
                #parametre
            
            
                #obtenim valors per al html
                values = formulariImpEnviar(usuari, idComanda)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'enviarImp.html') 
                self.response.out.write(template.render(path, values,))
                

###########################################################################################################################################################
#    FACTURES          FACTURES            FACTURES           FACTURES           FACTURES           FACTURES           FACTURES           FACTURES      
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariFactures (usuari):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)

    facturaTots= tablaFacturaTots(cursor)

    clientTots = tablaClientTots(cursor)
 
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'clientTots': clientTots, 
             'facturaTots': facturaTots,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class FacturaTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres

            
                #obtenim valors per al html
                values = formulariFactures(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'factures.html') 
                self.response.out.write(template.render(path, values,))
                

                
            


            


# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaFacturaTots(cursor):   
    cursor.execute('SELECT co.idComanda, co.idClient, co.numFactura, co.dataFactura, cl.nomClient, cl.cifClient, cl.direccioF, cl.direccioE FROM clients cl INNER JOIN comandes co ON cl.idClient = co.idClient WHERE numFactura IS NOT NULL')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        dataFactura=dataFormat(i[3])
        lista[indice] = Factura(i[0],i[1],i[2],dataFactura,i[4],i[5],i[6],i[7]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


class Factura:
    def __init__(self, idComanda, idClient, numFactura, dataFactura, nomClient, cifClient, direccioF, direccioE):
        self.idComanda = idComanda
        self.idClient = idClient
        self.numFactura = numFactura
        self.dataFactura = dataFactura
        self.nomClient = nomClient
        self.cifClient = cifClient
        self.direccioF = direccioF
        self.direccioE = direccioE
        

###########################################################################################################################################################
# LOTS        LOTS         LOTS        LOTS        LOTS        LOTS        LOTS        LOTS        LOTS        LOTS        LOTS        LOTS      
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariLot (usuari, idLot):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    
    lotSelect = ''
    lotTots = ''
    
    if idLot== -1: #tots intermediaris
        
        lotTots = tablaLotTots(cursor)
    elif idLot==-2:
        lotSelect = ''
        lotTots = ''   
    else: # select
        lotSelect = tablaLotSelect(cursor,idLot)
        lotTots = tablaLotTots(cursor)
    
    #ultim
    cursor.execute('SELECT codiLot, dataLot FROM lots ORDER BY codiLot DESC LIMIT 0,1')
    tabla = cursor.fetchall()
    if tabla:
        ultCodiLot = tabla[0][0]
        ultDataLot = dataFormat(tabla[0][1])
    else:
        ultCodiLot = '001 100512'
        ultDataLot = '2012-05-10'
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idLot': idLot,
             'lotSelect': lotSelect,
             'lotTots': lotTots,
             'ultCodiLot': ultCodiLot,
             'ultDataLot': ultDataLot,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class LotTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idLot = -1
            
                #obtenim valors per al html
                values = formulariLot(usuari, idLot)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'lot.html') 
                self.response.out.write(template.render(path, values,))
                
class LotNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idLot = -2
            
                #obtenim valors per al html
                values = formulariLot(usuari, idLot)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'lot.html') 
                self.response.out.write(template.render(path, values,))

                
            
class LotSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idLot= novar(self.request.get('idLot'))
            

            #obtenim valors per al html
            values = formulariLot(usuari, idLot)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'lot.html') 
            self.response.out.write(template.render(path, values,))

            

class LotEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idLot= novar(self.request.get('idLot'))
            codiLot = novar(self.request.get('codiLot'))
            lot = novar(self.request.get('lot'))
            dataLot = novar(self.request.get('dataLot'))
            titular = novar(self.request.get('titular'))
            receptor = novar(self.request.get('receptor'))
            descripcio = novar(self.request.get('descripcio'))

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                     
            cursor.execute('UPDATE lots SET codiLot=%s, lot=%s, dataLot=%s, titular=%s, receptor=%s, descripcio=%s WHERE idLot=%s', (codiLot, lot, dataLot, titular, receptor, descripcio, idLot,))          
            
            db.commit()
            db.close()
            

            
            #obtenim valors per al html
            values = formulariLot(usuari, idLot)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'lot.html') 
            self.response.out.write(template.render(path, values,))

class LotCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            codiLot = novar(self.request.get('codiLot'))
            lot = novar(self.request.get('lot'))
            dataLot = novar(self.request.get('dataLot'))
            titular = novar(self.request.get('titular'))
            receptor = novar(self.request.get('receptor'))
            descripcio = novar(self.request.get('descripcio'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            

            cursor.execute('INSERT INTO lots (codiLot, lot, dataLot, titular, receptor, descripcio) VALUES (%s, %s, %s, %s, %s, %s)', (codiLot, lot, dataLot, titular, receptor, descripcio,))
            cursor.execute('SELECT idLot FROM lots ORDER BY idLot DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idLot = lista[0][0]        
            db.commit()
            db.close()

            idLot = -1
            
            #obtenim valors per al html
            values = formulariLot(usuari, idLot)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'lot.html') 
            self.response.out.write(template.render(path, values,))
            
class LotElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idLot= novar(self.request.get('idLot'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
 
            cursor.execute('DELETE FROM lots WHERE idLot=%s',(idLot,))
    
            db.commit()
            db.close()
                
            idLot = -1
    
            #obtenim valors per al html
            values = formulariLot(usuari, idLot)
    
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'lot.html') 
            self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaLotTots(cursor):   
    cursor.execute('SELECT idLot, codiLot, lot, dataLot, titular, receptor, descripcio FROM lots ORDER BY codiLot DESC')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        dataLot=dataFormat(i[3])
        lista[indice] = Lot(i[0],i[1],i[2],dataLot,i[4],i[5],i[6]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaLotSelect(cursor, idLot):
    cursor.execute('SELECT idLot, codiLot, lot, dataLot, titular, receptor, descripcio FROM lots WHERE idLot=%s',(idLot,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        dataLot=dataFormat(i[3])
        lista = Lot(i[0],i[1],i[2],dataLot,i[4],i[5],i[6]) #Modificar si anyadim columna 
    return lista 


class Lot:
    def __init__(self, idLot, codiLot, lot, dataLot, titular, receptor, descripcio):
        self.idLot = idLot
        self.codiLot = codiLot
        self.lot = lot
        self.dataLot = dataLot
        self.titular = titular
        self.receptor = receptor
        self.descripcio = descripcio

###########################################################################################################################################################
# IMP LOT         IMP LOT         IMP LOT        IMP LOT        IMP LOT        IMP LOT        IMP LOT        IMP LOT              
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariImpLot (usuari):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    

    lotTots = tablaLotTots(cursor)

    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'lotTots': lotTots, 
              }
    return values 

class ImpLot (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                
                #parametre
            
            
                #obtenim valors per al html
                values = formulariImpLot(usuari)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'lotImp.html') 
                self.response.out.write(template.render(path, values,))
                

        
###########################################################################################################################################################
#     FINQUES         FINQUES            FINQUES           FINQUES           FINQUES           FINQUES           FINQUES           FINQUES    
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariFinca (usuari, idFinca):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    
    fincaSelect = ''
    fincaTots = ''
    
    if idFinca== -1: #tots intermediaris
        
        fincaTots = tablaFincaTots(cursor)
    elif idFinca==-2:
        fincaSelect = ''
        fincaTots = ''   
    else: # select
        fincaSelect = tablaFincaSelect(cursor,idFinca)
        fincaTots = tablaFincaTots(cursor)
    
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idFinca': idFinca,
             'fincaSelect': fincaSelect,
             'fincaTots': fincaTots,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class FincaTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idFinca = -1
            
                #obtenim valors per al html
                values = formulariFinca(usuari, idFinca)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'finca.html') 
                self.response.out.write(template.render(path, values,))
                
class FincaNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idFinca = -2
            
                #obtenim valors per al html
                values = formulariFinca(usuari, idFinca)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'finca.html') 
                self.response.out.write(template.render(path, values,))

                
            
class FincaSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idFinca= novar(self.request.get('idFinca'))
            

            #obtenim valors per al html
            values = formulariFinca(usuari, idFinca)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'finca.html') 
            self.response.out.write(template.render(path, values,))

            

class FincaEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idFinca= novar(self.request.get('idFinca'))
            codiFinca = novar(self.request.get('codiFinca'))
            finca = novar(self.request.get('finca'))
            superficie = novar(self.request.get('superficie'))
            refCatastral = novar(self.request.get('refCatastral'))

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                     
            cursor.execute('UPDATE finques SET codiFinca=%s, finca=%s, superficie=%s, refCatastral=%s WHERE idFinca=%s', (codiFinca, finca, superficie, refCatastral, idFinca,))          
            
            db.commit()
            db.close()
            

            
            #obtenim valors per al html
            values = formulariFinca(usuari, idFinca)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'finca.html') 
            self.response.out.write(template.render(path, values,))

class FincaCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            codiFinca = novar(self.request.get('codiFinca'))
            finca = novar(self.request.get('finca'))
            superficie = novar(self.request.get('superficie'))
            refCatastral = novar(self.request.get('refCatastral'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            

            cursor.execute('INSERT INTO finques (codiFinca, finca, superficie, refCatastral) VALUES (%s, %s, %s, %s)', (codiFinca, finca, superficie, refCatastral,))
            cursor.execute('SELECT idFinca FROM finques ORDER BY idFinca DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idFinca = lista[0][0]        
            db.commit()
            db.close()

            idFinca = -1
            
            #obtenim valors per al html
            values = formulariFinca(usuari, idFinca)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'finca.html') 
            self.response.out.write(template.render(path, values,))
            
class FincaElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idFinca= novar(self.request.get('idFinca'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('SELECT idFinca FROM produccio WHERE idFinca=%s',(idFinca,))
            lista = cursor.fetchall()
            if lista:
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                db.commit()
                db.close()
                error = "Esta finca te linies de produccio"
                values = {
                             'treballadorSelect': treballadorSelect,
                             'error': error,         
                              }
                path = os.path.join(os.path.dirname(__file__), 'error.html') 
                self.response.out.write(template.render(path, values,))
            
            else:
 
                cursor.execute('DELETE FROM finques WHERE idFinca=%s',(idFinca,))
        
                db.commit()
                db.close()
                    
                idFinca = -1
        
                #obtenim valors per al html
                values = formulariFinca(usuari, idFinca)
        
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'finca.html') 
                self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaFincaTots(cursor):   
    cursor.execute('SELECT idFinca, codiFinca, finca, superficie, refCatastral FROM finques ORDER BY codiFinca')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Finca(i[0],i[1],i[2],i[3],i[4]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaFincaSelect(cursor, idFinca):
    cursor.execute('SELECT idFinca, codiFinca, finca, superficie, refCatastral FROM finques WHERE idFinca=%s',(idFinca,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = Finca(i[0],i[1],i[2],i[3],i[4]) #Modificar si anyadim columna 
    return lista 


class Finca:
    def __init__(self, idFinca, codiFinca, finca, superficie, refCatastral):
        self.idFinca = idFinca
        self.codiFinca = codiFinca
        self.finca = finca
        self.superficie = superficie
        self.refCatastral = refCatastral

###########################################################################################################################################################
#     VARIETAT           VARIETAT           VARIETAT           VARIETAT           VARIETAT           VARIETAT           VARIETAT    
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariVarietat (usuari, idVarietat):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    
    varietatSelect = ''
    varietatTots = ''
    
    if idVarietat== -1: #tots 
        
        varietatTots = tablaVarietatTots(cursor)
    elif idVarietat==-2:
        varietatSelect = ''
        varietatTots = ''   
    else: # select
        varietatSelect = tablaVarietatSelect(cursor,idVarietat)
        varietatTots = tablaVarietatTots(cursor)
    
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idVarietat': idVarietat,
             'varietatSelect': varietatSelect,
             'varietatTots': varietatTots,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class VarietatTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idVarietat = -1
            
                #obtenim valors per al html
                values = formulariVarietat(usuari, idVarietat)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'varietat.html') 
                self.response.out.write(template.render(path, values,))
                
class VarietatNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idVarietat = -2
            
                #obtenim valors per al html
                values = formulariVarietat(usuari, idVarietat)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'varietat.html') 
                self.response.out.write(template.render(path, values,))

                
            
class VarietatSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idVarietat= novar(self.request.get('idVarietat'))
            

            #obtenim valors per al html
            values = formulariVarietat(usuari, idVarietat)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'varietat.html') 
            self.response.out.write(template.render(path, values,))

            

class VarietatEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idVarietat= novar(self.request.get('idVarietat'))
            varietat = novar(self.request.get('varietat'))

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                     
            cursor.execute('UPDATE trufes SET varietat=%s WHERE idTrufa=%s', (varietat, idVarietat,))          
            
            db.commit()
            db.close()
            

            
            #obtenim valors per al html
            values = formulariVarietat(usuari, idVarietat)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'varietat.html') 
            self.response.out.write(template.render(path, values,))

class VarietatCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            varietat = novar(self.request.get('varietat'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            

            cursor.execute('INSERT INTO trufes (varietat) VALUES (%s)', (varietat,))
     
            db.commit()
            db.close()

            idVarietat = -1
            
            #obtenim valors per al html
            values = formulariVarietat(usuari, idVarietat)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'varietat.html') 
            self.response.out.write(template.render(path, values,))
            
class VarietatElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idVarietat= novar(self.request.get('idVarietat'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('SELECT idTrufa FROM produccio WHERE idTrufa=%s',(idVarietat,))
            lista = cursor.fetchall()
            if lista:
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                db.commit()
                db.close()
                error = "Esta varietat te linies de produccio"
                values = {
                             'treballadorSelect': treballadorSelect,
                             'error': error,         
                              }
                path = os.path.join(os.path.dirname(__file__), 'error.html') 
                self.response.out.write(template.render(path, values,))
            
            else:
 
                cursor.execute('DELETE FROM trufes WHERE idTrufa=%s',(idVarietat,))
        
                db.commit()
                db.close()
                    
                idVarietat = -1
        
                #obtenim valors per al html
                values = formulariVarietat(usuari, idVarietat)
        
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'varietat.html') 
                self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaVarietatTots(cursor):   
    cursor.execute('SELECT idTrufa, varietat FROM trufes')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Varietat(i[0],i[1]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 



def tablaVarietatSelect(cursor, idVarietat):
    cursor.execute('SELECT idTrufa, varietat FROM trufes WHERE idTrufa=%s',(idVarietat,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = Varietat(i[0],i[1]) #Modificar si anyadim columna 
    return lista 


class Varietat:
    def __init__(self, idVarietat, varietat):
        self.idVarietat = idVarietat
        self.varietat = varietat

###########################################################################################################################################################
#     PRODUCCIO        PRODUCCIO         PRODUCCIO        PRODUCCIO        PRODUCCIO        PRODUCCIO        PRODUCCIO        PRODUCCIO  
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariProduccio (usuari, idProduccio, idVarietat):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    
    produccioSelect = ''
    produccioTots = ''
    fincaTots = tablaFincaTots(cursor)
    trufaTots = tablaTrufaTots(cursor)
    varietatSelect =''
    numeroUltim=''
    
    if idProduccio== -1: #tots 
        produccioTots = tablaProduccioQuadern(cursor, idVarietat)
        varietatSelect = tablaVarietatSelect(cursor, idVarietat)
    elif idProduccio==-2:
        cursor.execute('SELECT numero FROM produccio WHERE idTrufa=%s ORDER BY idProduccio DESC LIMIT 0,1',(idVarietat,))
        linia = cursor.fetchall()
        try:
            numeroUltim = linia[0][0]
        except:
            numeroUltim = 0
        produccioSelect = ''
        produccioTots = ''
        varietatSelect = tablaVarietatSelect(cursor, idVarietat)
    elif idProduccio==-3:
        produccioSelect = ''
        produccioTots = ''   
    else: # select
        produccioSelect = tablaProduccioSelect(cursor,idProduccio)
        produccioTots = tablaProduccioTots(cursor)
        varietatSelect = tablaVarietatSelect(cursor, idVarietat)
    
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idProduccio': idProduccio,
             'idVarietat': idVarietat,
             'varietatSelect': varietatSelect,
             'produccioSelect': produccioSelect,
             'produccioTots': produccioTots,
             'fincaTots': fincaTots,
             'trufaTots': trufaTots,
             'numeroUltim': numeroUltim,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class ProduccioElegir (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idProduccio = -3
                idVarietat = -1
            
                #obtenim valors per al html
                values = formulariProduccio(usuari, idProduccio, idVarietat)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'produccio.html') 
                self.response.out.write(template.render(path, values,))

class ProduccioQuadernSelect (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idProduccio = -1

                #captura del html
                idVarietat= novar(self.request.get('idVarietat'))
            
                #obtenim valors per al html
                values = formulariProduccio(usuari, idProduccio, idVarietat)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'produccio.html') 
                self.response.out.write(template.render(path, values,))
class ProduccioQuadernSelectGet (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idProduccio = -1

                #captura del html
                idVarietat= novar(self.request.get('idVarietat'))
            
                #obtenim valors per al html
                values = formulariProduccio(usuari, idProduccio, idVarietat)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'produccio.html') 
                self.response.out.write(template.render(path, values,))

class ProduccioTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idProduccio = -1
                idVarietat= novar(self.request.get('idVarietat'))
            
                #obtenim valors per al html
                values = formulariProduccio(usuari, idProduccio, idVarietat)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'produccio.html') 
                self.response.out.write(template.render(path, values,))
                
class ProduccioNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idProduccio = -2
                idVarietat= novar(self.request.get('idVarietat'))
            
                #obtenim valors per al html
                values = formulariProduccio(usuari, idProduccio, idVarietat)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'produccio.html') 
                self.response.out.write(template.render(path, values,))

                
            
class ProduccioSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idProduccio= novar(self.request.get('idProduccio'))
            idVarietat = novar(self.request.get('idVarietat'))
            

            #obtenim valors per al html
            values = formulariProduccio(usuari, idProduccio, idVarietat)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'produccio.html') 
            self.response.out.write(template.render(path, values,))

            

class ProduccioEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idProduccio= novar(self.request.get('idProduccio'))
            idFinca = novar(self.request.get('idFinca'))
            idVarietat = novar(self.request.get('idVarietat'))
            quantitat = novar(self.request.get('quantitat'))
            data = novar(self.request.get('data'))
            numero = novar(self.request.get('numero'))
            quantitatU = novar(self.request.get('quantitatU'))
            quantitatE = novar(self.request.get('quantitatE'))
            lotE = novar(self.request.get('lotE'))

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                     
            cursor.execute('UPDATE produccio SET idFinca=%s, idTrufa=%s, quantitat=%s, data=%s, numero=%s, quantitatU=%s, quantitatE=%s, lotE=%s WHERE idProduccio=%s', (idFinca, idVarietat, quantitat, data, numero, quantitatU, quantitatE, lotE, idProduccio,))          
            
            db.commit()
            db.close()
            

            
            #obtenim valors per al html
            values = formulariProduccio(usuari, idProduccio, idVarietat)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'produccio.html') 
            self.response.out.write(template.render(path, values,))

class ProduccioCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idFinca = novar(self.request.get('idFinca'))
            idVarietat = novar(self.request.get('idVarietat'))
            quantitat = novar(self.request.get('quantitat'))
            data = novar(self.request.get('data'))
            numero = novar(self.request.get('numero'))
            quantitatU = novar(self.request.get('quantitatU'))
            quantitatE = novar(self.request.get('quantitatE'))
            lotE = novar(self.request.get('lotE'))
            
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            

            cursor.execute('INSERT INTO produccio (idFinca, idTrufa, quantitat, data, numero, quantitatU, quantitatE, lotE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (idFinca, idVarietat, quantitat, data, numero, quantitatU, quantitatE, lotE))
                   
            db.commit()
            db.close()

            idProduccio = -1
            
            #obtenim valors per al html
            values = formulariProduccio(usuari, idProduccio, idVarietat)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'produccio.html') 
            self.response.out.write(template.render(path, values,))
            
class ProduccioElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idProduccio= novar(self.request.get('idProduccio'))
            idVarietat = novar(self.request.get('idVarietat'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
 
            cursor.execute('DELETE FROM produccio WHERE idProduccio=%s',(idProduccio,))
    
            db.commit()
            db.close()
                
            idProduccio = -1
    
            #obtenim valors per al html
            values = formulariProduccio(usuari, idProduccio, idVarietat)
    
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'produccio.html') 
            self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaProduccioTots(cursor):   
    cursor.execute('SELECT pr.idProduccio, pr.idFinca, pr.idTrufa, pr.quantitat, pr.data, tr.varietat, fi.finca, fi.codiFinca, pr.numero, pr.quantitatU, pr.quantitatE, pr.lotE FROM finques fi INNER JOIN ( trufes tr INNER JOIN produccio pr ON pr.idTrufa=tr.idTrufa) ON fi.idFinca=pr.idFinca')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[4])
        lista[indice] = Produccio(i[0],i[1],i[2],i[3],data,i[5],i[6],i[7],i[8],i[9],i[10],i[11]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

def tablaProduccioQuadern(cursor, idVarietat):   
    cursor.execute('SELECT pr.idProduccio, pr.idFinca, pr.idTrufa, pr.quantitat, pr.data, tr.varietat, fi.finca, fi.codiFinca, pr.numero, pr.quantitatU, pr.quantitatE, pr.lotE FROM finques fi INNER JOIN ( trufes tr INNER JOIN produccio pr ON pr.idTrufa=tr.idTrufa) ON fi.idFinca=pr.idFinca WHERE pr.idTrufa=%s ORDER BY idProduccio DESC',(idVarietat,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[4])
        lista[indice] = Produccio(i[0],i[1],i[2],i[3],data,i[5],i[6],i[7],i[8],i[9],i[10],i[11]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaProduccioSelect(cursor, idProduccio):
    cursor.execute('SELECT pr.idProduccio, pr.idFinca, pr.idTrufa, pr.quantitat, pr.data, tr.varietat, fi.finca, fi.codiFinca, pr.numero, pr.quantitatU, pr.quantitatE, pr.lotE FROM finques fi INNER JOIN ( trufes tr INNER JOIN produccio pr ON pr.idTrufa=tr.idTrufa) ON fi.idFinca=pr.idFinca WHERE pr.idProduccio=%s',(idProduccio,))
    tabla = cursor.fetchall()
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[4])
        lista = Produccio(i[0],i[1],i[2],i[3],data,i[5],i[6],i[7],i[8],i[9],i[10],i[11]) #Modificar si anyadim columna 
    return lista 


class Produccio:
    def __init__(self, idProduccio, idFinca, idTrufa, quantitat, data, varietat, finca, codiFinca, numero, quantitatU, quantitatE, lotE):
        self.idProduccio = idProduccio
        self.idFinca = idFinca
        self.idTrufa = idTrufa
        self.quantitat = quantitat
        self.data = data
        self.varietat = varietat
        self.finca = Finca
        self.codiFinca = codiFinca
        self.numero = numero
        self.quantitatU = quantitatU
        self.quantitatE = quantitatE
        self.lotE = lotE

def tablaTrufaTots(cursor):   
    cursor.execute('SELECT idTrufa, varietat FROM trufes')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Trufa(i[0],i[1]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

class Trufa:
    def __init__(self, idTrufa, varietat):
        self.idTrufa = idTrufa
        self.varietat = varietat

###########################################################################################################################################################
# IMP PRODUCCIO           IMP PRODUCCIO           IMP PRODUCCIO           IMP PRODUCCIO           IMP PRODUCCIO           IMP PRODUCCIO           IMP PRODUCCIO            
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariImpProduccio (usuari, idVarietat):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    

    quadernTots = tablaProduccioQuadern(cursor, idVarietat)
    varietatSelect = tablaVarietatSelect(cursor, idVarietat)

    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'quadernTots': quadernTots,
             'varietatSelect': varietatSelect,
              }
    return values 

class ImpProduccio (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                idVarietat = novar(self.request.get('idVarietat'))

                #parametre
            
            
                #obtenim valors per al html
                values = formulariImpProduccio(usuari, idVarietat)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'quadernImp.html') 
                self.response.out.write(template.render(path, values,))



###########################################################################################################################################################
# PRODUCTOR              PRODUCTOR                PRODUCTOR               PRODUCTOR               PRODUCTOR               PRODUCTOR         
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariProductor (usuari, idProductor):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    
    if idProductor== -1: #tots 
        productorSelect = ''
        productorTots = tablaProductorTots(cursor)
        
    elif idProductor==-2:
        productorSelect = ''
        productorTots = ''
        
    else: # select
        productorSelect = tablaProductorSelect(cursor,idProductor)
        productorTots = tablaProductorTots(cursor)
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idProductor': idProductor,
             'productorSelect': productorSelect,
             'productorTots': productorTots,          
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class ProductorTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idProductor = -1
            
                #obtenim valors per al html
                values = formulariProductor(usuari, idProductor)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'productor.html') 
                self.response.out.write(template.render(path, values,))
                
class ProductorNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idProductor = -2
            
                #obtenim valors per al html
                values = formulariProductor(usuari, idProductor)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'productor.html') 
                self.response.out.write(template.render(path, values,))

                
            
class ProductorSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idProductor= novar(self.request.get('idProductor'))
            

            #obtenim valors per al html
            values = formulariProductor(usuari, idProductor)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'productor.html') 
            self.response.out.write(template.render(path, values,))

            

class ProductorEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idProductor= novar(self.request.get('idProductor'))
            nomProductor = novar(self.request.get('nomProductor'))
            direccioF = novar(self.request.get('direccioF'))
            cifProductor = novar(self.request.get('cifProductor'))
            nomComercial = novar(self.request.get('nomComercial'))
            descripcio = novar(self.request.get('descripcio'))
          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT cifProductor FROM productors WHERE idProductor=%s',(idProductor,))
            cifANT = cursor.fetchall()
            cifANT = cifANT [0][0]
            cifNOU = cifProductor
            
            cursor.execute('SELECT cifProductor FROM productors WHERE cifProductor=%s',(cifProductor,))
            cifs = cursor.fetchall()

            if cifs:
                if cifANT == cifNOU:
                    cursor.execute('UPDATE productors SET nomProductor=%s, direccioF=%s, cifProductor=%s, nomComercial=%s, descripcio=%s WHERE idProductor=%s', (nomProductor, direccioF, cifProductor, nomComercial, descripcio, idProductor,))          
                    db.commit()
                    db.close()
                else:                    
                    db.commit()
                    db.close()
                    values = formulariInicio(usuari)
                    path = os.path.join(os.path.dirname(__file__), 'productorDuplicat.html') 
                    self.response.out.write(template.render(path, values,))
            else:                       
                cursor.execute('UPDATE productors SET nomProductor=%s, direccioF=%s, cifProductor=%s, nomComercial=%s, descripcio=%s WHERE idProductor=%s', (nomProductor, direccioF, cifProductor, nomComercial,descripcio, idProductor,))          
                db.commit()
                db.close()
            

            
            #obtenim valors per al html
            values = formulariProductor(usuari, idProductor)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'productor.html') 
            self.response.out.write(template.render(path, values,))

class ProductorCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            nomProductor = novar(self.request.get('nomProductor'))
            direccioF = novar(self.request.get('direccioF'))
            cifProductor = novar(self.request.get('cifProductor'))
            nomComercial = novar(self.request.get('nomComercial'))
            descripcio = novar(self.request.get('descripcio'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('SELECT cifProductor FROM productors WHERE cifProductor=%s',(cifProductor,))
            cifs = cursor.fetchall()
            
            if cifs:
                db.commit()
                db.close()
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                db.commit()
                db.close()
                error = "Este CIF ja existeix"
                values = {
                             'treballadorSelect': treballadorSelect,
                             'error': error,         
                              }
                path = os.path.join(os.path.dirname(__file__), 'error.html') 
                self.response.out.write(template.render(path, values,))
            else:
                cursor.execute('INSERT INTO productors (nomProductor, direccioF, cifProductor, nomComercial, descripcio) VALUES (%s, %s, %s, %s, %s)', (nomProductor, direccioF, cifProductor, nomComercial, descripcio))
                cursor.execute('SELECT idProductor FROM productors ORDER BY idProductor DESC LIMIT 0,1')
                lista = cursor.fetchall()
                idProductor = lista[0][0]        
                db.commit()
                db.close()

                idProductor = -1
                
                #obtenim valors per al html
                values = formulariProductor(usuari, idProductor)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'productor.html') 
                self.response.out.write(template.render(path, values,))
            
class ProductorElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idProductor= novar(self.request.get('idProductor'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            cursor.execute('SELECT idProductor FROM fcompra WHERE idProductor=%s',(idProductor,))
            lista = cursor.fetchall()
            if lista:
                treballadorSelect=tablaTreballadorSelect(cursor,usuari)
                db.commit()
                db.close()
                error = "Este productor esta en alguna factura de compra"
                values = {
                             'treballadorSelect': treballadorSelect,
                             'error': error,         
                              }
                path = os.path.join(os.path.dirname(__file__), 'error.html') 
                self.response.out.write(template.render(path, values,))

            else:
                cursor.execute('DELETE FROM productors WHERE idProductor=%s',(idProductor,))

                db.commit()
                db.close()
                
                idProductor=-1
            

                #obtenim valors per al html
                values = formulariProductor(usuari, idProductor)
    
                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'productor.html') 
                self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaProductorTots(cursor):   
    cursor.execute('SELECT idProductor, nomProductor, direccioF, cifProductor, nomComercial, descripcio FROM productors ORDER BY nomProductor')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        cifProductor=noimp(i[3])
        direccioF=noimp(i[2])
        lista[indice] = Productor(i[0],i[1],direccioF,cifProductor,i[4],i[5]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaProductorSelect(cursor, idProductor):
    cursor.execute('SELECT idProductor, nomProductor, direccioF, cifProductor, nomComercial, descripcio  FROM productors WHERE idProductor=%s',(idProductor,))
    tabla = cursor.fetchall()
    
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista = Productor(i[0],i[1],i[2],i[3],i[4],i[5]) #Modificar si anyadim columna 
    return lista 


class Productor:
    def __init__(self, idProductor, nomProductor, direccioF, cifProductor, nomComercial, descripcio):
        self.idProductor = idProductor
        self.nomProductor = nomProductor
        self.direccioF = direccioF
        self.cifProductor = cifProductor
        self.nomComercial = nomComercial
        self.descripcio = descripcio


###########################################################################################################################################################
# FACTURA COMPRA         FACTURA COMPRA         FACTURA COMPRA         FACTURA COMPRA         FACTURA COMPRA          
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariFCompra (usuari, idFCompra):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    productorTots= tablaProductorTots(cursor)
    
    if idFCompra== -1: #tots 
        fcompraSelect = ''
        fcompraTots = tablaFCompraTots(cursor)
        
    elif idFCompra==-2:
        fcompraSelect = ''
        fcompraTots = ''
        
    else: # select
        fcompraSelect = tablaFCompraSelect(cursor,idFCompra)
        fcompraTots = tablaFCompraTots(cursor)
    
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')

    #ultima comanda
    cursor.execute('SELECT numFCompra, dataFCompra FROM fcompra WHERE numFCompra<>%s ORDER BY numFCompra DESC LIMIT 0,1',('None',))
    fcompra = cursor.fetchall()
    
    #desconectar de la bd
    db.commit()
    db.close()
    
    if fcompra:
        ultNumFCompra = fcompra[0][0]
        ultDataFCompra = dataFormat(fcompra[0][1])
    else:
        ultNumFCompra = 'FC20/000'
        ultDataFCompra = '2020-01-01'
    
    #comanda seguent
    fcompraS=fcompraSeguent(ultNumFCompra)

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idFCompra': idFCompra,
             'fcompraSelect': fcompraSelect,
             'fcompraTots': fcompraTots, 
             'productorTots': productorTots,   
             'dataHui': dataHui,
             'ultNumFCompra': ultNumFCompra,
             'ultDataFCompra': ultDataFCompra,
             'fcompraS': fcompraS,
                    
              }
    return values   

# ACCIONS DEL FORMULARI
####################################
class FCompraTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idFCompra = -1
            
                #obtenim valors per al html
                values = formulariFCompra(usuari, idFCompra)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'fcompra.html') 
                self.response.out.write(template.render(path, values,))
                
class FCompraNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #parametres
                idFCompra = -2
            
                #obtenim valors per al html
                values = formulariFCompra(usuari, idFCompra)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'fcompra.html') 
                self.response.out.write(template.render(path, values,))

                
            
class FCompraSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idFCompra= novar(self.request.get('idFCompra'))
            

            #obtenim valors per al html
            values = formulariFCompra(usuari, idFCompra)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'fcompra.html') 
            self.response.out.write(template.render(path, values,))

            

class FCompraEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idFCompra= novar(self.request.get('idFCompra'))
            idProductor= novar(self.request.get('idProductor'))
            numFCompra= novar(self.request.get('numFCompra'))
            dataFCompra= novar(self.request.get('dataFCompra'))
            producte1= novar(self.request.get('producte1'))
            preuUnit1= novar(self.request.get('preuUnit1'))
            unitat1= novar(self.request.get('unitat1'))
            quantitat1 = novar(self.request.get('quantitat1'))
            producte2= novar(self.request.get('producte2'))
            preuUnit2= novar(self.request.get('preuUnit2'))
            unitat2= novar(self.request.get('unitat2'))
            quantitat2 = novar(self.request.get('quantitat2'))
            producte3= novar(self.request.get('producte3'))
            preuUnit3= novar(self.request.get('preuUnit3'))
            unitat3= novar(self.request.get('unitat3'))
            quantitat3 = novar(self.request.get('quantitat3'))
            

          
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
                  
            cursor.execute('UPDATE fcompra SET idProductor=%s, numFCompra=%s, dataFCompra=%s, producte1=%s, preuUnit1=%s, unitat1=%s, quantitat1=%s, producte2=%s, preuUnit2=%s, unitat2=%s, quantitat2, producte3=%s, preuUnit3=%s, unitat3=%s, quantitat3  WHERE idFCompra=%s', (idProductor, numFCompra, dataFCompra, producte1, preuUnit1, unitat1, quantitat1,  producte2, preuUnit2, unitat2, quantitat2,  producte3, preuUnit3, unitat3, quantitat3, idFCompra))          
            
            db.commit()
            db.close()
            

            
            #obtenim valors per al html
            values = formulariFCompra(usuari, idFCompra)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'fcompra.html') 
            self.response.out.write(template.render(path, values,))

class FCompraCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idProductor= novar(self.request.get('idProductor'))
            numFCompra= novar(self.request.get('numFCompra'))
            dataFCompra= novar(self.request.get('dataFCompra'))
            producte1= novar(self.request.get('producte1'))
            preuUnit1= novar(self.request.get('preuUnit1'))
            unitat1= novar(self.request.get('unitat1'))
            quantitat1 = novar(self.request.get('quantitat1'))
            producte2= novar(self.request.get('producte2'))
            preuUnit2= novar(self.request.get('preuUnit2'))
            unitat2= novar(self.request.get('unitat2'))
            quantitat2 = novar(self.request.get('quantitat2'))
            producte3= novar(self.request.get('producte3'))
            preuUnit3= novar(self.request.get('preuUnit3'))
            unitat3= novar(self.request.get('unitat3'))
            quantitat3 = novar(self.request.get('quantitat3'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()

            cursor.execute('INSERT INTO fcompra (idProductor, numFCompra, dataFCompra, producte1, preuUnit1, unitat1, quantitat1, producte2, preuUnit2, unitat2, quantitat2, producte3, preuUnit3, unitat3, quantitat3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (idProductor, numFCompra, dataFCompra, producte1, preuUnit1, unitat1, quantitat1,  producte2, preuUnit2, unitat2, quantitat2,  producte3, preuUnit3, unitat3, quantitat3))
            cursor.execute('SELECT idFCompra FROM fcompra ORDER BY idFCompra DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idFCompra = lista[0][0]        
            db.commit()
            db.close()

            idFCompra = -1
                
            #obtenim valors per al html
            values = formulariFCompra(usuari, idFCompra)
    
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'fcompra.html') 
            self.response.out.write(template.render(path, values,))
            
class FCompraElimina (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idFCompra= novar(self.request.get('idFCompra'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()

            cursor.execute('DELETE FROM fcompra WHERE idFCompra=%s',(idFCompra,))

            db.commit()
            db.close()
                
            idFCompra=-1
            

            #obtenim valors per al html
            values = formulariFCompra(usuari, idFCompra)
    
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'fcompra.html') 
            self.response.out.write(template.render(path, values,))

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaFCompraTots(cursor): 
    tipoIva=0.12 #TIPO IVA AGRICULTOR  
    tipoRet=0.02 #TIPO Retencion AGRICULTOR 
    cursor.execute('SELECT fc.idFCompra, fc.idProductor, fc.numFCompra, fc.dataFCompra, fc.producte1, fc.preuUnit1, fc.unitat1, fc.quantitat1, fc.producte2, fc.preuUnit2, fc.unitat2, fc.quantitat2, fc.producte3, fc.preuUnit3, fc.unitat3, fc.quantitat3, pr.nomProductor, pr.nomComercial, pr.direccioF, pr.cifProductor FROM productors pr INNER JOIN fcompra fc ON fc.idProductor= pr.idProductor ORDER BY fc.numFCompra DESC')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        preu1=0
        preu2=0
        preu3=0
        idFCompra=i[0]
        idProductor=i[1]
        numFCompra=i[2]       
        dataFCompra=dataFormat(i[3])
        producte1=i[4]
        try:
            preuUnit1=float(i[5])
        except:
            preuUnit1=0
        unitat1=i[6]
        try:
            quantitat1 = float(i[7])
        except:
            quantitat1=0
            
        preu1 = preuUnit1*quantitat1
        iva1 = preu1*tipoIva
        preuTot1= preu1+iva1
        
        preuUnitT1 = "%.2f" %preuUnit1
        quantitatT1 = "%.3f" %quantitat1
        preuT1 = "%.2f" %preu1
        preuTotT1 = "%.2f" %preuTot1
        
        producte2=i[8]
        
        try:
            preuUnit2=float(i[9])
        except:
            preuUnit2=0
        unitat2=i[10]
        try:
            quantitat2 = float(i[11])
        except:
            quantitat2=0
        
        preu2 = preuUnit2*quantitat2
        iva2 = preu2*tipoIva
        preuTot2= preu2+iva2
        
        preuUnitT2 = "%.2f" %preuUnit2
        quantitatT2 = "%.3f" %quantitat2
        preuT2 = "%.2f" %preu2
        preuTotT2 = "%.2f" %preuTot2
        
        producte3=i[12]
        try:
            preuUnit3=float(i[13])
        except:
            preuUnit3=0
        unitat3=i[14]
        try:
            quantitat3 = float(i[15])
        except:
            quantitat3=0
            
        preu3 = preuUnit3*quantitat3
        iva3 = preu3*tipoIva
        preuTot3= preu3+iva3
        
        preuUnitT3 = "%.2f" %preuUnit3
        quantitatT3 = "%.3f" %quantitat3
        preuT3 = "%.2f" %preu3
        preuTotT3 = "%.2f" %preuTot3
        
        nomProductor=i[16]
        nomComercial=i[17]
        direccioF = i[18]
        cifProductor = i[19]
        
        preuFn=preu1+preu2+preu3
        ivaFn = preuFn*tipoIva
        retFn = preuFn*tipoRet
        preuIvaFn = preuFn+ivaFn-retFn
        
        preuF = "%.2f" %preuFn
        ivaF = "%.2f" %ivaFn
        retF = "%.2f" %retFn
        preuIvaF = "%.2f" %preuIvaFn
        
        
        
        lista[indice] = FCompra(idFCompra, idProductor, numFCompra, dataFCompra, producte1, preuUnitT1, unitat1, quantitatT1, preuT1, preuTotT1, producte2, preuUnitT2, unitat2, quantitatT2, preuT2, preuTotT2, producte3, preuUnitT3, unitat3, quantitatT3, preuT3, preuTotT3, nomProductor, nomComercial, direccioF, cifProductor, preuF, ivaF, preuIvaF, retF) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 


def tablaFCompraSelect(cursor, idFCompra):
    tipoIva=0.12 #TIPO IVA AGRICULTOR 
    tipoRet=0.02 #TIPO Retencion AGRICULTOR 
    cursor.execute('SELECT fc.idFCompra, fc.idProductor, fc.numFCompra, fc.dataFCompra, fc.producte1, fc.preuUnit1, fc.unitat1, fc.quantitat1, fc.producte2, fc.preuUnit2, fc.unitat2, fc.quantitat2, fc.producte3, fc.preuUnit3, fc.unitat3, fc.quantitat3, pr.nomProductor, pr.nomComercial, pr.direccioF, pr.cifProductor FROM productors pr INNER JOIN fcompra fc ON fc.idProductor= pr.idProductor WHERE idFCompra=%s',(idFCompra,))
    tabla = cursor.fetchall()
    
    for i in tabla: #cada fila es converteix en un objecte de lista
        preu1=0
        preu2=0
        preu3=0       
        idFCompra=i[0]
        idProductor=i[1]
        numFCompra=i[2]       
        dataFCompra=dataFormat(i[3])
        producte1=i[4]
        try:
            preuUnit1=float(i[5])
        except:
            preuUnit1=0
        unitat1=i[6]
        try:
            quantitat1 = float(i[7])
        except:
            quantitat1=0
            
        preu1 = preuUnit1*quantitat1
        iva1 = preu1*tipoIva
        preuTot1= preu1+iva1
        
        preuUnitT1 = "%.2f" %preuUnit1
        quantitatT1 = "%.3f" %quantitat1
        preuT1 = "%.2f" %preu1
        preuTotT1 = "%.2f" %preuTot1
        
        producte2=i[8]
        
        try:
            preuUnit2=float(i[9])
        except:
            preuUnit2=0
        unitat2=i[10]
        try:
            quantitat2 = float(i[11])
        except:
            quantitat2=0
        
        preu2 = preuUnit2*quantitat2
        iva2 = preu2*tipoIva
        preuTot2= preu2+iva2
        
        preuUnitT2 = "%.2f" %preuUnit2
        quantitatT2 = "%.3f" %quantitat2
        preuT2 = "%.2f" %preu2
        preuTotT2 = "%.2f" %preuTot2
        
        producte3=i[12]
        try:
            preuUnit3=float(i[13])
        except:
            preuUnit3=0
        unitat3=i[14]
        try:
            quantitat3 = float(i[15])
        except:
            quantitat3=0
            
        preu3 = preuUnit3*quantitat3
        iva3 = preu3*tipoIva
        preuTot3= preu3+iva3
        
        preuUnitT3 = "%.2f" %preuUnit3
        quantitatT3 = "%.3f" %quantitat3
        preuT3 = "%.2f" %preu3
        preuTotT3 = "%.2f" %preuTot3
        
        nomProductor=i[16]
        nomComercial=i[17]
        direccioF = i[18]
        cifProductor = i[19]
        
        preuFn=preu1+preu2+preu3
        ivaFn = preuFn*tipoIva
        retFn = preuFn*tipoRet
        preuIvaFn = preuFn+ivaFn-retFn
        
        preuF = "%.2f" %preuFn
        ivaF = "%.2f" %ivaFn
        retF = "%.2f" %retFn
        preuIvaF = "%.2f" %preuIvaFn
        
        
        
        
        lista = FCompra(idFCompra, idProductor, numFCompra, dataFCompra, producte1, preuUnitT1, unitat1, quantitatT1, preuT1, preuTotT1, producte2, preuUnitT2, unitat2, quantitatT2, preuT2, preuTotT2, producte3, preuUnitT3, unitat3, quantitatT3, preuT3, preuTotT3, nomProductor, nomComercial, direccioF, cifProductor, preuF, ivaF, preuIvaF, retF) #Modificar si anyadim columna 
    return lista 


class FCompra:
    def __init__(self, idFCompra, idProductor, numFCompra, dataFCompra, producte1, preuUnitT1, unitat1, quantitatT1, preuT1, preuTotT1, producte2, preuUnitT2, unitat2, quantitatT2, preuT2, preuTotT2, producte3, preuUnitT3, unitat3, quantitatT3, preuT3, preuTotT3, nomProductor, nomComercial, direccioF, cifProductor, preuF, ivaF, preuIvaF, retF):
        self.idFCompra = idFCompra
        self.idProductor = idProductor
        self.numFCompra = numFCompra
        self.dataFCompra = dataFCompra
        self.producte1 = producte1
        self.preuUnitT1 = preuUnitT1
        self.unitat1 = unitat1
        self.quantitatT1 = quantitatT1
        self.preuT1 = preuT1
        self.preuTotT1 = preuTotT1
        self.producte2 = producte2
        self.preuUnitT2 = preuUnitT2
        self.unitat2 = unitat2
        self.quantitatT2 = quantitatT2
        self.preuT2 = preuT2
        self.preuTotT2 = preuTotT2
        self.producte3 = producte3
        self.preuUnitT3 = preuUnitT3
        self.unitat3 = unitat3
        self.quantitatT3 = quantitatT3
        self.preuT3 = preuT3
        self.preuTotT3 = preuTotT3
        self.nomProductor = nomProductor
        self.nomComercial = nomComercial
        self.direccioF = direccioF
        self.cifProductor = cifProductor
        self.preuF = preuF
        self.ivaF = ivaF
        self.preuIvaF = preuIvaF
        self.retF = retF

###########################################################################################################################################################
# IMP FCOMPRA       IMP FCOMPRA        IMP FCOMPRA       IMP FCOMPRA       IMP FCOMPRA       IMP FCOMPRA     
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariImpFCompra (usuari, idFCompra):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    

    fcompraSelect = tablaFCompraSelect(cursor,idFCompra)
    
  
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idFCompra': idFCompra,
             'fcompraSelect': fcompraSelect,
              }
    return values 

class ImpFCompra (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                idFCompra= novar(self.request.get('idFCompra'))
            
                #obtenim valors per al html
                values = formulariImpFCompra(usuari, idFCompra)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'fcompraImp.html') 
                self.response.out.write(template.render(path, values,))
                
###########################################################################################################################################################
# SIMPLIFICADA         SIMPLIFICADA         SIMPLIFICADA         SIMPLIFICADA         SIMPLIFICADA         SIMPLIFICADA         SIMPLIFICADA              
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
#Pasa variable amb tres estats -1 tots, -2 crea, v1 select

def formulariSimplificada (usuari, idSimplificada):

    v1 = idSimplificada

    #conectar a la bd
    db= connect_to_cloudsql()
    cursor = db.cursor()
        
    #tables necessaries
    t1=tablaTreballadorSelect(cursor,usuari)
    t2=tablaProducteTotsSimpli(cursor)
    t3=tablaSimplificadaTots(cursor)
    t5=tablaFormaPagamentTots(cursor)

    #selector de estats
    if v1== -1: #tots
        t4= ''
        
    elif v1==-2: #crea
        t4= ''
        
    else: # select
        t4 = tablaSimplificadaSelect(cursor,v1)

    #ultima simplificada
    cursor.execute('SELECT factSimpli, data FROM simplificada WHERE factSimpli<>%s ORDER BY factSimpli DESC LIMIT 0,1',('None',))
    simpli = cursor.fetchall()
    if simpli:
        ultNumSimpli = simpli[0][0]
        ultDataSimpli = dataFormat(simpli[0][1])
    else:
        ultNumSimpli = 'FS21/000'
        ultDataSimpli = '2021-01-01'
    
    #comanda seguent
    simplificadaS=factSimpliSeguent(ultNumSimpli)
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')


    #desconectar de la bd
    db.commit()
    db.close()
    
    

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': t1,
             'producteTotsSimpli':t2,
             'simplificadaTots': t3,
             'simplificadaSelect': t4,
             'idSimplificada' : v1,
             'formaPagamentTots':t5,
             'simplificadaS': simplificadaS,
             'dataHui': dataHui,
              }
    return values   

# ACCIONS DEL FORMULARI
####################################

class SimplificadaTots (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):

            v1=-1
            
            #obtenim valors per al html
            values = formulariSimplificada(usuari,v1)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'simplificada.html') 
            self.response.out.write(template.render(path, values,))


class SimplificadaNou (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            v1 = -2
            
            #obtenim valors per al html
            values = formulariSimplificada(usuari,v1)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'simplificada.html') 
            self.response.out.write(template.render(path, values,))                
            
class SimplificadaSelect (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            v1= novar(self.request.get('idSimplificada'))

            
            #obtenim valors per al html
            values = formulariSimplificada(usuari,v1)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'simplificada.html') 
            self.response.out.write(template.render(path, values,))

            

class SimplificadaEdita (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            v1 = novar(self.request.get('idSimplificada'))
            v2 = novar(self.request.get('idFormaPagament'))
            v3 = novar(self.request.get('factSimpli'))
            v4 = novar(self.request.get('data'))
            v5 = novar(self.request.get('idProducte1'))
            v6 = novar(self.request.get('idProducte2'))
            v7 = novar(self.request.get('idProducte3'))
            v8 = novar(self.request.get('idProducte4'))
            v9 = novar(self.request.get('idProducte5'))
            v10 = novar(self.request.get('idProducte6'))
            v11 = novar(self.request.get('quantitat1'))
            v12 = novar(self.request.get('quantitat2'))
            v13 = novar(self.request.get('quantitat3'))
            v14 = novar(self.request.get('quantitat4'))
            v15 = novar(self.request.get('quantitat5'))
            v16 = novar(self.request.get('quantitat6'))

            #accions sobre bd
            db= get_db()
            cursor = db.cursor()

            cursor.execute('UPDATE simplificada SET idFormaPagament=%s, factSimpli=%s, data=%s, idProducte1=%s, idProducte2=%s, idProducte3=%s, idProducte4=%s, idProducte5=%s, idProducte6=%s, quantitat1=%s, quantitat2=%s, quantitat3=%s, quantitat4=%s, quantitat5=%s, quantitat6=%s WHERE idSimplificada=%s', (v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v1,))          
            
           
            db.commit()
            db.close()
            
            v1=-1
            
            #obtenim valors per al html
            values = formulariSimplificada(usuari,v1)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'simplificada.html') 
            self.response.out.write(template.render(path, values,))

class SimplificadaCrea (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            v2 = novar(self.request.get('idFormaPagament'))
            v3 = novar(self.request.get('factSimpli'))
            v4 = novar(self.request.get('data'))
            v5 = novar(self.request.get('idProducte1'))
            v6 = novar(self.request.get('idProducte2'))
            v7 = novar(self.request.get('idProducte3'))
            v8 = novar(self.request.get('idProducte4'))
            v9 = novar(self.request.get('idProducte5'))
            v10 = novar(self.request.get('idProducte6'))
            v11 = novar(self.request.get('quantitat1'))
            v12 = novar(self.request.get('quantitat2'))
            v13 = novar(self.request.get('quantitat3'))
            v14 = novar(self.request.get('quantitat4'))
            v15 = novar(self.request.get('quantitat5'))
            v16 = novar(self.request.get('quantitat6'))

            #accions sobre bd
            db= get_db()
            cursor = db.cursor()

            cursor.execute('INSERT INTO simplificada (idFormaPagament, factSimpli, data, idProducte1,  idProducte2,  idProducte3,  idProducte4,  idProducte5,  idProducte6, quantitat1, quantitat2, quantitat3, quantitat4, quantitat5, quantitat6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16))
            
            cursor.execute('SELECT idSimplificada FROM simplificada ORDER BY idSimplificada DESC LIMIT 0,1')
            lista = cursor.fetchall()
            v1 = lista[0][0] 
            
            db.commit()
            db.close()
                
            
            #obtenim valors per al html
            values = formulariSimplificada(usuari,v1)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'simplificada.html') 
            self.response.out.write(template.render(path, values,))
            
class SimplificadaElimina (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            v1= novar(self.request.get('idSimplificada'))


            #conectar a la bd
            db= get_db()
            cursor = db.cursor()

            cursor.execute('DELETE FROM simplificada WHERE idSimplificada=%s',(v1,))
    
            db.commit()
            db.close()
                
            v1=-1
            
            #obtenim valors per al html
            values = formulariSimplificada(usuari,v1)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'simplificada.html') 
            self.response.out.write(template.render(path, values,))



# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaSimplificadaTots(cursor):   
    cursor.execute('SELECT idSimplificada, idFormaPagament, factSimpli, data, idProducte1, idProducte2, idProducte3, idProducte4, idProducte5, idProducte6, quantitat1, quantitat2, quantitat3, quantitat4, quantitat5, quantitat6  FROM simplificada ORDER BY idSimplificada DESC')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        v1=i[0]
        v2=i[1]
        v3=i[2]
        v4=dataFormat(i[3])
        v5=i[4]
        v6=i[5]
        v7=i[6]
        v8=i[7]
        v9=i[8]
        v10=i[9]
        v11=i[10]
        v12=i[11]
        v13=i[12]
        v14=i[13]
        v15=i[14]
        v16=i[15]
        lista[indice] = Simplificada(v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 

class Simplificada:
    def __init__(self, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10,v11,v12,v13,v14,v15,v16):
        self.idSimplificada = v1
        self.idFormaPagament = v2
        self.factSimpli = v3
        self.data = v4
        self.idProducte1 = v5
        self.idProducte2 = v6
        self.idProducte3 = v7
        self.idProducte4 = v8
        self.idProducte5 = v9
        self.idProducte6 = v10
        self.quantitat1 = v11
        self.quantitat2 = v12
        self.quantitat3 = v13
        self.quantitat4 = v14
        self.quantitat5 = v15
        self.quantitat6 = v16


def tablaSimplificadaSelect(cursor, idSimplificada):   
    cursor.execute('SELECT idSimplificada, idFormaPagament, factSimpli, data, idProducte1, idProducte2, idProducte3, idProducte4, idProducte5, idProducte6, quantitat1, quantitat2, quantitat3, quantitat4, quantitat5, quantitat6  FROM simplificada WHERE idSimplificada=%s ',(idSimplificada,))
    tabla = cursor.fetchall()
    
    for i in tabla: #cada fila es converteix en un objecte de lista
        v1=i[0]
        v2=i[1]
        v3=i[2]
        v4=dataFormat(i[3])
        v5=i[4]
        v6=i[5]
        v7=i[6]
        v8=i[7]
        v9=i[8]
        v10=i[9]
        v11=i[10]
        v12=i[11]
        v13=i[12]
        v14=i[13]
        v15=i[14]
        v16=i[15]
        lista = Simplificada(v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16) #Modificar si anyadim columna 
    return lista 

def tablaProducteTotsSimpli(cursor):   
    cursor.execute('SELECT pr.idProducte, pr.codiProducte, pr.producte, pr.preuP, pr.preuD, pr.idTipoIva, pr.unitat, pr.esFira, ti.percent FROM tipoiva ti INNER JOIN productes pr ON pr.idTipoIva = ti.idTipoIva WHERE pr.esFira=%s ORDER BY producte',(1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = ProducteT(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]) #Modificar si anyadim columna 
        indice=indice+1   
    return lista 



###########################################################################################################################################################
# IMP SIMPLIFICADA           IMP SIMPLIFICADA           IMP SIMPLIFICADA           IMP SIMPLIFICADA           IMP SIMPLIFICADA           IMP SIMPLIFICADA    
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariImpSimplificada (usuari, idSimplificada):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    treballadorSelect=tablaTreballadorSelect(cursor,usuari)
    

    impSimplificada = tablaImpSimplificadaSelect(cursor,idSimplificada)
    
  
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'treballadorSelect': treballadorSelect,
             'idSimplificada': idSimplificada,
             'impSimplificada': impSimplificada,
              }
    return values 

class ImpSimplificada (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
                #captura
                idSimplificada= novar(self.request.get('idSimplificada'))
            
                #obtenim valors per al html
                values = formulariImpSimplificada(usuari, idSimplificada)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'simplificadaImp.html') 
                self.response.out.write(template.render(path, values,)) 

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaImpSimplificadaSelect(cursor, idSimplificada):

    cursor.execute('SELECT idSimplificada, idFormaPagament, factSimpli, data, idProducte1, idProducte2, idProducte3, idProducte4, idProducte5, idProducte6, quantitat1, quantitat2, quantitat3, quantitat4, quantitat5, quantitat6  FROM simplificada WHERE idSimplificada=%s ',(idSimplificada,))
    tabla = cursor.fetchall()
    
    for i in tabla: #cada fila es converteix en un objecte de lista
        idSimplificada=i[0]
        factSimpli=i[2]
        data=dataFormat(i[3])

        idFormaPagament=i[1]
        cursor.execute('SELECT formaPagament FROM formaPagament WHERE idFormaPagament=%s ',(idFormaPagament,))
        vector = cursor.fetchall()
        formaPagament = vector[0][0]

        idProducte1=int(i[4])
        if (idProducte1 == -1):
            producte1=""
            unitat1=""
            percent1=""
            quantitat1=0
            total1n=0
            preuP1=""
            total1=""
            totalIva1=""
            tipoIva1=0
            totalIva1n=0
        else:
            cursor.execute('SELECT pr.producte, pr.preuP, pr.unitat, ti.tipoIva, ti.percent FROM tipoiva ti INNER JOIN productes pr ON pr.idTipoIva=ti.idTipoIva WHERE pr.idProducte=%s ',(idProducte1,))
            vector = cursor.fetchall()
            producte1 = vector[0][0]
            try:
                preuP1n=float(vector[0][1])
            except:
                preuP1n=0
            unitat1 = vector[0][2]
            tipoIva1 = float(vector[0][3])
            percent1 = vector[0][4]
            quantitat1=float(i[10])
            total1n = quantitat1*preuP1n
            totalIva1n = total1n*(1+tipoIva1)
            preuP1 = "%.2f" %preuP1n
            total1 = "%.2f" %total1n
            totalIva1 = "%.2f" %totalIva1n

        idProducte2=int(i[5])
        if (idProducte2 == -1):
                    producte2=""
                    unitat2=""
                    percent2=""
                    quantitat2=0
                    preuP2=""
                    total2=""
                    totalIva2=""
                    total2n=0
                    tipoIva2=0
                    totalIva2n=0
        else:
            cursor.execute('SELECT pr.producte, pr.preuP, pr.unitat, ti.tipoIva, ti.percent FROM tipoiva ti INNER JOIN productes pr ON pr.idTipoIva=ti.idTipoIva WHERE pr.idProducte=%s ',(idProducte2,))
            vector = cursor.fetchall()
            producte2 = vector[0][0]
            try:
                preuP2n=float(vector[0][1])
            except:
                preuP2n=0
            unitat2 = vector[0][2]
            tipoIva2 = float(vector[0][3])
            percent2 = vector[0][4]
            quantitat2=float(i[11])
            total2n = quantitat2*preuP2n
            totalIva2n = total2n*(1+tipoIva2)
            preuP2 = "%.2f" %preuP2n
            total2 = "%.2f" %total2n
            totalIva2 = "%.2f" %totalIva2n

        

        idProducte3=int(i[6])
        if (idProducte3 == -1):
                    producte3=""
                    unitat3=""
                    percent3=""
                    quantitat3=0
                    preuP3=""
                    total3=""
                    totalIva3=""
                    total3n=0
                    tipoIva3=0
                    totalIva3n=0
        else:
            cursor.execute('SELECT pr.producte, pr.preuP, pr.unitat, ti.tipoIva, ti.percent FROM tipoiva ti INNER JOIN productes pr ON pr.idTipoIva=ti.idTipoIva WHERE pr.idProducte=%s ',(idProducte3,))
            vector = cursor.fetchall()
            producte3 = vector[0][0]
            try:
                preuP3n=float(vector[0][1])
            except:
                preuP3n=0
            unitat3 = vector[0][2]
            tipoIva3 = float(vector[0][3])
            percent3 = vector[0][4]
            quantitat3=float(i[12])
            total3n = quantitat3*preuP3n
            totalIva3n = total3n*(1+tipoIva3)
            preuP3 = "%.2f" %preuP3n
            total3 = "%.2f" %total3n
            totalIva3 = "%.2f" %totalIva3n

        idProducte4=int(i[7])
        if (idProducte4 == -1):
                            producte4=""
                            unitat4=""
                            percent4=""
                            quantitat4=0
                            preuP4=""
                            total4=""
                            totalIva4=""
                            total4n=0
                            tipoIva4=0
                            totalIva4n=0
        else:
            cursor.execute('SELECT pr.producte, pr.preuP, pr.unitat, ti.tipoIva, ti.percent FROM tipoiva ti INNER JOIN productes pr ON pr.idTipoIva=ti.idTipoIva WHERE pr.idProducte=%s ',(idProducte4,))
            vector = cursor.fetchall()
            producte4 = vector[0][0]
            try:
                preuP4n=float(vector[0][1])
            except:
                preuP4n=0
            unitat4 = vector[0][2]
            tipoIva4 = float(vector[0][3])
            percent4 = vector[0][4]
            quantitat4=float(i[13])
            total4n = quantitat4*preuP4n
            totalIva4n = total4n*(1+tipoIva4)
            preuP4 = "%.2f" %preuP4n
            total4 = "%.2f" %total4n
            totalIva4 = "%.2f" %totalIva4n

        idProducte5=int(i[8])
        if (idProducte5 == -1):
                    producte5=""
                    unitat5=""
                    percent5=""
                    quantitat5=0
                    preuP5=""
                    total5=""
                    totalIva5=""
                    total5n=0
                    tipoIva5=0
                    totalIva5n=0
        else:
            cursor.execute('SELECT pr.producte, pr.preuP, pr.unitat, ti.tipoIva, ti.percent FROM tipoiva ti INNER JOIN productes pr ON pr.idTipoIva=ti.idTipoIva WHERE pr.idProducte=%s ',(idProducte5,))
            vector = cursor.fetchall()
            producte5 = vector[0][0]
            try:
                preuP5n=float(vector[0][1])
            except:
                preuP5n=0
            unitat5 = vector[0][2]
            tipoIva5 = float(vector[0][3])
            percent5 = vector[0][4]
            quantitat5=float(i[14])
            total5n = quantitat5*preuP5n
            totalIva5n = total5n*(1+tipoIva5)
            preuP5 = "%.2f" %preuP5n
            total5 = "%.2f" %total5n
            totalIva5 = "%.2f" %totalIva5n

        idProducte6=int(i[9])
        if (idProducte6 == -1):
                    producte6=""
                    unitat6=""
                    percent6=""
                    quantitat6=0
                    preuP6=""
                    total6=""
                    totalIva6=""
                    total6n=0
                    tipoIva6=0
                    totalIva6n=0
        else:
            cursor.execute('SELECT pr.producte, pr.preuP, pr.unitat, ti.tipoIva, ti.percent FROM tipoiva ti INNER JOIN productes pr ON pr.idTipoIva=ti.idTipoIva WHERE pr.idProducte=%s ',(idProducte6,))
            vector = cursor.fetchall()
            producte6 = vector[0][0]
            try:
                preuP6n=float(vector[0][1])
            except:
                preuP6n=0
            unitat6 = vector[0][2]
            tipoIva6 = float(vector[0][3])
            percent6 = vector[0][4]
            quantitat6=float(i[15])
            total6n = quantitat6*preuP6n
            totalIva6n = total6n*(1+tipoIva6)
            preuP6 = "%.2f" %preuP6n
            total6 = "%.2f" %total6n
            totalIva6 = "%.2f" %totalIva6n

        totalFSn = total1n+total2n+total3n+total4n+total5n+total6n
        totalFS = "%.2f" %totalFSn

        sumaIvan = total1n*tipoIva1+total2n*tipoIva2+total3n*tipoIva3+total4n*tipoIva4+total5n*tipoIva5+total6n*tipoIva6
        sumaIva = "%.2f" %sumaIvan

        totalFSIvan=totalIva1n+totalIva2n+totalIva3n+totalIva4n+totalIva5n+totalIva6n
        totalFSIva =  "%.2f" %totalFSIvan
        
        
        lista = SimplificadaImp( idSimplificada, formaPagament, factSimpli, data, producte1, quantitat1, preuP1, unitat1, percent1,total1, totalIva1, producte2, quantitat2, preuP2, unitat2, percent2,total2, totalIva2, producte3, quantitat3, preuP3, unitat3, percent3,total3, totalIva3, producte4, quantitat4, preuP4, unitat4, percent4,total4, totalIva4, producte5, quantitat5, preuP5, unitat5, percent5,total5, totalIva5, producte6, quantitat6, preuP6, unitat6, percent6, total6, totalIva6, totalFS, sumaIva, totalFSIva) #Modificar si anyadim columna 
    return lista 


class SimplificadaImp:
    def __init__(self, idSimplificada, formaPagament, factSimpli, data, producte1, quantitat1, preuP1, unitat1, percent1,total1, totalIva1, producte2, quantitat2, preuP2, unitat2, percent2,total2, totalIva2, producte3, quantitat3, preuP3, unitat3, percent3,total3, totalIva3, producte4, quantitat4, preuP4, unitat4, percent4,total4, totalIva4, producte5, quantitat5, preuP5, unitat5, percent5,total5, totalIva5, producte6, quantitat6, preuP6, unitat6, percent6, total6, totalIva6, totalFS, sumaIva, totalFSIva):
        self.idSimplificada = idSimplificada
        self.formaPagament = formaPagament
        self.factSimpli = factSimpli
        self.data = data
        self.producte1 = producte1
        self.quantitat1 = quantitat1
        self.preuP1 = preuP1
        self.unitat1 = unitat1
        self.percent1 = percent1
        self.total1 = total1
        self.totalIva1 = totalIva1
        self.producte2 = producte2
        self.quantitat2 = quantitat2
        self.preuP2 = preuP2
        self.unitat2 = unitat2
        self.percent2 = percent2
        self.total2 = total2
        self.totalIva2 = totalIva2
        self.producte3 = producte3
        self.quantitat3 = quantitat3
        self.preuP3 = preuP3
        self.unitat3 = unitat3
        self.percent3 = percent3
        self.total3 = total3
        self.totalIva3 = totalIva3
        self.producte4 = producte4
        self.quantitat4 = quantitat4
        self.preuP4 = preuP4
        self.unitat4 = unitat4
        self.percent4 = percent4
        self.total4 = total4
        self.totalIva4 = totalIva4
        self.producte5 = producte5
        self.quantitat5 = quantitat5
        self.preuP5 = preuP5
        self.unitat5 = unitat1
        self.percent5 = percent5
        self.total5 = total5
        self.totalIva5 = totalIva5
        self.producte6 = producte6
        self.quantitat6 = quantitat6
        self.preuP6 = preuP6
        self.unitat6 = unitat6
        self.percent6 = percent6
        self.total6 = total6
        self.totalIva6 = totalIva6
        self.totalFS = totalFS
        self.sumaIva = sumaIva
        self.totalFSIva = totalFSIva
        
                
###########################################################################################################################################################
# REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO
###########################################################################################################################################################
       

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Inicio', Inicio),
    ('/Index', Index),  
    ('/UsuariTots', UsuariTots),            #Control Usuaris 
    ('/UsuariNou', UsuariNou),
    ('/UsuariCrea', UsuariCrea),
    ('/UsuariSelect', UsuariSelect),
    ('/UsuariEdita', UsuariEdita),
    ('/ClientTots', ClientTots),                #Client
    ('/ClientNou', ClientNou),
    ('/ClientCrea', ClientCrea),
    ('/ClientSelect', ClientSelect),
    ('/ClientEdita', ClientEdita),
    ('/ClientElimina', ClientElimina), 
    ('/ProducteTots', ProducteTots),                #Producte
    ('/ProducteNou', ProducteNou),
    ('/ProducteCrea', ProducteCrea),
    ('/ProducteSelect', ProducteSelect),
    ('/ProducteEdita', ProducteEdita),
    ('/ProducteElimina', ProducteElimina), 
    ('/ComandaTots', ComandaTots),                #Comanda
    ('/ComandaNou', ComandaNou),
    ('/ComandaCrea', ComandaCrea),
    ('/ComandaSelect', ComandaSelect),
    ('/ComandaEdita', ComandaEdita),
    ('/ComandaElimina', ComandaElimina),                 #LiniaComanda
    ('/LiniaComandaNou', LiniaComandaNou),
    ('/LiniaComandaCrea', LiniaComandaCrea),
    ('/LiniaComandaSelect', LiniaComandaSelect),
    ('/LiniaComandaEdita', LiniaComandaEdita),
    ('/LiniaComandaElimina', LiniaComandaElimina),
    ('/PagamentNou', PagamentNou),         #Pagament
    ('/PagamentCrea', PagamentCrea),
    ('/PagamentSelect', PagamentSelect),
    ('/PagamentEdita', PagamentEdita),
    ('/PagamentElimina', PagamentElimina),  
    ('/ImpFactura', ImpFactura),
    ('/ImpAlbara', ImpAlbara),
    ('/ImpFacturaRecarrec', ImpFacturaRecarrec),
    ('/ImpAlbaraRecarrec', ImpAlbaraRecarrec),
    ('/ImpEnviar', ImpEnviar),
    ('/FacturaTots', FacturaTots), 
    ('/LotTots', LotTots),                #Lot
    ('/LotNou', LotNou),
    ('/LotCrea', LotCrea),
    ('/LotSelect', LotSelect),
    ('/LotEdita', LotEdita),
    ('/LotElimina', LotElimina), 
    ('/ImpLot', ImpLot), 
    ('/FincaTots', FincaTots),                #Finca
    ('/FincaNou', FincaNou),
    ('/FincaCrea', FincaCrea),
    ('/FincaSelect', FincaSelect),
    ('/FincaEdita', FincaEdita),
    ('/FincaElimina', FincaElimina), 
    ('/VarietatTots', VarietatTots),                #Varietat
    ('/VarietatNou', VarietatNou),
    ('/VarietatCrea', VarietatCrea),
    ('/VarietatSelect', VarietatSelect),
    ('/VarietatEdita', VarietatEdita),
    ('/VarietatElimina', VarietatElimina),
    ('/ProduccioTots', ProduccioTots),                #Produccio
    ('/ProduccioElegir', ProduccioElegir),
    ('/ProduccioQuadernSelect', ProduccioQuadernSelect),
    ('/ProduccioQuadernSelectGet', ProduccioQuadernSelectGet),
    ('/ProduccioNou', ProduccioNou),
    ('/ProduccioCrea', ProduccioCrea),
    ('/ProduccioSelect', ProduccioSelect),
    ('/ProduccioEdita', ProduccioEdita),
    ('/ProduccioElimina', ProduccioElimina),
    ('/ImpProduccio', ImpProduccio), 
    ('/ProductorTots', ProductorTots),                #Productor
    ('/ProductorNou', ProductorNou),
    ('/ProductorCrea', ProductorCrea),
    ('/ProductorSelect', ProductorSelect),
    ('/ProductorEdita', ProductorEdita),
    ('/ProductorElimina', ProductorElimina),
    ('/FCompraTots', FCompraTots),                #FCompra
    ('/FCompraNou', FCompraNou),
    ('/FCompraCrea', FCompraCrea),
    ('/FCompraSelect', FCompraSelect),
    ('/FCompraEdita', FCompraEdita),
    ('/FCompraElimina', FCompraElimina), 
    ('/ImpFCompra', ImpFCompra), 
    ('/SimplificadaTots', SimplificadaTots),     #Simplificada
    ('/SimplificadaNou', SimplificadaNou),
    ('/SimplificadaCrea', SimplificadaCrea),
    ('/SimplificadaSelect', SimplificadaSelect),  
    ('/SimplificadaEdita', SimplificadaEdita), 
    ('/SimplificadaElimina', SimplificadaElimina), 
    ('/ImpSimplificada', ImpSimplificada), 
    ], debug=True)
