import os
import shutil
import sys
import re
from unidecode import unidecode
import time



def main():
    try:
        sort_folders('C:/Users/kunan/Documents/test_clean/garbage')
    except:
        print('Error')

def sort_folders(path):
    ext = {
        "images" : ['JPEG', 'PNG', 'JPG', 'SVG'],
        "videos" : ['AVI', 'MP4', 'MOV', 'MKV'],
        "docs" : ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        "music" : ['MP3', 'OGG', 'WAV', 'AMR'],
        "archives" : ['ZIP', 'GZ', 'TAR'],
        "else" : [] 
    }
    file_list = []
    ext_list = []
    unknown_ext_list = []

    for folder in ext.keys():
        os.makedirs(os.path.join(path, folder), exist_ok=True)

    for root, _, files in os.walk(path):
        for filename in files:
            _, exten = os.path.splitext(filename)
            exten = exten.replace(".", "").upper()

            for folder, extensions in ext.items():
                if exten in extensions:
                    file_list.append(filename)
                    ext_list.append(exten)
                    move_file(root, filename, path, folder)
                    break
            else:
                file_list.append(filename)
                unknown_ext_list.append(exten)
                move_file(root, filename, path, "else")

    delete_empty_folders(path)
    print_files(file_list, ext_list, unknown_ext_list)    



def move_file(root, filename, path, folder):
    old_path = os.path.join(root, filename)
    new_path = os.path.join(path, folder, filename)
    try:
        if folder == "archives":
            shutil.unpack_archive(old_path, new_path)
            os.remove(old_path)
        else:
            shutil.move(old_path, new_path)
            rename_file(new_path)
    except:
        pass

def delete_empty_folders(path):
    for root, dirs, _ in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

def normalize(filename):
    filename = unidecode(filename)
    filename = re.sub(r'[^a-zA-Z0-9]', '_', filename)
    return filename

def rename_file(filename):
    directory, old_name = os.path.split(filename)
    old_name, extension = os.path.splitext(old_name)
    new_name = normalize(old_name)
    new_filename = os.path.join(directory, new_name + extension)
    os.rename(filename, new_filename)

def print_files(file_list, ext_list, unknown_ext_list):
    print("Here are all the files in this path:\n" + "\n".join(file_list))
    print("Here are all the known extensions:\n" + "\n".join(ext_list))
    print("Here are all the unknown extensions:\n" + "\n".join(unknown_ext_list))

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"The program took {execution_time} seconds to complete.")