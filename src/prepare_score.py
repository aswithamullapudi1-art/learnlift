import pandas as pd

print("Preparing score prediction dataset...")

# Load original student assessment data
students = pd.read_csv("data/studentInfo.csv")
assessments = pd.read_csv("data/assessments.csv")
student_assessments = pd.read_csv("data/studentAssessment.csv")

# Combine assessment scores with assessment information
merged = student_assessments.merge(
    assessments,
    on="id_assessment",
    how="left"
)

# Keep only records with an available numeric score
merged["score"] = pd.to_numeric(
    merged["score"],
    errors="coerce"
)
merged = merged.dropna(subset=["score", "date_submitted"])

# Sort assessments by student and date
merged = merged.sort_values(
    ["id_student", "code_module", "code_presentation", "date_submitted"]
)

# Use each student's earlier assessment scores to predict
# their next assessment score
merged["previous_score"] = merged.groupby(
    ["id_student", "code_module", "code_presentation"]
)["score"].transform(lambda scores: scores.shift(1))

# Keep rows that have a previous score
score_data = merged.dropna(subset=["previous_score"]).copy()

# Add student demographic information
student_features = students[
    [
        "id_student",
        "code_module",
        "code_presentation",
        "gender",
        "region",
        "highest_education",
        "age_band",
        "disability"
    ]
]

score_data = score_data.merge(
    student_features,
    on=["id_student", "code_module", "code_presentation"],
    how="left"
)

# Features available before the next assessment
features = [
    "previous_score",
    "gender",
    "region",
    "highest_education",
    "age_band",
    "disability"
]

# Target: the next assessment score
score_data = score_data[features + ["score"]].copy()

# Save dataset
score_data.to_csv(
    "data/score_dataset.csv",
    index=False
)

print("Score dataset created successfully!")
print("Shape:", score_data.shape)
print("Columns:", score_data.columns.tolist())
print("Saved to data/score_dataset.csv")