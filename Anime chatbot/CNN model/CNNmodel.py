# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 12:38:28 2023

@author: Alarn
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np


# Set the path to the directory containing the images
train_dir = 'D:/Uni Work/A.I. Module/revised_dataset/train'
test_dir = 'D:/Uni Work/A.I. Module/revised_dataset/test'

# Define the parameters for image preprocessing
image_size = (28, 28)
batch_size = 10

# Create image data generator for train and test datasets
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(train_dir, target_size=image_size, batch_size=batch_size, class_mode='sparse')

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(test_dir, target_size=image_size, batch_size=batch_size, class_mode='sparse')

output_classes = train_generator.num_classes

# Build the model
model = keras.Sequential([
    keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 3)),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(output_classes)
])

model.compile(optimizer='adam',
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

## Train the model
model.fit(train_generator, epochs=10, steps_per_epoch=train_generator.samples//batch_size)

# Save the trained model
model.save('D:/Uni Work/A.I. Module')

# Evaluate the trained model
test_loss, test_acc = model.evaluate(test_generator,  verbose=2)
print('\n Test accuracy:', test_acc)
