import math
d_entre_ants = 177
#alfa,beta = CalculoAngulo(Alfa,Beta)
ang_1 = -14
#print(ang_1)
ang_2 = 33
#print(ang_2)
Alfa = 0.0
Beta = 0.0
if ang_1 < 0.0:
    #Caso 1: Ángulo 1 positivo y Ángulo 2 negativo
    if ang_2 < 0.0:
        Alfa = 90.0 + ang_1
        Beta = 90.0 - ang_2
    #Caso 2:
    elif ang_2 > 0.0:
        Alfa = 90.0 + ang_1
        Beta = 90.0 - ang_2
    #Caso 3:    
    elif ang_2 == 0.0:
        Alfa = 90.0 + ang_1
        Beta = 90.0
#caso 4:
elif ang_1 > 0.0:
    if ang_2 > 0.0:
        Alfa = 90.0 + ang_1
        Beta = 90.0 - ang_2
#Caso 5:
elif ang_1 == 0.0:
    if ang_2 < 0.0:
        Alfa = 90.0
        Beta = 90.0 + ang_2

alfa = Alfa
beta = Beta
print(alfa)
print(beta)
# Distancia desde el punto C a A
# con a definido como la distancia entre las dos antenas
sigma = 180-beta-alfa
if(sigma!=0):
    B = d_entre_ants * math.sin(math.radians(alfa))/math.sin(math.radians(sigma))  # b=a*sin(beta)/sin(sigma)
    A = d_entre_ants * math.sin(math.radians(beta))/math.sin(math.radians(sigma)) # c=a*sin(alfa)/sin(sigma)
else:
    A = 0
    B = 0
print(50*'~')
print(A)
print(B)
# la altura del triangulo que se forma entre las dos distancias B y C
#h = d_entre_ants * (math.sin(math.radians(alfa))*math.sin(math.radians(beta))) / math.sin(math.radians(alfa+beta))