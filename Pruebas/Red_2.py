import tensorflow as tf
import tensorflow_datasets as tfds

# Guardamos los datos del dataset de Ropa desde la librería tensorflow_datasets
datos, metadatos = tfds.load('fashion_mnist',as_supervised=True, with_info=True)

# Revisando la información del dataset
metadatos

# Separamos los datos de entrenamiento de los datos de test.
datos_entrenamiento, datos_pruebas= datos['train'], datos['test']

# asignamos los indices a una variables
nombres_clases = metadatos.features['label'].names
nombres_clases

# Normalizar la entrenada de (0-255 a 0-1)
def normalizar(imagenes, etiquetas):
    imagenes = tf.cast(imagenes, tf.float32)
    imagenes /= 255 #Aquí lo pasamos de 0-255 a 0-1
    return imagenes, etiquetas

# Normalizar los datos de entrenamiento y pruebas con las funciones que hicimos
datos_entrenamiento = datos_entrenamiento.map(normalizar)
datos_pruebas = datos_pruebas.map(normalizar)

# Agregar a cache (Usar memoria en lugar de disco, entrenamiento más rápido)
datos_entrenamiento = datos_entrenamiento.cache()
datos_pruebas = datos_pruebas.cache()

# Mostar una imagen de los datos de pruebas, de momento mostremos la primera
for imagen, etiqueta in datos_entrenamiento.take(1):
    break
imagen = imagen.numpy().reshape((28,28)) # Redimensionar, cosas de tensores

import matplotlib.pyplot as plt

# Dibujar
plt.figure()
plt.imshow(imagen, cmap=plt.cm.binary)
plt.colorbar()
plt.grid(False)
plt.show()

# Le vamos a pedir que muestre una cantidad de imagenes con sus caracteristicas
plt.figure(figsize=(10,10))
for i, (imagen, etiqueta) in enumerate(datos_entrenamiento.take(25)):
    imagen = imagen.numpy().reshape((28,28))
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(imagen, cmap=plt.cm.binary)
    plt.xlabel(nombres_clases[etiqueta])
plt.show()

# Crea el modelo
modelo = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28,28,1)), # hacemos uso de una sola dimensión 1 - blanco y negro
    tf.keras.layers.Dense(50, activation = tf.nn.relu),
    tf.keras.layers.Dense(50, activation = tf.nn.relu),
    tf.keras.layers.Dense(10, activation = tf.nn.softmax) # Se usa en redes de clasificación
])

# Compilar el modelo
modelo.compile(
    optimizer = 'adam',
    loss = tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics = ['accuracy']
)

# Cuando tenemos muchos datos, el entrenamiento puede ser lento, se puede implementar en este caso un entrenamiento por lotes
TAMANO_LOTE = 32
num_ej_entrenamiento = metadatos.splits["train"].num_examples
num_ej_pruebas = metadatos.splits["test"].num_examples

# Ajustamos los datos de entrenamiento, como se realizaran varias vueltas al dataset, queremos que los datos no se le entreguen en el mismo orden a la red
datos_entrenamiento = datos_entrenamiento.repeat().shuffle(60000).batch(TAMANO_LOTE)
datos_pruebas = datos_pruebas.batch(TAMANO_LOTE)

import math
# Entrenamiento
historial = modelo.fit(datos_entrenamiento, epochs=5, steps_per_epoch=math.ceil(num_ej_entrenamiento/TAMANO_LOTE))

# Revisamos el aprendizaje de la red con respecto a cada epoca
plt.xlabel("# Epoca")
plt.ylabel("Magnitud de pérdida")
plt.plot(historial.history["loss"])

#
import numpy as np
for imagenes_prueba, etiquetas_prueba in datos_pruebas.take(1):
    imagenes_prueba = imagenes_prueba.numpy()
    etiquetas_prueba = etiquetas_prueba.numpy()
    predicciones = modelo.predict(imagenes_prueba)

def graficar_imagen(i, arr_predicciones, etiquetas_reales, imagenes):
    arr_predicciones, etiqueta_real, img = arr_predicciones[i], etiquetas_reales[i],imagenes[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img[...,0], cmap = plt.cm.binary)

    etiqueta_prediccion = np.argmax(arr_predicciones)
    if(etiqueta_prediccion == etiqueta_real):
        color = 'blue' # Si le acerto a la predicción
    else:
        color = 'red'
  
    plt.xlabel("{} {:2.0f}% ({})".format(nombres_clases[etiqueta_prediccion],
                                    100*np.max(arr_predicciones),
                                    nombres_clases[etiqueta_real]),
                                    color=color)
    
def graficar_valor_arreglo(i, arr_predicciones, etiqueta_real):
  arr_predicciones, etiqueta_real = arr_predicciones[i], etiqueta_real[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  grafica = plt.bar(range(10), arr_predicciones, color="#777777")
  plt.ylim([0, 1]) 
  etiqueta_prediccion = np.argmax(arr_predicciones)
  
  grafica[etiqueta_prediccion].set_color('red')
  grafica[etiqueta_real].set_color('blue')
  
filas = 5
columnas = 5
num_imagenes = filas*columnas
plt.figure(figsize=(2*2*columnas, 2*filas))
for i in range(num_imagenes):
  plt.subplot(filas, 2*columnas, 2*i+1)
  graficar_imagen(i, predicciones, etiquetas_prueba, imagenes_prueba)
  plt.subplot(filas, 2*columnas, 2*i+2)
  graficar_valor_arreglo(i, predicciones, etiquetas_prueba)

#Probar una imagen suelta
imagen = imagenes_prueba[4] #AL ser la variable imagenes_prueba solo tiene lo que se le puso en el bloque anterior heheh
imagen = np.array([imagen])
prediccion = modelo.predict(imagen)

print("Prediccion: " + nombres_clases[np.argmax(prediccion[0])])

#Exportacion del modelo a h5
modelo.save('modelo_exportado.h5')

#Instalar tensorflowjs para convertir el h5 a un modelo que pueda cargar tensorflowjs en un explorador
#!pip install tensorflowjs

#Convertir el archivo h5 a formato de tensorflowjs
#!mkdir tfjs_target_dir
#!tensorflowjs_converter --input_format keras modelo_exportado.h5 tfjs_target_dir

#Veamos si si creo la carpeta
#!ls

#Veamos el contenido de la carpeta
#!ls tfjs_target_dir




