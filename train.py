import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# =========================
# 1. Load dataset
# =========================

print("Loading dropout dataset...")

df = pd.read_csv("data/dropout_dataset.csv")

print("Dataset shape:", df.shape)


# =========================
# 2. Separate features and target
# =========================

X = df.drop("dropout", axis=1)
y = df["dropout"]


# =========================
# 3. Feature columns
# =========================

categorical_features = [
    "gender",
    "region",
    "highest_education",
    "age_band",
    "imd_band",
    "disability"
]

numeric_features = [
    "num_of_prev_attempts",
    "studied_credits",
    "average_assessment_score",
    "assessment_count",
    "total_clicks",
    "active_days",
    "average_clicks_per_day"
]


# =========================
# 4. Preprocessing
# =========================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        ),
        (
            "numeric",
            StandardScaler(),
            numeric_features
        )
    ]
)


# =========================
# 5. Logistic Regression
# =========================

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)


# =========================
# 6. Pipeline
# =========================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# =========================
# 7. Train/Test split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# =========================
# 8. Train model
# =========================

print("\nTraining dropout model...")

pipeline.fit(X_train, y_train)


# =========================
# 9. Predictions
# =========================

y_pred = pipeline.predict(X_test)


# =========================
# 10. Evaluation
# =========================

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("DROPOUT MODEL RESULTS")
print("==============================")

print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# =========================
# 11. Save model
# =========================

joblib.dump(
    pipeline,
    "models/dropout_model.pkl"
)

print("\nModel saved successfully!")
print("Location: models/dropout_model.pkl")