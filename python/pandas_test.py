'''
doing some examples with pandas and numpy
'''

import numpy as np
import pandas as pd

# creating series
s = pd.Series(['hello', np.nan, 15, 36, 3])

print(s)
print(s[3])

# dataframe from list of lists
data = [['a', 'b', 'c'],
        ['d', 'e', 'f'],
        ['g', 'h', 'i']]

df1 = pd.DataFrame(data)
print(df1)

# dataframe from np array
array = np.array([['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']])

columns = ['X', 'Y', 'Z']
index = [1, 2, 3]

df2 = pd.DataFrame(array, index, columns)
print(df2)

# iterate over rows
row = df2.iloc[1]
length = row.size
for i in range(length):
    print(row[i])

# import .csv (table notification) 
try: 
    df3 = pd.read_csv("data.csv")
except:
    pass

# dataframe shape
shape = df2.shape
print('\nDataFrame Shape :', shape)
print('\nNumber of rows :', shape[0])
print('\nNumber of columns :', shape[1])

# create excel-sheet from dataframe 
df4 = pd.DataFrame({'name': ['a', 'b', 'c', 'd'],
     'a': [1, 2, 3, 4],
     'b': [5, 6, 7, 8],
     'c': [9, 10, 11, 12]})

# create excel writer object
wr = pd.ExcelWriter('output.xlsx')
# write dataframe to excel
df4.to_excel(wr)
# save the excel
wr.save()
print('DataFrame is written successfully to Excel File.')