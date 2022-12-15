## Instancias

import pandas as pd
import glob
import os

import tensorflow as tf
import re
import matplotlib as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from keras.models import Sequential
from keras.layers import Dense, Flatten, Convolution1D, Dropout
from keras.optimizers import SGD
from keras.optimizers import Adam
from keras.initializers import random_uniform
from keras.optimizers.optimizer_v2 import adam

import numpy as np
import pandas as pd
import seaborn as sns
from numpy import interp
from itertools import cycle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import mean_absolute_error, accuracy_score, precision_score, recall_score, f1_score, roc_curve, plot_roc_curve
from sklearn.metrics import confusion_matrix, classification_report, auc
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from keras.layers import Input, Conv1D, MaxPooling1D, UpSampling1D, concatenate, BatchNormalization, Activation, add
from keras.layers import Conv2D, MaxPooling2D, Reshape, Flatten, Dense
from keras.models import Model, model_from_json
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
sns.set_theme(style="whitegrid")



# Archivos que se van a unir
files_joined = os.path.join('.\\Memoria\\Dataset', 'Entre*.csv')

# Devuelve la lista con todos los archivos unidos
list_files = glob.glob(files_joined)

print(list_files)

os.system('cls')
print("Union de todos los archivos en uno solo...")
li = []

for filename in list_files:
    df = pd.read_csv(filename,encoding_errors= 'ignore')
    li.append(df)

frame = pd.concat(li, ignore_index = True)
frame = frame.drop(['Unnamed: 0'],axis=1)
frame = frame.dropna()
frame.head()

frame_1 = frame.drop(['_id','hora','Id_tag','Id_Ant'],axis=1)

# Escalamos los datos
scaler_0 = MinMaxScaler()
scaler_0 = scaler_0.fit(frame_1)

frame_1[['RSSI','Ang_azimuth','Ang_elevacion','Canal','Altura_ant(cm)','Distancia_entre_ant_tag(cm)','Error_dato_medido','Distancia_entre_ant','Distancia_ant_tag']] = scaler_0.transform (frame_1[['RSSI','Ang_azimuth','Ang_elevacion','Canal','Altura_ant(cm)','Distancia_entre_ant_tag(cm)','Error_dato_medido','Distancia_entre_ant','Distancia_ant_tag']])

train, test = train_test_split(frame_1, test_size = 0.20, shuffle = False)

train_x = (train.drop(['Distancia_entre_ant_tag(cm)','Error_dato_medido'],axis=1)).to_numpy()
train_y = (train.drop(['RSSI','Ang_azimuth','Ang_elevacion','Canal','Altura_ant(cm)','Distancia_entre_ant_tag(cm)', 'Distancia_ant_tag','Distancia_entre_ant'],axis=1)).to_numpy()

test_x = (test.drop(['Distancia_entre_ant_tag(cm)','Error_dato_medido'],axis=1)).to_numpy()
test_y = (test.drop(['RSSI','Ang_azimuth','Ang_elevacion','Canal','Altura_ant(cm)','Distancia_entre_ant_tag(cm)', 'Distancia_ant_tag','Distancia_entre_ant'],axis=1)).to_numpy()

X_train = train_x.reshape(train_x.shape[0],train_x.shape[1],1)
X_test = test_x.reshape(test_x.shape[0],test_x.shape[1],1)


# ResNet models for Keras.
# Reference for ResNets - [Deep Residual Learning for Image Recognition](https://arxiv.org/pdf/1512.03385.pdf))

import tensorflow as tf


def Conv_1D_Block(x, model_width, kernel, strides):
    # 1D Convolutional Block with BatchNormalization
    x = tf.keras.layers.Conv1D(model_width, kernel, strides=strides, padding="same", kernel_initializer="he_normal")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)

    return x


def stem(inputs, num_filters):
    # Construct the Stem Convolution Group
    # inputs : input vector
    # First Convolutional layer, where pooled feature maps will be reduced by 75%
    conv = Conv_1D_Block(inputs, num_filters, 7, 2)
    if conv.shape[1] <= 2:
        pool = tf.keras.layers.MaxPooling1D(pool_size=1, strides=2, padding="valid")(conv)
    else:
        pool = tf.keras.layers.MaxPooling1D(pool_size=2, strides=2, padding="valid")(conv)
    
    return pool


def conv_block(inputs, num_filters):
    # Construct Block of Convolutions without Pooling
    # x        : input into the block
    # n_filters: number of filters
    conv = Conv_1D_Block(inputs, num_filters, 3, 2)
    conv = Conv_1D_Block(conv, num_filters, 3, 1)
    
    return conv


def residual_block(inputs, num_filters):
    # Construct a Residual Block of Convolutions
    # x        : input into the block
    # n_filters: number of filters
    shortcut = inputs
    #
    conv = Conv_1D_Block(inputs, num_filters, 3, 1)
    conv = Conv_1D_Block(conv, num_filters, 3, 1)
    conv = tf.keras.layers.Add()([conv, shortcut])
    out = tf.keras.layers.Activation('relu')(conv)
    
    return out


def residual_group(inputs, num_filters, n_blocks, conv=True):
    # x        : input to the group
    # n_filters: number of filters
    # n_blocks : number of blocks in the group
    # conv     : flag to include the convolution block connector
    out = inputs
    for i in range(n_blocks):
        out = residual_block(out, num_filters)

    # Double the size of filters and reduce feature maps by 75% (strides=2, 2) to fit the next Residual Group
    if conv:
        out = conv_block(out, num_filters * 2)
    
    return out
def stem_bottleneck(inputs, num_filters):
    # Construct the Stem Convolution Group
    # inputs :input vector
    # First Convolutional layer, where pooled feature maps will be reduced by 75%
    conv = Conv_1D_Block(inputs, num_filters, 7, 2)
    if conv.shape[1] <= 2:
        pool = tf.keras.layers.MaxPooling1D(pool_size=1, strides=2, padding="valid")(conv)
    else:
        pool = tf.keras.layers.MaxPooling1D(pool_size=2, strides=2, padding="valid")(conv)
    
    return pool


def residual_block_bottleneck(inputs, num_filters):
    # Construct a Residual Block of Convolutions
    # x        : input into the block
    # n_filters: number of filters
    shortcut = Conv_1D_Block(inputs, num_filters * 4, 1, 1)
    #
    conv = Conv_1D_Block(inputs, num_filters, 1, 1)
    conv = Conv_1D_Block(conv, num_filters, 3, 1)
    conv = Conv_1D_Block(conv, num_filters * 4, 1, 1)
    conv = tf.keras.layers.Add()([conv, shortcut])
    out = tf.keras.layers.Activation('relu')(conv)

    return out


def residual_group_bottleneck(inputs, num_filters, n_blocks, conv=True):
    # x        : input to the group
    # n_filters: number of filters
    # n_blocks : number of blocks in the group
    # conv     : flag to include the convolution block connector
    out = inputs
    for i in range(n_blocks):
        out = residual_block_bottleneck(out, num_filters)

    # Double the size of filters and reduce feature maps by 75% (strides=2, 2) to fit the next Residual Group
    if conv:
        out = conv_block(out, num_filters * 2)

    return out


def learner18(inputs, num_filters):
    # Construct the Learner
    x = residual_group(inputs, num_filters, 2)          # First Residual Block Group of 64 filters
    x = residual_group(x, num_filters * 2, 1)           # Second Residual Block Group of 128 filters
    x = residual_group(x, num_filters * 4, 1)           # Third Residual Block Group of 256 filters
    out = residual_group(x, num_filters * 8, 1, False)  # Fourth Residual Block Group of 512 filters
    
    return out


def learner34(inputs, num_filters):
    # Construct the Learner
    x = residual_group(inputs, num_filters, 3)          # First Residual Block Group of 64 filters
    x = residual_group(x, num_filters * 2, 3)           # Second Residual Block Group of 128 filters
    x = residual_group(x, num_filters * 4, 5)           # Third Residual Block Group of 256 filters
    out = residual_group(x, num_filters * 8, 2, False)  # Fourth Residual Block Group of 512 filters
    
    return out


def learner50(inputs, num_filters):
    # Construct the Learner
    x = residual_group_bottleneck(inputs, num_filters, 3)  # First Residual Block Group of 64 filters
    x = residual_group_bottleneck(x, num_filters * 2, 3)   # Second Residual Block Group of 128 filters
    x = residual_group_bottleneck(x, num_filters * 4, 5)   # Third Residual Block Group of 256 filters
    out = residual_group_bottleneck(x, num_filters * 8, 2, False)  # Fourth Residual Block Group of 512 filters
    
    return out


def learner101(inputs, num_filters):
    # Construct the Learner
    x = residual_group_bottleneck(inputs, num_filters, 3)  # First Residual Block Group of 64 filters
    x = residual_group_bottleneck(x, num_filters * 2, 3)   # Second Residual Block Group of 128 filters
    x = residual_group_bottleneck(x, num_filters * 4, 22)  # Third Residual Block Group of 256 filters
    out = residual_group_bottleneck(x, num_filters * 8, 2, False)  # Fourth Residual Block Group of 512 filters
    
    return out


def learner152(inputs, num_filters):
    # Construct the Learner
    x = residual_group_bottleneck(inputs, num_filters, 3)  # First Residual Block Group of 64 filters
    x = residual_group_bottleneck(x, num_filters * 2, 7)   # Second Residual Block Group of 128 filters
    x = residual_group_bottleneck(x, num_filters * 4, 35)  # Third Residual Block Group of 256 filters
    out = residual_group_bottleneck(x, num_filters * 8, 2, False)  # Fourth Residual Block Group of 512 filters
    
    return out


def classifier(inputs, class_number):
    # Construct the Classifier Group
    # inputs       : input vector
    # class_number : number of output classes
    out = tf.keras.layers.Dense(class_number, activation='softmax')(inputs)
    
    return out
def regressor(inputs, feature_number):
    # Construct the Regressor Group
    # inputs       : input vector
    # feature_number : number of output features
    out = tf.keras.layers.Dense(feature_number, activation='linear')(inputs)
    
    return out


class ResNet:
    def __init__(self, length, num_channel, num_filters, problem_type='Regression',
                 output_nums=1, pooling='avg', dropout_rate=False):
        self.length = length
        self.num_channel = num_channel
        self.num_filters = num_filters
        self.problem_type = problem_type
        self.output_nums = output_nums
        self.pooling = pooling
        self.dropout_rate = dropout_rate

    def MLP(self, x):
        if self.pooling == 'avg':
            x = tf.keras.layers.GlobalAveragePooling1D()(x)
        elif self.pooling == 'max':
            x = tf.keras.layers.GlobalMaxPooling1D()(x)
        # Final Dense Outputting Layer for the outputs
        x = tf.keras.layers.Flatten(name='flatten')(x)
        if self.dropout_rate:
            x = tf.keras.layers.Dropout(self.dropout_rate, name='Dropout')(x)
        outputs = tf.keras.layers.Dense(self.output_nums, activation='linear')(x)
        if self.problem_type == 'Classification':
            outputs = tf.keras.layers.Dense(self.output_nums, activation='softmax')(x)

        return outputs

    def ResNet18(self):
        inputs = tf.keras.Input((self.length, self.num_channel))      # The input tensor
        stem_ = stem(inputs, self.num_filters)               # The Stem Convolution Group
        x = learner18(stem_, self.num_filters)               # The learner
        outputs = self.MLP(x)
        # Instantiate the Model
        model = tf.keras.Model(inputs, outputs)

        return model

    def ResNet34(self):
        inputs = tf.keras.Input((self.length, self.num_channel))      # The input tensor
        stem_ = stem(inputs, self.num_filters)               # The Stem Convolution Group
        x = learner34(stem_, self.num_filters)               # The learner
        outputs = self.MLP(x)
        # Instantiate the Model
        model = tf.keras.Model(inputs, outputs)

        return model

    def ResNet50(self):
        inputs = tf.keras.Input((self.length, self.num_channel))     # The input tensor
        stem_b = stem_bottleneck(inputs, self.num_filters)  # The Stem Convolution Group
        x = learner50(stem_b, self.num_filters)             # The learner
        outputs = self.MLP(x)
        # Instantiate the Model
        model = tf.keras.Model(inputs, outputs)

        return model

    def ResNet101(self):
        inputs = tf.keras.Input((self.length, self.num_channel))     # The input tensor
        stem_b = stem_bottleneck(inputs, self.num_filters)  # The Stem Convolution Group
        x = learner101(stem_b, self.num_filters)            # The learner
        outputs = self.MLP(x)
        # Instantiate the Model
        model = tf.keras.Model(inputs, outputs)

        return model

    def ResNet152(self):
        inputs = tf.keras.Input((self.length, self.num_channel))     # The input tensor
        stem_b = stem_bottleneck(inputs, self.num_filters)  # The Stem Convolution Group
        x = learner152(stem_b, self.num_filters)            # The learner
        outputs = self.MLP(x)
        # Instantiate the Model
        model = tf.keras.Model(inputs, outputs)

        return model

"Configurations for ResNet in Regression Mode"
length = X_train.shape[1]   # Number of Features (or length of the signal)
model_width = 128           # Number of Filter or Kernel in the Input Layer
num_channel = 1             # Number of Input Channels
problem_type = 'Regression' # Regression or Classification
output_number = 1           # Number of Outputs in the Regression Mode

Regression_Model = ResNet(length, num_channel, model_width, problem_type=problem_type, output_nums=output_number).ResNet18() # Build Model
# ResNet Models supported: ResNet18, ResNet34, ResNet50, ResNet101, ResNet152, 
Regression_Model.compile(loss=tf.keras.losses.MeanAbsoluteError(), optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),  metrics=tf.keras.metrics.MeanSquaredError()) # Compile Model
# Here, Model validation metric is set as Mean Squared Error or MSE

Regression_Model.summary() # Summary of the Model

# Early Stopping and Model_Checkpoints are optional parameters
# Early Stopping is to stop the training based on certain condition set by the user
# Model Checkpoint is to save a model in a directory based on certain conditions so that it can be used later for Transfer Learning or avoiding retraining
Dir = '.\\Memoria\\best_only_ResNet\\model-ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5'
callbacks = [EarlyStopping(monitor='val_loss', patience=30, mode='min'), ModelCheckpoint(Dir, verbose=1, monitor='val_loss', save_best_only=True, mode='min')]
history_4 = Regression_Model.fit(X_train, train_y, epochs=200, batch_size=128, verbose=1, validation_split=0.1, shuffle=True, callbacks=callbacks)  ##128
# Save 'History' of the model for model performance analysis performed later