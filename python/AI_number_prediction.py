'''
this AI predicts, what the corresponding number (y) to a given number (x) is, 
when its actual relation is: y(x) = 2x
'''

import tensorflow as tf 
from tensorflow import keras 

# create net, Dense creates 1 neuron
model = keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])]) 

# loss measures error, optimizer lowers loss
model.compile(optimizer='sgd', loss='mean_squared_error') 

# number rows for training,  y = 2x
xs = [1, 2, 3] 
ys = [2, 4, 6] 

# fit data to model, epochs means training runs, train net
model.fit(xs, ys, epochs=1000) 

# predict second number
print(model.predict([7])) 