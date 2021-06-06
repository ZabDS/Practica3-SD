import Pyro4
import time
import socket
import datetime
from  tkinter import Tk,Button,Label,messagebox
import threading


uriPrincipalCoordinator = "PYRONAME:principal@127.0.0.1:9091"
uriRespaldoCoordinator = "PYRONAME:Redundancia@127.0.0.1:9092"
DBServer = Pyro4.Proxy(uriPrincipalCoordinator) 
DBServerR = Pyro4.Proxy(uriRespaldoCoordinator)

now=datetime.datetime.now()
global timeNow
timeNow = [now.second,now.minute,now.hour]

root=Tk()
root.geometry("720x480")
root.title("Usuario")

def TimeAtoS(timeArray):
    return str(timeArray[2])+":"+str(timeArray[1])+":"+str(timeArray[0])

class Usuario():
    def __init__(self,interfaz):
        self.Interfaz = interfaz
        self.Name = socket.gethostname()
        self.Server = DBServer
        self.IP= socket.gethostbyname(self.Name)
        self.ID = DBServer.anounceMe(self.IP,self.Name)
        self.threadSync = threading.Thread(target=self.callClk, name='Clk')
        self.threadSync.start()
        
    def callClk(self):
        global timeNow
        while True:
            try:
                futurecall = Pyro4.Future(self.Server.syncDetonator)
                #futurecall.iferror()
                result = futurecall()
                if result.wait(3) and result.value != None:                    
                    masterClkStr = result.value 
                    clientClkStr = TimeAtoS(self.Interfaz.timeForLook)
                    #print(clientClkStr)
                    clientClk = datetime.datetime.strptime(clientClkStr,"%H:%M:%S").time()
                    masterClk = datetime.datetime.strptime(masterClkStr,"%H:%M:%S").time()
                    Di = datetime.datetime.combine(datetime.date.today(), masterClk) - datetime.datetime.combine(datetime.date.today(), clientClk)
                    
                    Dif = self.Server.syncCordinator(self.ID,Di.total_seconds())
                    clientClkStr = TimeAtoS(self.Interfaz.timeForLook)
                    print(Dif)
                    timeNow = datetime.datetime.strptime(clientClkStr,"%H:%M:%S") - datetime.timedelta(seconds=Dif)
                    self.Interfaz.setTime([timeNow.second,timeNow.minute,timeNow.hour])

            except Pyro4.errors.ConnectionClosedError:
                print("Error al conectarse con el coordinador principal")
                #print(e)
                self.changeServer()
                break

                
    def changeServer(self):
        print("Intentando conectarse con el coordinador de respaldo...")
        self.Server = DBServerR
        print("Conexión exitosa")

    def getBook(self):
        try:
            now = datetime.datetime.now()
            horaI=datetime.time(now.hour,now.minute,now.second,now.microsecond)
            Libro = self.Server.getBook(self.ID,horaI) 
            #print(self.Server.getBook(self.ID,horaI))
            return (1,Libro)
        except Pyro4.errors.ConnectionClosedError as e:
            print("Error al conectarse con el coordinador principal")
            print(e)
            self.changeServer()
            return (-1,"")

    def reset(self):
        self.Server.resetSys()

class Interfaz(threading.Thread):
    def __init__(self,time):
        threading.Thread.__init__(self)
        self.timeForLook = time
        self.label = Label(root,font=("times",50,"bold"))
        self.labelBook = Label(root,font=("times",25,"bold"))
        self.buttonReset = Button(root, text="Reiniciar")
        self.buttonBook = Button(root, text="Pedir Libro")
        self.Usuario = Usuario(self)

    def run(self):
        self.label.grid(row=0,column=0,pady=25,padx=100)
        self.buttonReset.grid(row=1,column=0,pady=25,padx=100)
        self.buttonReset.config(command = self.buttonActionRestart)
        self.buttonBook.grid(row=2,column=0,pady=25,padx=100)
        self.buttonBook.config(command = self.buttonActionBook)
        self.labelBook.grid(row=3,column=0,pady=25,padx=100)
        self.time()

    def time(self):
        while True:    
            textLabel = str(self.timeForLook[2])+":"+str(self.timeForLook[1])+":"+str(self.timeForLook[0])
            self.label.config(text=textLabel)
            self.timeForLook[0]=self.timeForLook[0]+1
            time.sleep(1)
            if (self.timeForLook[0]>59):
                self.timeForLook[0]=0
                self.timeForLook[1]=self.timeForLook[1]+1
            if (self.timeForLook[1]>59):
                self.timeForLook[1]=0
                self.timeForLook[2]=self.timeForLook[2]+1
            if (self.timeForLook[2]>23):
                self.timeForLook[2]=0
#Aqui no se si deberamos eliminar el if
    def buttonActionBook(self):
        (cod,Libro) = self.Usuario.getBook()
        print(Libro)
        if cod < 0:
            self.labelBook.config(text = "Error, intente de nuevo")
        elif type(Libro) != int:
            self.labelBook.config(text = Libro[1][1])
        else:
            answer = messagebox.askyesnocancel("Ya no quedan libros", "Desea salir de la tienda?")
            if answer == True:
                exit(1)

    def buttonActionRestart(self):
        self.Usuario.reset()
    
    def setTime(self,newTime):
        self.timeForLook = newTime

NewUsuario = Interfaz([0,0,12])
NewUsuario.start()
root.mainloop()


#i=0
#while (i<5):
#    i = i+1
#    #DBServer.resetSys()
#    try:
#        NewUsuario.getBook()
#    except Pyro4.errors.ConnectionClosedError as e:
#        print("Error al conectarse con el coordinador principal")
#        print(e)
#        NewUsuario.changeServer()
#    #time.sleep(1)