import json
import os
import math
import pandas as pd
import numpy as np
import keras.models 
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import model_from_json




from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys




#Loads Model
def loadModel():
    with open('model.json','r') as f:
        model_json = json.load(f)
    model = model_from_json(json.dumps(model_json))
    model.load_weights('model.h5')
    return model


#Return Array for input of LSTM
def clean(fileName):
    params=[]
    # y=[]
    data = pd.read_csv(os.curdir + "/" + fileName , sep='|')
    data.drop(['EtCO2','Fibrinogen', 'Unit1', 'Unit2', 'BaseExcess', 'DBP', 'Hct', 'Hgb', 'PTT', 'WBC', 'pH','HCO3','FiO2', 'PaCO2', 'Platelets', 'Magnesium',  'Phosphate',  'Potassium', 'Bilirubin_total',  'TroponinI','SaO2', 'AST','BUN', 'Alkalinephos', 'Bilirubin_direct','Glucose','Lactate', 'Calcium',  'Chloride', 'Creatinine' ],axis = 1,inplace = True)

    data.dropna(thresh=data.shape[1]*0.40,how='all',inplace = True)
    # La_1 = data['SepsisLabel'].sum()
    # if La_1:
    #     y.append(1)
    # else:
    #     y.append(0)
    data.drop(['SepsisLabel'],axis = 1,inplace = True)
    data = data.apply(lambda x: x.fillna(x.median()),axis=0)
    data = data.fillna(0)
    if len(data) < 40:
        Pad = pd.DataFrame({'HR':0.0 ,'O2Sat':0.0, 'Temp':0.0 , 'SBP':0.0, 'MAP':0.0, 'Resp':0.0, 'Age':0.0, 'Gender': 0 ,'HospAdmTime':0.0, 'ICULOS':0}, index =[item for item in range(0,40-len(data))])
        data = pd.concat([Pad, data]).reset_index(drop = True)
    elif len(data) >40:
        data = data[len(data)-40::1]
    data = data.values
    params.append(data)
    return params


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)
     
        self.show()
        self.pushButton.clicked.connect(self.pushButton_handler)

    def pushButton_handler(self):
        print("hhdvcjhsvjvjsj")
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        path= filename[0]
        print(path)
        
        #Machine Learning
        Model = loadModel()

        X_test = clean(path.split('/')[-1])
        print(X_test)

        X_test = np.reshape(X_test,(1,40,10))

        y_pred = Model.predict(X_test)
        print(y_pred)
        
        if (y_pred <= 0.2):
            print("no Sepsis")
        else:
            print("Sepsis Go to Hospital")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()





    
