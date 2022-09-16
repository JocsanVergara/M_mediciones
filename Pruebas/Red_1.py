import tensorflow as tf
import numpy as np

# Definimos los datos para el entrenamiento
celsius = np.array([-40,-10,0,8,15,22,38], dtype=float)
fahrenheit = np.array([-40,14,32,46,59,72,100], dtype=float)

# Tenemos el número de capas y el modelo a utilizar
capa = tf.keras.layers.Dense(units=1, input_shape=[1])
modelo = tf.keras.Sequential([capa])

# Compilamos el modelo y definimos el modelo de optimización y la función de costo o perdida
modelo.compile(
    optimizer = tf.keras.optimizers.Adam(0.1),
    loss='mean_squared_error'
)

# Iniciamos el entrenamiento
print("Comenzando entrenamiento...")
historial = modelo.fit(celsius,fahrenheit, epochs=1000,verbose=False)
print("modelo entrenado!")

# Graficamos la función de perdida / aprendizaje de la red
import matplotlib.pyplot as plt
plt.xlabel("# Epoca")
plt.ylabel("Magnitud de pérdida")
plt.plot(historial.history["loss"])

# Revisemos si la red obtiene correctamente los valores de la red
print("Hagamos una predicción!")
resultado = modelo.predict([100.0])
print("El resultado es "+str(resultado)+"fahrenheit!")

# Obtenemos los valores internos de la red
print("Variables internas del modelo")
print(capa.get_weights())
