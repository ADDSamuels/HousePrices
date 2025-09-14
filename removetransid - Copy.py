input_file = "prices.csv"
output_file = "prices3.csv"

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:
    
    for line in infile:
        # Strip newline
        
        line = line.strip()
        
        # Remove leading/trailing quote, then split by "," safely
        parts = line.strip('"').split('","')
        
        # Drop the first element
        new_parts = parts[1:]
        c = ","
        year = parts[2]
        year = year[:4] + year[5:7] + year[8:10]
        # Rebuild the line with quotes
        new_line = parts[1] + c + year + c + parts[3] +c + parts[7] + c + parts[8] + c + parts[9] + c + parts[4] + parts [5] + parts[6] + parts[14] 
        #print(new_line)
        outfile.write(new_line + "\n")
