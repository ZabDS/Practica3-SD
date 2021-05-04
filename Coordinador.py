# saved as greeting-server.py
import Pyro4
import Pyro4.naming as naming
import threading
import DBConnector

def initDNS():
    #Thread for start the DNS
    naming.startNSloop()

@Pyro4.expose
class DBServer():
    def __init__(self):
        self.DBM = DBConnector.DBManager("zabdiel","psw","127.0.0.1")    

    def getLibro(self,idLibro):
        libro = self.DBM.getLibroByID(idLibro)
        return libro

daemon = Pyro4.Daemon()                # make a Pyro daemon

DNServer = threading.Thread(target=initDNS, name='DNS')
DNServer.start()
    
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(DBServer)   # register the greeting maker as a Pyro object
ns.register("principal.coordinator", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
