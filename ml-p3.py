import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neural_network import MLPClassifier

# 1. Read dataset

df = pd.read_csv("Churn_Modelling.csv")

# 2. Features and target

X = df.drop(columns=["RowNumber", "CustomerId", "Surname", "Exited"])
y = df["Exited"]

X = pd.get_dummies(X, columns=["Geography", "Gender"], drop_first=True)

# 3. Split and normalize data

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 4. Build and train neural network

model = MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=300,
                      early_stopping=True, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# 5. Improved model

model2 = MLPClassifier(hidden_layer_sizes=(64, 32, 16),
                       alpha=0.001, max_iter=500,
                       early_stopping=True, random_state=42)

model2.fit(X_train, y_train)
y_pred2 = model2.predict(X_test)

print("\nImproved Accuracy:", accuracy_score(y_test, y_pred2))
print("Improved Confusion Matrix:\n", confusion_matrix(y_test, y_pred2))