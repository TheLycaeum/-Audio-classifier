from audio_classifier import get_mp3
def test_get_mp3_no_mp3():

    expected = []
    actual = get_mp3("/home/majid")

    assert actual == expected

