#!/usr/bin/python3
import json
import os
from pprint import pprint
import shutil
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
    
    def extract_from_cbz(self, filepath:str, view_only: str = False):
        path_deconstruct = [
            x for x in filepath.split(os.sep) if x != ""
        ]
        the_file = path_deconstruct[-1]
        outputfolder = filepath.replace('.cbz', '')
        if not view_only:
            os.makedirs(outputfolder, exist_ok=True)
        print(f"Extracting {the_file}")
        with ZipFile(filepath, 'r') as zip:
            files_in_archives = zip.namelist()
            if view_only:
                print('Files in Archive: ')
                for item in files_in_archives:
                    print(item)
            else:
                for temp_file in files_in_archives:
                    filename = temp_file.split(os.sep)[-1]
                    print(f"\t\tExtracting {outputfolder}{os.sep}{filename}")
                    os.makedirs(outputfolder, exist_ok=True)
                    with open(f"{os.path.join(outputfolder, filename)}", "wb") as img:
                        img.write(zip.read(temp_file))
        if not view_only:
            self.manga_data(outputfolder)
    
    def convert_to_cbz(self, folderpath:str):
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
            print(folderpathi, folder)
            os.makedirs(folder, exist_ok=True)
            with ZipFile(f"{os.path.join(folderpath, *folderpathi)}.cbz", "w") as zipfile:
                for file in filestoadd[f"{folder}"]:
                    print(f"Zipping,\t {file}")
                    zipfile.write(file, arcname=file.split(f"{os.sep}")[-1])
                    pass
            print(f"CBZ Created at {folder}")
        self.manga_data(folderpath)
        self.cleanup(".")

    def cleanup(self, currentpath:str = '.'):
        for root, dirs, files in os.walk(currentpath):
            if len(files) == 0 and os.path.getsize(root) == 0:
                if os.name in ['nt', "NT", "Nt"]:
                    os.system(f'rmdir "{root}"')
                else:
                    os.system(f'rm -rf "{root}"')
    
    def separator(self, path:str):
        print("Chapter Separating")
        os.chdir(f".{os.sep}{path}")
        for file in os.listdir("."):
            if file.__contains__("index"):
                continue
            filename, ext = file.split('.')
            chap_num = ""
            if filename.__contains__('-'):
                chap_num = filename.split('-')[1]
            elif filename.__contains__('_'):
                chap_num = filename.split('_')[-1][0:3]
            os.makedirs(f"{chap_num}", exist_ok=True)
            shutil.move(file, os.path.join(chap_num, file))
        print("successfully separated Chapters")
        os.chdir('..')
        pass
    
    def start_up(
        self, 
        path: str = ".", 
        seperator: bool = False,
        reconvert: bool = False,
        view_only: bool = False,
    ):
        if not type(path) == list:
            path = [path]
        for pathitem in path:
            if pathitem.split('.')[-1] == 'cbz':
                self.extract_from_cbz(pathitem, view_only=view_only)
                if seperator:
                    self.separator(pathitem.removesuffix(".cbz"))
                if reconvert:
                    self.separator(pathitem.removesuffix(".cbz"))
                    self.convert_to_cbz(pathitem.removesuffix(".cbz"))
                if not view_only:
                    print(f"Extracted {pathitem}")
            elif os.path.isdir(pathitem):
                self.convert_to_cbz(pathitem)
            else:
                print("Nani is this? " + pathitem)

    def manga_data(self, path: str = "."):
        if "index.json" in os.listdir(path):
            print('\nManga Info:')
            with open(f"{os.path.join(path ,'index.json')}") as jsonfile:
                data = json.load(jsonfile)
            needed_data = ["title", "author", "description", "cover", "status", "tags", "rating", "nsfw"]
            for required in needed_data:
                if required in list(data.keys()):
                    if type(data[required]) == list:
                        print(required, ":")
                        for item in data[required]:
                            if "title" in list(item.keys()):
                                print(item["title"], end=" | ")
                        print()
                    else:
                        print(required, ":", data[required])
        else: print("No Data found")
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gimme a path, default is . (current folder)\nIf input is a folder, then it will convert all files inside it as a cbz,\nIf it is a file, it will extract it")
    parser.add_argument("path", nargs='+', help="Give a path, to cbz or folder, That's it")
    parser.add_argument('-separate', action="store_true", help="Separate Chapters by Number, won't work probably")
    parser.add_argument('-reconvert', action="store_true", help="Separate chapters by Number and Reconvert, no need for separator tag")
    parser.add_argument('-viewonly', action="store_true", help="View What's In the Archive")
    converter = CBX_Converter()
    converter.start_up(
        parser.parse_args().path, 
        parser.parse_args().separate, 
        parser.parse_args().reconvert, 
        parser.parse_args().viewonly
    )
