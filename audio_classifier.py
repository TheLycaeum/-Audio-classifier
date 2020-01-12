from os import listdir
def get_mp3(path):

    mp3 = []

    for file in listdir(path):
        if ".mp3" in file:
            mp3.append(file)

    return mp3
