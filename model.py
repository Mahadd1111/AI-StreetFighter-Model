from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
scaler = StandardScaler()
import pickle
import time

df = pd.read_csv("dataset_1.csv")
df = df.drop(['result'],axis=1)
df = df.astype(int)
df.head()

df = df.drop(['timer','round_over','p1btnA','p1btnB','p1btnR','p1btnL','p1btnY','p1btnX','p1btnLeft','p1btnRight','p1btnUp','p1btnDown'],axis=1)

# Feature Standardization
df['p1_hp'] = scaler.fit_transform(df['p1_hp'].values.reshape(-1,1))
df['p2_hp'] = scaler.fit_transform(df['p2_hp'].values.reshape(-1,1))
df['p1_xc'] = scaler.fit_transform(df['p1_xc'].values.reshape(-1,1))
df['p2_xc'] = scaler.fit_transform(df['p2_xc'].values.reshape(-1,1))
df['p1_yc'] = scaler.fit_transform(df['p1_yc'].values.reshape(-1,1))
df['p2_yc'] = scaler.fit_transform(df['p2_yc'].values.reshape(-1,1))

X= df.drop(['p2btnA','p2btnB','p2btnR','p2btnL','p2btnY','p2btnX','p2btnLeft','p2btnRight','p2btnUp','p2btnDown'],axis=1)
y = df[['p2btnA','p2btnB','p2btnR','p2btnL','p2btnY','p2btnX','p2btnLeft','p2btnRight','p2btnUp','p2btnDown']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# create an instance of the decision tree classifier
dtc =  DecisionTreeClassifier()

# train the model on the training data
dtc.fit(X_train, y_train)
dtc.feature_names_ = None
# make predictions on the test data
y_pred =dtc.predict(X_test)

# Calculate the mean squared error on the test set
mse = mean_squared_error(y_test, y_pred)
print("Mean squared error: {:.2f}".format(mse))
score = r2_score(y_test, y_pred)
print(f"R^2 score: {score:.3f}")

# Saving Model to Pickle File
with open('model2.pkl','wb') as f:
    pickle.dump(dtc,f)

start_time = time.time()
new_data=np.array([7,0.84,0.21,0.28,1,33686532,0,1,8,-0.75416,-1.535241,0.41569,1,515,0,0])
new_data = new_data.reshape(1,-1)
temp2 = dtc.predict(new_data)
end_time = time.time()
print(temp2)
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time, "seconds")

