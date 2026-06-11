import pandas as pd

df = pd.read_csv('../week2_pandas/train.csv')
pd.set_option('display.max_columns', None)
# print(df)
print(df.groupby('Sex')['Survived'].mean())
print(df.groupby('Pclass')['Survived'].mean())
print(df.groupby('Sex')['Survived'].count())
print(df.groupby('Pclass')['Survived'].count())
print(df.groupby('Embarked')['Survived'].mean())
print(df.groupby('Embarked')['Survived'].count())
print(df.groupby(['Sex', 'Pclass'])['Survived'].mean())

# 今日发现:
# 1. 女性存活率74%,男性19%,差距约4倍 → 妇女优先是真实存在的
# 2. 头等舱存活率63%,二等舱47%,三等舱24%，头等舱是三等舱的2.6倍,说明了逃生机会和社会阶层高度相关
# 3. 三等舱乘客基数最大(491人,占全船55%),但存活率仅24%为三档最低,死亡人数远超其他舱位——灾难的代价主要由底层乘客承担。
