# -*- coding: utf-8 -*-
"""ProyekPertamaNLPTensorFlow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_2bZKH1touDJO__b2ECWFZ8lVJPjRPi9

Nama : Muhammad Fadli Ramadhan

Gmail : fadlinisasileader@gmail.com

Proyek Pertama Membuat Model NLP TensorFlow (datasets: >2000)

Senin, 13 September 2021
"""

# Upload Dataset
from google.colab import files
uploaded = files.upload()

# Read Dataset
import pandas as pd
train = pd.read_csv('train.txt', sep=';', names=['sentences', 'feelings'])
test = pd.read_csv('test.txt', sep=';', names=['sentences', 'feelings'])
val = pd.read_csv('val.txt', sep=';', names=['sentences', 'feelings'])
df = train.append(test)
df = df.append(val)
df

# Data Preprocessing
df.info()

# Cek Null
df.isna().sum()

# Cek data yang terduplikat
df.duplicated().sum()

# Menghapus data duplikat
df.drop_duplicates(inplace=True)

# One Hot Encoding Label
category = pd.get_dummies(df['feelings'])
df_baru = pd.concat([df, category], axis=1)
df_baru = df_baru.drop(columns='feelings')
df_baru.tail()

# Melakukan train test split
sinopsis = df_baru['sentences'].values
label = df_baru[['anger', 'fear', 'joy', 'love', 'sadness', 'surprise']].values

from sklearn.model_selection import train_test_split
# Rasio train 80% dan test 20%
sinopsis_latih, sinopsis_test, label_latih, label_test = train_test_split(sinopsis, label, test_size=0.2)

# Mencari dan menghitung banyak kata
from collections import Counter

def counter_words(text):
  count = Counter()
  for i in text.values:
    for word in i.split():
      count[word] += 1
  return count

sentence = df_baru['sentences']
counter = counter_words(sentence)
num_words = len(counter)
num_words

# Melakukan tokenizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=num_words, oov_token='x')
tokenizer.fit_on_texts(sinopsis_latih)
tokenizer.fit_on_texts(sinopsis_test)

sekuens_latih = tokenizer.texts_to_sequences(sinopsis_latih)
sekuens_test= tokenizer.texts_to_sequences(sinopsis_test)

padded_latih = pad_sequences(sekuens_latih)
padded_test = pad_sequences(sekuens_test)

# Arsitektur Model (Sequential, Embedding, LSTM)
import tensorflow as tf

model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=num_words, output_dim=64),
        tf.keras.layers.LSTM(128),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(6, activation='softmax')                            
])

model.compile(
    loss='categorical_crossentropy',
    optimizer='rmsprop',
    metrics=['accuracy']
)

# Melatih Model 
history = model.fit(padded_latih, label_latih, epochs=10,
                    validation_data=(padded_test, label_test),
                    verbose=1)

import matplotlib.pyplot as plt

# inisiasi akurasi dan loss
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

# Plot Akurasi
plt.plot(epochs, acc, 'r', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Akurasi Training dan Validation')
plt.legend()

# Plot Loss
plt.figure()
plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Loss Training dan Validation')
plt.legend()

plt.show()

# Memanggil fungsi Callback
# inisiasi callback dengan syarat diatas 91%
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if (logs.get('val_accuracy') > 0.91) & (logs.get('accuracy') > 0.91):
      print('\Akurasi telah mencapai >91%')
      self.model.stop_training = True
callbacks = myCallback()

# Melatih Model fungsi callback

history = model.fit(
    padded_latih, label_latih, epochs=30,
    validation_data=(padded_test, label_test),
    callbacks=callbacks,
    verbose=1
)
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

# Plot akurasi
plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()

# plot loss
plt.figure()
plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, loss, 'b', label='Validation Loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()