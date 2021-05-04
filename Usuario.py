import Pyro4
import time
import socket

uriPrincipalCoordinator = "PYRONAME:principal@127.0.0.1:9091"
#DBServer = Pyro4.Proxy("PYRONAME:principal")    # use name server object lookup uri shortcut
DBServer = Pyro4.Proxy(uriPrincipalCoordinator)    # use name server object lookup uri shortcut

Name = socket.gethostname()
IP= socket.gethostbyname(Name)

while True:
    try:
        print(DBServer.getLibro(1))
        time.sleep(1)
    except Pyro4.errors.ConnectionClosedError as e:
        print("Error al conectarse con el coordinador principal")
        print("Intentando conectarse con el coordinador de respaldo...")
        exit(-1)