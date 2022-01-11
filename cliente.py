from random import choice
import socket
from time import sleep

def menu():
    print("Bienvenido a nuestra aplicación de reservas: ")
    print("1) Iniciar sesión.")
    print("2) Registrar usuario.")
    op = int(input("Elige una opción: "))
    s.send(str(op).encode())
    
    if op == 1:
        print("|LOGIN DE USUARIO|")
        login()
    
    elif op == 2:
        print("|REGISTRO DE USUARIO|")
        registrar()
        
    else:
        print("Opcion no valida")
        menu()
        
def login():
    
    print("|******LOGIN DE USUARIO******|")
    email = input("Escriba su email: ")
    s.send(email.encode())

    clave = input("Escriba su clave: ")
    
    loginValido = s.recv(1024).decode()
    if(loginValido == "N"):
        print("Su email no es válido. Porfavor, registrate!!!")
        menu()
    else:
        print("Ha iniciado sesion correctamente!!!")
        inicio()
        
def registrar():
    
    print("|******REGISTRO DE USUARIO******|")
    email = input("Escriba su email: ")
    s.send(email.encode())
        
    clave = input("Escriba su clave: ")
    s.send(clave.encode())
    
    sleep(0.5)
        
    registroValido = s.recv(1024).decode()
    if(registroValido =="Y"):
        print("Te has registrado correctamente!!")
        menu()
    else:
        print("Error de registro. Intentalo de nuevo")
        menu()
        

def inicio():
    
    print("*** M E N U ***\n1) Salir\n2) Listar Hoteles\n3) Reservar habitaciones\n4) Enviar mensaje a otro usuario\n5) Leer mensajes")
    opc = int(input("Elige una opción: "))
    s.send(str(opc).encode())
    
    if(opc == 1):
        print("Saliendo del sistema.\nHasta pronto\nGracias")
        s.close()
        
    if(opc == 2):
        listar()
        
    if(opc == 3):
        reservar()
         
    if( opc == 4):
        enviarMensaje()
        
    if(opc==5):
        leerMensaje()

def listar():
    nh = int(s.recv(1024).decode())
    for i in range(0,nh):
        info = s.recv(1024).decode()
        print(info)
    reservas = s.recv(1024).decode()
    print("\nHas hecho "+str(reservas)+" reservas.\n")
    inicio()

def reservar():
        hotel = int(input("Bienvenido al apartado de reservas.\nPorfavor introduce el número del hotel donde quieres reservar: "))
        s.send(str(hotel).encode())
        # sleep(1)
        isH = s.recv(1024).decode()
        if(isH =="Y"):
            hab_res = int(input("Introduce el número de habitaciones que va a reservar: "))
            s.send(str(hab_res).encode())
            print("Comprobando disponibilidad...")
            r = s.recv(1024).decode()
            if(r=="T"):
                rsv = input("Existe disponibilidad. Quieres realizar la reserva?(Y/N): ")
                s.send(rsv.encode())
                if(rsv=="Y"):
                    while hab_res!=0:
                        num_hab = int(input("Introduce el número de habitacion que quiere reservar: "))
                        s.send(str(num_hab).encode())
                        isF = s.recv(1024).decode()
                        if(isF=="F"):
                            print("\nLo sentimos, la habitación que quiere reservar no se encuentra disponible\n")
                            inicio()
                        hab_res-=1
                    print("Estamos gestionando su reserva....")
                    ms = s.recv(1024).decode()
                    print(ms)
                    inicio()
                elif(rsv=="N"):
                    inicio()
            elif(r=="F"):
                print("\nLo sentimos, pero no existe disponibilidad\n")
                inicio()
        else:
            print("Lo sentimos, pero el número que ha introducido no corresponde a ningun hotel")
            inicio()

def enviarMensaje():
        receptor = input("Introduce el email al que quieres enviar el mensaje: ")
        s.send(receptor.encode())
        isU = s.recv(1024).decode()
        if(isU == "T"):
            mensaje = input("Introduce el mensaje: ")
            s.send(str(mensaje).encode())
            resp = s.recv(1024).decode()
            print(resp)
            inicio()
        else:
            print("\nNo existe ningún usuario registrado con ese email\n")
            inicio()
            
def leerMensaje():
        correo = input("Porfavor, por motivos de seguridad:\nIntroduce tu email: ")
        s.send(correo.encode())
        contr = input("Introduce tu contraseña: ")
        s.send(contr.encode())
        isC= s.recv(1024).decode()
        if(isC=="T"):
            print("Abriendo los mensajes....\n")
            num = int(s.recv(1024).decode())
            while num!= 1:
                mensj = s.recv(1024).decode()
                print("Mensaje:\n"+str(mensj))
                num-=1
            if(num == 1):
                mens = s.recv(1024).decode()
                print(mens)
            inicio()
        else:
            print("El email o la contraseña no son correctos")
            inicio()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9999))
datos = s.recv(1024).decode()
print("Conexión: "+str(datos)+"\n")

menu()
