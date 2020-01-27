import pandas as pd
import numpy as np
from sklearn.svm import LinearSVC
from sklearn import preprocessing
from sklearn.metrics import accuracy_score

df = pd.read_csv('mltesting.csv')
lab_enc = preprocessing.LabelEncoder()

x = df.drop(columns=['user_rating','movieId'],axis=1)
y = df['user_rating']
y = lab_enc.fit_transform(y)
y = y.astype('int')
train_x = x.iloc[:50]
train_y = y[:50]
test_x = x.iloc[50:]
test_y = y[50:]
gnb = LinearSVC()
gnb.fit(train_x, train_y)
predict_test = gnb.predict(test_x)
accuracy_test = accuracy_score(test_y,predict_test)
for i,j in zip(np.array(test_y),predict_test):
    print(i,j)
print('accuracy_score on train dataset : ' ,accuracy_test)
