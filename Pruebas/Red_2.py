import tensorflow as tf
import tensorflow_datasets as tfds

# Guardamos los datos del dataset de Ropa desde la librería tensorflow_datasets
datos, metadatos = tfds.load('fashion_mnist',as_supervised=True, with_info=True)

# Revisando la información del dataset
metadatos

# Separamos los datos de entrenamiento de los datos de test.
datos_entrenamiento, datos_pruebas= datos['train'], datos['test']

# asignamos los indices a una variables
nombre_clases = metadatos.features['label'].names
nombre_clases

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
    plt.xlabel(nombre_clases[etiqueta])
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