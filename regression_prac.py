import numpy as np
import pandas as pd
import statsmodels.formula.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import re
from sklearn import preprocessing

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

# csv 파일을 가져옴
df= pd.read_csv("/Users/yoon/Documents/data/prev_count_data.csv")

### 데이터 전처리

for col in df.columns:
    if 'Unnamed' in col:
        del df[col]
df = df.drop('label', 1)
df = df.drop('buyCountAtFirst', 1)
df = df.drop('marketing_text', 1)

# 문자열에서 숫자만 추출
for idx, mystr in enumerate(df['discount']): ## good, 노말라이즈만 ㄱ
    df['discount'][idx] = re.sub('[^0-9]', '', mystr)

for idx, mystr in enumerate(df['price']): ## good, 노말라이즈만 ㄱ
    df['price'][idx] = re.sub('[^0-9]', '', mystr)

for idx, mystr in enumerate(df['buyCount']): ## y값!
    df['buyCount'][idx] = re.sub('[^0-9]', '', mystr)

for idx, mystr in enumerate(df['timer']):
    try:
        newTimer = re.sub('[^0-9]', '', mystr)
        if len(newTimer) > 2:
            df['timer'][idx] = 0.5
        else:
            df['timer'][idx] = newTimer
    except:
        pass

df = df.dropna()

min_max_scaler = preprocessing.MinMaxScaler()

df['price'] = pd.to_numeric(min_max_scaler.fit_transform(df['price']))

df['discount'] = pd.to_numeric(min_max_scaler.fit_transform(df['discount']))

df['timer'] = pd.to_numeric(min_max_scaler.fit_transform(df['timer']))

list = df['price'].tolist()
x = np.array(list, dtype='|S4')
x1 = x.astype(np.float)

list = df['discount'].tolist()
x = np.array(list, dtype='|S4')
x2 = x.astype(np.float)

list = df['timer'].tolist()
x = np.array(list, dtype='|S4')
x3 = x.astype(np.float)

y = pd.to_numeric(df['buyCount'], errors='coerce').tolist()

### 데이터 전처리
#####################

# df = pd.DataFrame({"A": y, "B": x1, "C": x2, "D": x3})
# result = sm.ols(formula="A ~ B + C + D", data=df).fit()
#
# print (result.params.tolist())
# print (result.summary())
#
# # 회귀계수에 대한 P,T-value 출력
# print('Pvalue :', result.pvalues.tolist())
# print('Tvalue :', result.tvalues.tolist())
# print ('index :', result.pvalues.tolist().index(max(result.pvalues.tolist())))
# print ('index :', result.tvalues.tolist().index(max(result.tvalues.tolist())))

# P가 높으면서 T가 낮은 변수 제거하는 알고리즘 넣기

# 여기까지의 결과로 변수 제거

x_data = []
for index, row in df.iterrows():
    x_data.append([row['price'], row['discount'], row['timer']])

y_data = []
for index, row in df.iterrows():
    y_data.append([pd.to_numeric(row['buyCount'], errors='coerce')])

# placeholders for a tensor that will be always fed.
X = tf.placeholder(tf.float32, shape=[None, 3])
Y = tf.placeholder(tf.float32, shape=[None, 1])

W = tf.Variable(tf.random_normal([3, 1]), name='weight')
b = tf.Variable(tf.random_normal([1]), name='bias')

# Hypothesis
hypothesis = tf.matmul(X, W) + b

# Simplified cost/loss function
cost = tf.reduce_mean(tf.square(hypothesis - Y))

# Minimize
optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-5)
train = optimizer.minimize(cost)

# Launch the graph in a session.
sess = tf.Session()
# Initializes global variables in the graph.
sess.run(tf.global_variables_initializer())

for step in range(2001):
    cost_val, hy_val, W_val, b_val, _ = sess.run(
        [cost, hypothesis, W, b, train], feed_dict={X: x_data, Y: y_data})
    if step % 10 == 0:
        print(step, "Cost: ", cost_val, "\nPrediction:\n", hy_val, "\nW value:\n", W_val, "\nb value:\n", b_val)

## W_val에서 가장 큰값을 가지는 인덱스(변수) 추출하고, 모델 식 저장. --> DB Model
pred = sess.run(hypothesis, feed_dict={X: [[0.009433063363506432, 0.25, 0.10982658959537572]]}) ## 예측하는 방법
print (pred)
# 모델 식은 그냥 W,b 이용해서 수학식 저장.