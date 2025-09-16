import os
import csv
from collections import Counter

# Folder containing CSV files
folder_path = "./blocks_output"  # change to your folder path

word_counter = Counter()

# Loop through all CSV files in the folder
i = 0 
for filename in os.listdir(folder_path):
    if i % 500==0:
        print(i)
    if filename.endswith(".csv"):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, newline='', encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 1:
                    text = row[1]  # second column
                    words = text.replace("-", " ").replace("/", " ").split()
                    for word in words:
                        word = word.strip().upper()
                        if len(word) > 3:
                            word_counter[word] += 1
    i += 1
# Get the 650 most common words
most_common_words = word_counter.most_common(650)

# Save results to a CSV file
output_file = os.path.join(folder_path, "word_frequencies.csv")
with open(output_file, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Word", "Count"])
    writer.writerows(most_common_words)

print(f"Results saved to {output_file}")