import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# ------------------------------------------
# 1. Load and preprocess data
# ------------------------------------------
# Note: Update this path to wherever your uber.csv is located
df = pd.read_csv(r"uber.csv")
print(df.head())
print(df.isnull().sum())

# Drop irrelevant columns and missing values
df.drop(columns=["Unnamed: 0", "key"], errors="ignore", inplace=True)
df.dropna(inplace=True)

# Convert datetime
# 1. Preprocessing

df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
df.dropna(subset=["pickup_datetime"], inplace=True)

def euclidean_distance(lat1, lon1, lat2, lon2):
    return 111 * np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)

df["distance"] = euclidean_distance(
    df["pickup_latitude"], df["pickup_longitude"],
    df["dropoff_latitude"], df["dropoff_longitude"]
)

df["hour"] = df["pickup_datetime"].dt.hour
df["month"] = df["pickup_datetime"].dt.month
df["year"] = df["pickup_datetime"].dt.year
df.drop(columns=["pickup_datetime"], inplace=True)

df = df[
    (df["fare_amount"] > 0) & (df["distance"] > 0) &
    (df["passenger_count"].between(1, 6)) &
    (df["pickup_latitude"].between(-90, 90)) &
    (df["dropoff_latitude"].between(-90, 90)) &
    (df["pickup_longitude"].between(-180, 180)) &
    (df["dropoff_longitude"].between(-180, 180))
    ].copy()


# 2. Outlier Detection

sns.boxplot(x=df["fare_amount"])
plt.title("Fare Before Outlier Removal")
plt.show()

rows_before = len(df)

for col in ["fare_amount", "distance"]:
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    df = df[df[col].between(q1 - 1.5*iqr, q3 + 1.5*iqr)]

print("Outliers removed:", rows_before - len(df))

sns.boxplot(x=df["fare_amount"])
plt.title("Fare After Outlier Removal")
plt.show()


# 3. Correlation Analysis

cols = ["fare_amount", "distance", "passenger_count", "hour", "month", "year"]

sns.heatmap(df[cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

print(df[cols].corr()["fare_amount"].sort_values(ascending=False))


# 4. Train-Test Split

X = df.drop(columns=["fare_amount"])
y = df["fare_amount"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# 5. Model Training and Evaluation

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
}

results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    results.append([
        name,
        r2_score(y_test, pred),
        np.sqrt(mean_squared_error(y_test, pred)),
        mean_absolute_error(y_test, pred)
    ])


# 6. Model Comparison

print("\nModel Comparison:")
print(pd.DataFrame(results, columns=["Model", "R2 Score", "RMSE", "MAE"]).round(4))