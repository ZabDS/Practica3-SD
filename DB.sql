CREATE SCHEMA LibraryDB;

USE LibraryDB;

CREATE TABLE Libro(
	ISBN INT AUTO_INCREMENT,
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
	hora_inicio TIME(2),
	hora_fin TIME(2),
	
	PRIMARY KEY(ID)
);

CREATE TABLE Usuario(
	ID INT AUTO_INCREMENT,
	IP VARCHAR(20),
	Nombre VARCHAR(45),
	
	PRIMARY KEY(ID)
);

CREATE TABLE UsuarioSesion(
	ID INT,
	ID_Usuario INT,
	ID_Pedido INT,
	Tiempo_Usuario TIME(2),
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

INSERT INTO Libro (nombre,Autor,Editorial,Precio,Portada) VALUES("Il Principe","Nicolas Maquiavelo","Titivillus",700.00,"IMG/Port1.jpg");
INSERT INTO Libro (nombre,Autor,Editorial,Precio,Portada) VALUES("Orgullo y prejuicio","Jane Austn","Penguin Clasicos",300.00,"IMG/Port2.jpg");
INSERT INTO Libro (nombre,Autor,Editorial,Precio,Portada) VALUES("Dracula","Bram Stoker","Valdemar",2000.00,"IMG/Port3.jpg");
INSERT INTO Libro (nombre,Autor,Editorial,Precio,Portada) VALUES("1984","George Orwell","libra",421.00,"IMG/Port4.jpg");
INSERT INTO Libro (nombre,Autor,Editorial,Precio,Portada) VALUES("La Mandragora","Nicolas Maquiavelo","Titivillus",543.00,"IMG/Port5.jpg");
INSERT INTO Libro (nombre,Autor,Editorial,Precio,Portada) VALUES("Sueno de una noche de verano","William Shakespeare","Planeta Libro",678.00,"IMG/Port6.jpg");
INSERT INTO Libro (nombre,Autor,Editorial,Precio,Portada) VALUES("El Ultimo Deseo","Andrzej Sapkowski","Ikero",912.00,"IMG/Port7.jpg");
INSERT INTO Libro (nombre,Autor,Editorial,Precio,Portada) VALUES("La Nacion de las Bestias","Mariana Palova","Titivillus",345.00,"IMG/Port8.jpg");
INSERT INTO Libro (nombre,Autor,Editorial,Precio,Portada) VALUES("El conde de Montecristo","Alexandre Sumas","Titivillus",678.00,"IMG/Port9.jpg");
