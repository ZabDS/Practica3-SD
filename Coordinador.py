# saved as greeting-server.py
import Pyro4
import Pyro4.naming as naming
import threading
import DBConnector

def initDNS(port):
    #Thread for start the DNS
    naming.startNSloop(port=port)

@Pyro4.expose
class DBServer():
    def __init__(self):
        self.DBM = DBConnector.DBManager("zabdiel","idscom","127.0.0.1")
    def getBook(self,idLibro):
        libro = self.DBM.getLibroByID(idLibro)
        return libro
    def anounceMe(self,IP,Nombre):
        self.DBM.setUsuario(IP,Nombre)

port = 9091
daemon = Pyro4.Daemon()                # make a Pyro daemon

DNServer = threading.Thread(target=initDNS,args=(port,) ,name='DNS')
DNServer.start()
    
ns = Pyro4.locateNS(port=port)                  # find the name server
uri = daemon.register(DBServer)   # register the greeting maker as a Pyro object
ns.register("principal", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
