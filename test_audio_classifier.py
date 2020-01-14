from audio_classifier import get_mp3, get_names
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

