import os

blocks_folder = "blocks_output"
district_folder = "districts_output"
os.makedirs(district_folder, exist_ok=True)

# Keep 50 district files open
writers = {}

def get_district(postcode: str) -> str:
    postcode = postcode.strip().upper()
    if not postcode:
        return None
    return postcode[:2] if len(postcode) >= 2 and postcode[1].isalpha() else postcode[0]
i=0
for filename in os.listdir(blocks_folder):
    if i % 1000==0:
        print(i)
    if not filename.endswith(".csv"):
        continue

    block_id = filename.replace(".csv", "")
    filepath = os.path.join(blocks_folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()

    if not lines:
        continue

    # Get all district codes in this block
    districts = {get_district(line.split(",", 1)[0]) for line in lines if line}
    districts.discard(None)

    if not districts:
        continue

    block_text = f"={block_id}=\n" + "\n".join(lines) + "\n\n"

    for d in districts:
        if d not in writers:
            writers[d] = open(os.path.join(district_folder, f"{d}.txt"), "w", encoding="utf-8")
        writers[d].write(block_text)
    i += 1
# Close all files at the end
for f in writers.values():
    f.close()

print(f"✅ Created {len(writers)} district files in '{district_folder}'")
