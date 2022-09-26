import pandas as pd
import glob
import os

# Archivos que se van a unir
# files_joined = os.path.join('.\\Base_datos\\Fusion_26_9\\Entrenamiento', '2022*.csv')
files_joined = os.path.join('.\\Base_datos\\Fusion_26_9\\Test', '2022*.csv')

# Devuelve la lista con todos los archivos unidos
list_files = glob.glob(files_joined)

os.system('cls')
# print(list_files)
print("Union de todos los archivos en uno solo...")
# dataframe = pd.concat(map(pd.read_csv(),list_files), ignore_index = True)
li = []

for filename in list_files:
    df = pd.read_csv(filename,encoding_errors= 'ignore')
    li.append(df)

frame = pd.concat(li, ignore_index = True)

# Corregimos las columnas que tienen valores incorrectos (anoté tildes x.x) -> encoding = 'latin-1'
Columnas = ['Hora', 'Antena', 'iden.Tag', 'RSSI_1', 'Ang.Azimuth', 'Ang.Elevacion',
       'RSSI_2', 'Canal', 'Linea de visin libre(si=1, no=0)',
       'altura de la antena, respecto del nivel del suelo',
       'Distancia entre antena con el tag en cm',
       'Distancia entre el suelo con el tag en cm',
       'Existe un error en la medicin', 'Linea de vision libre(si=1, no=0)',
       'Existe un error en la medicion']
frame.columns = Columnas

# Elimino las columnas repetidas y datos irrelevantes para el entrenamiento
frame = frame.drop(['Antena','RSSI_2','Linea de vision libre(si=1, no=0)'
            ,'Existe un error en la medicion'], axis = 1)

# Le damos nombres más acordes a lo que estamos usando.
frame.columns = ['Hora','Iden_tag','RSSI','Ang_azimuth','Ang_elevacion','Canal','LOS(si=1,no=0)','Altura_ant(cm)','Distancia_entre_ant_tag(cm)','Altura_tag(cm)','Error_dato_medido']

# Finalmente lo guardamos, se recomienda usar utf-8 cuando usamos diferentes sistemas operativos
# frame.to_csv('Entrenamiento.csv',encoding = 'utf-8')
frame.to_csv('Test.csv',encoding = 'utf-8')