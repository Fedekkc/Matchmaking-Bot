import mysql.connector
from bs4 import BeautifulSoup
import json
import os

#• Matchmaking (emparejamiento por rango limitado)
#• Sistema de puntos
#• Leaderboard (General y por roles)
#• Perfil/Stats
#• Confirmación de victoria/derrota

divisiones = [
		"Division V",
		"Division IV",
		"Division III",
		"Division II",
		"Division I"
	]
rangos = 	[
		"Esmeralda IV",
		"Esmeralda III",
		"Esmeralda II",
		"Esmeralda I",
		"Diamante IV",
		"Diamante III",
		"Diamante II",
		"Diamante I",
		"Maestro",
		"Gran Maestro",
		"Aspirante"
	]

with open("BD_INFO.json", "r") as j:
	data = json.load(j)
	db = mysql.connector.connect(
    host = data["host"],
    user = data["user"],
    password = data["password"],
    database = data["database"])
cursor = db.cursor()

def welcome():
	checkAllPlayersRank()
	print("\t██       ▄ ▄     █▄▄▄▄ ");
	print("\t█ █     █   █    █  ▄▀ ");
	print("\t█▄▄█   █ ▄   █   █▀▀▌  ");
	print("\t█  █   █  █  █   █  █  ");
	print("\t   █    █ █ █      █   ");
	print("\t  █      ▀ ▀      ▀    ");
	print("\t ▀                    ");

def main():

	if(db):
		readme = open("README.txt")
		welcome()
		print("[+] BOT Ascension War Rift - AWR 1.0.0 ON")
		print("POR FAVOR LEER: ")
		for linea in readme:
			print(linea.replace("\n",""))

		input("Presione una tecla para continuar...")
		os.system("cls")
		while(True):
			print("Comandos disponibles:\n - mp\n - lb\n - mm")
			cmd =  input("\n\n\n[+] Comando: ")
			ID = 0
			if(cmd == "mp"):
				cmd = input("1. Sumar\n2. Restar\n3. Establecer\n")
				ID = input("ID del usuario: ")
				if(checkID(ID)):
					info = getProfile(ID)
					print("Username: {} || Puntos: {}".format(info[3],info[4]))
					num = input("Puntos: ")
					if(cmd == '1'):
						addPoints(ID,num)
					elif(cmd == '2'):
						removePoints(ID,num)
					elif(cmd == '3'):
						setPoints(ID,num)
					checkPlayerRank(ID)
				else:
					print("No existe un jugador con este ID")
			if(cmd == "lb"):
				l = leaderboard()
				count = 0
				for i in l:
					count += 1
					print("\n")
					print("Posicion {}: {}".format(count, i))
			if(cmd == "mm"):
				ID = input("ID del usuario: ")
				if(checkID(ID)):
					print("Lista de posibles rivales: ")
					for i in matchmaking(ID): 
						print(i)
				else:
					print("No existe un jugador con este ID")
					
	else:
		print("[-] Error conectando a la Base de datos.")
		print("Si estas recibiendo este error, \n\
			probablemente las credenciales \n\
			de la base de datos sean incorrectas \n\
			o inexistentes. \n\
			Porfavor, asegurate de modificarlas \n\
			en el archivo BD_INFO.json")








def addPoints(ID,cant):
	cursor.execute("UPDATE Usuarios SET Puntos = Puntos + {} WHERE ID = {}".format(cant,ID))
	db.commit()


def removePoints(ID,cant):
	cursor.execute("UPDATE Usuarios SET Puntos = Puntos - {} WHERE ID = {}".format(cant,ID))
	db.commit()

def setPoints(ID,cant):
	cursor.execute("UPDATE Usuarios SET Puntos = {} WHERE ID = {}".format(cant,ID))
	db.commit()


def checkID(ID):
	cursor.execute("SELECT * FROM Usuarios WHERE ID = {}".format(ID))
	data = cursor.fetchone()
	if data:
		return 1
	else:
		return 0

def checkAllPlayersRank():
	cursor.execute("SELECT ID FROM Usuarios")
	data = cursor.fetchall()
	for f in data:
		checkPlayerRank(int(str(f).replace("(","").replace(",","").replace(")","").replace("'","")))

def checkPlayerRank(ID):
	cursor.execute("SELECT Puntos FROM Usuarios WHERE ID = {}".format(ID))
	data = cursor.fetchone()
	rank = 0
	puntos = 0
	for f in data:
		puntos = int(str(f).replace("(","").replace(",","").replace(")","").replace("'",""))
		
	if(puntos >= 0 and puntos < 10):
		rank = 0
	elif(puntos >= 10 and puntos < 20 ):
		rank = 1
	elif(puntos >= 20 and puntos < 30 ):
		rank = 2
	elif(puntos >= 30 and puntos < 40 ):
		rank = 3
	elif(puntos >= 40 and puntos < 50 ):
		rank = 4
	elif(puntos >= 50 and puntos < 60 ):
		rank = 5
	elif(puntos >= 60 and puntos < 70 ):
		rank = 6
	elif(puntos >= 70 and puntos < 80 ):
		rank = 7
	elif(puntos >= 80 and puntos < 150):
		rank = 8
	elif(puntos >= 150):
		cursor.execute("SELECT RankingPos FROM Usuarios WHERE ID = {}".format(ID))
		data = cursor.fetchone()
		rankingpos = 0
		for f in data: 
			rankingpos = int(str(f).replace("(","").replace(",","").replace(")","").replace("'",""))
		if(rankingpos <= 30):
			rank = 10
		else:
			rank = 9
	cursor.execute("UPDATE Usuarios SET ID_Rango = {} WHERE ID = {}".format(rank,ID))
	db.commit()




def leaderboard(): # ESTA FUNCION IMPRIME DIRECTAMENTE UNA LEADERBOARD BASADA EN LA BASE DE DATOS
	cursor.execute("SELECT Usuario, Puntos FROM Usuarios ORDER BY Puntos DESC")
	datos = cursor.fetchall()
	contador = 0
	lista = []
	for f in datos:
		contador += 1
		lista.append("{} || Puntaje: {}".format(f[0],f[1]))
		#print("Posicion {}:".format(contador))
		#print(str(f).replace("(","").replace(",","").replace(")","").replace("'","").replace(" "," | ") + " Puntos")
	return lista
	#

	
def matchmaking(ID): # EL RETURN DE ESTA FUNCIÓN DEVUELVE UNA LISTA CON LOS POSIBLES RIVALES, EL PROGRAMA BASE SERÁ EL ENCARGADO DE EMPAREJAR AL USUARIO CON CUALQUIERA DE ESA LISTA
	cursor.execute("UPDATE Usuarios SET Connected = TRUE, Matchmaking = TRUE WHERE ID = {}".format(ID))
	db.commit()
	cursor.execute("SELECT ID_Rango FROM Usuarios WHERE ID = {}".format(ID))
	rango = ""
	datos = cursor.fetchone()
	for f in datos:
		rango = int(str(f).replace("(","").replace(",","").replace(")",""))

	cursor.execute("SELECT Puntos FROM Usuarios WHERE ID = {}".format(ID))
	datos = cursor.fetchone()
	for f in datos:
		puntos = int(str(f).replace("(","").replace(",","").replace(")",""))
		print("Puntaje del usuario: {}".format(puntos))

	cursor.execute("SELECT * FROM Usuarios WHERE ID_Rango = '{}' AND (Connected = TRUE AND Matchmaking = TRUE) AND (Puntos >= {} AND Puntos <= {}) AND ID NOT LIKE {}".format(rango, puntos-15,puntos+15,ID))
	datos = cursor.fetchall()
	puntos2 = [];
	for f in datos:
		puntos2.append(f)
		
	
	return puntos2
	




def getProfile(ID): # ESTA FUNCION DEVUELVE EL PERFIL COMPLETO SACADO DE LA BD
	cursor.execute("SELECT * FROM Usuarios WHERE ID = {}".format(ID))
	data = cursor.fetchall()
	info = []
	for f in data:
		info = f
	return info
	


if __name__ == '__main__':
	main()