from os import listdir,rename,path, mkdir
from sys import argv
from key import api_key
from shutil import move
from acoustid import match

path = "."
if len(argv) == 2:
    path = argv[1]

def get_mp3(path):

    mp3_list = []

    for files in listdir(path):
        if ".mp3" in files:
            mp3_list.append(files)

    return mp3_list

def get_file_details(files):
    artists = []
    titles = []
    for score, recording_id, title, artist in match(api_key,files):
        artists.append(artist)
        titles.append(title)

    return artists, titles

def get_names(artists, titles):

    names = []
    
    if artists == [] or titles == []:
        status = False

    else:
        status = True
        for artist, title in zip(artists,titles):
            if isinstance(artist,str) and isinstance(title,str):
                name = ""
                name += artist + "-" + title + ".mp3"
                names.append(name)

    return names,status

def get_best_name(names,status):
    best_name = ""
    best_name = names[0]
    max_count = 0
    for name in names:
        if names.count(name) > max_count:
            max_count = names.count(name)
            best_name = name
    return best_name

def get_paths(choice, old_name, best_name):

    if choice == 1:
        artist = best_name.split("-")[0]
        title = best_name.split("-")[1]
        if artist not in listdir(path):
            artist_directory = path + "/" + artist
            mkdir(artist_directory)

        old_path = path + "/" + old_name
        new_path = path + "/"+ artist + "/" + title

        return old_path,new_path

    if choice == 2:
        
        old_path = path + "/" + old_name
        new_path = path + "/" + best_name

        return old_path,new_path
    
if __name__ == "__main__":
    print("How you want to classify?\n 1. artist/title.mp3 \n 2. artist-title.mp3 \n")
    choice = int(input())
    mp3_list = get_mp3(path)
    for files in mp3_list:
        file_path = path + "/" + files
        artists, titles = get_file_details(file_path)
        names, status = get_names(artists, titles)
        best_name = get_best_name(names,status)
        if status:
            best_name = get_best_name(names,status)
            old_path, new_path = get_paths(choices, files, best_name)

            if choice == 1:
                move(old_path,new_path)

            if choice == 2:
                rename(old_path, new_path)
                
        
