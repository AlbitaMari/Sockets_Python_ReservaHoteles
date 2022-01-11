from threading import Thread, Semaphore, Lock
import socket
import random
import operator
from time import sleep 
import re

class Hotel(Thread):
    def __init__(self, socket_cliente, datos_cliente):
        Thread.__init__(self)
        self.socket = socket_cliente
        self.datos = datos_cliente
        self.reserva_cliente = 0
        self.email=""

    def run(self):
        global mutex
        isLog = True
        while isLog:
            opcion = self.socket.recv(1024).decode()
    
            if(opcion == "1"):
                    
                email = self.socket.recv(1024).decode()
                sleep(1)
                
                if re.match(validacion,email):
                    print(email)
                    with open("usuarios.txt",'r') as f:     
                        if email not in f.read():
                            self.socket.send(str("N").encode())
                        else:
                            self.socket.send(str("Y").encode())
                            self.email = email
                            isLog=False
                            
                else:
                    self.socket.send(str("N").encode())
                    
            if(opcion=="2"): 
                    
                email = self.socket.recv(1024).decode()
                print(email)
                sleep(1)

                clave = self.socket.recv(1024).decode()
                sleep(1)
                        
                if re.match(validacion, email):
                    print("registro")
                    with open("usuarios.txt",'r+') as f:
                        if email in f.read():
                            resultado = email[0:len(email)]
                            isRegister= "N"
                            self.socket.send(str(isRegister).encode())
                            sleep(1)
                        else:
                            f.write(str(email)+":"+str(clave)+":\n")
                            isRegister = "Y"
                            self.socket.send(str(isRegister).encode())
                            sleep(1)
                else:
                    print(error_email)
                    self.socket.send(error_email.encode())
                    sleep(1)
        onLine=True
        while onLine:
            with open("hoteles.txt","r") as f:
                info=[]
                for l in f:
                    infor = l.split(":")
                    info.append(infor)
                f.close()
            opcion = int(self.socket.recv(1024).decode())
            if(opcion == 1):
                onLine = False
                self.socket.close()
            if(opcion == 2):
                self.socket.send(str(nh).encode())
                sleep(1)
                for i in range(0,len(info)):
                    mi = "Nº "+str(i+1)+":\n NOMBRE: "+info[i][0]+"\nHab.Totales: "+str(nhnes)+" habitaciones.\nHab.Libres: "+str(info[i][1])+"\nHabitaciones ocupadas:"+str(info[i][2])+"\n"
                    self.socket.send(mi.encode())
                    sleep(1)
                self.socket.send(str(self.reserva_cliente).encode())
                sleep(1)
                
            if(opcion==3):
                hotel = int(self.socket.recv(1024).decode())
                if(hotel<=nh and hotel>0 and hotel!=0):
                    self.socket.send(str("Y").encode())
                    num_hab = int(self.socket.recv(1024).decode())
                    sleep(1)
                    reserva.acquire()
                    mutex.acquire()
                    sleep(1)
                    with open("hoteles.txt","r") as f:
                        lineas = []
                        for l in f:
                            linea = l.split(":")
                            lineas.append(linea)
                        f.close()
                        for i in range(0,len(lineas)):
                            if((i+1)==hotel):
                                hl = lineas[i][1].split(",")
                                ho = lineas[i][2].split(",")
                        for i in hl:
                            if(i == ""):
                                hl.remove(i)
                        for i in ho:
                            if(i == ""):
                                ho.remove(i)
                        if(len(hl)>=num_hab):
                            m = "T"
                            self.socket.send(m.encode())
                            rc = self.socket.recv(1024).decode()
                            if(rc =="Y"):
                                while num_hab!=0:
                                    hab_num = self.socket.recv(1024).decode()
                                    ho.append(hab_num)
                                    if(hab_num not in hl):
                                        isF = "F"
                                        self.socket.send(isF.encode())
                                        break
                                    elif(hab_num in hl):
                                        isF="T"
                                        self.socket.send(isF.encode())
                                        for i in hl:
                                            if(hab_num==i):
                                                hl.remove(i)
                                    num_hab-=1
                                if(isF=="T"):
                                    self.reserva_cliente += 1
                                    f = open("hoteles.txt","w")
                                    for i in range(0,len(lineas)):
                                        if(i==(hotel-1)):
                                            f.write(str(lineas[i][0])+":")
                                            for i in hl:
                                                f.write(str(i)+",")
                                            f.write(":")
                                            for i in ho:
                                                f.write(str(i)+",")
                                            f.write(":\n")
                                        elif(i!=(hotel-1)):
                                            f.write(str(lineas[i][0])+":"+str(lineas[i][1])+":"+str(lineas[i][2])+":\n")
                                    f.close()
                                    sleep(1)
                                    ms = "\nHa reservado correctamente.\n"
                                    print(ms)
                                    self.socket.send(ms.encode())
                        elif((len(hl)<num_hab)):
                            self.socket.send(str("F").encode())
                    reserva.release()
                    mutex.release()
                else:
                    self.socket.send(str("N").encode())

            if(opcion==4):
                receptor = self.socket.recv(1024).decode()
                with open("usuarios.txt","r") as f:
                    if receptor not in f.read():
                        self.socket.send(str("F").encode())
                    else:
                        self.socket.send(str("T").encode())
                        mensaje = self.socket.recv(1024).decode()
                        users = []
                        reserva.acquire()
                        with open("usuarios.txt","r") as f:
                            for l in f:
                                li = l.split(":")
                                users.append(li)
                            f.close()
                        for i in range(0,len(users)):
                            users[i].remove("\n")
                            if(str(users[i][0])==str(receptor)):
                                users[i].append(mensaje)
                        f = open("usuarios.txt","w")
                        for i in range(0,len(users)):
                            for j in range(0,len(users[i])):
                                f.write(str(users[i][j])+":")
                            f.write("\n")
                        f.close()
                        resp = "Mensaje enviado correctamente"
                        self.socket.send(resp.encode())
                        reserva.release()
            
            if(opcion==5):
                correo = self.socket.recv(1024).decode()
                contr = self.socket.recv(1024).decode()
                sleep(1)
                if(correo == self.email):
                    self.socket.send(str("T").encode())
                    with open("usuarios.txt","r") as f:
                        lin=[]
                        for l in f:
                            li = l.split(":")
                            lin.append(li)
                        f.close()
                    for i in range(0,len(lin)):
                        if((str(lin[i][0])==str(correo)) and (str(lin[i][1])==contr)):
                            usuario = lin[i]
                    for i in usuario:
                        if(i=="\n"):
                            usuario.remove(i)
                            usuario.append("")
                    num = str(len(usuario)-2)
                    self.socket.send(num.encode())
                    sleep(1)
                    for i in range(2,len(usuario)):
                        if(usuario[i] == ""):
                            self.socket.send(str("No tiene mensajes").encode())
                            sleep(1)
                        else:
                            self.socket.send(str(usuario[i]).encode())
                            sleep(1)
                    for i in range(2,len(usuario)):
                        usuario.pop(2)
                    reserva.acquire()
                    f= open("usuarios.txt","w")
                    for i in range(0,len(lin)):
                        if(str(lin[i][0])==str(usuario[0])):
                            for i in range(0,len(usuario)):
                                f.write(usuario[i]+":")
                            f.write("\n")
                        else:
                            f.write(str(lin[i][0]+":"+str(lin[i][1]+":\n")))
                    f.close()
                    reserva.release()
                else:
                    self.socket.send(str("F").encode())
                    sleep(1) 
                               
def crearFichero():
    f = open("hoteles.txt","w")
    for i in range(0,len(hoteles)):
        f.write(str(hoteles[i]+":"))
        for i in range(0,len(hab_lib)):
            f.write(str(hab_lib[i])+",")
        f.write(":")
        for i in range(0,len(hab_ocu)):
            f.write(str(hab_ocu[i])+",")
        f.write(":\n") 

hoteles=[]
hab_lib=[]
hab_ocu=[]
contador=1
mutex = Lock()
reserva = Semaphore(1)
error_email = "Mensaje de error. Debe introducir un email válido"
validacion = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9999))
server.listen(1)

nh = int(input("Bienvenido\n¿Cuántos hoteles desea registrar?"))
nhnes = int(input("¿Cuantas habitaciones tendrán los hoteles?"))

for i in range(0,nhnes):
    hab_lib.append(i+1)
for i in range(0,nh):
    name = input("Introduce el nombre para el hotel número "+str(i+1)+" :")
    hoteles.append(name)


crearFichero() 

while True:
        
    socket_cliente, datos_cliente = server.accept()
    socket_cliente.send(str(datos_cliente).encode())
    hilo=Hotel(socket_cliente,datos_cliente)
    hilo.start()