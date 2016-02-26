#sound_module.py
import webbrowser

sound = [
"It gets bigger when i pull.mp3"
]

play_sound("It gets bigger when i pull.mp3")

def play_sound(string s):
	webbrowser.open(s)
