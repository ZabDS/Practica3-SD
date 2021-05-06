import Pyro4
import time
import socket
import datetime


uriPrincipalCoordinator = "PYRONAME:principal@127.0.0.1:9091"
uriRespaldoCoordinator = "PYRONAME:Redundancia@127.0.0.1:9092"
DBServer = Pyro4.Proxy(uriPrincipalCoordinator) 
DBServerR = Pyro4.Proxy(uriRespaldoCoordinator)



class Usuario():
    def __init__(self):
        self.Name = socket.gethostname()
        self.Server = DBServer
        self.IP= socket.gethostbyname(self.Name)
        self.ID = DBServer.anounceMe(self.IP,self.Name)

    def changeServer(self):
        print("Intentando conectarse con el coordinador de respaldo...")
        self.Server = DBServerR
        print("Conexión exitosa")

    def getBook(self):
        try:
            now = datetime.datetime.now()
            horaI=datetime.time(now.hour,now.minute,now.second,now.microsecond)
            print(self.Server.getBook(self.ID,horaI))
            time.sleep(1)
        except Pyro4.errors.ConnectionClosedError as e:
            print("Error al conectarse con el coordinador principal")
            print(e)
            self.changeServer()
    
NewUsuario = Usuario()

i=0
while (i<5):
    i = i+1
    #DBServer.resetSys()
    try:
        NewUsuario.getBook()
    except Pyro4.errors.ConnectionClosedError as e:
        print("Error al conectarse con el coordinador principal")
        print(e)
        NewUsuario.changeServer()
    #time.sleep(1)