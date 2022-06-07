#!/bin/python3
import os
from pprint import pprint
import sys
from zipfile import ZipFile
import argparse

class CBX_Converter():
    '''I was Bored, Was tryin to read some manga
    got it in cbz format, so i was like, let's make a converter
    usage: just make an object of this class and simply run start_up
    with path to the files
    this tool can also convert folders to cbz archives
    just give a folder to start_up
    default path is "." (current folder)'''
    def __init__(self):
        pass
    
    def extract_from_cbz(self, filepath):
        path_deconstruct = [
            x for x in filepath.split(os.sep) if x != ""
        ]
        the_file = path_deconstruct[-1]
        outputfolder = filepath.replace('.cbz', '')
        os.makedirs(outputfolder, exist_ok=True)
        print(f"Extracting {the_file}")
        with ZipFile(filepath, 'r') as zip:
            files_in_archives = zip.namelist()
            for temp_file in files_in_archives:
                filename = temp_file.split(os.sep)[-1]
                print(f"\t\tExtracting {outputfolder}{os.sep}{filename}")
                os.makedirs(outputfolder, exist_ok=True)
                with open(f"{os.path.join(outputfolder, filename)}", "wb") as img:
                    img.write(zip.read(temp_file))
        pass
    
    def convert_to_cbz(self, folderpath):
        filestoadd = dict()
        for root, dirs, files in os.walk(folderpath):
            if len(root.split(os.sep)) > 2:
                pathdecons = root.split(os.sep)[-2] + f"{os.sep}" + root.split(os.sep)[-1]
            elif len(root.split(os.sep)) > 1:
                pathdecons = root.split(os.sep)[-1]
            else:
                pathdecons = root
            filestoadd[f"{pathdecons}"] = list()
            for file in files:
                if file.split(".")[-1] in ['png', 'jpg', 'bmp', 'webp', 'jpeg']:
                    filestoadd[f"{pathdecons}"].append(os.path.join(root, file))
        for folder in list(filestoadd.keys()):
            folderpathi = folder.split(f"{os.sep}")
            os.makedirs(folder, exist_ok=True)
            with ZipFile(f"{os.path.join(folderpath, *folderpathi)}.cbz", "w") as zipfile:
                for file in filestoadd[f"{folder}"]:
                    print(f"Zipping,\t {file}")
                    zipfile.write(file, arcname=file.split(f"{os.sep}")[-1])
                    pass
            print(f"CBZ Created at {folder}")
        self.cleanup(".")

    def cleanup(self, currentpath = '.'):
        for root, dirs, files in os.walk(currentpath):
            if len(files) == 0 and os.path.getsize(root) == 0:
                if os.name in ['nt', "NT", "Nt"]:
                    os.system(f'rmdir "{root}"')
                else:
                    os.system(f'rm -rf "{root}"')

    def start_up(self, path = ".", seperator = False):
        if not type(path) == list:
            path = [path]
        for pathitem in path:
            if pathitem.split('.')[-1] == 'cbz':
                self.extract_from_cbz(pathitem)
                print(f"Extracted {pathitem}")
            elif os.path.isdir(pathitem):
                self.convert_to_cbz(pathitem)
            else:
                print("Nani is this? " + pathitem)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gimme a path, default is . (current folder)\nIf input is a folder, then it will convert all files inside it as a cbz,\nIf it is a file, it will extract it")
    parser.add_argument("path", nargs='+', help="Give a path, to cbz or folder, That's it")
    path = parser.parse_args().path
    seperator = parser.parse_args().s
    converter = CBX_Converter()
    converter.start_up(path, seperator)
