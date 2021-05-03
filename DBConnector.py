import mariadb
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
    def setUsuario(self,ID,IP,Nombre):
        try: 
            self.cur.execute("INSERT INTO Usuario VALUES(?,?,?)",(ID,IP,Nombre))
            DBM.conn.commit()
        except mariadb.Error as e: 
            print(f"Error insertando usuario: {e}")
    def setPedido(self,ID,fecha,hora_inicio,hora_fin):
        try: 
            self.cur.execute("INSERT INTO Pedido VALUES(?,?,?,?)",(ID,fecha,hora_inicio,hora_fin)) 
            DBM.conn.commit()
        except mariadb.Error as e: 
            print(f"Error insertando Pedido: {e}")
    def setSesion(self,ID,ID_Pedido,ID_Libro,ID_Usuario,tiempoUsuario,lugarJugador):
        try: 
            self.cur.execute("INSERT INTO Sesion VALUES(?,?,?)",(ID,ID_Pedido,ID_Libro))
            self.cur.execute("INSERT INTO UsuarioSesion VALUES(?,?,?,?,?)",(ID,ID_Usuario,ID_Pedido,tiempoUsuario,lugarJugador))
            DBM.conn.commit()
        except mariadb.Error as e: 
            print(f"Error insertando Sesion: {e}")
    def resetDB(self):
        try: 
            self.cur.execute("DELETE FROM UsuarioSesion") 
            self.cur.execute("DELETE FROM Sesion") 
            self.cur.execute("DELETE FROM Pedido") 
            self.cur.execute("DELETE FROM Usuario") 
            DBM.conn.commit()
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

#DBM.setUsuario(0,"192.168.12.12","Zabdiel")
#DBM.setPedido(0,"2021-05-2","00:00:00","00:00:00")
#DBM.setSesion(0,0,1,0,"00:00:00",1)

