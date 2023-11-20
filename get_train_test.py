import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv("./data/processed_data.csv")

train_idx = np.random.choice(len(df), int(0.8 * len(df)), replace=False)

train_data = df.iloc[train_idx]
test_data = df.drop(train_idx)

train_data.reset_index(drop=True, inplace=True)
test_data.reset_index(drop=True, inplace=True)

if 'Unnamed: 0' in train_data.columns:  train_data = train_data.drop('Unnamed: 0', axis=1)
if 'Unnamed: 0' in test_data.columns:   test_data = test_data.drop('Unnamed: 0', axis=1)

print(train_data)
print(test_data)

train_data.to_csv("./data/train_data.csv")
test_data.to_csv("./data/test_data.csv")