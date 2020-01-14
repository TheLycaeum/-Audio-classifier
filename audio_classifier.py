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
    message = "No Records Found"
    return message

if __name__ == "__main__":

    mp3_list = get_mp3(".")
    for files in mp3_list:
        artists, titles = get_file_details(files)
