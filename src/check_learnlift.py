import pandas as pd

df = pd.read_csv(
    "data/learnlift_dataset.csv"
)

print("Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDropout:")
print(df["dropout"].value_counts())

print("\nFinal result:")
print(df["final_result"].value_counts())

print("\nFirst 5 rows:")
print(df.head())