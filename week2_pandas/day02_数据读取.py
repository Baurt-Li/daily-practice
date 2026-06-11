import pandas as pd

df = pd.read_csv('./train.csv')
print(df.shape)
print(df.head())
print(df.info())
print(df.describe())
surviver = df['Survived'].sum()
print(surviver)