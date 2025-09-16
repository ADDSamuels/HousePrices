import os
import re

# ----------------------------
# Folder containing TXT files
# ----------------------------
folder_path = r".\districts_output"  # change to your folder path

if not os.path.exists(folder_path):
    raise FileNotFoundError(f"The folder path does not exist: {folder_path}")

# ----------------------------
# File containing the 650 most common words
# ----------------------------
word_freq_file = "word_frequencies.csv"  # change path if needed

if not os.path.exists(word_freq_file):
    raise FileNotFoundError(f"Word frequencies file not found: {word_freq_file}")

# ----------------------------
# Step 1: Load the 650 words
# ----------------------------
most_common_words = []
with open(word_freq_file, newline='', encoding="utf-8", errors="ignore") as f:
    for line in f:
        word = line.strip().split(",")[0].upper()  # ignore everything after first comma
        if word and word != "WORD":
            most_common_words.append(word)

most_common_words = most_common_words[:650]  # limit to 650 words

# ----------------------------
# Step 2: Build mapping: word -> 2-letter code
# ----------------------------
def num_to_two_letters(n):
    n -= 1  # zero-based
    first = n // 26
    second = n % 26
    return chr(97 + first) + chr(97 + second)

word_to_code = {word: num_to_two_letters(i + 1) for i, word in enumerate(most_common_words)}

# ----------------------------
# Step 3: Prepare output folder
# ----------------------------
output_folder = os.path.join(folder_path, "processed")
os.makedirs(output_folder, exist_ok=True)
print(f"Processed files will be saved to: {output_folder}")

# ----------------------------
# Step 4: Process TXT files
# ----------------------------
# Regex pattern to match words
pattern = re.compile(r'\b\w+\b')

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, "r", encoding="utf-8", errors="ignore") as infile, \
             open(output_path, "w", encoding="utf-8") as outfile:

            for line in infile:
                # Convert entire line to uppercase first
                line_upper = line.upper()

                # Replace words from the 650-word list
                def replace_match(match):
                    word = match.group(0)
                    return word_to_code.get(word, word)  # lowercase code replaces the uppercase word

                new_line = pattern.sub(replace_match, line_upper)
                outfile.write(new_line)

print("Processing complete.")
