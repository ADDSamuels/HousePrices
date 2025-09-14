import os

# Cache for postcode files
postcode_data = {}

folder = "post/Data/multi_csv"

# Preload all CSV files into memory
for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        code = filename.split("_")[-1].split(".")[0]  # Extract postcode_letters from filename
        with open(os.path.join(folder, filename), "r") as f:
            postcode_data[code] = [line.strip().split(",") for line in f]

# Now process the main CSV
with open("prices3.csv", "r") as f:
    for line_number, line in enumerate(f, start=1):
        items = line.strip().split(",")
        soldyear = items[1].strip()
        soldyear = soldyear[:6]
        soldpost = items[2].strip()

        # Extract letters before first number (fast, non-regex)
        postcode_letters = ""
        for char in soldpost:
            if char.isdigit():
                break
            if char.isalpha():
                postcode_letters += char
            else:
                break

        # Lookup preloaded data
        postcodeFound = False
        while not postcodeFound:
            for items2 in postcode_data.get(postcode_letters, []):
                if items2[0] == soldpost:
                    if int(soldyear) >= int(items2[1]) and (items2[2] == "" or int(items2[2]) > int(soldyear)):
                        postcodeFound = True
                        break
                        #if line_number % 10000 == 0:
                            #print(line_number)
                            #s
                    else:
                        print(f"Line {line_number} -> 2nd: {soldyear}, 3rd: {soldpost}, {postcode_letters}")
                        print(items2)
            else:
                print("For loop didn't break")
                postcodeFound = True
