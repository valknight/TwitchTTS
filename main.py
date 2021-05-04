
from pydub.playback import play
from audio import generate_sound
from config import twitch_token
import twitch
import gtts.tts
def handle(message):
    sound = generate_sound(message)
    if sound is not None:
        play(sound)

twitch.Chat(channel='#vknilive', nickname='vknilive', oauth=twitch_token).subscribe(lambda message: handle(message))