import mariadb
import random
import datetime
import sys

class DBManager:
    def __init__(self,usr,psw,host):
        try:
            self.conn = mariadb.connect(
            user=usr,
            password=psw,
            host=host,
            port=3306,
            database="LibraryDB"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cur = self.conn.cursor()
    
    def getLibroByID(self,ID):
        try:
            self.cur.execute("SELECT * FROM Libro WHERE ISBN=?", (ID,)) 
            for libro in self.cur:
                return libro
        except mariadb.Error as e:
            print(f"Error obteniendo libro: {e}")
    def setUsuario(self,IP,Nombre):
        try: 
            self.cur.execute("INSERT INTO Usuario (IP,Nombre) VALUES(?,?)",(IP,Nombre))
            self.conn.commit()
        except mariadb.Error as e: 
            print(f"Error insertando usuario: {e}")
    def setPedido(self,ID_Usuario,ID_Libro,fecha,hora_inicio,hora_fin):
        try:
            ID_Pedido = random.randrange(1,1000,3)
            ID_Sesion = random.randrange(1,1000,3)
            
            tiempoUsuario=datetime.datetime.combine(datetime.date.today(), hora_fin) - datetime.datetime.combine(datetime.date.today(), hora_inicio)
            self.cur.execute("INSERT INTO Pedido VALUES(?,?,?,?)",(ID_Pedido,fecha,hora_inicio,hora_fin)) 
            self.cur.execute("INSERT INTO Sesion VALUES(?,?,?)",(ID_Sesion,ID_Pedido,ID_Libro))
            self.cur.execute("INSERT INTO UsuarioSesion VALUES(?,?,?,?,?)",(ID_Sesion,ID_Usuario,ID_Pedido,tiempoUsuario,0))
            self.conn.commit()        
        except mariadb.Error as e: 
            print(f"Error insertando Pedido: {e}")
    def setSesion(self,ID,ID_Pedido,ID_Libro,ID_Usuario,tiempoUsuario,lugarJugador):
        try: 
            self.cur.execute("INSERT INTO Sesion VALUES(?,?,?)",(ID,ID_Pedido,ID_Libro))
            self.cur.execute("INSERT INTO UsuarioSesion VALUES(?,?,?,?,?)",(ID,ID_Usuario,ID_Pedido,tiempoUsuario,lugarJugador))
            self.conn.commit()
        except mariadb.Error as e: 
            print(f"Error insertando Sesion: {e}")
    def resetDB(self):
        try: 
            self.cur.execute("DELETE FROM UsuarioSesion") 
            self.cur.execute("DELETE FROM Sesion") 
            self.cur.execute("DELETE FROM Pedido") 
            self.cur.execute("DELETE FROM Usuario") 
            self.conn.commit()
        except mariadb.Error as e: 
            print(f"Error reiniciando BD: {e}")

#DBM = DBManager('zabdiel','PSW','127.0.0.1')
#
#libro = DBM.getLibroByID(2)
#
#for element in libro:
#    print(element)
#
#DBM.resetDB()
#DBM.setUsuario("192.168.12.12","Zabdiel")
#DBM.setPedido(8,1,"2021-05-2",datetime.time(0,0,0),datetime.time(0,0,2))


