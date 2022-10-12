import numpy as np
import matplotlib.pyplot as plt

def tangente_hiperbolica(x):
    return (np.power(np.e, x) - np.power(np.e, -x)) / (np.power(np.e, x) + np.power(np.e, -x))

def relu(x):
    return max(0, x)

def sigmoid(x):
    return 1 / (1+np.power(np.e,-x))

def escalon(x):
    if(x<0):
        return 0
    else:
        return 1

def graficar(x,y,text):
    plt.plot(x,y)
    #plt.grid()
    plt.title(text)
    plt.show()

# Defino el eje X
vector = np.arange(-6,6,0.1)

# Defino el eje y
y1 = []
y2 = []
y3 = []
y4 = []

for x in range(0,len(vector)):
    y1.append(tangente_hiperbolica(vector[x])) 
    y2.append(relu(vector[x])) 
    y3.append(sigmoid(vector[x])) 
    y4.append(escalon(vector[x])) 

graficar(vector,y1,"TANH")
graficar(vector,y2,"ReLU")
graficar(vector,y3,"Sigmoid")
graficar(vector,y4,"Escalón")