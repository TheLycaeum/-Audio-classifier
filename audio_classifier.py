from os import listdir
from key import api_key
from acoustid import fingerprint_file, lookup

def get_mp3(path):

    mp3_list = []

    for files in listdir(path):
        if ".mp3" in files:
            mp3_list.append(files)

    return mp3_list

def get_file_details(files):
    duration, fingerprint = fingerprint_file(files)
    file_details =  lookup(api_key, fingerprint, duration)
    return file_details
    
if __name__ == "__main__":

    mp3_list = get_mp3(".")
    for files in mp3_list:
        file_details = get_file_details(files)
