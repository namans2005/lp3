import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# ------------------------------------------
# 1. Load dataset
# ------------------------------------------
df = pd.read_csv(r"emails.csv")
print(df.head())

# ------------------------------------------
# 2. Preprocess data
# ------------------------------------------
df.dropna(inplace=True)

X = df.drop(columns=["Prediction", "Email No."], errors="ignore")
y = df["Prediction"]

# ------------------------------------------
# 3. Split data
# ------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# ------------------------------------------
# 4. Scale features
# ------------------------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# ------------------------------------------
# 5. Train KNN and SVM
# ------------------------------------------
models = {
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "SVM": SVC(kernel="linear")
}
results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred, zero_division=0),
        "F1 Score": f1_score(y_test, y_pred, zero_division=0)
    })
    
    print("\n", name)
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ------------------------------------------
# 6. Compare performance
# ------------------------------------------
print("\nModel Comparison:")
print(pd.DataFrame(results).round(4))

pd.DataFrame(results).plot(kind="bar")
plt.title("KNN vs SVM")
plt.show()
