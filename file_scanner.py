import pandas as pd
from pathlib import Path
import os

# path = Path(__file__).parent
path = Path(r"D:\Dell Files\Songs")
print(f"Current Path is\n{path}")
 
# Create the dataset

data = ({
    'song': [],
    'singer': [],
})


# for file in path.iterdir():
for file in path.rglob("*"):
    if file.suffix.lower() in [".mp3", ".wav"]:

        # Check if file name has singer
        if "-" in file.stem: # stem -> Remove the extension
            singer,song = file.stem.split("-", 1)
        else:
            singer = "Unknown"
            song = file.stem

        data['singer'].append(singer)
        data['song'].append(song)

df = pd.DataFrame(data)

print(df)

# Save files 
desktop_path = Path.home() / "OneDrive" / "桌面"/ "Output_file.csv"
df.to_csv(desktop_path, index = False, encoding='utf-8-sig')

print(os.path.exists(desktop_path))
print(os.getcwd())