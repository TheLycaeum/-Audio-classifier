from os import listdir,rename, path, mkdir
from key import api_key
from shutil import move, copyfile
from acoustid import match
import logging
import argparse
import os
path = "."
directory_path = []


 
def get_logger():
    l = logging.getLogger('')
    sh = logging.StreamHandler()
 
    l.addHandler(sh)
    fh = logging.FileHandler('prog.log')
    fmt = logging.Formatter('%(asctime)s | %(filename)s:%(lineno)d | %(message)s')
    fh.setFormatter(fmt)
    l.addHandler(fh)
 
    l.setLevel(logging.DEBUG)
    fh.setLevel(logging.DEBUG)
    sh.setLevel(logging.WARNING)
    return l


def get_args():

    parser = argparse.ArgumentParser(description='Classify audio, according to user options')

    parser.add_argument('path',help='path of directory to classify')

    parser.add_argument('-d', '--dire', default = False, action = 'store_true', help = 'if mentioned, classified as artist/title.mp3,if False renamed as artist-title.mp3, by default False')

    parser.add_argument('-i', '--inplace', default = False, action = 'store_true', help = 'if mentioned, classified by not deleting current file,by default False')

    parser.add_argument('-r', '--recurse', default = False, action = 'store_true', help = 'if mentioned, classifies audio files in sub-directories residing in given directory, by default False')

    args = parser.parse_args()
  
    return args.path, args.dire, args.inplace, args.recurse

def get_mp3(audio_path):
    l = get_logger()
    mp3_list = []
    for files in listdir(audio_path):
        if ".mp3" in files:
            mp3_list.append(files)
    if len(mp3_list) == 0:
        l.warning("No mp3 found in folder")
    else:
        l.info("mp3 from %s fetched",audio_path)

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

def get_best_name(names):
    l = get_logger()
    best_name = names[0]
    max_count = 0
    for name in names:
        if names.count(name) > max_count:
            max_count = names.count(name)
            best_name = name
    l.debug("Chosen name:%s",best_name)

    return best_name

def get_paths(dire,old_name, best_name):

    if dire:
        
        artist = best_name.split("-")[0]
        title = best_name.split("-")[1]

        if artist not in listdir(path):

            artist_directory = path + "/" + artist
            mkdir(artist_directory)

        old_path = path + "/" + old_name
        new_path = path + "/"+ artist + "/" + title

        return old_path,new_path

    else:
        
        old_path = path + "/" + old_name
        new_path = path + "/" + best_name
      
        return old_path,new_path

def get_directories(audio_path):

    directory_path =  [x[0] for x in os.walk(audio_path)]
    directory_path.sort()
    return directory_path
def classify(audio_path,dire,inplace):
    
    mp3_list = get_mp3(audio_path)

    for files in mp3_list:
        file_path = audio_path + "/" + files
        artists, titles = get_file_details(file_path)
        names, status = get_names(artists, titles)
        if status:
            l.info("%s details found",files)
            best_name = get_best_name(names)
            old_path, new_path = get_paths(dire,files, best_name)

            if dire:
                if inplace:
                    copyfile(old_path, new_path)
                    l.debug("%s copied to %s",old_path,new_path)
                else:
                    move(old_path,new_path)
                    l.debug("%s moved to %s",old_path,new_path)
            else:

                if inplace and old_path != new_path :
                    copyfile(old_path, new_path)

                else:
                    rename(old_path, new_path)

                l.debug("%s moved to %s",old_path,new_path)
        else:
            l.warning("%s details not found",files)
    
    
if __name__ == "__main__":
    l = get_logger()
    path, dire, inplace, recurse = get_args()
    if recurse:
        directory_path = get_directories(path)

    else:
        classify(path, dire, inplace)
            
        
