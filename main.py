
from pydub.playback import play
from audio import generate_sound
import config
from log import get_logger
import traceback
import twitch
import gtts.tts

l = get_logger(__name__)


def handle(message):
    try:
        sound = generate_sound(message)
        if sound is not None:
            play(sound)
    except gtts.tts.gTTSError:
        l.error('{}'.format(traceback.format_exc()))
        l.error('check region is correct for a person if you manually edited it')
    except AssertionError:
        l.info('no text to speak! skipping')


def connect_to_chat(channel: str, nickname: str, oauth: str) -> twitch.Chat:
    l.info('connecting to {}'.format(channel))
    return twitch.Chat(channel=channel, nickname=nickname,
                       oauth=oauth)

l.info("starting...")

if __name__ == '__main__':
    chat = connect_to_chat(config.channel, config.nickname, config.twitch_token)
    chat.subscribe(lambda message: handle(message))