# saved as greeting-server.py
import Pyro4
import Pyro4.naming as naming
import threading
import DBConnectorRed as DBConnector
import random
import time
import datetime
from  tkinter import Tk,Canvas,PhotoImage,Button
from PIL import ImageTk, Image
from clockObj import Clock

#La cola es controlada por el servidor de redundancia
global bookQueue
bookQueue = list(range(9))
random.shuffle(bookQueue)

global synClk
global synCond
synCond = threading.Condition()
synClk=False

def startSynClk(x):
    global synClk
    global synCond
    while True:
        synClk = True 
        print("True")

        with synCond:
            synCond.wait()

        time.sleep(3)       
        #print(synClk)

def TimeAtoS(timeArray):
    return str(timeArray[2])+":"+str(timeArray[1])+":"+str(timeArray[0])

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
        self.timeToLook = [0,0,12]
        self.Clock1 = Clock(self.root,0,2,self.timeToLook)
        self.Clock1.start()
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
        #Conectar con Maestro de sincronización
        self.uriPrincipalCoordinator = "PYRONAME:principal@127.0.0.1:9091"
        self.Server = Pyro4.Proxy
        self.threadSync = threading.Thread(target=self.callClk, name='Clk')
        self.coordinatorFlag = True
        self.threadSync.start()
        self.cliQueue = []
        self.DifsCli = {}
        self.time0 = ""

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
    #Métodos de sincronización con el servidor maestro
    def connectToMaster(self):
        print("Conexion con el coordinador principal")
        self.Server = Pyro4.Proxy(self.uriPrincipalCoordinator)
        self.coordinatorFlag = False

    def callClk(self):
        #print("Iniciando Hilo")
        while self.coordinatorFlag:
            pass

        while True:
            try:
                futurecall = Pyro4.Future(self.Server.syncDetonator)
                #futurecall.iferror()
                result = futurecall()
                if result.wait(3) and result.value != None: 
                    masterClkStr = result.value 
                    clientClkStr = TimeAtoS(window.Clock1.getTime())
                    #print(clientClkStr)
                    try:
                        clientClk = datetime.datetime.strptime(clientClkStr,"%H:%M:%S").time()
                        masterClk = datetime.datetime.strptime(masterClkStr,"%H:%M:%S").time()
                    finally:
                        print("error extraño")
                    Di = datetime.datetime.combine(datetime.date.today(), masterClk) - datetime.datetime.combine(datetime.date.today(), clientClk)
                    
                    Dif = self.Server.syncCordinator(0,Di.total_seconds())
                    clientClkStr = TimeAtoS(window.Clock1.getTime())
                    print(Dif)
                    timeNow = datetime.datetime.strptime(clientClkStr,"%H:%M:%S") - datetime.timedelta(seconds=Dif)
                    window.Clock1.setTime([timeNow.second,timeNow.minute,timeNow.hour])

            except Pyro4.errors.ConnectionClosedError:
                print("Convirtiendose en el nuevo servidor de tiempo...")
                #print(e)
                #self.changeServer()
                break

    #Métodos de sincronización como maestro
    def syncAverage(self):
        #Esperamos a que todos los cientes hayan respondido
        flag = 0
        while len(self.DifsCli.keys()) < len(self.cliQueue):
            flag = flag + 1
            if flag > 2: #NUmero de clientes máximo para no quedarse en ciclo inf
                break
        
        #Realizamos el promedio
        sum = 0.0
        i=0.0
        for Dif in self.DifsCli.values():
            sum = sum + Dif 
            i = i + 1
        
        average = sum / (i+1)
        print("La suma es ",sum," el numero division es ",i+1," tf ", average)
        #print(average)
        self.DifsCli.clear()
        return (average)

    def syncDif(self,Di):
        #Calculamos el Di' 
        T0 = datetime.datetime.strptime(self.time0,"%H:%M:%S").time()
        T1i = datetime.datetime.strptime(TimeAtoS(window.Clock1.getTime()),"%H:%M:%S").time()
        Dif1 = datetime.datetime.combine(datetime.date.today(), T1i) - datetime.datetime.combine(datetime.date.today(), T0)
        
        return (Di - Dif1.total_seconds() / 2)

    def syncCordinator(self,ID,Di):
        global synCond               
        #print(Di)
        Dif = self.syncDif(Di)

        #Añadimos el nuevo diferencial del cliente y lo actualizamos en el dicionario
        newDif = {ID:Dif}
        self.DifsCli.update(newDif)
        print(self.DifsCli)

        #Calculamos el promedio
        Av = self.syncAverage()
        with synCond:
            synCond.notifyAll()
            print("liberando")

        print(Av - Dif)
        return (Av - Dif)

    def syncDetonator(self):
        global synClk
        global synCond
        #Este metodo es invocado de forma asincrona multiples veces por el cliente
        #Esperamos a que pase el tiempo de sincronización programado
        if synClk:
            synClk=False
            print("sincronizando")
            timeStr0 = TimeAtoS(window.Clock1.getTime())
            self.time0 = timeStr0
            print(timeStr0)
            return (self.time0) 
    

#MAIN
port = 9092
daemon = Pyro4.Daemon()                # make a Pyro daemon

DNServer = threading.Thread(target=initDNS,args=(port,) ,name='DNS')
DNServer.start()
    
Clk = threading.Thread(target=startSynClk, args=(2,) ,name='Clk')
Clk.start()

ns = Pyro4.locateNS(port=port)                  # find the name server
uri = daemon.register(DBServer)   # register the greeting maker as a Pyro object
ns.register("Redundancia", uri)   # register the object with a name in the name server

print("Ready.")
window.start()
daemon.requestLoop()                   # start the event loop of the server to wait for calls
