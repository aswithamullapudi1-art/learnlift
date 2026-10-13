import pandas as pd

files = [
    "assessments.csv",
    "courses.csv",
    "studentAssessment.csv",
    "studentInfo.csv",
    "studentRegistration.csv",
    "studentVle.csv",
    "vle.csv"
]

for file in files:

    print("\n" + "=" * 60)
    print(file)
    print("=" * 60)

    df = pd.read_csv("data/" + file)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    print("Column names:")
    print(df.columns.tolist())