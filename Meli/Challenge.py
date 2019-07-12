import pymysql
import smtplib


##FUNCIONES
def crear_base_de_datos(bd, nombre):
	cursor=db.cursor()
	sql = "CREATE DATABASE %s"%(nombre)
	try:
		cursor.execute(sql)
	except:
		print("Hubo un error al crear la base de datos")

def eliminar_base_de_datos(bd, nombre):
	cursor=db.cursor()
	cursor.execute("DROP SCHEMA nombre") %(nombre)
	print("Base de datos, eliminada con exito")

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
def seEncuentraEnBd(nombreAIngresar, emailAIngresar):
	# Prepare SQL query to READ a record into the database.
	sql = "SELECT * FROM test WHERE id > {0}".format(0)

	# Execute the SQL command	
	cursor.execute(sql)

	# Fetch all the rows in a list of lists.
	results = cursor.fetchall()
	flag = False
	for row in results:
		if row[1]==nombreAIngresar and row[2] == emailAIngresar:
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
crear_base_de_datos(db, "prueba1")

#MOSTRAR BASES DE DATOS EXISTENTES
cursor.execute("SHOW DATABASES")
bases_de_datos=cursor.fetchall()
print (bases_de_datos)

#ELIMINAR UNA BASE DE DATOS
#eliminar_base_de_datos(db, "prueba")

#SELECCIONO LA BASE DE DATOS CON LA QUE QUIERO OPERAR
db = pymysql.connect("127.0.0.1","root","Diego2019", "prueba")

#CREAR TABLA EN BASE DE DATOS
#cursor.execute("CREATE TABLE usuarios (nombre_usuario VARCHAR(25), email_usuario varchar(40))")

db.close()

