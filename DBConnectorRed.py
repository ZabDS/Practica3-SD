import mariadb
import random
import datetime
import sys

class DBManager:
    def __init__(self,usr,psw,host,db):
        try:
            self.conn = mariadb.connect(
            user=usr,
            password=psw,
            host=host,
            port=3306,
            database=db
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
            return -1

    def setUsuario(self,IP,Nombre,ID_Usr=-1):
        if(ID_Usr < 0):
            ID = random.randrange(1,10000,3)
        else:
            ID=ID_Usr
        try:
            self.cur.execute("INSERT INTO Usuario VALUES(?,?,?)",(ID,IP,Nombre))
            self.conn.commit()
            return ID
        except mariadb.Error as e: 
            print(f"Error insertando usuario: {e}")
            return -1

    def setPedido(self,ID_Usuario,ID_Libro,fecha,hora_inicio,hora_fin):
        try:
            ID_Pedido = random.randrange(1,10000,3)
            ID_Sesion = random.randrange(1,10000,3)

            HI= datetime.datetime.strptime(hora_inicio,"%H:%M:%S.%f").time()
            HF= datetime.datetime.strptime(hora_inicio,"%H:%M:%S.%f").time()
            tiempoUsuario=datetime.datetime.combine(datetime.date.today(), HF) - datetime.datetime.combine(datetime.date.today(), HI)

            self.cur.execute("INSERT INTO Pedido VALUES(?,?,?,?)",(ID_Pedido,fecha,hora_inicio,hora_fin)) 
            self.cur.execute("INSERT INTO Sesion VALUES(?,?,?)",(ID_Sesion,ID_Pedido,ID_Libro))
            self.cur.execute("INSERT INTO UsuarioSesion VALUES(?,?,?,?,?)",(ID_Sesion,ID_Usuario,ID_Pedido,tiempoUsuario,0))
            self.conn.commit()     
            return (ID_Pedido,ID_Sesion)   
        except mariadb.Error as e: 
            print(f"Error insertando Pedido: {e}")
            return -1
    def setPedidoBU(self,ID_Pedido,ID_Sesion,ID_Usuario,ID_Libro,fecha,hora_inicio,hora_fin):
        try:
            #ID_Pedido = random.randrange(1,10000,3)
            #ID_Sesion = random.randrange(1,10000,3)

            HI= datetime.datetime.strptime(hora_inicio,"%H:%M:%S.%f").time()
            HF= datetime.datetime.strptime(hora_inicio,"%H:%M:%S.%f").time()
            tiempoUsuario=datetime.datetime.combine(datetime.date.today(), HF) - datetime.datetime.combine(datetime.date.today(), HI)

            self.cur.execute("INSERT INTO Pedido VALUES(?,?,?,?)",(ID_Pedido,fecha,hora_inicio,hora_fin)) 
            self.cur.execute("INSERT INTO Sesion VALUES(?,?,?)",(ID_Sesion,ID_Pedido,ID_Libro))
            self.cur.execute("INSERT INTO UsuarioSesion VALUES(?,?,?,?,?)",(ID_Sesion,ID_Usuario,ID_Pedido,tiempoUsuario,0))
            self.conn.commit()     
            return ID_Pedido   
        except mariadb.Error as e: 
            print(f"Error insertando Pedido: {e}")
            return -1
    def resetDB(self):
        try: 
            self.cur.execute("DELETE FROM UsuarioSesion") 
            self.cur.execute("DELETE FROM Sesion") 
            self.cur.execute("DELETE FROM Pedido") 
            #self.cur.execute("DELETE FROM Usuario") 
            self.conn.commit()
            return 1
        except mariadb.Error as e: 
            print(f"Error reiniciando BD: {e}")
            return -1
    
            
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


