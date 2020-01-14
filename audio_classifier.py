from os import listdir
from key import api_key
from acoustid import match

def get_mp3(path):

    mp3_list = []

    for files in listdir(path):
        if ".mp3" in files:
            mp3_list.append(files)

    return mp3_list

def get_file_details(files):
    artists = []
    titles = []
    for score, recording_id, title, artist in acoustid.match(api_key,files):
        artists.append(artist)
        titles.append(title)

    return artists, titles

def get_names(artists, titles):

    names = []
    
    if artists == [] and titles == []:
        status = False

    else:
        status = True
        for artist, title in zip(artists,titles):
            name = ""
            name += artist + "-" + title + ".mp3"
            names.append(name)
    return [names,status]

# def choose_name(artists, titles, choice):
#     name = "" 
#     name += artists[choice-1] + "-" + titles[choice-1] + ".mp3"

def get_best_name(names,status):
    best_name = ""
    if status:
        best_name = names[0]
        max_count = 0
        for name in names:
            if names.count(name) > max_count:
                max_count = names.count(name)
                best_name = name
    return best_name
                

if __name__ == "__main__":

    mp3_list = get_mp3(".")
    for files in mp3_list:
        artists, titles = get_file_details(files)
