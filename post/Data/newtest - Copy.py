import os

input_folder = "multi_csv"
output_folder = "multi_csv2"

# Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if not filename.endswith(".csv"):
        continue

    input_file = os.path.join(input_folder, filename)
    output_file = os.path.join(output_folder, filename.replace(".csv", ".csv"))

    print(f"Processing {filename} -> {os.path.basename(output_file)}")

    with open(input_file, "r", encoding="utf-8") as f_in, \
         open(output_file, "w", encoding="utf-8") as f_out:

        # Read header and determine column indexes
        header = f_in.readline().strip().split(",")
        idx_pcds = header.index("pcds")
        idx_dointr = header.index("dointr")
        idx_doterm = header.index("doterm")
        idx_lat = header.index("lat")
        idx_long = header.index("long")

        # Write new header
        f_out.write("pcds,dointr,doterm,lat,long\n")

        # Process each line
        for line in f_in:
            items = line.strip().split(",")
            pcds = items[idx_pcds].strip('"')
            dointr = items[idx_dointr].strip('"')
            doterm = items[idx_doterm].strip('"')
            lat = items[idx_lat]
            long = items[idx_long]

            f_out.write(f"{pcds},{dointr},{doterm},{lat},{long}\n")
