input_file = "prices.csv"
output_file = "prices2.csv"

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:
    
    for line in infile:
        # Strip newline
        line = line.strip()
        
        # Remove leading/trailing quote, then split by "," safely
        parts = line.strip('"').split('","')
        
        # Drop the first element
        new_parts = parts[1:]
        
        # Rebuild the line with quotes
        new_line = '"' + '","'.join(new_parts) + '"'
        
        outfile.write(new_line + "\n")
