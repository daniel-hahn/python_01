'''
this AI predicts, which category one piece of cloths belongs to.

categories:
0 T-shirt/top
1 Trouser
2 Pullover
3 Dress
4 Coat
5 Sandal
6 Shirt
7 Sneaker
8 Bag
9 Ankle boot
'''

import tensorflow as tf 
import numpy as np
import matplotlib.pyplot as plt


#load database "Mnist Fashion"
mnist = tf.keras.datasets.fashion_mnist
(training_images, training_labels), (test_images, test_labels) = mnist.load_data()

# reshape datasets
training_images = training_images.reshape(60000, 28, 28, 1)
training_images = training_images / 255.0
test_images = test_images.reshape(10000, 28, 28, 1)
test_images = test_images / 255.0

# build net
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

# fit datasets to model, set optimizer and loss, train net
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(training_images,training_labels, epochs=4)



# predicts category of unseen test image
classes = model.predict(test_images)
predicted_classes = np.argmax(classes, axis=1)
print(classes[0])
print(test_labels[0])

# show test image
plt.imshow(test_images[0], cmap='Greys_r')