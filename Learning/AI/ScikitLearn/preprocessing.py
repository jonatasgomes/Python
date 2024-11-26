from sklearn.datasets import load_wine
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer, KNNImputer

data = load_wine()
x = data.data
y = data.target

df = pd.DataFrame(x, columns=data.feature_names)
df['target'] = y

print(df.head())

std_scaler = StandardScaler()
x_std = std_scaler.fit_transform(x)

min_max_scaler = MinMaxScaler()
x_min_max = min_max_scaler.fit_transform(x)

df_std = pd.DataFrame(x_std, columns=data.feature_names)
print(df_std.head())

df_min_max = pd.DataFrame(x_min_max, columns=data.feature_names)
print(df_min_max.head())

x_missing = df.copy()
x_missing.loc[0:4, 'alcohol'] = np.nan
x_missing.loc[0:2, 'malic_acid'] = np.nan

x_features = x_missing.drop('target', axis=1)
y_target = x_missing['target']

simple_imputer = SimpleImputer(strategy='mean')
x_simple_imputed = simple_imputer.fit_transform(x_features)

knn_imputer = KNNImputer(n_neighbors=5)
x_knn_imputed = knn_imputer.fit_transform(x_features)

df_simple_imputed = pd.DataFrame(x_simple_imputed, columns=x_features.columns)
df_simple_imputed['target'] = y_target.values
df_knn_imputed = pd.DataFrame(x_knn_imputed, columns=x_features.columns)
df_knn_imputed['target'] = y_target.values

print(df_simple_imputed.head())
print(df_knn_imputed.head())
