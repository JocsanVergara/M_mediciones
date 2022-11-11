
# Importando librerias
import pandas as pd
import numpy as np
import seaborn as sns
import datetime
import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler

sns.set_theme(style='darkgrid')

# IMPORTANDO LOS DATOS
# Si nuestro archivo csv que estamos leyendo esta separado por comas
df_train = pd.read_csv("./data/Entrenamiento.csv", encoding='utf-8', index_col = False, usecols = [1,3,4,5,6,8,9,10,11])
# Corrige el error de lectura del archivo, pasa de string/objetc a float
#df_train = df_train.replace('[^\d.]','', regex=True).astype(float) 
df_train.head()

df_train['Fecha'] = pd.to_datetime(df_train.Hora, format="%Y/%m/%d %H:%M:%S", errors='coerce')
df_train.Fecha.head()
