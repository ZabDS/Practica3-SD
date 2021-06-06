from  tkinter import *
import time
import threading
from datetime import datetime
from random import randrange
from tkinter import messagebox
from tkinter import simpledialog
import socket

class Clock(threading.Thread):
   def __init__(self,root,row,column,time):
      threading.Thread.__init__(self)
      self.root = root
      self.row = row
      self.column = column
      self.speed = 1
      self.event = threading.Event()
      self.event.set()
      self.timeForLook = time
      self.label = Label(self.root,font=("times",50,"bold"))
      self.buttonModificar = Button(self.root, text="Modificar")
      self.buttonEnviar = Button(self.root, text="Enviar")
      self.eventFlag = False

   def run(self):
      self.label.grid(row=self.row,column=self.column,pady=25,padx=100)
      self.buttonModificar.grid(row=self.row+1,column=self.column,pady=25,padx=50)
      self.buttonModificar.config(command = self.buttonActionPause)
      self.buttonEnviar.grid(row=self.row+2,column=self.column,pady=25,padx=50)
      self.buttonEnviar.config(command = self.buttonActionSend)
      self.time()

   def time(self):
      while True:
         while self.event.isSet():
            textLabel = str(self.timeForLook[2])+":"+str(self.timeForLook[1])+":"+str(self.timeForLook[0])
            self.label.config(text=textLabel)
            self.timeForLook[0]=self.timeForLook[0]+1
            time.sleep(self.speed)
            if (self.timeForLook[0]>59):
                 self.timeForLook[0]=0
                 self.timeForLook[1]=self.timeForLook[1]+1
            if (self.timeForLook[1]>59):
                 self.timeForLook[1]=0
                 self.timeForLook[2]=self.timeForLook[2]+1
            if (self.timeForLook[2]>23):
                 self.timeForLook[2]=0
#Aqui no se si deberamos eliminar el if
   def buttonActionPause(self):
     if self.event.isSet():
      self.event.clear()
      hora = simpledialog.askinteger("Ajuste","Hora",parent=self.root,minvalue=0,maxvalue=24)
      minuto = simpledialog.askinteger("Ajuste","Minuto",parent=self.root,minvalue=0,maxvalue=59)
      segundo = simpledialog.askinteger("Ajuste","Segundo",parent=self.root,minvalue=0,maxvalue=59)
      
      velocidad = simpledialog.askfloat("Ajuste","Velocidad",parent = self.root, minvalue = 0.0,maxvalue=1.0)

      self.timeForLook = [segundo,minuto,hora]

      self.speed = velocidad
      
      self.event.set()
     else:
      self.event.set()
   
   def buttonActionSend(self):
      self.eventFlag = True
   
   def setTime(self, time):
      self.timeForLook = time
   
   def getTime(self):
      return self.timeForLook
   
   def getEventFlag(self):
      return self.eventFlag

   def setEventFlag(self,value):
      self.eventFlag = value

