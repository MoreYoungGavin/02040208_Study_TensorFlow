import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.contrib import learn,layers

N = 10000
weight = np.random.randn(N) * 5 + 70
spec_id = np.random.randint(0, 3, N)
bias = [0.9, 1, 1.1]
height = np.array([weight[i] / 100 + bias[b] for i, b in enumerate(spec_id)])
spec_name = ['Goblin', 'Human', 'ManBears']
spec = [spec_name[s] for s in spec_id]

def input_fn(df):
    feature_cols = {}
    feature_cols['Weight'] = tf.constant(df['Weight'].values)
    feature_cols['Species'] = tf.SparseTensor(indices=[[i, 0] for i in range(df['Species'].size)],values=df['Species'].values,dense_shape=[df['Species'].size, 1])
    labels = tf.constant(df['Height'].values)
    return feature_cols, labels
df = pd.DataFrame({'Species':spec,'Weight':weight,'Height':height})
Weight = layers.real_valued_column("Weight")
Species = layers.sparse_column_with_keys(column_name="Species", keys=['Goblin','Human','ManBears'])
reg = learn.LinearRegressor(feature_columns=[Weight,Species])
reg.fit(input_fn=lambda:input_fn(df), steps=50000)

w_w = reg.get_variable_value('linear/Weight/weight')
print('Estimation for Weight: {}'.format(w_w))
s_w = reg.get_variable_value('linear/Species/weights')
b = reg.get_variable_value('linear/bias_weight')
print('Estimation for Species: {}'.format(s_w + b))


