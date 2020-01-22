#**Introduction**

Audio Classifier helps you to sort your messed up music directories with no proper name for mp3 files. It renames and classifies mp3 files with records from [AcoustID](acoustid.org) web service.

User register Application [AcoustID](acoustid.org) and get the API key. Copy API key in key.py file.

#**Working**

-Read directory to classify from user
-Read classifying option from the user
-List mp3 files in directory
-Get file details from database.
-Classify the files according to user choice

#**Requirements**

Check _requirements.txt_

#**Usage**

```
Classify audio with records from acoustid.org, according to user options

positional arguments:
  path           path of directory to classify

optional arguments:
  -h, --help     show this help message and exit
  -d, --dire     if mentioned, classified as artist/title.mp3,if False renamed
                 as artist-title.mp3, by default False
  -i, --inplace  if mentioned, classified keeping current file,by default
                 False
  -r, --recurse  if mentioned, classifies audio files in sub-directories of
                 given path, by default False
```

