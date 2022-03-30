#librerias a utilizar
import tkinter as tk
import turtle as tl
import random
from time import sleep

#funciones lamdda para calculos sencillo (espacio entre las cartas y hitbox de las cartas)
calcular = lambda tamaño: 0-(15*tamaño)
hitbox = lambda x,signo: (15*x)+25

#se guarda el nombre y se elimina la primera venta
def cerrar_ventana():
    ventana.destroy()

#se quitan 7 cartas de la mesa y se le asignan al jugador
def repartir(mesa,jugador):
    for i in range(7):
        carta = random.choice(mesa)
        jugador[0].append(carta)
        jugador[1].append(tl.Turtle())
        jugador[1][i].hideturtle()
        jugador[1][i].penup()
        jugador[1][i].shape("carta_"+carta+".gif")
        mesa.remove(carta)

#Funcion que imprime las cartas al inicio de la partida
def imprimir_inicio(jugador,num):
    tamaño = jugador[0].__len__()
    x = calcular(tamaño-1)
    for i in range(tamaño):
        jugador[1][i].speed(6)
        jugador[1][i].goto(-220,0)
        jugador[1][i].showturtle()
        if(num==1):
            jugador[1][i].goto(x,-100)
        elif(num==2):
            jugador[1][i].shape("carta_rv.gif")
            jugador[1][i].goto(x,100)
        x+=30
        
#funcion para imprimir las cartas cuando se agregue o se deje una
def imprimir(jugador,num):
    tamaño = jugador[0].__len__()
    x = calcular(tamaño-1)
    for i in range(tamaño):
        if(num==1):
            jugador[1][i].goto(x,-100)
        elif(num==2):
            jugador[1][i].shape("carta_rv.gif")
            jugador[1][i].goto(x,100)
        x+=30
        
#funcion para ejecutar la logica del juego cuando se haga un click
def click(x,y):
    global jugador
    global carta_mesa
    global mesa
    global banco
    global saltar_turno
    global screen
    global compu

    if(mesa.__len__()==0 and saltar_turno>=2):
        ganador = 0
        tl.clearscreen()
        tl.hideturtle()
        screen.bye()
    
    if(jugador.__len__()==1):
        circulo = tl.Turtle()
        circulo.hideturtle()
        circulo.penup()
        circulo.goto(40,-60)
        circulo.pendown()
        circulo.circle(20)
        texto = tl.hideturtle()
        texto.hideturtle()
        texto.penup()
        texto.sety(-37)
        texto.write("UNO",font=("Arial Black",8),align="center")
        tl.listen()
        screen.onclick(UNO)

    #se verifica si el click fue dado en hitbox de kas cartas
    if(y<-75 and y>-135 and x<(15*jugador[1].__len__())+25 and x>(-15*jugador[1].__len__())-25):
        carta = buscar(jugador,x)
        indice = jugador[1].index(carta)
        #e busca la carta del jugador y si tiene el mismo color o numero de la carta centro
        if(carta_mesa[0][0:1]==jugador[0][indice][0:1] or carta_mesa[0][1:2]==jugador[0][indice][1:2]):
            #si lo tiene se cambia la carta del centro y se quita del maso
            jugador[1][indice].speed(4)
            carta.home()
            cod = jugador[0][indice]
            jugador[1][indice].hideturtle()
            carta_mesa[1].shape("carta_"+cod+".gif")
            carta_mesa[0] = jugador[0][indice]
            jugador[0].pop(indice)
            jugador[1].pop(indice)
            if carta_mesa[0][:-1] == "p": 
                mas_dos(compu)
                imprimir(jugador, 1)

            #se reimprime el maso, se comprueba si tiene cartas y si pasa al turno del CPU
            imprimir(jugador, 1)
            victoria(jugador,1)
            turno = 0
            sleep(1)
            IA(mesa, carta_mesa)
    #se comprueba que el click haya sido dado en el banco de cartas y si tiene cartas
    elif(y<35 and y>-35 and x<-145 and x>-200 and mesa.__len__()>0):
        #se comprueba que no tenga una carta que pueda poner en el centro
        tienes = check(jugador,carta_mesa)
        if(tienes == 0):
            #si no tiene se le agrega una carta al jugador y se le quita al banco
            carta = random.choice(mesa)
            jugador[0].append(carta)
            jugador[1].append(tl.Turtle())
            indice = jugador[0].__len__()-1
            jugador[1][indice].speed(4)
            jugador[1][indice].hideturtle()
            jugador[1][indice].penup()
            jugador[1][indice].shape("carta_"+carta+".gif")
            mesa.remove(carta)
            jugador[1][indice].setx(-180)
            jugador[1][indice].showturtle()
            imprimir(jugador, 1)
            #se comprueba que el banco aun tenga carta y se pasa al turno del CPU
            if(mesa.__len__()==0):
                banco.hideturtle()
                banco.clearstamps()
            sleep(1)
            IA(mesa, carta_mesa)
            turno = 0
    elif(mesa.__len__()==0):
        saltar_turno+=1
        IA(mesa, carta_mesa)
            
#Funcion para el comportamiento del CPU
def IA(mesa,carta_mesa):
    global compu
    global saltar_turno
    global jugador
    #se comprueba que tiene cartas y si tiene al menos una que pueda colocar en el centro
    tienes = check(compu,carta_mesa)
    if(tienes==1):
        #si si la tiene se coloca en el centro y se le quita del maso
        carta = buscar_compu(compu, carta_mesa)
        indice = compu[0].index(carta)
        compu[1][indice].speed(4)
        compu[1][indice].home()
        compu[1][indice].hideturtle()
        carta_mesa[1].shape("carta_"+carta+".gif")
        carta_mesa[0] = carta
        compu[0].pop(indice)
        compu[1].pop(indice)
        turno = 0
        if carta_mesa[0][:-1] == "p": 
            mas_dos(jugador)
            imprimir(compu, 2)

        #se actualiza al maso y se comprueba si aun tiene cartas
        imprimir(compu, 2)
        victoria(compu,2)
    elif(tienes==0):
        #si no tiene toma una de la mesa
        if(mesa.__len__()>0):
            carta = random.choice(mesa)
            compu[0].append(carta)
            compu[1].append(tl.Turtle())
            indice = compu[0].__len__()-1
            compu[1][indice].speed(4)
            compu[1][indice].hideturtle()
            compu[1][indice].penup()
            compu[1][indice].shape("carta_"+carta+".gif")
            mesa.remove(carta)
            compu[1][indice].setx(-180)
            compu[1][indice].showturtle()
            #se actualiza el maso
            imprimir(compu, 2)
            saltar_turno = 0
        else:
            saltar_turno+=1
    
def mas_dos(maso):
    global mesa
    for i in range(2):
        carta = random.choice(mesa)
        maso[0].append(carta)
        maso[1].append(tl.Turtle())
        indice = maso[0].__len__()-1
        maso[1][indice].speed(4)
        maso[1][indice].hideturtle()
        maso[1][indice].penup()
        maso[1][indice].shape("carta_"+carta+".gif")
        mesa.remove(carta)
        maso[1][indice].setx(-180)
        maso[1][indice].showturtle()

#comprueba si un jugador se quedo sin cartas
def victoria(jugador,num):
    global ganador
    cantidad = jugador[0].__len__()
    if(cantidad<1):
        if(num==1):
            ganador = 1
        elif(num==2):
            ganador = 2
        tl.clearscreen()
        tl.hideturtle()
        screen.bye()

#busca la carta en el arreglo del jugador
def buscar(jugador,x):
    indice = jugador[0].__len__()-1
    if(x>indice*15 and x<=(indice+1)*15):
        x=x-30
    for i in jugador[1]:
        if(i.xcor()-30<=x<=i.xcor()):
            return i

#busca la carta en el arreglo del CPU
def buscar_compu(jugador,carta):
    for i in jugador[0]:
            if(i[0:1]==carta_mesa[0][0:1] or i[1:2]==carta_mesa[0][1:2]):
                return i

#verifica que hay al menos una carta igual a la del centro en color o numero
def check(jugador,carta):
    encontre=0
    for i in jugador[0]:
        if(i[0:1]==carta[0][0:1] or i[1:2]==carta[0][1:2]):
            encontre = 1
    return encontre

def UNO(x,y): 
    print()

#Pantalla para pedir nombres
#se crea la ventana
ventana = tk.Tk()
ventana.title("UNO")

#fondo
imagen = tk.PhotoImage(file="fondo.gif")

#lienzo para dibujae
canvas = tk.Canvas(ventana,width=600,heigh=360)
canvas.pack()

#se crea el fondo
fondo = tk.Label(canvas,image=imagen)
fondo.pack()

#se crea el texto
texto = tk.Label(ventana, text="Jugador 1:", font=("Comic Sans Ms", 13),bg="#cc0000",fg="white")
texto.place(x=200,y=100)

#se crea el cuadro dodnde se coloca el nombre y la variable donde se guarda el nombre
nombre = tk.StringVar()
cuadroTexto = tk.Entry(canvas, width=20, textvariable=nombre)
cuadroTexto.place(x=350,y=100)

#se crea el boton para continuar
boton = tk.Button(canvas, text="Aceptar", command=lambda: cerrar_ventana())
boton.place(x=275,y=300)

#loop para mantener la ventana abierta
ventana.mainloop()

#Pantalla de juego
#se crea la pantalla
tl.setup(600,360)
screen = tl.Screen()
screen.title("UNO")
screen.bgpic("fondo.gif")
screen.screensize(600,360)

#todas las combinaciones de cartas
colores = ["r","b","y","g"]
numeros = ["1","2","3","4","5","6","7","8","9"]
comodines = ["p"]
#variables que van a contener cartas y coordenada x para imprimir las cartas correctamente
jugador = [[],[]]
compu = [[],[]]
mesa = []
x= -255

#creamos todas las cartas y las guardamos
for i in colores:
    for j in numeros:
        screen.addshape("carta_"+j+i+".gif")
        mesa.append(j+i)
for k in range(2):
    for i in colores:
        for j in comodines:
            screen.addshape("carta_"+j+i+".gif")
            mesa.append(j+i)
#se agrega el reverso de la carta
screen.addshape("carta_rv.gif")

#repartir las cartas entre los dos jugadores
repartir(mesa, jugador)
repartir(mesa, compu)

#se imprime el banco de cartas
banco = tl.Turtle()
banco.hideturtle()
banco.speed(0)
banco.penup()
banco.goto(-200,0)
banco.shape("carta_rv.gif")
x = -190
for i in range(2):
    banco.stamp()
    banco.setx(x+(10*i))
banco.setx(x-20)
banco.showturtle()

#imprimen y colocan las cartas al principio de la partida
imprimir_inicio(compu,2)
imprimir_inicio(jugador,1)

#imprime el nombre de los jugadores
tl.hideturtle()
tl.penup()
tl.sety(140)
tl.color("white")
tl.write("CPU",font=("Arial Black",8),align="center")
tl.sety(-150)
tl.color("white")
tl.write(nombre.get(),font=("Arial Black",8),align="center")

#Coloca la carta central 
carta_mesa = [""]
carta_mesa.append(tl.Turtle())
carta_mesa[1].hideturtle()
carta_mesa[1].penup()
carta_mesa[1].goto(-200,0)
carta_mesa[1].showturtle()
carta_mesa[0] = mesa[(mesa.__len__())-1]
carta_mesa[1].shape("carta_"+carta_mesa[0]+".gif")
mesa.pop()
carta_mesa[1].speed(6)
carta_mesa[1].goto(-0,0)

saltar_turno = 0
#variable en donde se guarda el ganador
ganador = 0
#funcion que detecta el click del mouse
tl.listen()
screen.onclick(click)

#loop para mantener la ventana abierta
tl.done() 

#Pantalla de victoria
#Se crea la ventana
ventana = tk.Tk()
ventana.title("UNO")

#fondo
imagen = tk.PhotoImage(file="fondo.gif")

#lienzo para dibujae
canvas = tk.Canvas(ventana,width=600,heigh=360)
canvas.pack()

#se crea el fondo
fondo = tk.Label(canvas,image=imagen)
fondo.pack()

#se muestra el texto de victoria
texto1 = tk.Label(canvas, text="Victoria", font=("Lucida Fax", 20),bg="#cc0000",fg="#E0C50E")
texto1.place(x=250,y=100)
#se muestra el ganador de la partida
if(ganador==1):
    coordenada = 250-(4*len(nombre.get()))
    texto2 = tk.Label(canvas, text="Ganador: " + nombre.get(), font=("Lucida Fax", 14),bg="#cc0000",fg="#E0C50E")
    texto2.place(x=coordenada,y=150)
elif(ganador==2):    
    texto3 = tk.Label(canvas, text="Ganador: CPU", font=("Lucida Fax", 14),bg="#cc0000",fg="#E0C50E")
    texto3.place(x=240,y=150)
else:
    texto3 = tk.Label(canvas, text="Empate", font=("Lucida Fax", 14),bg="#cc0000",fg="#E0C50E")
    texto3.place(x=260,y=150)

#boton para cerrar
boton = tk.Button(canvas, text="Cerrar", command=lambda: cerrar_ventana())
boton.place(x=275,y=300)

#loop para mantener abierta la ventana
ventana.mainloop()
