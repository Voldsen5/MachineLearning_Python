import pandas as pd

data = pd.read_csv('titanic_800.csv')

average_age = data['Age'].mean()
average_sibSp = data['SibSp'].mean()
average_parch = data['Parch'].mean()
average_fare = data['Fare'].mean()

print(f'Average Age: {average_age}')
print(f'Average sibSp: {average_sibSp}')
print(f'Average Parch: {average_parch}')
print(f'Average fare: {average_fare}')