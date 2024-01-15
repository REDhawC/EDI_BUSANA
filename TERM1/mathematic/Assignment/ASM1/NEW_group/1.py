import os
from datetime import datetime

# Directory path where the CSV files are stored
directory_path = "./crops_Import/results/"

# List of crop names in the order they should be used for renaming
crop_names = [
    "Rice",
    "Wheat",
    "Cotton_Raw",
    "Maize",
    "Horsegram",
    "Jute",
    "Potato",
    "Soybean",
]

# Get a list of all files in the directory sorted by their modification time
file_paths = sorted(
    [os.path.join(directory_path, f) for f in os.listdir(directory_path)],
    key=lambda x: os.path.getmtime(x),
)

# Loop over the files and rename them according to the crop names list
for i, file_path in enumerate(file_paths):
    # Break the loop if there are more files than crop names
    if i >= len(crop_names):
        break

    # Prepare the new file name with the corresponding crop name and existing timestamp
    file_name = os.path.basename(file_path)
    timestamp = file_name.split("_")[-1]  # Extract timestamp from the file name
    new_name = f"{crop_names[i]}_{timestamp}"  # Combine crop name with timestamp

    # Form the full path for the new file name
    new_file_path = os.path.join(directory_path, new_name)

    # Rename the file
    os.rename(file_path, new_file_path)
    print(f'Renamed "{file_name}" to "{new_name}"')
