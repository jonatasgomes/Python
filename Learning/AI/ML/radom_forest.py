from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Creating the dataset from the table
data = {
    'Dia': list(range(1, 15)),
    'Previsao': [
        'ensolarado', 'ensolarado', 'nublado', 'chuvoso', 'chuvoso',
        'chuvoso', 'nublado', 'ensolarado', 'ensolarado', 'chuvoso',
        'ensolarado', 'nublado', 'nublado', 'chuvoso'
    ],
    'Umidade': [
        'alta', 'alta', 'alta', 'alta', 'normal',
        'normal', 'normal', 'alta', 'normal', 'normal',
        'normal', 'alta', 'normal', 'alta'
    ],
    'Vento': [
        'fraco', 'forte', 'fraco', 'fraco', 'fraco',
        'forte', 'forte', 'fraco', 'fraco', 'fraco',
        'forte', 'forte', 'fraco', 'forte'
    ],
    'Jogou?': [
        'não', 'não', 'sim', 'sim', 'sim',
        'não', 'sim', 'não', 'sim', 'sim',
        'sim', 'sim', 'sim', 'não'
    ]
}

# Converting the dataset to a DataFrame
df = pd.DataFrame(data)

# Encoding categorical variables to numerical values
label_encoders = {}
for column in ['Previsao', 'Umidade', 'Vento', 'Jogou?']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Splitting features and target variable
X = df[['Previsao', 'Umidade', 'Vento']]
y = df['Jogou?']

# Training the Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Preparing the data for prediction (day 15: chuvoso, alta, fraco)
day_15_features = pd.DataFrame({
    'Previsao': [label_encoders['Previsao'].transform(['chuvoso'])[0]],
    'Umidade': [label_encoders['Umidade'].transform(['alta'])[0]],
    'Vento': [label_encoders['Vento'].transform(['fraco'])[0]]
})

# Predicting the outcome for day 15
day_15_prediction = model.predict(day_15_features)
day_15_result = label_encoders['Jogou?'].inverse_transform(day_15_prediction)

print(day_15_result[0])  # Displaying the prediction result for day 15
