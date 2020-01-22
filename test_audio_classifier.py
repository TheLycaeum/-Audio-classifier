from audio_classifier import get_mp3, get_names, get_best_name, get_paths, get_directories
from unittest import mock
import unittest
import os
import shutil


class Test_get_mp3(unittest.TestCase):

    def test_get_mp3(self):
        with mock.patch('audio_classifier.listdir') as mocked_listdir:
            mocked_listdir.return_value = ['1.py','2.mp3','3.mp3','4.mp3','n.py']
            mp3_list = get_mp3(".")
            self.assertEqual(len(mp3_list),3)


    def test_get_mp3_no_mp3(self):
        with mock.patch('audio_classifier.listdir') as mocked_listdir:
            mocked_listdir.return_value = ['1.py','2.py','3.txt','4','n.py']
            mp3_list = get_mp3(".")
            self.assertEqual(len(mp3_list),0)
            
def test_get_possible_names_no_records():

    artists = []
    titles = []

    actual = get_names(artists, titles)
    expected = [],False
    assert actual == expected

def test_get_possible_names_with_records():
    artists = ['John','John Denver','John D','John Denver',None]
    titles = ['Country roads','Country roads','Take me Home','Country roads',None]

    actual = get_names(artists, titles)
    expected = ["John-Country roads.mp3", "John Denver-Country roads.mp3","John D-Take me Home.mp3","John Denver-Country roads.mp3"],True
    assert actual == expected

def test_get_best_name():
    names = ["John-Country roads.mp3", "John Denver-Country roads.mp3","John D-Take me Home.mp3","John Denver-Country roads.mp3"]

    expected = "John Denver-Country roads.mp3"
    actual = get_best_name(names) 

    assert expected == actual

def test_get_paths_dire_true():
    dire = True
    old_name = "abc.mp3"
    best_name = "John Denver-Country roads.mp3"

    assert get_paths(dire, old_name, best_name) == ("./abc.mp3","./John Denver/Country roads.mp3")

def test_get_paths_dire_false():
    dire = False
    old_name = "abc.mp3"
    best_name = "John Denver-Country roads.mp3"

    assert get_paths(dire,old_name, best_name) == ("./abc.mp3","./John Denver-Country roads.mp3")

def test_get_directories_single_level():
    os.mkdir('/tmp/a')
    os.mkdir('/tmp/a/1')
    os.mkdir('/tmp/a/2')
    os.mkdir('/tmp/a/3')

    actual = get_directories("/tmp/a")
    expected = ['/tmp/a','/tmp/a/1','/tmp/a/2','/tmp/a/3']
    shutil.rmtree('/tmp/a')

    assert actual == expected
