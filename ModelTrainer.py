import pandas as pd
import numpy as np
import tensorflow as tf
import datetime as dt
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

class ModelTrainer:
    gestures = ['open_palm', 'closed_fist', 'pointing_up']

    data_folder_path = os.path.join(os.getcwd(), "Datasets")

    def preprocess_data():
        loaded_data = np.load(os.path.join(ModelTrainer.data_folder_path, f'data_{ModelTrainer.gestures[0]}.npz'))
        X, y = loaded_data['X'], loaded_data['y']
        for data_class in ModelTrainer.gestures[1:]:
            if os.path.exists(os.path.join(ModelTrainer.data_folder_path, f'data_{data_class}.npz')):
                loaded_data = np.load(os.path.join(ModelTrainer.data_folder_path, f'data_{data_class}.npz'))
                X = np.vstack((X, loaded_data['X']))
                y = np.concatenate((y, loaded_data['y']))
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.2, random_state=1, stratify=y)
        print(X_train.shape)
        print(X_test.shape)

        ModelTrainer.build_RF(X_train, X_test, y_train, y_test)

    # def preprocess_data():
    #     gesture_data = []
    #     labels = []

    #     for gesture in ModelTrainer.gestures:
    #         print(ModelTrainer.label_map)
    #         data_folder_path = os.path.join(os.getcwd(), "Datasets", str(gesture))
    #         for file in os.listdir(data_folder_path):
    #             if file.endswith(".npy"):
    #                 print(os.path.join(data_folder_path), file)
    #                 data = np.load(os.path.join(data_folder_path, file))
    #                 gesture_data.append(data)
    #             labels.append(ModelTrainer.label_map[gesture])

    #     x = np.array(gesture_data)
    #     y = tf.keras.utils.to_categorical(labels).astype(int)
                
    #     #x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.05)
    #     x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, test_size=0.2, random_state=1, stratify=y)
    #     #ModelTrainer.build_lstm(x_train, x_test, y_train, y_test)
    #     ModelTrainer.build_RF(x_train, x_test, y_train, y_test)
    #     print(x_train.shape)
    #     print(x_test.shape)
    #     print(y_train.shape)
    #     print(y_test.shape)     

    def build_lstm(x_train, x_test, y_train, y_test):
        log_dir = os.path.join('Logs')
        tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.LSTM(64, return_sequences=True, activation='relu', input_shape=(3,21)))
        model.add(tf.keras.layers.LSTM(128, return_sequences=True, activation='relu'))
        model.add(tf.keras.layers.LSTM(64, return_sequences=False, activation='relu'))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(32, activation='relu'))
        model.add(tf.keras.layers.Dense(ModelTrainer.gestures.shape[0], activation='softmax'))

        model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

        model.fit(x_train, y_train, epochs=2000, callbacks=[tb_callback])

        model.summary()
    
    def build_RF(x_train, x_test, y_train, y_test):
        with tf.device('/GPU:0'):
            model = RandomForestClassifier()
            model.fit(x_train, y_train)

            yhat_test = model.predict(x_test)
            test_accuracy = accuracy_score(y_test, yhat_test)
            print(f'Accuracy: {test_accuracy}')

            date_time_format = '%Y_%m_%d__%H_%M_%S'
            current_date_time_dt = dt.datetime.now()
            current_date_time_str = dt.datetime.strftime(current_date_time_dt, date_time_format)

            model_name = f'model_rf__date_time_{current_date_time_str}__acc_{test_accuracy}__hand__oneimage.pkl'
            joblib.dump(model, model_name)





