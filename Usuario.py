import Pyro4
import time

DBServer = Pyro4.Proxy("PYRONAME:principal.coordinator")    # use name server object lookup uri shortcut

while True:
    try:
        print(DBServer.getLibro(1))
        time.sleep(1)
    except Pyro4.errors.ConnectionClosedError as e:
        print("Error al conectarse con el coordinador principal")
        print("Intentando conectarse con el coordinador de respaldo...")
        exit(-1)