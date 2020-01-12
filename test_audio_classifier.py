from audio_classifier import get_mp3

def test_get_mp3_no_mp3():

    expected = []
    actual = get_mp3("/home/majid")

    assert actual == expected

def test_get_mp3_with_mp3():

    expected = ['Oasis - Wonderwall (Official Video).mp3', 'Stand By Me, Ben E King, 1961.mp3', "Bob Dylan - Blowin' in the Wind (Audio).mp3"]
    actual = get_mp3(".")

    assert actual == expected
