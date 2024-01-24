import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import datetime as dt
import os

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from scipy.stats import randint
import joblib

class ModelTrainer:
    gestures = ['open_palm', 'closed_fist', 'pointing_up', 'thumbs_down']
    data_folder_path = os.path.join(os.getcwd(), "Datasets")

    #Handles preprocessing of recorded landmark data
    def preprocess_data(): #process and label data points
        #incase the folder doesn't exist
        if os.path.exists(ModelTrainer.data_folder_path) == False:
            os.makedirs(ModelTrainer.data_folder_path)

        loaded_data = np.load(os.path.join(ModelTrainer.data_folder_path, 'data.npz'))
        X, y = loaded_data['X'], loaded_data['y']
        #iterate through all files in each sub directory in Datasets folder
        for data_class in ModelTrainer.gestures:
            sub_dir_path = os.path.join(ModelTrainer.data_folder_path, data_class)
            for file in os.listdir(sub_dir_path):
                if file.endswith(".npz"): 
                    print(file)                   
                    loaded_data = np.load(os.path.join(sub_dir_path, file))
                    X = np.vstack((X, loaded_data['X']))
                    y = np.concatenate((y, loaded_data['y']))                                          
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.2, random_state=1, stratify=y)
        
        print(X_train.shape)
        print(X_test.shape)
        print(X_train)
        print(X_test)
        print(y_train)
        print(y_test)

        ModelTrainer.build_RF(X_train, X_test, y_train, y_test)
   
    def build_RF(x_train, x_test, y_train, y_test): #creates model file with 
        with tf.device('/GPU:0'):
            param_dist = {'n_estimators': randint(50,500),
              'max_depth': randint(1,20)}
                        
            model = RandomForestClassifier()

            rand_search = RandomizedSearchCV(model, 
                                 param_distributions = param_dist, 
                                 n_iter=5, 
                                 cv=5)

            # Fit the random search object to the data
            rand_search.fit(x_train, y_train)
            
            # Create a variable for the best model
            best_rf = rand_search.best_estimator_

            # Print the best hyperparameters
            print('Best hyperparameters:',  rand_search.best_params_)

            # add in cross validation

            yhat_pred = best_rf.predict(x_test)
            
            test_accuracy = accuracy_score(y_test, yhat_pred)
            # precision = precision_score(y_test, yhat_pred)
            # recall = recall_score(y_test, yhat_pred)

            print(f'Accuracy: {test_accuracy}')
            # print(f'Precision: {precision}')
            # print(f'Recall: {recall}')

            date_time_format = '%Y_%m_%d__%H_%M_%S'
            current_date_time_dt = dt.datetime.now()
            current_date_time_str = dt.datetime.strftime(current_date_time_dt, date_time_format)

            model_name = f'model_rf__date_time_{current_date_time_str}_acc_{test_accuracy}.pkl'
            joblib.dump(best_rf, model_name)

    #to add Gesture to the Array
    def Add_gesture(Name):
        gestures.append(Name)

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
             
    # def build_lstm(x_train, x_test, y_train, y_test):
    #     log_dir = os.path.join('Logs')
    #     tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

    #     model = tf.keras.models.Sequential()
    #     model.add(tf.keras.layers.LSTM(64, return_sequences=True, activation='relu', input_shape=(3,21)))
    #     model.add(tf.keras.layers.LSTM(128, return_sequences=True, activation='relu'))
    #     model.add(tf.keras.layers.LSTM(64, return_sequences=False, activation='relu'))
    #     model.add(tf.keras.layers.Dense(64, activation='relu'))
    #     model.add(tf.keras.layers.Dense(32, activation='relu'))
    #     model.add(tf.keras.layers.Dense(ModelTrainer.gestures.shape[0], activation='softmax'))

    #     model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

    #     model.fit(x_train, y_train, epochs=2000, callbacks=[tb_callback])

    #     model.summary()


