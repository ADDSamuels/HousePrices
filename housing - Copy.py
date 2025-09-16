import os
import math
import csv

# ==============================
# Helper: map lat/lon to 500m blocks
# ==============================
def latlon_to_block(lat, lon, block_size_m=500):
    lat_block_size = block_size_m / 111000
    lon_block_size = block_size_m / (111000 * math.cos(math.radians(lat)))
    return int(lat // lat_block_size), int(lon // lon_block_size)

# ==============================
# Load postcode CSV files into memory
# ==============================
postcode_data = {}
folder = "post/Data/multi_csv"

for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        with open(os.path.join(folder, filename), "r") as f:
            next(f)  # skip header
            for line in f:
                cols = line.rstrip("\n").split(",")
                if len(cols) < 5:
                    continue
                postcode = cols[0].strip()
                start_year = int(cols[1]) if cols[1] else 0
                end_year = int(cols[2]) if cols[2] else float("inf")
                lat = float(cols[3])
                lon = float(cols[4])
                postcode_data.setdefault(postcode, []).append((start_year, end_year, lat, lon))

# ==============================
# Block storage with property consolidation
# ==============================
blocks = {}  # key = (lat_block, lon_block), value = dict with property tuples

def add_to_block(lat, lon, price, soldyear, postcode, number, subnumber, streetname, memory):
    lat_block, lon_block = latlon_to_block(lat, lon)
    key = (lat_block, lon_block)
    if key not in blocks:
        blocks[key] = {}
    
    # Use (postcode, streetname) as property key
    prop_key = (postcode, streetname, number, subnumber)
    
    if prop_key not in blocks[key]:
        blocks[key][prop_key] = {
            "number": number,
            "subnumber": subnumber,
            "memory": memory,
            "prices": [],
            "soldyears": []
        }
    
    # Append sale info to the lists
    blocks[key][prop_key]["prices"].append(price)
    blocks[key][prop_key]["soldyears"].append(soldyear)

# ==============================
# Process main CSV
# ==============================
empty = [] #
with open("prices3.csv", "r") as f:
    for line_number, line in enumerate(f, start=1):
        items = line.rstrip("\n").split(",")

        price = int(items[0])
        soldyear = int(items[1][:6])
        soldyear2 = int(items[1])
        soldpost = items[2]
        number = items[3]
        subnumber = items[4]
        streetname = items[5]
        memory = items[6]

        # Lookup postcode
        postcodeFound = False
        while not postcodeFound:
            for start_year, end_year, lat, lon in postcode_data.get(soldpost, []):
                if start_year <= soldyear < end_year:
                    postcodeFound = True
                    break
            else:
                postcodeFound = True
                empty = str(line_number)+"~" + line

        if postcodeFound:
            add_to_block(lat, lon, price, soldyear2, soldpost, number, subnumber, streetname, memory)

        if line_number % 50000 == 0:
            print(f"Processed {line_number} rows...")

# ==============================
# Write blocks to disk
# ==============================
output_folder = "blocks_output"
os.makedirs(output_folder, exist_ok=True)
print("deposit")
with open('lines.txt', 'w') as f:
    for line in empty:
        f.write(f"{line}\n")
empty = []
print("empty finished")
for block_key, properties in blocks.items():
    lat_block, lon_block = block_key
    filename = f"{lat_block}_{lon_block}.csv"
    filepath = os.path.join(output_folder, filename)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        #writer.writerow(["postcode", "streetname", "number", "subnumber", "memory", "prices", "soldyears"])
        for (postcode, streetname, number, subnumber), info in properties.items():
            writer.writerow([
                postcode,
                streetname,
                number,
                subnumber,
                info["memory"],
                ";".join(map(str, info["prices"])),      # join prices as string
                ";".join(map(str, info["soldyears"]))    # join sold years as string
            ])
