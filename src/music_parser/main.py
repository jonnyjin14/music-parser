import music_parser.helper as helper

def main():
    parser = helper.MusicParser(r"D:\Dell Files\Songs")
    parser.scanLibrary()
    
if __name__== '__main__':
    main()

