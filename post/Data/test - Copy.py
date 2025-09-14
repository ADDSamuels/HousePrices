import os

folder = "multi_csv"

for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        input_file = os.path.join(folder, filename)
        output_file = os.path.join(folder, filename)  # overwrite original

        with open(input_file, "r", encoding="utf-8") as infile:
            lines = infile.readlines()

        with open(output_file, "w", encoding="utf-8") as outfile:
            # keep header
            outfile.write(lines[0])

            for line in lines[1:]:
                parts = line.strip().split(",")
                doterm = parts[4].strip('"')  # 5th value (remove quotes)

                # Keep if no termination or 1996+
                if len(doterm) == 0 or doterm.startswith("S") or int(doterm[:4]) >= 1995:
                    outfile.write(line)
