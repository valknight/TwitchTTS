from gtts import gTTS
from pydub import AudioSegment
from filter import parse_sentence
from twitch.chat import Message
import random
from lookup import lookup
from animalese import animalese

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
        return None
    message_text = parse_sentence(message.text)
    print("{}: {}".format(message.sender, message.text))
    if (data.get('animalese')):
        return animalese(message_text, data.get('pitch'))
    else:
        # generate the message
        tts = gTTS(message_text, lang=data.get('language'), tld=data.get('accent'))
        # save
        tts.save('temp.mp3')
        # reload
    audio = AudioSegment.from_mp3("temp.mp3")
    # change speed and return
    return(speed_change(audio, 0.9 + data.get('pitch') * 0.3))