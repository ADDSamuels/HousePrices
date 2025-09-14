import csv
import os

# Cache for postcode files
postcode_data = {}

folder = "post/Data/multi_csv"

# Preload all CSV files into memory
for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        code = filename.split("_")[-1].split(".")[0]  # Extract postcode_letters from filename
        with open(os.path.join(folder, filename), "r") as f:
            postcode_data[code] = [line.strip().split(",") for line in f]

# Now process the main CSV
with open("prices2.csv", "r") as f:
    for line_number, line in enumerate(f, start=1):
        items = line.strip().split(",")
        soldyear = items[1].strip()
        soldyear = soldyear[1:5] + soldyear[6:8]
        soldpost = items[2].strip().strip('"')

        # Extract letters before first number (fast, non-regex)
        postcode_letters = ""
        for char in soldpost:
            if char.isdigit():
                break
            if char.isalpha():
                postcode_letters += char
            else:
                break

        # Lookup preloaded data
        for items2 in postcode_data.get(postcode_letters, []):
            if items2[2].strip('"') == soldpost:
                print(f"Line {line_number} -> 2nd: {soldyear}, 3rd: {soldpost}, {postcode_letters}")
                break
