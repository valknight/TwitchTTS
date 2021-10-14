import json
import random
import sys
import os

from twitch.chat import Message

from log import get_logger
from config import accents


l = get_logger(__name__)


def read_from_file(key):
    if not os.path.isfile('lookup/people.json'):
        with open('lookup/people.json', 'w') as f:
            f.write(json.dumps({}))

    l.debug('[read] {}'.format(key))
    with open('lookup/people.json', 'r') as f:
        data = json.loads(f.read())
        # fix existing voice that is only pitch
        if type(data.get(key)) == float:
            l.warn('only found pitch data for {} - attempting to normalise'.format(key))
            new_data = random.choice(accents)
            new_data['pitch'] = data.get(key)
            write_to_file(key, new_data)
            return read_from_file(key)
        return data.get(key)


def write_to_file(key, value):
    l.debug('[write] {} <- {}'.format(key, value))
    with open('lookup/people.json', 'r') as f:
        existing_data = json.loads(f.read())
    existing_data[key] = value
    with open('lookup/people.json', 'w') as f:
        f.write(json.dumps(existing_data))


def lookup(message: Message):
    existing = read_from_file(message.sender)
    if existing is not None:
        return existing
    # at this point, no existing data
    # generate new pitch value
    l.debug('[new viewer] {} - setting data'.format(message.sender))
    random_value = random.random()
    random_value = (int(random_value * 100)) / 100
    new_data = random.choice(accents)
    new_data['pitch'] = random_value
    write_to_file(message.sender, new_data)
    return read_from_file(message.sender)
