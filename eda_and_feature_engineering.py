# -*- coding: utf-8 -*-
"""eda and feature engineering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G3ch0RAFdglJO-JfFzEcEinzxkaNxcK_
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
from six.moves import urllib
from scipy.stats import normaltest
warnings.filterwarnings("ignore")
# %matplotlib inline

data = pd.read_csv('/content/Travel.csv')

data.head()

data.columns

data.info()

data.describe().T

data.shape

num_col = [feature for feature in data.columns if data[feature].dtype!='O']

cat_col = [feature for feature in data.columns if data[feature].dtype =='O']

for col in cat_col:
    print(data[col].value_counts(normalize=True) * 100)

#UA of Num Values
plt.figure(figsize=(20, 20))
for i in range(1, len(num_col)):
    plt.subplot(14, 5, i+1)
    sns.kdeplot(x=data[num_col[i]],shade=True, color='b')
    plt.xlabel(num_col[i])

data.head()

#UA of Cat Values
plt.figure(figsize=(20, 20))
cat = ['TypeofContact', 'Occupation', 'Gender', 'ProductPitched', 'MaritalStatus', 'Designation','OwnCar','Passport','ProdTaken']
for i in range(0, len(cat)):
    plt.subplot(9, 10, i+1)
    sns.countplot(x=data[cat[i]])
    plt.xlabel(cat[i])
    plt.xticks(rotation=45)
    plt.tight_layout()

data.isnull().sum()

data['Age'] = data['Age'].replace(np.nan,data['Age'].mean())
data['DurationOfPitch'] = data['DurationOfPitch'].replace(np.nan,data['DurationOfPitch'].mean())
data['NumberOfTrips'] = data['NumberOfTrips'].replace(np.nan, data['NumberOfTrips'].mean())
data['NumberOfFollowups'] = data['NumberOfFollowups'].replace(np.nan, data['NumberOfFollowups'].mean())
data['PreferredPropertyStar'] = data['PreferredPropertyStar'].replace(np.nan, data['PreferredPropertyStar'].mean())
data['NumberOfChildrenVisiting'] = data['NumberOfChildrenVisiting'].replace(np.nan,data['NumberOfChildrenVisiting'].mean())
data['MonthlyIncome'] = data['MonthlyIncome'].replace(np.nan, data['MonthlyIncome'].mean())

data.isnull().sum()

data[(list(data.columns)[1:])].corr()

#corr between variable
sns.heatmap(data.corr(),annot=True,cmap='icefire',linewidths=0.5)
fig=plt.gcf()
fig.set_size_inches(15,15)
plt.show()

fig, ax = plt.subplots(figsize=(15,10))
sns.boxplot(data=data, width= 0.5,ax=ax,  fliersize=3)

data_n = data.drop(['CustomerID'], axis=1)

data_n

fig, ax = plt.subplots(figsize=(15,10))
sns.boxplot(data=data_n, width= 0.5,ax=ax,  fliersize=3)

from sklearn.preprocessing import LabelEncoder
le_classes = LabelEncoder()
data_n['TypeofContact'] = le_classes.fit_transform(data_n['TypeofContact'])
data_n['Occupation'] = le_classes.fit_transform(data_n['Occupation'])
data_n['Gender'] = le_classes.fit_transform(data_n['Gender'])
data_n['ProductPitched'] = le_classes.fit_transform(data_n['ProductPitched'])
data_n['MaritalStatus'] = le_classes.fit_transform(data_n['MaritalStatus'])
data_n['Designation'] = le_classes.fit_transform(data_n['Designation'])

data_n

X = data_n.drop(columns = ['TypeofContact'])
y = data_n['TypeofContact']

X

y

from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor 
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, roc_auc_score

scalar = StandardScaler()
X_scaled = scalar.fit_transform(X)

vif = pd.DataFrame()
vif["vif"] = [variance_inflation_factor(X_scaled,i) for i in range(X_scaled.shape[1])]
vif["Features"] = X.columns

vif

x_train,x_test,y_train,y_test = train_test_split(X_scaled,y, test_size= 0.25, random_state = 0)

from sklearn.ensemble import RandomForestClassifier
rand_reg = RandomForestClassifier()

rand_reg.fit(x_train,y_train)

y_pred = rand_reg.predict(x_test)

accuracy = accuracy_score(y_test,y_pred)
accuracy