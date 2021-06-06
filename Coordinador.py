# saved as greeting-server.py
import Pyro4
import Pyro4.naming as naming
import threading
import DBConnector
import random
import datetime
import time
from  tkinter import Tk,Canvas,PhotoImage,Button
from PIL import ImageTk, Image
from clockObj import Clock

uriPrincipalCoordinator = "PYRONAME:principal@127.0.0.1:9091"
now = datetime.datetime.now()

global synClk
global synCond
synCond = threading.Condition()
synClk=False

def initDNS(port):
    #Thread for start the DNS
    naming.startNSloop(port=port)

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

class Interfaz(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):    
        self.root = Tk()
        self.root.geometry("1080x480")
        self.root.title("Coordinador")
        self.canvas = Canvas(self.root,width = "450",height = "500", background="black")
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
        print(routeImg)
        self.ImgCanvas = ImageTk.PhotoImage(Image.open(routeImg))
        self.canvas.create_image(50, 10, image=self.ImgCanvas, anchor="nw")

    def buttonActionRestart(self):
        DBServerMS = Pyro4.Proxy(uriPrincipalCoordinator) 
        self.ImgCanvas = PhotoImage(file="")
        DBServerMS.resetSys()


window = Interfaz()

@Pyro4.expose
class DBServer():
    def __init__(self):
        self.DBM = DBConnector.DBManager("zabdiel","idscom","127.0.0.1","LibraryDB")
        self.uriRedundacia = "PYRONAME:Redundancia@127.0.0.1:9092"
        self.DBServerR = Pyro4.Proxy(self.uriRedundacia)
        self.cliQueue = []
        self.DifsCli = {}
        self.time0 = ""

    def getBook(self,ID_Usuario,horaI):
        numLibros = len(self.DBServerR.getBQueue())
        if numLibros > 0:
            idLibro = self.DBServerR.popBQueue()+1
            libro = self.DBM.getLibroByID(idLibro)
            
            routeImg = libro[5]
            #print(routeImg)
            window.setPortada(routeImg)
            fecha = datetime.datetime.today()
            now = datetime.datetime.now()
            horaF=datetime.time(now.hour,now.minute,now.second,now.microsecond)

            (NumPedido,NumSesion) = self.DBM.setPedido(ID_Usuario,idLibro,fecha,horaI,horaF)
            self.DBServerR.BUPedido(NumPedido,NumSesion,ID_Usuario,idLibro,fecha,horaI,horaF,routeImg)
            return (NumPedido,libro)
        else:
            return -1
    def anounceMe(self,IP,Nombre):
        ID = self.DBM.setUsuario(IP,Nombre)
        self.DBServerR.anounceMe(IP,Nombre,int(ID))
        self.cliQueue.append(Pyro4.core.current_context.client)
        return ID

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
        T1i = datetime.datetime.strptime(TimeAtoS(window.timeToLook),"%H:%M:%S").time()
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
            timeStr0 = str(window.timeToLook[2])+":"+str(window.timeToLook[1])+":"+str(window.timeToLook[0])
            self.time0 = timeStr0
            return (self.time0)           
            

    def resetSys(self):
        self.DBServerR.restartBQueue()
        self.DBM.resetDB()
        self.DBServerR.resetSys()
        print("Sistema reiniciado")


port = 9091
daemon = Pyro4.Daemon()                # make a Pyro daemon

DNServer = threading.Thread(target=initDNS,args=(port,) ,name='DNS')
DNServer.start()

Clk = threading.Thread(target=startSynClk, args=(2,) ,name='Clk')
Clk.start()
    
ns = Pyro4.locateNS(port=port)                  # find the name server
uri = daemon.register(DBServer)   # register the greeting maker as a Pyro object
ns.register("principal", uri)   # register the object with a name in the name server

print("Ready.")
window.start()
daemon.requestLoop()                   # start the event loop of the server to wait for calls
