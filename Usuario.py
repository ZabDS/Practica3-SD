import Pyro4

name = input("What is your name? ").strip()

DBServer = Pyro4.Proxy("PYRONAME:principal.coordinator")    # use name server object lookup uri shortcut
print(DBServer.getLibro(1))