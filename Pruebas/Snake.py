#Librerías importadas
import turtle
import time
import random

posponer = 0.1
#Marcador
Score = 0
High_Score = 0

#Creamos una lista vacia
segmentos = []

#Creamos una ventana
wn = turtle.Screen()
wn.title("Juego de Snake")
wn.bgcolor("black")
wn.setup(width = 600, height = 600)
wn.tracer(0)

#Texto de información
texto = turtle.Turtle()
texto.speed(0)
texto.color("white")
texto.penup()
texto.hideturtle()
texto.goto (0,260)
texto.write("Score: 0    High Score: 0", align="center",font=("Courire",24,"normal"))

#Creamos la cabeza de la serpiente
cabeza = turtle.Turtle()
cabeza.speed(0)         #para que el objeto este aquí.
cabeza.shape("square")
cabeza.color("white")
cabeza.penup()          #Evitamos que quede rastro de nuestro objeto en pantalla.
cabeza.goto(0,0)        #Comenzamos en el centro de la pantalla.
cabeza.direction = "stop"

#Comida
comida = turtle.Turtle()
comida.speed(0)         #para que el objeto este aquí.
comida.shape("circle")
comida.color("red")
comida.penup()          #Evitamos que quede rastro de nuestro objeto en pantalla.
comida.goto(0,100)        #Comenzamos en el centro de la pantalla.

#Funciones
def arriba():
    cabeza.direction = "up"
def abajo():
    cabeza.direction = "down"
def izquierda():
    cabeza.direction = "left"
def derecha():
    cabeza.direction = "right"

def mov():
    if cabeza.direction == "up":
        y = cabeza.ycor()
        cabeza.sety(y + 20)
        #cabeza.direction = "stop"
    if cabeza.direction == "down":
        y = cabeza.ycor()
        cabeza.sety(y - 20)
        #cabeza.direction = "stop"
    if cabeza.direction == "left":
        x = cabeza.xcor()
        cabeza.setx(x - 20)
        #cabeza.direction = "stop"
    if cabeza.direction == "right":
        x = cabeza.xcor()
        cabeza.setx(x + 20)
        #cabeza.direction = "stop"

#Teclado
wn.listen()
wn.onkeypress(arriba, "Up")
wn.onkeypress(abajo,"Down")
wn.onkeypress(izquierda,"Left")
wn.onkeypress(derecha,"Right")

#Todo corre dentro de un bucle principal
while True:
    wn.update()

    #Colisiones con los bordes
    if cabeza.xcor()>280 or cabeza.xcor() <-280 or cabeza.ycor()>280 or cabeza.ycor() <-280:
        time.sleep(1)
        cabeza.goto(0,0)
        cabeza.direction = "stop"
        #mi idea para solucionarlo que no funciono
        #for i in range(len(segmentos)-1):
        #    cabeza.clearstamp(segmentos[i])
        #segmentos.clear()
        
        #Esconder los segmentos.
        for segmento in segmentos:
            segmento.goto(1000,1000)
        
        #Limpiar lista de segmentos
        segmentos.clear()
        Score = 0
        texto.clear()
        texto.write("Score: {}    High Score: {}".format(Score,High_Score),
        align="center",font=("Courire",24,"normal"))

    #Colisión con la comida
    if cabeza.distance(comida) < 20:
        x = random.randint(-280,280)
        y = random.randint(-280,280)
        comida.goto(x,y)

        nuevo_segmento = turtle.Turtle()
        nuevo_segmento.speed(0)         #para que el objeto este aquí.
        nuevo_segmento.shape("square")
        nuevo_segmento.color("grey")
        nuevo_segmento.penup()          #Evitamos que quede rastro de nuestro objeto en pantalla.
        segmentos.append(nuevo_segmento)

        Score += 10
        if Score > High_Score:
            High_Score = Score 
        
        texto.clear()
        texto.write("Score: {}    High Score: {}".format(Score,High_Score),
        align="center",font=("Courire",24,"normal"))


    #Mover el cuerpo de la serpiente
    totalSeg = len(segmentos)
    for index in range(totalSeg-1,0,-1):
        x = segmentos[index-1].xcor()
        y = segmentos[index-1].ycor()
        segmentos[index].goto(x,y)

    if totalSeg > 0:
        x = cabeza.xcor()
        y = cabeza.ycor()
        segmentos[0].goto(x,y)        

    mov()

    #Colisiones con el cuerpo de la serpiente
    for segmento in segmentos:
        if segmento.distance(cabeza) < 20:
            time.sleep(1)
            cabeza.goto(0,0)
            cabeza.direction = "stop"

            #Esconder los segmentos
            for segmento in segmentos:
                segmento.goto(1000,1000)
                
            segmentos.clear()


    time.sleep(posponer)