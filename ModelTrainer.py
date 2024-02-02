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

import ProgramSettings as PS

class ModelTrainer:
    #Handles preprocessing of recorded landmark data
    def preprocess_data(): #process and label data points
        #load data from gesture dataset file
        loaded_data = np.load(os.path.join(PS.data_folder_path, 'data.npz'))
        X, y = loaded_data['X'], loaded_data['y']
        #iterate through all files in each sub directory in Datasets folder
        for data_class in PS.allowed_gestures:
            sub_dir_path = os.path.join(PS.data_folder_path, data_class)
            for file in os.listdir(sub_dir_path):
                if file.endswith(".npz"): 
                    print(file)                   
                    loaded_data = np.load(os.path.join(sub_dir_path, file))
                    X = np.vstack((X, loaded_data['X']))
                    y = np.concatenate((y, loaded_data['y']))                                          
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.2, random_state=1, stratify=y)
        
        print(f'X_train shape: {X_train.shape}')
        print(f'X_test shape: {X_test.shape}')
        
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

            # add in cross validation?

            yhat_pred = best_rf.predict(x_test)
            
            test_accuracy = accuracy_score(y_test, yhat_pred)
            precision = precision_score(y_test, yhat_pred, average='weighted')
            recall = recall_score(y_test, yhat_pred, average='weighted')

            print(f'Accuracy: {test_accuracy}')
            print(f'Precision: {precision}')
            print(f'Recall: {recall}')
            
            #===For testing============#
            #date_time_format = '%Y_%m_%d__%H_%M_%S'
            #current_date_time_dt = dt.datetime.now()
            #current_date_time_str = dt.datetime.strftime(current_date_time_dt, date_time_format)
            #model_name = f'rf_model_{current_date_time_str}.pkl'
            #==========================#
            model_name = 'rf_model.pkl'
            joblib.dump(best_rf, os.path.join(PS.model_folder_path, model_name))

            

            



