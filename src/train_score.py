import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("Loading score dataset...")

df = pd.read_csv("data/score_dataset.csv")
df = df.dropna()

print("Dataset shape:", df.shape)

# Separate input features and target
X = df.drop("score", axis=1)
y = df["score"]

# Feature types
categorical_features = [
    "gender",
    "region",
    "highest_education",
    "age_band",
    "disability"
]

numeric_features = ["previous_score"]

# Convert text columns into numbers
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)

# Create model
model = LinearRegression()

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# Train
print("\nTraining score model...")
pipeline.fit(X_train, y_train)

# Predict
predictions = pipeline.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5
r2 = r2_score(y_test, predictions)

print("\n==============================")
print("SCORE MODEL RESULTS")
print("==============================")
print(f"MAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R2:   {r2:.4f}")

# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(
    pipeline,
    "models/score_model.pkl"
)

print("\nScore model saved successfully!")
print("Location: models/score_model.pkl")