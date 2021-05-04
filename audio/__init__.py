from gtts import gTTS
from pydub import AudioSegment
from filter import parse_sentence
from twitch.chat import Message
import random
from io import BytesIO
from lookup import lookup
from animalese import animalese as render_animalese
from log import get_logger
import os

# try to import the animalese option if the user has it set
try:
    from config import animalese
except ImportError:
    animalese = False

l = get_logger(__name__)
temp = BytesIO()
def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def generate_sound(message: Message) -> AudioSegment:
    data = lookup(message)
    if (data.get('ignored')):
        l.debug('message from {} ignored'.format(message.sender))
        return None
    l.debug('parsing sentence {}'.format(message.text))
    message_text = parse_sentence(message.text)
    l.info("[chat] {}: {}".format(message.sender, message.text))
    if (data.get('animalese', animalese)):
        l.debug('sending sentence to animalese, and returning')
        return render_animalese(message_text, data.get('pitch'))
    l.debug('sending data to google TTS')
    # generate the message
    tts = gTTS(message_text, lang=data.get(
        'language'), tld=data.get('accent'))
    # save
    tts.save('temp.mp3')
    # reload
    audio = AudioSegment.from_mp3("temp.mp3")
    os.remove('temp.mp3')
    # change speed and return
    return(speed_change(audio, 0.9 + data.get('pitch') * 0.3))
