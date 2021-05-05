# saved as greeting-server.py
import Pyro4
import Pyro4.naming as naming
import threading
import DBConnector
import random
import datetime

def initDNS(port):
    #Thread for start the DNS
    naming.startNSloop(port=port)

@Pyro4.expose
class DBServer():
    def __init__(self):
        self.DBM = DBConnector.DBManager("zabdiel","idscom","127.0.0.1","LibraryDB")
        self.uriRedundacia = "PYRONAME:Redundancia@127.0.0.1:9092"
        self.DBServerR = Pyro4.Proxy(self.uriRedundacia)

    def getBook(self,ID_Usuario,horaI):
        numLibros = len(self.DBServerR.getBQueue())
        if numLibros > 0:
            idLibro = self.DBServerR.popBQueue()+1
            libro = self.DBM.getLibroByID(idLibro)
            
            fecha = datetime.datetime.today()
            now = datetime.datetime.now()
            horaF=datetime.time(now.hour,now.minute,now.second,now.microsecond)

            (NumPedido,NumSesion) = self.DBM.setPedido(ID_Usuario,idLibro,fecha,horaI,horaF)
            self.DBServerR.BUPedido(NumPedido,NumSesion,ID_Usuario,idLibro,fecha,horaI,horaF)
            return (NumPedido,libro)
        else:
            return -1
    def anounceMe(self,IP,Nombre):
        ID = self.DBM.setUsuario(IP,Nombre)
        self.DBServerR.anounceMe(IP,Nombre,int(ID))
        return ID

    def resetSys(self):
        self.DBServerR.restartBQueue()
        self.DBM.resetDB()
        self.DBServerR.resetSys()
    

port = 9091
daemon = Pyro4.Daemon()                # make a Pyro daemon

DNServer = threading.Thread(target=initDNS,args=(port,) ,name='DNS')
DNServer.start()
    
ns = Pyro4.locateNS(port=port)                  # find the name server
uri = daemon.register(DBServer)   # register the greeting maker as a Pyro object
ns.register("principal", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
