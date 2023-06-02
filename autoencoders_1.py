"""
Implementación de un autoencoder simple usando Keras
"""

import keras
from keras import layers

# Tamaño de las representaciones codificadas (32 floats -- factor compresión 24.5,
# asumiendo entrada de 784 floats de entrada)
encoding_dim = 32
input_img = keras.Input(shape=(784,))
# 'encoded' es la representación codificada de la entrada
encoded = layers.Dense(encoding_dim, activation='relu')(input_img)
# 'decoded' es la pérdida en la reconstrucción de la entrada
decoded = layers.Dense(784, activation='sigmoid')(encoded)

# Este modelo mapea una entrada para su reconstrucción.
autoencoder = keras.Model(input_img, decoded)

# Vamos a crear además, un modelo de encoder separado así como el modelo del decoder
# ENCODER
# Este modelo asigna una entrada a su representación codificada
encoder = keras.Model(input_img, encoded)
# DECODER
# Esta es nuestra entrada codificada (32 dimensiones)
encoded_input = keras.Input(shape=(encoding_dim,))
# Recuperar la última capa del modelo de autoencoder
decoder_layer = autoencoder.layers[-1]
# Crea el modelo del decoder
decoder = keras.Model(encoded_input, decoder_layer(encoded_input))

# Entrenando el autoencoder para reconstruir digitos de MNIST

# Configurando el modelo para usar una pérdida de entropía cruzada binaria por píxel y el optimizador de Adam
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

# Preparando los datos de entrada. Se usa MNIST descartando las etiquetas
from keras.datasets import mnist
import numpy as np

(x_train, _), (x_test, _) = mnist.load_data()
# Normalizando todos los valores entre 0 y 1 y planando las imágenes de 28x28 en vectores de 784 de tamaño
x_train = x_train.astype('float32')/255.
x_test = x_test.astype('float32')/255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
print(x_train.shape)
print(x_test.shape)
# Ahora se va a entrenar el autoencoder para 50 épocas
autoencoder.fit(x_train,  x_train,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))
# Luego de 50 épocas, el autoencoder parece alcanzar un valor estable "train/validation loss" de aproximadamente 0,09
encoded_imgs = encoder.predict(x_test)
decoded_imgs = decoder.predict(encoded_imgs)

# Usando Matplotlib
import matplotlib.pyplot as plt

n = 10  # How many digits we will display
plt.figure(figsize=(20, 4))
for i in range(n):
    # Display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()









