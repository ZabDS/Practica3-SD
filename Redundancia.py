# saved as greeting-server.py
import Pyro4
import Pyro4.naming as naming
import threading
import DBConnectorRed as DBConnector
import random
import datetime
from  tkinter import Tk,Canvas,PhotoImage,Button
from PIL import ImageTk, Image

#La cola es controlada por el servidor de redundancia
global bookQueue
bookQueue = list(range(9))
random.shuffle(bookQueue)

def initDNS(port):
    #Thread for start the DNS
    naming.startNSloop(port=port)

class Interfaz(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):    
        self.root = Tk()
        self.root.geometry("1080x480")
        self.root.title("Redundancia")
        self.canvas = Canvas(self.root,width = "395",height = "550", background="black")
        self.canvas.grid(column=0, row=0)
        self.ImgCanvas = PhotoImage(file="")
        self.button = Button(self.root, text="Reiniciar")
        self.button.grid(row=0,column=1,pady=25,padx=100)
        self.button.config(command = self.buttonActionRestart)
        self.root.mainloop()
    
    def setPortada(self,routeImg):
        #print(routeImg)
        self.ImgCanvas = ImageTk.PhotoImage(Image.open(routeImg))
        self.canvas.create_image(50, 10, image=self.ImgCanvas, anchor="nw")

    def buttonActionRestart(self):
        uriRespaldoCoordinator = "PYRONAME:Redundancia@127.0.0.1:9092"
        DBServerMS = Pyro4.Proxy(uriRespaldoCoordinator)
        self.ImgCanvas = PhotoImage(file="") 
        DBServerMS.resetSys()


window = Interfaz()

#Objeto que será compartido a través de la red
@Pyro4.expose
class DBServer():
    def __init__(self):
        #Conector de BD
        self.DBM = DBConnector.DBManager("zabdiel","idscom","127.0.0.1","LibraryDBR")

    #Método para obtener un libro
    def getBook(self,ID_Usuario,horaI):
        global bookQueue
        numLibros = len(bookQueue)
        if numLibros > 0:
            idLibro = bookQueue.pop()+1
            libro = self.DBM.getLibroByID(idLibro)
            
            routeImg = libro[5]
            window.setPortada(routeImg)

            fecha = datetime.datetime.today()
            now = datetime.datetime.now()
            horaF=datetime.time(now.hour,now.minute,now.second,now.microsecond)

            #Escribe los calculos de tiempo y los id's a la bd
            (NumPedido,NumSesion) = self.DBM.setPedido(ID_Usuario,idLibro,fecha,horaI,horaF)
            return (NumPedido,libro)
        else:
            return -1
    #Método para el BackUp del pedido hecho en la bd del BackUp
    def BUPedido(self,ID_Pedido,ID_Sesion,ID_Usuario,idLibro,fecha,horaI,horaF,routeImg):
        self.DBM.setPedidoBU(ID_Pedido,ID_Sesion,ID_Usuario,idLibro,fecha,horaI,horaF)
        window.setPortada(routeImg)

    #Método que sirve para anunciar que un nuevo cliente se ha conectado y se registre a la BD
    def anounceMe(self,IP,Nombre,ID_usr=-1):
        if(ID_usr < 0):
            ID = self.DBM.setUsuario(IP,Nombre)
            return ID
        else:
            ID_usr = self.DBM.setUsuario(IP,Nombre,ID_usr)
            return ID_usr
    #Método para reiniciar el sistema y limpiar la base de datos
    def resetSys(self):
        global bookQueue
        bookQueue = self.restartBQueue()
        self.DBM.resetDB()
    #Método de prueba de conexión; útil para los usuarios
    def connTest(self):
        return 1
    #Métodos para el control de la cola de libros. Utilies para su manejo en el coordinador principal
    def getBQueue(self):
        return bookQueue
    def popBQueue(self):
        return bookQueue.pop()
    def restartBQueue(self):
        NewbookQueue = list(range(9))
        random.shuffle(NewbookQueue)
        bookQueue=NewbookQueue
        return bookQueue

#MAIN
port = 9092
daemon = Pyro4.Daemon()                # make a Pyro daemon

DNServer = threading.Thread(target=initDNS,args=(port,) ,name='DNS')
DNServer.start()
    
ns = Pyro4.locateNS(port=port)                  # find the name server
uri = daemon.register(DBServer)   # register the greeting maker as a Pyro object
ns.register("Redundancia", uri)   # register the object with a name in the name server

print("Ready.")
window.start()
daemon.requestLoop()                   # start the event loop of the server to wait for calls
