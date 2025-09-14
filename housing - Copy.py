import os
import math
import csv
# ==============================
# Step 0: Helper function to map lat/lon to 500m blocks
# ==============================
def latlon_to_block(lat, lon, block_size_m=500):
    """Convert lat/lon into ~500m grid indices."""
    lat_block_size = block_size_m / 111000  # ~0.0045° per 500m
    lon_block_size = block_size_m / (111000 * math.cos(math.radians(lat)))
    return int(lat // lat_block_size), int(lon // lon_block_size)

# ==============================
# Step 1: Load postcode CSV files into memory
# ==============================
postcode_data = {}  # key = full postcode, value = list of (start_year, end_year, lat, lon)

folder = "post/Data/multi_csv"

for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        with open(os.path.join(folder, filename), "r") as f:
            next(f)  # skip header row "pcds,dointr,doterm,lat,long"
            for line in f:
                cols = line.rstrip("\n").split(",")
                if len(cols) < 5:
                    continue  # skip malformed lines

                postcode = cols[0].strip()
                start_year = int(cols[1]) if cols[1] else 0
                end_year = int(cols[2]) if cols[2] else float("inf")
                lat = float(cols[3])
                lon = float(cols[4])

                postcode_data.setdefault(postcode, []).append(
                    (start_year, end_year, lat, lon)
                )

# ==============================
# Step 2: Prepare dictionary for 500m blocks
# ==============================
# key = (lat_block, lon_block), value = list of entries
# each entry = (price, postcode, number, subnumber, streetname, memory)
blocks = {}

def add_to_block(lat, lon, price, postcode, soldyear2, number, subnumber, streetname, memory=""):
    """Add an entry into the correct 500m block."""
    lat_block, lon_block = latlon_to_block(lat, lon)
    key = (lat_block, lon_block)
    if key not in blocks:
        blocks[key] = []
    blocks[key].append((price, postcode, soldyear2, number, subnumber, streetname, memory))

# ==============================
# Step 3: Process main CSV
# ==============================
with open("prices3.csv", "r") as f:
    for line_number, line in enumerate(f, start=1):
        items = line.rstrip("\n").split(",")

        price = int(items[0])
        soldyear = int(items[1][:6])  # first 6 chars
        soldyear2 = int(items[1])
        soldpost = items[2]
        number = items[3]
        subnumber = items[4]
        streetname = items[5]
        memory = items[6]

        # ==============================
        # Lookup preloaded postcode data (with while loop)
        # ==============================
        postcodeFound = False
        while not postcodeFound:
            for start_year, end_year, lat, lon in postcode_data.get(soldpost, []):
                if start_year <= soldyear < end_year:
                    postcodeFound = True
                    break
            else:
                # no match, still exit loop
                postcodeFound = True

        # ==============================
        # Add entry to block if postcode matched
        # ==============================
        if postcodeFound:
            add_to_block(lat, lon, price, soldpost, soldyear2, number, subnumber, streetname, memory)

        # Progress indicator
        if line_number % 10000 == 0:
            print(f"Processed {line_number} rows...")

# ==============================
# Step 4: Example usage of blocks
# ==============================
output_folder = "blocks_output"
os.makedirs(output_folder, exist_ok=True)  # create if it doesn't exist

for block_key, entries in blocks.items():
    lat_block, lon_block = block_key
    filename = f"block_{lat_block}_{lon_block}.csv"
    filepath = os.path.join(output_folder, filename)

    # Write CSV for this block
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        # Optional header
        writer.writerow(["price", "postcode", "soldyear", "number", "subnumber", "streetname", "memory"])
        # Write all entries
        writer.writerows(entries)