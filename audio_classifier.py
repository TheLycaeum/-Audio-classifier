from os import listdir,rename, path, mkdir
from key import api_key
from shutil import move, copyfile
from acoustid import match
import logging
import argparse
import os
import os.path
path = "."
directory_path = []


 
def get_logger():
    l = logging.getLogger('')
    sh = logging.StreamHandler()
 
    l.addHandler(sh)
    fh = logging.FileHandler('classified.log')
    fmt = logging.Formatter('%(asctime)s | %(filename)s:%(lineno)d | %(message)s')
    fh.setFormatter(fmt)
    l.addHandler(fh)
 
    l.setLevel(logging.DEBUG)
    fh.setLevel(logging.DEBUG)
    sh.setLevel(logging.WARNING)
    return l


def get_args():

    parser = argparse.ArgumentParser(description='Classify audio with records from acoustid.org, according to user options')

    parser.add_argument('path',help='path of directory to classify')

    parser.add_argument('-d', '--dire', default = False, action = 'store_true', help = 'if mentioned, classified as artist/title.mp3,if False renamed as artist-title.mp3, by default False')

    parser.add_argument('-i', '--inplace', default = False, action = 'store_true', help = 'if mentioned, classified keeping current file,by default False')

    parser.add_argument('-r', '--recurse', default = False, action = 'store_true', help = 'if mentioned, classifies audio files in sub-directories of given path, by default False')

    args = parser.parse_args()
  
    return args.path, args.dire, args.inplace, args.recurse

def get_mp3(audio_path):
    "list mp3 files in audio_path" ## Use docstrings
    l = get_logger()
    mp3_list = []
    for files in listdir(audio_path): ## Try using glob instead of os.listdir
        if ".mp3" in files:
            mp3_list.append(files)
    if len(mp3_list) == 0:
        l.warning("No mp3 found in folder %s",audio_path)
    else:
        l.info("mp3 from %s fetched",audio_path)

    return mp3_list

def get_file_details(files): # get details from acoustid, with acoustid.match
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

def get_best_name(names): # Choose Best possible name. Most occuring name is names list is right 
    l = get_logger()
    best_name = names[0]
    max_count = 0
    for name in names:
        if names.count(name) > max_count:
            max_count = names.count(name)
            best_name = name
    l.info("Chosen name:%s",best_name)

    return best_name

def get_paths(dire,old_name, best_name): # new path is returned. 

    if dire:
        
        artist = best_name.split("-")[0]
        title = best_name.split("-")[1]

        if artist not in listdir(path):

            artist_directory = os.path.join(path,artist)
            mkdir(artist_directory)

        new_path = path + "/"+ artist + "/" + title

        return new_path

    else:
        
        new_path = path + "/" + best_name
      
        return new_path

def get_directories(audio_path): # if recurse, all subdirectories are returned

    directory_path =  [x[0] for x in os.walk(audio_path)]
    directory_path.sort()

    return directory_path

def classify(audio_path,dire,inplace): # Classification or rename done here, shutil.copy, shutil.move , os.rename used
    l = get_logger()
    mp3_list = get_mp3(audio_path)

    for files in mp3_list:
        file_path = audio_path + "/" + files
        artists, titles = get_file_details(file_path)
        names, status = get_names(artists, titles)
        if status:
            l.info("%s details found",files)
            best_name = get_best_name(names)
            new_path = get_paths(dire, files, best_name)

            if dire:

                if inplace and file_path != new_path :
                    print(file_path, new_path, inplace)
                    copyfile(file_path, new_path)
                    l.debug("%s copied to %s", file_path,new_path)
                   
                else:
                    move(file_path,new_path)
                    l.debug("%s moved to %s", file_path, new_path)
            else:

                if inplace and file_path != new_path :
                    copyfile(file_path, new_path)
                    l.debug("%s copied to %s", file_path,new_path)

                else:
                    rename(file_path, new_path)
                    l.debug("%s moved to %s",file_path,new_path)
        else:
            l.warning("%s records not found",files)
    
     
if __name__ == "__main__":
    path, dire, inplace, recurse = get_args()
    if recurse:
        directory_path = get_directories(path)
        for directory in directory_path:
            classify(directory, dire, inplace)

    else:
        classify(path, dire, inplace)
            
        
