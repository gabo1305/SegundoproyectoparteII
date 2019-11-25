info="""

Producido en Costa Rica
Instituto Tecnólogico de Costa Rica
Ingeniería en Computadores
Taller de programación

Primer año de carrera(2019)
Grupo: 2

Profesor: Milton Villegas Lemus
Versión 3.5

Autores:
Gabriel Solano Coronado - 2019033687
Hansel Hampton Fallas  -2019049765

Autor de módulos módificados
José Morales-Telemetry(conexión con el node)

"""
Instrucciones="""
Instrucciones
Para poder realizar los movimientos debe conectar
ambos dispositivos con las teclas w y s se mueve hacia
adelante y atrás, con las teclas a y d  se mueve  hacia la
derecha o izquierda, con la tecla b y f enciende los leds
delanteros y traseros,con las teclas q y e las luces direccionales.

"""

from tkinter import *
from threading import Thread  
import threading  
import os  
import time  

##### Biblioteca para el Carro
from WiFiClient import NodeMCU

active = True

#________________________________
#_______________/Función para cargar las imagenes

def cargarImg(nombre):
    """
Función para cargar imagenes


    """

    ruta = os.path.join("Imagenes", nombre)
    imagen = PhotoImage(file=ruta)
    return imagen

#_____________________________
# __________/Ventana Principal

winini=Tk()
winini.title("Escudería XD")
winini.minsize(1100,687)
winini.resizable(width=NO,height=NO)
#Crear canvas
canvass = Canvas(winini, width= 1100, height = 687, bg = "black")


#______________________________________
#___________________/Se cargan las imagenes


bg1=cargarImg('fondo.png')  #fondo
Add=cargarImg('ADD.png')  #add
bg3=cargarImg('circle.png')  #Circulo para agregar los botones


#_________________________
#__________/Se crean las imagens
canvass.create_image(0, 0, image= bg1 , anchor= NW)
canvass.create_image(0, 380, image= bg3 , anchor= NW)
canvass.create_image(212, 380, image= bg3 , anchor= NW)
canvass.create_image(424, 380, image= bg3 , anchor= NW)
canvass.create_image(636, 380, image= bg3 , anchor= NW)
canvass.create_image(848, 380, image= bg3 , anchor= NW)
canvass.create_image(800, 0, image= Add , anchor= NW)


#_________________________________
#______________/Ventana de información
def  winabout():
    winini.withdraw()
    winabout=Toplevel()
    winabout.title("About")
    winabout.minsize(1080,600)
    winabout.resizable(width=NO,height=NO)
    
    canvas = Canvas(winabout, width= 1080, height = 1080, bg = "black")
    canvas.place(x=0,y=0)

    bg1=cargarImg('FABOUT.png')
    canvas.create_image(0, 0, image= bg1, anchor= NW)


    labelinfo= Label(canvas, text=info ,bg= "black",fg="white", justify='left', font="century")
    labelinfo.place(x=700,y=40)

    labelinstrucciones= Label(canvas, text=Instrucciones ,bg= "black",fg="white", justify='left', font="century")
    labelinstrucciones.place(x=200,y=40)

    Hanselphoto=cargarImg ('Hansel.png')
    canvas.create_image(300,350, image=Hanselphoto, anchor= NW)

    Gabrielphoto1=  cargarImg( 'Gabriel.png')
    Gabrielphoto=canvas.create_image(50,350, image=Gabrielphoto1, anchor= NW)
    
    #_____________
    #__________/Salir de la ventana al incicio
    
    def out():
        winabout.destroy()
        winini.deiconify()
        

    botonatras=Button(winabout, text= "Atrás",command=out,bg="black", activebackground="white", fg="white",font="Century")
    botonatras.place(x=800, y=550)

    winabout.mainloop()

#_____________________________________________
#___________/Ventana para ingresar el nombre del jugador
def wintest():
    """
Gabriel Solano
Haansel Hampton
función: Ventana donde se obtiene el nombre del piloto y se inicia el test

    """
    winini.withdraw()
    test=Toplevel()
    test.title("Test")
    test.minsize(400,360)
    test.resizable(width=NO,height=NO)
    
    ctest=Canvas(test,width=400,height=400)
    ctest.place(x=0,y=0)
    bg11=cargarImg('relleno.png')
    ctest.create_image(0, 0, image= bg11, anchor= NW)
    Label_IngrNomb= Label(ctest,text="Ingrese Nombre de Corredor",font=('Arial',15),bg='white',fg='black')
    Label_IngrNomb.place(x=10,y=10)
    Entry_Nombre= Entry(ctest,width=20,font=('Arial',14))
    Entry_Nombre.place(x=10,y=60)

    def openwindrives():
        nombre=str(Entry_Nombre.get())
        test.destroy()
        windrives(nombre)
        
    Binitest=Button(ctest, text= "iniciar test",command= openwindrives,bg="blue", activebackground="white", fg="light blue",font="Century")
    Binitest.place(x=10, y=150)
    def out():
        winini.deiconify()
        test.destroy()

        
    Binitest=Button(ctest, text= "Vovler al inicio",command= out,bg="blue", activebackground="white", fg="light blue",font="Century")
    Binitest.place(x=10, y=250)
    ctest.mainloop()

#_____________________________-
#______/Ventana para el test
#E: nombre de jugador
def windrives(nombreG):
    """
Gabriel Solano
Haansel Hampton
función: Ventana test

    """

    global adelante,atras,leftlight,rigthlight,frontlight,backlight,dirR,dirL,dirN,pwm,stop,nothing,Bpwm,pressing,sense,Blevel,blevel,lightoff,config_active
    leftlight = False
    rigthlight = False
    frontlight = False
    backlight = True
    dirN = True
    dirR = False
    dirL = False
    stop= True
    pwm_back = False
    pressing = False
    belvel = 0
    pwm = 0
    Blevel = 0
    lightfpress=False
    adelante=False
    atras=False
    config_active=False

    winini.withdraw()
    windrive=Toplevel()
    windrive.title("Text drive")
    windrive.minsize(1000,650)
    windrive.resizable(0,0)

    
    canvas = Canvas(windrive, width= 1000, height = 650, bg = "white")
    canvas.place(x=0,y=0)

    bg1=cargarImg('test.png')  #bg=background
    dirR=cargarImg("direccional1.png")
    dirL=cargarImg("direccional2.png")
    delante=cargarImg("direccional3.png")
    atras=cargarImg("direccional4.png")
    

    
    canvas.create_image(0, 0, image= bg1 , anchor= NW)
    LabelNomb= Label(canvas,text=nombreG,font=('Arial',15),bg='white',fg='black')
    LabelNomb.place(x=0,y=10)
    

    textura=cargarImg('textura.png')  
    panel=cargarImg('PANEL.png')
    off=cargarImg("off.png")
    on=cargarImg("on.png")
    canvas.create_image(450, 324, image= textura , anchor= NW)
    canvas.create_image(0, 325, image= panel , anchor= NW)
    canvas.create_image(660, 400, image=dirR, anchor=NW, tags=("dirR1", "direccion"), state=HIDDEN)
    canvas.create_image(660, 400, image=dirL, anchor=NW, tags=("dirL1", "direccion"), state=HIDDEN)
    canvas.create_image(660, 400, image=delante, anchor=NW, tags=("delante1", "direccion"), state=HIDDEN)
    canvas.create_image(660, 400, image=atras, anchor=NW, tags=("atras11", "direccion"), state=HIDDEN)

    canvas.create_image(760, 470, image=off,anchor=NW, tags=("offF", "luces"), state=NORMAL)
    canvas.create_image(760, 470, image=on, anchor=NW, tags=("onF", "luces"), state=HIDDEN)

    canvas.create_image(760, 570, image=off, anchor=NW, tags=("offB", "luces"), state=NORMAL)
    canvas.create_image(760, 570, image=on, anchor=NW, tags=("onB", "luces"), state=HIDDEN)
    
    canvas.create_image(700, 520, image=on, anchor=NW, tags=("onI", "luces"), state=HIDDEN)
    canvas.create_image(700, 520, image=off, anchor=NW, tags=("offI", "luces"), state=NORMAL)
    
    canvas.create_image(800, 520, image=on, anchor=NW, tags=("onD", "luces"), state=HIDDEN)
    canvas.create_image(800, 520, image=off, anchor=NW, tags=("offD", "luces"), state=NORMAL)

    #_________________________________________________________
    #____________________________________/Cliente para el NodeCMU
    myCar = NodeMCU()
    myCar.start()



    #_________________
    #__/Envía los mensajes
    def send(mns):
        """
Gabriel Solano
Haansel Hampton
función: Envía los mensajes y comunica con el wificlient

    """
        if (len(mns)>0 and mns[-1]==";"):
            myCar.send(mns)
        else:
            return


     #_____________________________________________
    #________/Depende de la tecla presionada realiza una acción
    def bind_press(event):
        """
Gabriel Solano
Haansel Hampton
función: presiona boton y obtiene el valor

        """
        global dirR, dirL, dirN, Bpwm, pwm,adelante,atras,stop,backlight,frontlight,leftlight,rigthlight
        key = event.char
        if key == "a":
            if dirR:
                return
            else:
                if dirL:
                    dirN = False
                    dirL = True
                else:
                    dirN = False
                    dirL = True
                    canvas.itemconfig("dirR1", state=HIDDEN)
                    canvas.itemconfig("dirL1", state=NORMAL)
                    canvas.itemconfig("atras11", state=HIDDEN)
                    canvas.itemconfig("delante1", state=HIDDEN) 
                    send("dir:-1;")
        elif key == "d":
            if dirL:
                return
            else:
                if dirR:
                    dirN = False
                    dirR = True
                else:
                    dirN = False
                    dirR = True
                    canvas.itemconfig("dirR1", state=NORMAL)
                    canvas.itemconfig("dirL1", state=HIDDEN)
                    canvas.itemconfig("atras11", state=HIDDEN)
                    canvas.itemconfig("delante1", state=HDDEN) 
                    send("dir:1;")
        elif key == "w":
            if atras:
                return
            else:
                if adelante:
                    adelante=True
                    stop=False
                else:
                    adelante=True
                    canvas.itemconfig("dirR1", state=HIDDEN)
                    canvas.itemconfig("dirL1", state=HIDDEN)
                    canvas.itemconfig("atras11", state=HIDDEN)
                    canvas.itemconfig("delante1", state=NORMAL) 
                    send("pwm:1000;")
        elif key == "s":
            if adelante:
                return
            else:
                if atras:
                    atras=True
                    stop=False
                else:
                    atras = True
                    stop=False
                    canvas.itemconfig("dirR1", state=HIDDEN)
                    canvas.itemconfig("dirL1", state=HIDDEN)
                    canvas.itemconfig("atras11", state=NORMAL)
                    canvas.itemconfig("delante1", state=HIDDEN) 
                    send("pwm:-1023;")
        elif key=="f":
            if backlight:
                return
            else:
                if frontlight:
                    frontlight=True
                    backlight=False
                else:
                    frontlight = True
                    backlight=False
                    canvas.itemconfig("offF", state=HIDDEN)
                    canvas.itemconfig("onF", state=NORMAL)
                    send("lf:1;")
        elif key=="b":
            if backlight:
                return
            else:
                if frontlight:
                    frontlight=False
                    backlight=True
                else:
                    frontlight = False
                    backlight=True
                    canvas.itemconfig("offB", state=HIDDEN)
                    canvas.itemconfig("onB", state=NORMAL)
                    send("lb:1;")
        elif key=="q":
            if rigthlight:
                return
            else:
                if leftlight:
                    rigthlight=False
                    leftlight=True
                else:
                    rigthlight = False
                    leftlight=True
                    canvas.itemconfig("offI", state=HIDDEN)
                    canvas.itemconfig("onI", state=NORMAL)
                    send("ll:1;")               
        elif key=="e":
            if leftlight:
                return
            else:
                if rigthlight:
                    rigthlight=True
                    leftlight=False
                else:
                    rigthlight = True
                    leftlight=False
                    canvas.itemconfig("offD", state=HIDDEN)
                    canvas.itemconfig("onD", state=NORMAL)
                    send("lr:1;")

    #_______________________________
    #________/Depende de la tecla que suelte 
    def bind_release(event):

        global dirR, dirN, dirL, pressing,adelante,atras,frontlight,backlight,leftlight,rightlight
        key = event.char
        if key in ["a","d"]:
            if dirR and dirL:
                return
            else:
                dirN = True
                dirR = False
                dirL = False
                canvas.itemconfig("dirR1", state=HIDDEN)
                canvas.itemconfig("dirL1", state=HIDDEN)
                canvas.itemconfig("atras", state=HIDDEN)
                canvas.itemconfig("adelante", state=HIDDEN) 
                send("dir:0;")
        elif key == "s":
            if atras:
                atras = False
                canvas.itemconfig("dirR1", state=HIDDEN)
                canvas.itemconfig("dirL1", state=HIDDEN)
                canvas.itemconfig("atras11", state=HIDDEN)
                canvas.itemconfig("delante1", state=HIDDEN) 
                send("pwm:0;")
        elif key == "w":
            if adelante:
                adelante=False
                canvas.itemconfig("dirR1", state=HIDDEN)
                canvas.itemconfig("dirL1", state=HIDDEN)
                canvas.itemconfig("atras", state=HIDDEN)
                canvas.itemconfig("adelante", state=HIDDEN) 
                send("pwm:0;")
                return
        elif key == "f":
                if frontlight:
                    frontlight=False
                    canvas.itemconfig("onF", state=HIDDEN)
                    canvas.itemconfig("offF", state=NORMAL)
                    send("lf:0;")
        elif key == "b":
                if backlight:
                    backlight=False
                    canvas.itemconfig("onB", state=HIDDEN)
                    canvas.itemconfig("offB", state=NORMAL)
                    send("lb:0;")
        elif key == "q":
                if leftlight:
                    leftlight=False
                    canvas.itemconfig("onI", state=HIDDEN)
                    canvas.itemconfig("offI", state=NORMAL)
                    send("ll:0;")
        elif key == "b":
                if rightlight:
                    rigthlight=False
                    canvas.itemconfig("onD", state=HIDDEN)
                    canvas.itemconfig("offD", state=NORMAL)
                    send("lr:0;")
                        

    def config(variable):
        global config_active
        if variable == "TurnTime:1":
            if not config_active:
                config_active = True
                send("TurnTime:1;")
                print("started")
                time.sleep(20)
                print("ended")
                config_active = False
        elif variable=="TurnTime:-1":
            if not config_active:
                config_active = True
                send("TurnTime:-1;")
                print("started")
                time.sleep(20)
                print("ended")
                config_active = False  
        elif variable == "Infinite":
            if not config_active:
                config_active = True
                send("Infinite;")
                print("started")
                time.sleep(20)
                print("ended")
                config_active = False
        elif variable == "Especial":
            if not config_active:
                config_active = True
                send("Especial;")
                print("started")
                time.sleep(20)
                print("ended")
                config_active = False
        
        

    
    ###________________________________________________-
    #_______________________/Se agrega el .bind para cuando se presiona la tecla y cuando es liberada
    windrive.bind("<KeyPress>", bind_press)

    windrive.bind("<KeyRelease>", bind_release)

    #___________________________________
    #____________________/Fin nodemcu

    Btn_command1 = Button(windrive, text="TurnTime \n derecha", command=lambda: config("TurnTime:1"), fg='white', bg='black')
    Btn_command1.place(x=50, y=580)

    Btn_command11 = Button(windrive, text="TurnTime \n izquierda", command=lambda: config("TurnTime:-1"), fg='white', bg='black')
    Btn_command11.place(x=150, y=580)

    Btn_command2 = Button(windrive, text="Infinite", command=lambda: config("Infinite"), fg='white', bg='black')
    Btn_command2.place(x=385, y=590)
            
    bmovimientoespecial=Button(windrive, text= "Especial",command= lambda:config("Especial"),bg="black", activebackground="white", fg="white",font="Century")
    bmovimientoespecial.place(x=485, y=590)
    


    def out():
        windrive.destroy()
        winini.deiconify()


    botonatras=Button(windrive, text= "Atrás",command=out,bg="black", activebackground="white", fg="white",font="Century")
    botonatras.place(x=875, y=615)

    windrive.mainloop()
#________________________-
#___/Tabla para ordenamiento
def piloto():
    """
Gabriel Solano
Haansel Hampton
función: Ventana de ordenamiento

    """
    winini.withdraw()
    piloto=Toplevel()
    piloto.title("Valores obtenidos")
    piloto.geometry("700x550")
    piloto.resizable(0,0)

    canvas = Canvas(piloto, width= 700, height = 550, bg = "black")
    canvas.place(x=0,y=0)

    frame1=Frame(piloto)
    frame1.grid(row=0,column=0)
    
    labPosicion=Label(frame1,text="          Posición    ")
    labPosicion.grid(row=0,column=0)

    labName=Label(frame1,text="      Piloto      ")
    labName.grid(row=0,column=1)

    labluz=Label(frame1,text="         Nivel luz        ")
    labluz.grid(row=0,column=2)

    labbat=Label(frame1,text=" Batería       ")
    labbat.grid(row=0,column=3)

    labTemp=Label(frame1,text=" Temp      ")
    labTemp.grid(row=0,column=4)

    labcon=Label(frame1,text="Conexión")
    labcon.grid(row=0,column=5)

    labace=Label(frame1,text="Acele(m/s)")
    labace.grid(row=0,column=6)

    labtiem=Label(frame1,text="Tiem Giro(s)")
    labtiem.grid(row=0,column=7)

    labedit=Label(frame1,text="                                ")
    labedit.grid(row=0,column=8)

    global cont
    cont = 0
    def tablflag(frame1, opc):
        global cont
        print(str(cont))
        cont+=1
        tabla(frame1, opc, cont)
    def out():
        piloto.destroy()
        winini.deiconify()


    botonatras=Button(piloto, text= "Volver atrás",command=out,bg="black", activebackground="white", fg="white",font="Century")
    botonatras.place(x=290, y=425)

    Bacea=Button(piloto, text= "Orden Aceleracion \n ascendente",command= lambda:tablflag(frame1, 3),bg="black", activebackground="white", fg="white",font="Century")
    Bacea.place(x=420, y=485)
    
    Bga=Button(piloto, text= "Orden Tiempo giro \n ascendente",command= lambda:tablflag(frame1, 4),bg="black", activebackground="white", fg="white",font="Century")
    Bga.place(x=550, y=425)

    Baced=Button(piloto, text= "Orden Aceleracion \n descendente",command= lambda:tablflag(frame1, 2),bg="black", activebackground="white", fg="white",font="Century")
    Baced.place(x=160, y=485)

    Bgd=Button(piloto, text= "Orden Tiempo Giro \n descendente",command= lambda:tablflag(frame1, 1),bg="black", activebackground="white", fg="white",font="Century")
    Bgd.place(x=30, y=425)

    piloto.mainloop()

    ready=Button(editar, text="Listo", command=lambda:editaraux(entnombre.get(), entedad.get(), entnacionalidad.get(), enttemp.get(), entcomp.get(), fill), bg="black", activebackground="white", fg="white",font="Century")
    ready.place(x=185, y=180)
    editar.mainloop()
def changev(winc,wino): ##función cambiar de ventanas
    winc.destroy()
    wino()


def salir(win):# cerrar la ventana

    global active
    active = False
    time.sleep(1)
    win.destroy()

    
def archivo_principal():  
    archivo=open("Corredores/Nombres.txt","r")
    lista = []
    linea = "l"
    while linea != "":
        linea = archivo.readline()
        linea = linea[0:-1]
        lista.append(linea)

    return lista

#ORDNAMIENTO
class Corredor:
    def __init__(self, nombre, edad, nat, temp, comp, rgb, rep):
        self.nombre = nombre
        self.edad = edad
        self.nat = nat
        self.temp = temp
        self.comp = comp
        self.rgb = rgb
        self.rep= rep

def tabla(frame1, opc, cont):
    frame2=Frame(frame1)
    frame2.grid(in_=frame1, row=1, column=0, columnspan=15, sticky=W+E)
    lista_corredores = archivo_principal()
    i=1
    corrlist=[]
    for corredor in lista_corredores:
        if corredor == "":
            break
        archivo=open("Corredores/" + corredor,"r")
        nombre = archivo.readline()
        edad=archivo.readline()
        nacionalidad=archivo.readline()
        victorias=int(archivo.readline())
        segyter=int(archivo.readline())
        abandonos=int(archivo.readline())
        temp=archivo.readline()
        competencias=int(archivo.readline())
        archivo.close()
        arch=open("Corredores/"+corredor,"a")
        x=segyter
        y=victorias
        y=round(y,2)
        corrlist.append(Corredor(nombre, edad, nacionalidad, temp, competencias,x,y))
        archivo.close()
        
    n = len(corrlist)
    if opc ==1:
        if cont>=1:
            frame2.destroy()
            frame2=Frame(frame1)
            frame2.grid(in_=frame1, row=1, column=0, columnspan=15, sticky=W+E)
        for i in range(n):
            for j in range(0, n-i-1):
                if corrlist[j].rep > corrlist[j+1].rep:
                    corrlist[j], corrlist[j+1] = corrlist[j+1], corrlist[j]
    elif opc ==2:
        if cont>=1:
            frame2.destroy()
            frame2=Frame(frame1)
            frame2.grid(in_=frame1, row=1, column=0, columnspan=15, sticky=W+E)
        for i in range(n):
            for j in range(0, n-i-1):
                if corrlist[j].rgb > corrlist[j+1].rgb:
                    corrlist[j], corrlist[j+1] = corrlist[j+1], corrlist[j]
    elif opc ==3:
        if cont>=1:
            frame2.destroy()
            frame2=Frame(frame1)
            frame2.grid(in_=frame1, row=1, column=0, columnspan=15, sticky=W+E)
        for i in range(n):
            for j in range(0, n-i-1):
                if corrlist[9-j].rgb > corrlist[8-j].rgb:
                    corrlist[9-j], corrlist[8-j] = corrlist[8-j], corrlist[9-j]
    elif opc ==4:
        if cont>=1:
            frame2.destroy()
            frame2=Frame(frame1)
            frame2.grid(in_=frame1, row=1, column=0, columnspan=15, sticky=W+E)
        for i in range(n):
            for j in range(0, n-i-1):
                if corrlist[9-j].rep > corrlist[8-j].rep:
                    corrlist[9-j], corrlist[8-j] = corrlist[8-j], corrlist[9-j]
    
    for i in range(n):

        label=Label(frame2,text="                "+str(i)+"            ")
        label.grid(row=i,column=0, sticky=W+E)
            
        labpilot=Label(frame2,text="   "+str(corrlist[i].nombre)+"               ")
        labpilot.grid(row=i,column=1)

        labluz=Label(frame2,text="             "+str(corrlist[i].edad)+"          ")
        labluz.grid(row=i,column=2)

        labbateria=Label(frame2,text="                   "+str(corrlist[i].nat)+"          ")
        labbateria.grid(row=i,column=3)
        
        labtemp=Label(frame2,text="               "+str(corrlist[i].temp)+"          ")
        labtemp.grid(row=i,column=4)

        labconexion=Label(frame2,text="           "+str(corrlist[i].comp)+"       ")
        labconexion.grid(row=i,column=5)

        labaceleracion=Label(frame2,text="   "+str(corrlist[i].rgb)+"          ")
        labaceleracion.grid(row=i,column=6)

        labtiempo=Label(frame2,text="     "+str(corrlist[i].rep)+"              ")
        labtiempo.grid(row=i,column=7)


        
################################################################

class Boton:
    def __init__(self, ventana, n_archivo, fill):
        self.but = Button(ventana, text = "Editar", command = lambda:editar(n_archivo, fill))

logos = [cargarImg("logo0.png"),
         cargarImg("logo1.png"),
         cargarImg("logo2.png"),
         cargarImg("logo3.png")]

#Añadido estético para que varien logos
def change_logo():
    global active, logos
    con = 0

    try:
        while active:
            if con % len(logos) == 0:
                con = 0
            canvass.create_image(300, 35, image=logos[con], anchor=NE, tags="logos")
            time.sleep(1.5)
            con += 1
            canvass.delete("logos")
        return
    except:
        return


def change_logo_thread():
    global active
    if active:
        Logo_thread = Thread(target=change_logo)
        Logo_thread.start()
    else:
        return


change_logo_thread()

#___________________
#__/Botones
botonabout=Button(canvass, text= "About",command=winabout,bg="blue", activebackground="light blue", fg="light blue",activeforeground="blue",font="Century")
botonabout.place(x=105, y=500)
botonpos=Button(canvass, text= "Tabla de \n Posiciones",command= piloto,bg="blue", activebackground="light blue", fg="light blue",activeforeground="blue",font="Century")
botonpos.place(x=300, y=485) 
botontest=Button(canvass, text= "Test Drive",command=wintest,bg="blue", activebackground="light blue", fg="light blue",activeforeground="blue",font="Century")
botontest.place(x=514, y=500) 
botonsalir=Button(canvass,text="Cerrar \n aplicación",command=lambda:salir(winini),bg="blue", activebackground="light blue", fg="light blue",activeforeground="blue",font="Century")
botonsalir.place(x=938,y=485)

canvass.pack()
print(info)
print(cargarImg.__doc__)
print(winabout.__doc__)
print(wintest.__doc__)
print(windrives.__doc__)
print(piloto.__doc__)

winini.mainloop()

