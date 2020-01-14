from audio_classifier import get_mp3, get_names, choose_name
import unittest
from unittest import mock

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

def test_get_file_details():
    pass
            
def test_get_possible_names_no_records():
    artists = []
    titles = []

    actual = get_names(artists, titles)
    expected = "No Records Found"
    assert actual == expected

def test_get_possible_names_with_records():
    artists = ['John','John Denver','John D']
    titles = ['Country roads','Country roads','Take me Home']

    actual = get_names(artists, titles)
    expected = "Choose Name:\n1 John-Country roads.mp3\n2 John Denver-Country roads.mp3\n3 John D-Take me Home.mp3\n"
    assert actual == expected


def test_choose_name():
    choice = 2
    artists = ['John','John Denver','John D']
    titles = ['Country roads','Country roads','Take me Home']

    expected = "John Denver-Country roads.mp3"
    actual = choose_name(artists, titles, choice)
    
