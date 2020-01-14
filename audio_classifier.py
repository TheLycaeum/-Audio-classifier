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
    if artists == [] and titles == []:
        message = "No Records Found"

    else:
        message = "Choose Name:\n"
        n = 1
        for artist, title in zip(artists,titles):
            message += str(n) + " " + artist + "-"
            message += title +".mp3\n"
            n += 1
    return message

def choose_name(artists, titles, choice):
    name = "" 
    name += artists[choice-1] + "-" + titles[choice-1] + ".mp3"
    

if __name__ == "__main__":

    mp3_list = get_mp3(".")
    for files in mp3_list:
        artists, titles = get_file_details(files)
