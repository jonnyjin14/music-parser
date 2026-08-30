import pandas as pd
from pathlib import Path
import os

class MusicParser:
    def __init__(self, path):
        # path = Path(__file__).parent
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Music library path does not exist: {self.path}")
        if not self.path.is_dir():
            raise NotADirectoryError(f"Music library path is not a directory: {self.path}")
        print(f"Current Path is\n{self.path}")

    def scanLibrary(self):
        # Create the dataset
        data = ({
            'song': [],
            'singer': [],
        })

        # for file in path.iterdir():
        for file in self.path.rglob("*"):
            
            if file.suffix.lower() in [".mp3", ".wav"]:
                # Check if file name has singer
                if "-" in file.stem: # stem -> Remove the extension
                    singer,song = file.stem.split("-", 1)
                else:
                    singer = "Unknown"
                    song = file.stem

                data['singer'].append(singer)
                data['song'].append(song)

        self.df = pd.DataFrame(data)

        print(self.df)

    def writeCsv(self): 
        # Save files to desktop. 
        desktop_path = Path.home() / "OneDrive" / "桌面"/ "Output_file.csv"
        self.df.to_csv(desktop_path, index = False, encoding='utf-8-sig')

        print(os.path.exists(desktop_path))
        print(os.getcwd())

