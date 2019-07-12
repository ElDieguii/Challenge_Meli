import pymysql
import smtplib
from datetime import datetime

##IMPORTO ARCHIVO CON FUNCION DE GOOGLE API
import quickstart


##FUNCIONES
def mostrar_files_google_drive():
	if __name__ == '__main__':
        	quickstart.main()

def crear_base_de_datos(bd, nombre):
	cursor=db.cursor()
	sql = "CREATE DATABASE %s"%(nombre)
	try:
		cursor.execute(sql)
	except:
		print("Ya existe una base de datos llamada %s"%(nombre))

def eliminar_base_de_datos(bd, nombre):
	cursor=db.cursor()
	try:
		cursor.execute("DROP SCHEMA nombre") %(nombre)
		print("Base de datos, eliminada con exito")
	except:
		print("No se pudo borrar la base de datos %s, ya que no existe"%(nombre))

def insertarEnBaseDeDatos(nombreUsuario, emailDeUsuario):
	# Prepare SQL query to INSERT a record into the database.
	sql = "INSERT INTO test(id, name, email) VALUES (NULL,'{0}','{1}')".format(nombreUsuario,emailDeUsuario)
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   # Commit your changes in the database
	   db.commit()
	except:
	   # Rollback in case there is any error
	   db.rollback()

def alterarBD(cambioDeNombre,identificador):
	sql = "UPDATE test SET name = '%s' WHERE id= %i" %(cambioDeNombre,identificador)
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   # Commit your changes in the database
	   db.commit()
	except:
	   # Rollback in case there is any error
	   db.rollback()

def eliminarFilaBd(idAEliminar):
	sql = "DELETE FROM test WHERE  id= %i" %(idAEliminar)
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   # Commit your changes in the database
	   db.commit()
	except:
	   # Rollback in case there is any error
	   db.rollback()

def mostrarBaseDeDatos():
	# Prepare SQL query to READ a record into the database.
	sql = "SELECT * FROM test WHERE id > {0}".format(0)

	# Execute the SQL command	
	cursor.execute(sql)

	# Fetch all the rows in a list of lists.
	results = cursor.fetchall()
	for row in results:
   		id = row[0]
   		name = row[1]
   		email = row[2]
   		# Now print fetched result
   		print ("id = {0}, name = {1}, email = {2}".format(id,name,email))
def seEncuentraEnBd(archivo_a_ingresar):
	# Prepare SQL query to READ a record into the database.
	sql = "SELECT * FROM tabla_archivos WHERE id > {0}".format(0)

	# Execute the SQL command	
	cursor.execute(sql)

	# Fetch all the rows in a list of lists.
	results = cursor.fetchall()
	flag = False
	for row in results:
		if row[1]==archivo_a_ingresar:
			flag = True
	return flag
		
def enviarEmail(mensaje, emailDestino):
	
	fromaddr= 'dieg0xilla@gmail.com'
	toaddrs = emailDestino
	msg= mensaje

	username = 'dieg0xilla@gmail.com'
	password = 'Diego2017'

	server= smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()


def insertarNombreYEmailEnBd():
	respuesta0 = input("Desea agregar usuario y mail? ")
	while(respuesta0!="no"):
		nombreUsuario = input("Ingrese su nombre: ")
		emailDeUsuario = input("Ingrese su email: ")
		if(not seEncuentraEnBd(nombreUsuario, emailDeUsuario)):
			insertarEnBaseDeDatos(nombreUsuario, emailDeUsuario)
		else:
			mensaje= "El usuario ingresado, ya se encuentra en nuestra base de datos."
			enviarEmail(mensaje, emailDeUsuario)
			print("Se envio un mail de notificacion de acceso denegado")
		respuesta0 = input("Desea agregar otro usuario y mail? ")


def modificarUnUsuarioEnBd():
	nombreNuevo= input("Ingrese nuevo nombre: ")
	identificador=int(input("Ingrese el id a modificar: "))
	alterarBD(nombreNuevo,identificador)

def eliminarIds():
	respuesta1=input("Desea eliminar un id? ")
	while(respuesta1!="no"):
		idAEliminar = int(input("Ingrese el id a eliminar: "))
		eliminarFilaBd(idAEliminar)
		respuesta1=input("Desea eliminar otro id? ")

	

##MAIN##
#CONECTARSE A BASE DE DATOS

db = pymysql.connect("127.0.0.1","root","Diego2019")
cursor = db.cursor()
#IMPRIME VERSION DE BD
print(db)

##CREAR BASE DE DATOS
#crear_base_de_datos(db, "prueba")

#MOSTRAR BASES DE DATOS EXISTENTES
cursor.execute("SHOW DATABASES")
bases_de_datos=cursor.fetchall()
print (bases_de_datos)

#ELIMINAR UNA BASE DE DATOS
#eliminar_base_de_datos(db, "prueba")

#SELECCIONO LA BASE DE DATOS CON LA QUE QUIERO OPERAR
db = pymysql.connect("127.0.0.1","root","Diego2019", "prueba")
cursor=db.cursor()

#CREAR TABLA EN BASE DE DATOS
cursor.execute("CREATE TABLE tabla_archivos (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), archivo VARCHAR(100),fecha_creacion VARCHAR(10) )")

#ELIMINAR TABLA EN BASE DE DATOS
#cursor.execute("DROP TABLE tabla_archivos")

#MUESTRO ARCHIVOS DE GOOGLE DRIVE
##LISTA DE NOMBRES DE ARCHIVOS EN DRIVE
file_names = []
##LISTA DE DATETIME DE ARCHIVOS EN DRIVE
file_createdTime = []
#LISTA CON TODOS LOS ARCHIVOS QUE VIENE DE LA FUNCION QUICKSTART
files = quickstart.main()
##LLENO LAS LISTAS PREVIAMENTE CREADAS, CON LOS DATOS PROVENIENTES DE QUICKSTART
for file in files:
    file_names.append('{0}'.format(file['name']))
for file in files:
	file_createdTime.append('{0}'.format(file['createdTime']))

i=-1
#RECORTO LA FECHA 
for file in file_createdTime:
    i=i+1
    file_createdTime[i] = file_createdTime[i][0:10]

#ORDENO AMBAS LISTAS SEGUN FECHA
def ordenar(x):
	aux1=file_createdTime[x]
	file_createdTime[x]=file_createdTime[x+1]
	file_createdTime[x+1]=aux1
	aux2=file_names[x]
	file_names[x] = file_names[x+1]
	file_names[x+1] = aux2

for k in range(len(file_createdTime)):
    for x in range(len(file_createdTime)-1):	
    	if (file_createdTime[x]>file_createdTime[x+1]):ordenar(x)

##ENVIAR MAIL Y SUMAR CONTADOR
def mail_contador(contador, mensaje, mail_recepto):
	enviarEmail("Hay un archivo duplicado", "vivona.diego98@gmail.com")
	contador = contador + 1
	return contador


##INSERTO EN LA TABLA DE PRUEBA, LOS DATOS ALMACENADOS EN LAS LISTAS PREVIAS
contador=0
for file in files:
	sql = "INSERT INTO tabla_archivos (id, archivo, fecha_creacion) VALUES (NULL,'%s','%s')"%(file_names[contador], file_createdTime[contador])
	if seEncuentraEnBd(file_names[contador]):enviarEmail("Hay un archivo duplicado", "vivona.diego98@gmail.com")
	
	else: 
		try: 
			cursor.execute(sql)
			db.commit()
			contador = contador +1
			print("ingresado en tabla")
		except:
			print("No ingresado en tabla")
			contador = contador+1

print(file_names, file_createdTime)

db.close()

