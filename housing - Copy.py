import os
import math
##Used ChatGPT
# ==============================
# Step 0: Helper function to map lat/lon to 500m blocks
# ==============================
def latlon_to_block(lat, lon, block_size_m=500):
    """
    Convert latitude and longitude into grid indices representing ~500m blocks.
    Returns (lat_block, lon_block) as integers.
    """
    lat_block_size = block_size_m / 111000  # 1 degree latitude ≈ 111 km
    lon_block_size = block_size_m / (111000 * math.cos(math.radians(lat)))  # longitude scales with latitude

    lat_block = int(lat // lat_block_size)
    lon_block = int(lon // lon_block_size)

    return lat_block, lon_block

# ==============================
# Step 1: Load postcode CSV files into memory
# ==============================
postcode_data = {}  # key = postcode letters, value = list of [postcode, start_year, end_year]

folder = "post/Data/multi_csv"

for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        # Extract postcode letters from filename (assumes format like 'data_ABC.csv')
        code = filename.split("_")[-1].split(".")[0]
        with open(os.path.join(folder, filename), "r") as f:
            postcode_data[code] = [line.strip().split(",") for line in f]

# ==============================
# Step 2: Prepare dictionary for 500m blocks
# ==============================
# key = (lat_block, lon_block), value = list of entries
# each entry: [price, postcode, number, subnumber, streetname, memory]
blocks = {}

def add_to_block(lat, lon, price, postcode, number, subnumber, streetname, memory=""):
    """
    Add an entry to the appropriate 500m block in the dictionary.
    """
    lat_block, lon_block = latlon_to_block(lat, lon)
    key = (lat_block, lon_block)

    if key not in blocks:
        blocks[key] = []

    blocks[key].append([price, postcode, number, subnumber, streetname, memory])

# ==============================
# Step 3: Process main CSV
# ==============================
with open("prices3.csv", "r") as f:
    for line_number, line in enumerate(f, start=1):
        items = line.strip().split(",")

        # Extract values from CSV
        price = int(items[0].strip())           # assuming first column is price
        soldyear = int(items[1].strip()[:6])      # first 6 chars of year column
        soldpost = items[2].strip()               # postcode
        number = items[3].strip()                 # custom number field
        subnumber = items[4].strip()              # custom subnumber field
        #lat = float(items[3].strip())             # latitude
        #lon = float(items[4].strip())             # longitude
        streetname = items[5].strip()                 # streetname
        memory = items[6].strip()              # memory

        # ==============================
        # Extract postcode letters (before first number)
        # ==============================
        postcode_letters = ""
        for char in soldpost:
            if char.isdigit():
                break
            if char.isalpha():
                postcode_letters += char
            else:
                break

        # ==============================
        # Lookup preloaded postcode data
        # ==============================
        if line_number % 1000 == 0:
            print(line_number)
        postcodeFound = False
        while not postcodeFound:
            for items2 in postcode_data.get(postcode_letters, []):
                if items2[0] == soldpost:
                    start_year = int(items2[1])
                    end_year = int(items2[2]) if items2[2] else float('inf')
                    if start_year <= soldyear < end_year:
                        postcodeFound = True
                        lat, long = float(items2[3]), float(items2[4])
                        break
                    else:
                        # Debugging info if year doesn't match
                        #print(f"Line {line_number} -> soldyear: {soldyear}, soldpost: {soldpost}, {postcode_letters}")
                        #print(items2)
                        a =1
            else:
                #print(f"Line {line_number} -> no matching postcode entry found for {soldpost}")
                postcodeFound = True
 

        # ==============================
        # Add the entry to the appropriate 500m block
        # ==============================
        add_to_block(lat, long, price, soldpost, number, subnumber, streetname, memory)  # memory 

# ==============================
# Step 4: Example usage of blocks
# ==============================
for block_key, entries in blocks.items():
    print(f"Block {block_key} contains {len(entries)} entries")
