import pandas as pd
import os

print("=" * 60)
print("LEARNLIFT DATASET CREATION")
print("=" * 60)

# ============================================================
# STEP 1 — Load Student Information
# ============================================================

print("\nSTEP 1 — Loading student information...")

student_info = pd.read_csv(
    "data/studentInfo.csv"
)

print("Student info:", student_info.shape)

# ============================================================
# STEP 2 — Load Assessment Data
# ============================================================

print("\nSTEP 2 — Loading assessment data...")

student_assessment = pd.read_csv(
    "data/studentAssessment.csv"
)

assessments = pd.read_csv(
    "data/assessments.csv"
)

print("Student assessment:", student_assessment.shape)
print("Assessments:", assessments.shape)

# ============================================================
# STEP 3 — Convert Assessment Score to Numeric
# ============================================================

print("\nSTEP 3 — Converting assessment scores...")

student_assessment["score"] = pd.to_numeric(
    student_assessment["score"],
    errors="coerce"
)

# ============================================================
# STEP 4 — Merge Assessment Information
# ============================================================

print("\nSTEP 4 — Merging assessment information...")

student_assessment = student_assessment.merge(
    assessments[
        [
            "id_assessment",
            "code_module",
            "code_presentation"
        ]
    ],
    on="id_assessment",
    how="left"
)

print(
    "Merged assessment data:",
    student_assessment.shape
)

# ============================================================
# STEP 5 — Create Assessment Features
# ============================================================

print("\nSTEP 5 — Creating assessment features...")

assessment_features = (
    student_assessment
    .groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )
    .agg(
        average_assessment_score=("score", "mean"),
        assessment_count=("score", "count"),
        highest_assessment_score=("score", "max"),
        lowest_assessment_score=("score", "min")
    )
    .reset_index()
)

print(
    "Assessment features:",
    assessment_features.shape
)

print("\nAssessment features preview:")
print(assessment_features.head())

# ============================================================
# STEP 6 — Load VLE Activity
# ============================================================

print("\nSTEP 6 — Loading VLE data...")

student_vle = pd.read_csv(
    "data/studentVle.csv"
)

print("Student VLE:", student_vle.shape)

# ============================================================
# STEP 7 — Process VLE Activity
# ============================================================

print("\nSTEP 7 — Creating VLE features...")

vle_features = (
    student_vle
    .groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )
    .agg(
        total_clicks=("sum_click", "sum"),
        active_days=("date", "nunique")
    )
    .reset_index()
)

# Average clicks per active day
vle_features["average_clicks_per_day"] = (
    vle_features["total_clicks"]
    /
    vle_features["active_days"].replace(0, 1)
)

print("\nVLE features:")
print(vle_features.head())

print(
    "\nVLE features shape:",
    vle_features.shape
)

# ============================================================
# STEP 8 — Load Registration Data
# ============================================================

print("\nSTEP 8 — Loading registration data...")

student_registration = pd.read_csv(
    "data/studentRegistration.csv"
)

print(
    "Student registration:",
    student_registration.shape
)

# ============================================================
# STEP 9 — Create Registration Features
# ============================================================

print("\nSTEP 9 — Creating registration features...")

student_registration["unregistered"] = (
    student_registration["date_unregistration"]
    .notna()
    .astype(int)
)

registration_features = (
    student_registration
    [
        [
            "id_student",
            "code_module",
            "code_presentation",
            "unregistered"
        ]
    ]
)

print("\nRegistration features:")
print(registration_features.head())

# ============================================================
# STEP 10 — Merge Everything with Student Information
# ============================================================

print("\nSTEP 10 — Merging all datasets...")

df = student_info.merge(
    assessment_features,
    on=[
        "id_student",
        "code_module",
        "code_presentation"
    ],
    how="left"
)

df = df.merge(
    vle_features,
    on=[
        "id_student",
        "code_module",
        "code_presentation"
    ],
    how="left"
)

df = df.merge(
    registration_features,
    on=[
        "id_student",
        "code_module",
        "code_presentation"
    ],
    how="left"
)

print("\nCombined dataset:")
print("Shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

# ============================================================
# STEP 11 — Create Dropout Target
# ============================================================

print("\nSTEP 11 — Creating dropout target...")

df["dropout"] = (
    df["final_result"] == "Withdrawn"
).astype(int)

print("\nDropout distribution:")
print(df["dropout"].value_counts())

# ============================================================
# STEP 12 — Handle Missing Numeric Values
# ============================================================

print("\nSTEP 12 — Handling numeric missing values...")

numeric_columns = [
    "average_assessment_score",
    "assessment_count",
    "highest_assessment_score",
    "lowest_assessment_score",
    "total_clicks",
    "active_days",
    "average_clicks_per_day",
    "unregistered"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = df[column].fillna(0)

print("Numeric missing values handled.")

# ============================================================
# STEP 13 — Handle Missing Categorical Values
# ============================================================

print("\nSTEP 13 — Handling categorical missing values...")

categorical_columns = [
    "gender",
    "region",
    "highest_education",
    "age_band",
    "imd_band",
    "disability"
]

for column in categorical_columns:

    if column in df.columns:

        df[column] = df[column].fillna("Unknown")

print("Categorical missing values handled.")

# ============================================================
# STEP 14 — Remove Unnecessary Columns
# ============================================================

print("\nSTEP 14 — Preparing final dataset...")

# We keep final_result for checking the target,
# but it should NOT be used as an input feature later.

# ============================================================
# STEP 15 — Check Dataset
# ============================================================

print("\nSTEP 15 — Dataset information...")

print("\nFinal dataset shape:")
print(df.shape)

print("\nColumn names:")

for column in df.columns:
    print("-", column)

print("\nMissing values:")

print(
    df.isnull().sum()
)

# ============================================================
# STEP 16 — Check Dropout Target
# ============================================================

print("\nSTEP 16 — Checking dropout target...")

print(
    df["dropout"].value_counts()
)

print("\nDropout percentage:")

print(
    df["dropout"].value_counts(normalize=True) * 100
)

# ============================================================
# STEP 17 — Save LearnLift Dataset
# ============================================================

print("\nSTEP 17 — Saving dataset...")

output_file = "data/learnlift_dataset.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nLearnLift dataset created successfully!")

print(
    "Saved to:",
    output_file
)

# ============================================================
# STEP 18 — Final Confirmation
# ============================================================

print("\nSTEP 18 — Final confirmation")

if os.path.exists(output_file):

    file_size = os.path.getsize(output_file)

    print("File exists: YES")
    print(
        "File size:",
        round(file_size / (1024 * 1024), 2),
        "MB"
    )

else:

    print("File exists: NO")

print("\n" + "=" * 60)
print("LEARNLIFT DATASET CREATION COMPLETED")
print("=" * 60)