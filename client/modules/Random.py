import re

WORDS = ["FIST BUMP"]

def handle(text, mic, profile):
	mic.speaker.play(jasperpath.data('audio', 'fist_bump.wav'))

def isValid(text):
	return (bool(re.search(r'\bfist bump\b', text, re.IGNORECASE)))
