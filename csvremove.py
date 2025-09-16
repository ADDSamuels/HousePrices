# Input and output files
input_file = "word_frequencies.csv"   # change to your file name
output_file = "output.csv" # change to desired output file name

with open(input_file, "r", encoding="utf-8", errors="ignore") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:
    
    for line in infile:
        # Strip newline and remove everything after the first comma
        new_line = line.strip().split(",", 1)[0]
        outfile.write(new_line + "\n")

print(f"Processed file saved to {output_file}")
