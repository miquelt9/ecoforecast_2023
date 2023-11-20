# -*- coding: utf-8 -*-
"""EcoChallenge.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ROKeqyYTzW2muFEA1-dAsgBHwFxoVSh8

#Problem Statement

➡️ Context:

With increasing digitalisation and the ever-growing reliance on data servers, the significance of sustainable computing is on the rise. Schneider Electric, a pioneer in digital transformation and energy management, brings you this innovative challenge to play your part in reducing the carbon footprint of the computing industry.

The task is simple, yet the implications are profound. We aim to predict which European country will have the highest surplus of green energy in the next hour. This information will be critical in making important decisions, such as optimizing computing tasks to use green energy effectively and, consequently, reducing CO2 emissions.
🎯 Objective:

Your goal is to create a model capable of predicting the country (from a list of nine) that will have the most surplus of green energy in the next hour. For this task, you need to consider both the energy generation from renewable sources (wind, solar, geothermic, etc.), and the load (energy consumption). The surplus of green energy is considered to be the difference between the generated green energy and the consumed energy.

The countries to focus on are: Spain, UK, Germany, Denmark, Sweden, Hungary, Italy, Poland, and the Netherlands.

The solution must not only align with Schneider Electric's ethos but also go beyond its current offerings, presenting an unprecedented approach.

#Dependencies imports and data treatment

0️⃣ - First of all we have to make sure our libraries are installed:
"""

pip install pandas numpy keras tensorflow

"""1️⃣ - 📚 Import the libraries we will use for creating the model and load the training data file"""

# Import libraries
## Basic libs
import pandas as pd
import numpy as np
import warnings
## Data Visualization
import seaborn as sns
import matplotlib.pyplot as plt

# Configure libraries
warnings.filterwarnings('ignore')
plt.rcParams['figure.figsize'] = (10, 10)
plt.style.use('seaborn')


# Load dataset
df_bank = pd.read_csv('https://raw.githubusercontent.com/miquelt9/ecoforecast_2023/main/data/train_data.csv')

"""2️⃣ - ✨ Get the data ready

Plot the data so we can get some thoughs about how to properly train the model.
"""

import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO

df_plot = df_bank.copy()

df_plot['Datetime'] = pd.to_datetime(df_plot['Datetime'])

# Extract date part from the datetime and set it as a new column 'Date'
df_plot['Date'] = df_plot['Datetime'].dt.date

# Group by 'Date' and calculate the mean of each day
daily_mean = df_plot.groupby('Date').mean()



plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

# Iterate through columns (excluding non-numeric columns like country_code and country_num)
for col in ['load_HU', 'load_IT', 'load_PO', 'load_SP', 'load_UK', 'load_DE', 'load_DK', 'load_SE', 'load_NE']:
    plt.plot(daily_mean.index, daily_mean[col], label=col)  # Plot each column as a line

plt.xlabel('Date')
plt.ylabel('Load (MAW)')
plt.title('Load per day')
plt.legend(loc='upper right')  # Show legend
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()

# Show the plot
plt.show()

plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

for col in  ['gen_green_HU', 'gen_green_IT', 'gen_green_PO', 'gen_green_SP', 'gen_green_UK', 'gen_green_DE', 'gen_green_DK', 'gen_green_SE', 'gen_green_NE']:
      plt.plot(daily_mean.index, daily_mean[col], label=col)  # Plot each column as a line

plt.xlabel('Date')
plt.ylabel('Green Gen (MAW)')
plt.title('Green generation per day')
plt.legend(loc='upper right')  # Show legend
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()

# Show the plot
plt.show()


plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

for col_l, col_g in  zip(['load_HU', 'load_IT', 'load_PO', 'load_SP', 'load_UK', 'load_DE', 'load_DK', 'load_SE', 'load_NE'], ['gen_green_HU', 'gen_green_IT', 'gen_green_PO', 'gen_green_SP', 'gen_green_UK', 'gen_green_DE', 'gen_green_DK', 'gen_green_SE', 'gen_green_NE']):
  plt.plot(daily_mean.index, daily_mean[col_g] - daily_mean[col_l], label="surplus_"+col[-2:])  # Plot each column as a line

plt.xlabel('Date')
plt.ylabel('Surplus (MAW)')
plt.title('Surplus of Green Energy per day')
plt.legend(loc='upper right')  # Show legend
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()

# Show the plot
plt.show()

"""We can clearly see that DE is the main country in our list that is responsible for the green energy surplus, that why we'll consider later to add some synthetic datapoints on the train and test data, so the model can also learn that is not the same country the one that is doing the best but it depends on the values, and therefore it will be able to display any country as a result."""

from sklearn.preprocessing import StandardScaler
import pandas as pd

# Copying original dataframe
df_bank_ready = df_bank.copy()

df_bank_ready = df_bank_ready.drop('country_code', axis=1)
if 'Unnamed: 0' in df_bank_ready.columns:  df_bank_ready = df_bank_ready.drop('Unnamed: 0', axis=1)
df_bank_ready['Datetime'] = pd.to_datetime(df_bank_ready['Datetime'])
df_bank_ready['Datetime'] = df_bank_ready['Datetime'].dt.strftime('%s').astype(float)

print('Shape of dataframe:', df_bank_ready.shape)
df_bank_ready.head()

df_bank_ready['country_num'].value_counts()
df_bank_ready = df_bank_ready.drop('country_num', axis=1)

"""🖖 Splitting data for training and testing"""

# Select Features
features = df_bank_ready['Datetime']

# Select Target
labels = df_bank_ready.drop('Datetime', axis=1)

n_features = features.shape[0]
m = df_bank_ready.shape[0]
X = np.array(features).reshape(m,1)
y = np.array(labels).astype(float)

print("number of datapoints:",m)
print("the shape of the feature matrix is: ",X.shape)
print('the shape of the label vector is: ',y.shape)

"""💾 Save the prepared data"""

from joblib import dump, load
from sklearn.model_selection import train_test_split

# Saving model and loading model
if 'features' in globals():
  dump(features, 'features.data')
  dump(labels, 'labels.data')
else:
  features = load('features.data')
  labels = load('labels.data')

n_features = features.shape[0]
m = df_bank_ready.shape[0]
X = np.array(features).reshape(m,1)
y = np.array(labels).astype(float)

"""# Model Training

### Auxiliar functions import
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np # import numpy package under shorthand "np"
import pandas as pd # import pandas package under shorthand "pd"
import matplotlib.pyplot as plt
from numpy.testing import assert_array_equal
# Polynomial Regression import
# %config Completer.use_jedi = False # enable code auto-completion
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
# Random Forest Regressor import
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

"""4️⃣ - Building the clasification models

##Polynomial regression 🎢

Training the model and getting results
"""

X = np.array(features).reshape(m,1)
y = np.array(labels).astype(float)

## define a list of values for polynomial degrees
degrees = [2, 3, 5, 7, 10]

# declare a variable to store the resulting training errors for each polynomial␣
tr_errors = []

print(X.shape)
print(y.shape)

for i in range(len(degrees)): # use for-loop to fit polynomial regression␣
  print("Polynomial degree = ",degrees[i])
  poly = PolynomialFeatures(degree=degrees[i])
  X_poly = poly.fit_transform(X)
  lin_regr = LinearRegression()
  lin_regr.fit(X_poly,y)
  y_pred = lin_regr.predict(X_poly)
  tr_error = mean_squared_error(y, y_pred)
  r_squared = r2_score(y, y_pred)
  # print("The first two rows of X_poly: \n",X_poly[0:2])
  # print("\nThe learned weights: \n",lin_regr.coef_)
  tr_errors.append(tr_error)
  X_fit = np.linspace(-25, 25, 100) # generate samples

  plt.plot(X, lin_regr.predict(X_poly), 'r', label="Model")
  # plt.scatter(X, y, color="b", label="datapoints") # plot a scatter plot
  plt.xlabel('Year-Trimester') # set the label for the x/y-axis
  plt.ylabel('Average Rent')
  plt.legend(loc="best") # set the location of the legend
  plt.title('Polynomial degree = {}\nTraining error = {:.5}\nR squared = {:.5}'.format(degrees[i], tr_error, r_squared)) # set the title
  plt.show() # show the plot

"""##Random Forest 🌲🌲🌲

Training the model
"""

X = np.array(features).reshape(m,1)
y = np.array(labels).astype(float)
print(X.shape)
print(y.shape)

#y = np.array(labels).astype(float) # convert a list of len=m to a ndarray
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=2)
# Create the parameter grid for GridSearchCV
rf_param_grid = {
'max_depth': [5, 10, 20, 30, 50], # Maximum number of levels in each decision tree
'max_features': [2, 3], # Maximum number of features considered for␣
'min_samples_leaf': [1, 2, 3], # Minimum number of data points allowed in a␣
'n_estimators': [100, 300] # Number of trees in the forest
}
rf_reg = RandomForestRegressor(random_state = 42)
# Setup grid search
rf_grid = GridSearchCV(estimator = rf_reg, param_grid = rf_param_grid, cv=3, verbose=2)

rf_grid.fit(X_train, y_train)
print(pd.concat([pd.DataFrame(rf_grid.cv_results_["params"]),pd.DataFrame(rf_grid.cv_results_["mean_test_score"], columns=["Accuracy"])],axis=1))

"""Plotting results"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
results_grid = pd.concat([pd.DataFrame(rf_grid.cv_results_["params"]),pd.DataFrame(rf_grid.cv_results_["mean_test_score"], columns=["Accuracy"])],axis=1)
# print(results_grid)
pivot_results_grid = results_grid.pivot_table(index='max_depth', columns=['max_features', 'min_samples_leaf', 'n_estimators'], values='Accuracy')
# Create a heatmap with a different colormap and color scale
plt.figure(figsize=(10, 4))
sns.heatmap(pivot_results_grid, annot=True, cmap='viridis', fmt='.3f', cbar=True, center=0.9)
plt.title('Accuracy Heatmap for Different Parameter Combinations')
plt.xlabel('max_features, min_samples_leaf, n_estimators')
plt.ylabel('max_depth')
plt.show()

"""Choosing bests params"""

rf_best = rf_grid.best_estimator_
y_pred_test = rf_best.predict(X_test)
print("Best Parameters:")
print(rf_grid.best_params_)
# Calculate performance metrics
rf_dict = {'Model':'Random Forest Regressor',
'R^2':r2_score(y_test, y_pred_test),
'Adjusted R^2':(1 - (1-r2_score(y_test, y_pred_test))*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1))}
# Display model performance metrics
rf_reg_metrics = pd.DataFrame.from_dict(rf_dict, orient = 'index').T
rf_reg_metrics

"""💾 Save the models"""

from joblib import dump, load
import os

## SELECT PARAMS BASED ON PREVIOUS OBSERVATIONS ##
# Polynomial regerssion model
polynomial_degree = 3
# Random Forest Regressor
max_depth = 50
max_features = 2
min_samples_leaf = 1
n_estimators = 300

poly = PolynomialFeatures(polynomial_degree)
X_poly = poly.fit_transform(X)
plr = LinearRegression()
plr.fit(X_poly,y)

clf = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, max_features=max_features, min_samples_leaf=min_samples_leaf)
clf.fit(X_train, y_train)

if not os.path.exists("./models/"):
  os.makedirs("./models/")

# Saving model
dump(plr, './models/polynomial_regression_predictor.joblib')
dump(clf, './models/randomTree_regressor_predictor.joblib')

"""#Solution generation

Load models:
"""

# Loading model
plr = load('./models/polynomial_regression_predictor.joblib')
clf = load('./models/randomTree_regressor_predictor.joblib')

"""Load testing file:"""

from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn import utils

# Load dataset
df_bank_test = pd.read_csv('https://raw.githubusercontent.com/miquelt9/ecoforecast_2023/main/data/test_data.csv')

df_correct = df_bank_test['country_num'].astype(int)
df_bank_test['Datetime'] = pd.to_datetime(df_bank_test['Datetime'])
df_bank_test['Datetime'] = df_bank_test['Datetime'].dt.strftime('%s').astype(float)
df_bank_test = df_bank_test['Datetime']

# Select Features
test_feature = df_bank_test
m_test = df_bank_test.shape[0]
test_feature = np.array(test_feature).reshape(m_test,1)

print('Shape of dataframe:', df_bank_test.shape)
df_bank_test.head()

def evalute_result(df_predicted):
  accuracy = (df_correct == df_predicted).sum() / len(df_correct)
  precision = (df_correct & df_predicted).sum() / df_correct.sum()
  recall = (df_correct & df_predicted).sum() / df_predicted.sum()
  f1 = 2 * precision * recall / (precision + recall)
  return {'acc': accuracy, 'prec': precision, 'rec': recall, 'f1': f1}

def most_surplus(l_sp, g_sp, l_uk, g_uk, l_de, g_de, l_dk, g_dk, l_hu, g_hu, l_se, g_se, l_it, g_it, l_po, g_po, l_nl, g_nl):
    diffs = {}
    diffs['sp'] = g_sp - l_sp
    diffs['uk'] = g_uk - l_uk
    diffs['de'] = g_de - l_de
    diffs['dk'] = g_dk - l_dk
    diffs['hu'] = g_hu - l_hu
    diffs['se'] = g_se - l_se
    diffs['it'] = g_it - l_it
    diffs['po'] = g_po - l_po
    diffs['nl'] = g_nl - l_nl
    max_diff = max(diffs, key=diffs.get)
    # max_diff_value = diffs[max_diff]
    # print(diffs)
    # print(max_diff)
    return str(max_diff).upper()

def get_country_number(cc):
     return int(country_codes[cc])

country_codes = {
    "ES": 0,
    "UK": 1,
    "DE": 2,
    "DK": 3,
    "HU": 5,
    "SE": 4,
    "IT": 6,
    "PL": 7,
    "NL": 8,
}

# Given the scores seen on the plots we'll be using the random forest regressor to predict
df_bank_result = clf.predict(test_feature)

if not os.path.exists("./predictions/"):
  os.makedirs("./predictions/")

# Save new dataframe into csv file
df = pd.DataFrame(df_bank_result)
df.columns = ['load_HU', 'load_IT', 'load_PO', 'load_SP', 'load_UK', 'load_DE', 'load_DK', 'load_SE', 'load_NE', 'gen_green_HU', 'gen_green_IT', 'gen_green_PO', 'gen_green_SP', 'gen_green_UK', 'gen_green_DE', 'gen_green_DK', 'gen_green_SE', 'gen_green_NE']
df.to_csv('./predictions/energy_predictions.csv', index=False)

df = pd.read_csv(r'./predictions/energy_predictions.csv')

df['country_code'] = np.nan
df['country_num'] = np.nan
for index, row in df.iterrows():
    cc = most_surplus(row['load_SP'], row['gen_green_SP'],	row['load_UK'],	row['gen_green_UK'], row['load_DE'], row['gen_green_DE'], row['load_DK'], row['gen_green_DK'],	row['load_HU'],	row['gen_green_HU'], row['load_SE'], row['gen_green_SE'], row['load_IT'], row['gen_green_IT'], row['load_PO'], row['gen_green_PO'], row['load_NE'], row['gen_green_NE'])
    df.loc[index, 'country_code'] = cc
    df.loc[index, 'country_num'] = get_country_number(cc)

print(df.head(8))
eval = evalute_result(df['country_num'].astype(int))
# Print result
print('Accuracy:', eval['acc'])
print('Precision:', eval['prec'])
print('Recall:', eval['rec'])
print('F1 Score:', eval['f1'])

df.to_csv('./predictions/energy_predictions.csv', index=False)
predictions = df['country_num']
predictions.to_json('./predictions/predictions.json')