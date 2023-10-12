import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('titanic_800.csv', sep=',', header=0)

data.drop('Name', axis=1, inplace= True)
data.drop('PassengerId', axis=1, inplace= True)
data.drop('Ticket', axis=1, inplace= True)
data.drop('Cabin', axis=1, inplace= True)

# Handle missing values
data["Survived"].fillna(1, inplace=True)
data["Pclass"].fillna(3, inplace=True)
data["Sex"].fillna("female", inplace=True)
data["Age"].fillna(29.87, inplace=True)
data["SibSp"].fillna(0.51875, inplace=True)
data["Parch"].fillna(0.37375, inplace=True)
data["Fare"].fillna(4284.72009825, inplace=True)
data["Embarked"].fillna(0, inplace=True)

# Encode categorical variables (Sex and Embarked)

# Select features and target
X = data[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]
y = data["Survived"]

yvalues = pd.DataFrame( dict ( Survived =[]), dtype = int )
yvalues[ "Survived" ] = data [ "Survived" ].copy()

data.drop( 'Survived' , axis = 1 , inplace = True )

xtrain = data.head( 800 )
xtest = data.tail( 160 )

ytrain = yvalues.head( 800 )
ytest = yvalues.tail( 160 )

xtrain['Sex'] = xtrain['Sex'].replace(['female'],1.0 )
xtrain['Sex'] = xtrain['Sex'].replace(['male'],0 )

xtrain['Embarked'] = xtrain['Embarked'].replace(['S'],0 )
xtrain['Embarked'] = xtrain['Embarked'].replace(['C'],1.0 )
xtrain['Embarked'] = xtrain['Embarked'].replace(['Q'],2.0 )

xtest['Sex'] = xtrain['Sex'].replace(['female'],1.0 )
xtest['Sex'] = xtrain['Sex'].replace(['male'],0 )

xtest['Embarked'] = xtrain['Embarked'].replace(['S'],0 )
xtest['Embarked'] = xtrain['Embarked'].replace(['C'],1.0 )
xtest['Embarked'] = xtrain['Embarked'].replace(['Q'],2.0 )

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.10)

scaler = StandardScaler()
scaler.fit(xtrain)
xtrain = scaler.transform(xtrain)
xtest = scaler.transform(xtest)

mlp = MLPClassifier( hidden_layer_sizes =(9,7,5,3), max_iter = 1000 ,random_state = 1)

mlp.fit(xtrain,ytrain.values.ravel())

predictions = mlp.predict(xtest)

matrix = confusion_matrix(ytest,predictions)
print (matrix)
print (classification_report(ytest,predictions))

depth = [];

for i in range(1,7):
    clf_tree = DecisionTreeClassifier(criterion="entropy", random_state = 100, max_depth = i)
    clf_tree.fit(xtrain,ytrain.values.ravel())
    yhat = clf_tree.predict(xtest)
    depth.append(accuracy_score(ytest,yhat))
    print("For max depth = ",i, " : ",accuracy_score(ytest,yhat))


clf_tree = DecisionTreeClassifier(criterion="entropy", random_state = 100, max_depth = 5)
clf_tree.fit(xtrain,ytrain.values.ravel())
yhat = clf_tree.predict(xtest)

print (classification_report(ytest,yhat))
