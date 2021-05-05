import Pyro4
import time
import socket
import datetime

uriPrincipalCoordinator = "PYRONAME:principal@127.0.0.1:9091"
#DBServer = Pyro4.Proxy("PYRONAME:principal")    # use name server object lookup uri shortcut
DBServer = Pyro4.Proxy(uriPrincipalCoordinator)    # use name server object lookup uri shortcut

Name = socket.gethostname()
IP= socket.gethostbyname(Name)
DBServer.resetSys()
ID = DBServer.anounceMe(IP,Name)
while True:
    try:
        now = datetime.datetime.now()
        horaI=datetime.time(now.hour,now.minute,now.second,now.microsecond)
        print(DBServer.getBook(ID,horaI))
        time.sleep(1)
    except Pyro4.errors.ConnectionClosedError as e:
        print("Error al conectarse con el coordinador principal")
        print("Intentando conectarse con el coordinador de respaldo...")
        exit(-1)