import pandas as pd

print("Loading LearnLift dataset...")

df = pd.read_csv("data/learnlift_dataset.csv")

print("Original shape:", df.shape)

# Features for dropout prediction
features = [
    "gender",
    "region",
    "highest_education",
    "age_band",
    "imd_band",
    "num_of_prev_attempts",
    "studied_credits",
    "disability",
    "average_assessment_score",
    "assessment_count",
    "total_clicks",
    "active_days",
    "average_clicks_per_day"
]

# Target
target = "dropout"

# Create clean dataset
dropout_df = df[features + [target]].copy()

# Save
dropout_df.to_csv(
    "data/dropout_dataset.csv",
    index=False
)

print("Dropout dataset created!")
print("Shape:", dropout_df.shape)

print("\nColumns:")
print(dropout_df.columns.tolist())

print("\nFirst 5 rows:")
print(dropout_df.head())

print("\nSaved to:")
print("data/dropout_dataset.csv")