# Cargando los datos
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt

from sklearn.datasets import make_circles

# Creamos nuetros datos artificiales, donde buscaremos clasificar
# dos anillos concéntricos de datos.
X, Y = make_circles(n_samples=500, factor=0.5,noise=0.05)

#Resolución del mapa de predicción.
res = 100

#Coordenadas del mapa de predicción.
_x0 = np.linspace(-1.5, 1.5, res)
_x1 = np.linspace(-1.5, 1.5, res)

# Input con cada combo de coordenadas del mapa de predicción.
_pX = np.array(np.meshgrid(_x0, _x1)).T.reshape(-1, 2)

# Objeto vacio a 0.5 del mapa de predicción.
_pY = np.zeros((res, res)) + 0.5

# Visualización del mapa de predicción.
plt.figure(figsize=(8, 8))
plt.pcolormesh(_x0, _x1, _pY, cmap="coolwarm", vmin=0, vmax=1)

# Visualización de la nube de datos.
plt.scatter(X[Y == 0,0] , X[Y== 0,1], c="skyblue")
plt.scatter(X[Y == 1,0] , X[Y== 1,1], c="salmon")

plt.tick_params(labelbottom=False, labelleft=False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from matplotlib import animation
from IPython.core.display import display, HTML

import tensorflow as tf

# Creamos los puntos de entrada de datos de nuestro grafo.
iX = tf.placeholder('float', shape =[None, X.shape[1]])
iY = tf.placeholder('float', shape=[None])

nn = [2, 16, 8 ,1]  # Número de neuronas por capa.
lr = 0.01           # Learning Rate del optimizador.

# Capa 1
W1 = tf.Variable(tf.random_normal([nn[0], nn[1]]), name='Weight_1')
b1 = tf.Variable(tf.random_normal([nn[1]]), name='bias_1')

l1 = tf.nn.relu(tf.add(tf.matmul(iX, W1), b1)) # f(XW + b)

# Capa 2
W2 = tf.Variable(tf.random_normal([nn[1], nn[2]]), name='Weight_2')
b2 = tf.Variable(tf.random_normal([nn[2]]), name='bias_2')

l2 = tf.nn.relu(tf.add(tf.matmul(l1, W2), b2)) # f(XW + b)

# Capa 3
W3 = tf.Variable(tf.random_normal([nn[2], nn[3]]), name='Weight_3')
b3 = tf.Variable(tf.random_normal([nn[3]]), name='bias_3')

# Vector de predicciones de Y
pY = tf.nn.sigmoid(tf.add(tf.matmul(l2, W3), b3))[:,0]

# Evaluación de las predicciones.
loss = tf.losses.mean_squared_error(pY, iY)

# Creamos el optimizador que entrenará a la red.
optimizer = tf.train.GradientDescentOptimizer(learning_rate = lr).minimize(loss)

# Para iniciar nuestro grafo computacional debemos iniciar una sección c:
n_steps = 1000 # número de pasos para entrenar a la red.

with tf.Session() as sess:

    sess.run(tf.global_variables_initializer()) # De esta forma, inicializamos todos los parametros de la red neuronal, matrices de pesos y bias

    for step in range(n_steps):

        _, _loss, _py = sess.run([optimizer, loss, pY], feed_dict={ iX : X, iY : Y})

        if step % 25 == 0:
            # Cálculo del accuracy entre el vector real y las predicciones.
            acc = np.mean(np.round(_pY) == Y)

            print('Step', step, '/', n_steps, ' - Loss = ', _loss, '- Acc',acc)
