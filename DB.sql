CREATE SCHEMA LibraryDB;

USE LibraryDB;

CREATE TABLE Libro(
	ISBN INT,
	nombre VARCHAR(45),
	Autor VARCHAR(45),
	Editorial VARCHAR(45),
	Precio FLOAT,
	Portada VARCHAR(100),
   
   PRIMARY KEY(ISBN)
);

CREATE TABLE Pedido(
	ID INT,
	fecha DATE,
	hora_inicio TIME,
	hora_fin TIME,
	
	PRIMARY KEY(ID)
);

CREATE TABLE Usuario(
	ID INT,
	IP VARCHAR(20),
	Nombre VARCHAR(45),
	
	PRIMARY KEY(ID)
);

CREATE TABLE UsuarioSesion(
	ID INT,
	ID_Usuario INT,
	ID_Pedido INT,
	Tiempo_Usuario TIME,
	Lugar_Jugador INT,
	
	PRIMARY KEY(ID),
	FOREIGN KEY(ID_Usuario) REFERENCES Usuario(ID) ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY(ID_Pedido) REFERENCES Pedido(ID) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE Sesion(
	ID INT,
	ID_Pedido INT,
	ID_libro INT,
	
	PRIMARY KEY(ID),
	FOREIGN KEY(ID_Pedido) REFERENCES Pedido(ID) ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY(ID_libro) REFERENCES Libro(ISBN) ON UPDATE CASCADE ON DELETE SET NULL
);

INSERT INTO Libro VALUES(1,"Il Principe","Nicolas Maquiavelo","Titivillus",700.00,"~/Documentos/Distribuidos/Practica\ 3/IMG/Port1.jpeg");
INSERT INTO Libro VALUES(2,"Orgullo y prejuicio","Jane Austn","Penguin Clasicos",300.00,"~/Documentos/Distribuidos/Practica\ 3/IMG/Port2.jpeg");
INSERT INTO Libro VALUES(3,"Dracula","Bram Stoker","Valdemar",2000.00,"~/Documentos/Distribuidos/Practica\ 3/IMG/Port3.jpeg");
INSERT INTO Libro VALUES(4,"1984","George Orwell","libra",421.00,"~/Documentos/Distribuidos/Practica\ 3/IMG/Port4.jpeg");
INSERT INTO Libro VALUES(5,"La Mandragora","Nicolas Maquiavelo","Titivillus",543.00,"~/Documentos/Distribuidos/Practica\ 3/IMG/Port5.jpeg");
INSERT INTO Libro VALUES(6,"Sueno de una noche de verano","William Shakespeare","Planeta Libro",678.00,"~/Documentos/Distribuidos/Practica\ 3/IMG/Port6.jpeg");
INSERT INTO Libro VALUES(7,"El Ultimo Deseo","Andrzej Sapkowski","Ikero",912.00,"~/Documentos/Distribuidos/Practica\ 3/IMG/Port7.jpeg");
INSERT INTO Libro VALUES(8,"La Nacion de las Bestias","Mariana Palova","Titivillus",345.00,"~/Documentos/Distribuidos/Practica\ 3/IMG/Port8.jpeg");
INSERT INTO Libro VALUES(9,"El conde de Montecristo","Alexandre Sumas","Titivillus",678.00,"~/Documentos/Distribuidos/Practica\ 3/IMG/Port9.jpeg");