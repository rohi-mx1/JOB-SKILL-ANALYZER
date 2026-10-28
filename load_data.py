import os
import pandas as pd

# Get absolute project root from where script is run
base_dir = os.getcwd()

csv_path = None

# Search for postings.csv anywhere inside project
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.lower() == "postings.csv":
            csv_path = os.path.join(root, file)
            break
    if csv_path:
        break

# If still not found, search for ANY csv
if not csv_path:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(".csv"):
                csv_path = os.path.join(root, file)
                break
        if csv_path:
            break

# Final check
if not csv_path:
    print("❌ NO CSV FILE FOUND ANYWHERE IN PROJECT")
    exit()

# Load CSV
df = pd.read_csv(csv_path)

print("✅ CSV FOUND & LOADED FROM:")
print(csv_path)
print("\n✅ First 5 Rows:")
print(df.head())