input_file = "ONSPD_AUG_2025_UK.csv"
output_file = "filtered.csv"

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:

    # keep header
    header = infile.readline()
    outfile.write(header)

    for line in infile:
        parts = line.strip().split(",")
        doterm = parts[4].strip('"')  # 5th value (remove quotes)

        # Keep if no termination or 1996+
        if  len(doterm)==0 or doterm.startswith("S") or int(doterm[:4]) >= 1995:
            outfile.write(line)
