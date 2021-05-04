import json
from twitch.chat import Message
import random
import sys

accents = [{'language': 'en', 'accent': 'com'},
           {'language': 'en', 'accent': 'com.au'},
           {'language': 'en', 'accent': 'co.uk'},
           {'language': 'en', 'accent': 'co.za'},
           {'language': 'en', 'accent': 'ca'},
           {'language': 'fr', 'accent': 'fr'},
           {'language': 'fr', 'accent': 'ca'},
           {'language': 'es', 'accent': 'es'}]


def read_from_file(key):
    with open('lookup/people.json', 'r') as f:
        data = json.loads(f.read())
        # fix existing voice that is only pitch
        if type(data.get(key)) == float:
            print('normalising data for {}'.format(key))
            new_data = random.choice(accents)
            new_data['pitch'] = data.get(key)
            write_to_file(key, new_data)
            return read_from_file(key)
        return data.get(key)    


def write_to_file(key, value):
    with open('lookup/people.json', 'r') as f:
        existing_data = json.loads(f.read())
    existing_data[key] = value
    with open('lookup/people.json', 'w') as f:
        f.write(json.dumps(existing_data))


def lookup(message: Message) -> float:
    existing = read_from_file(message.sender)
    if existing is not None:
        return existing
    # at this point, no existing data
    # generate new pitch value
    random_value = random.random()
    random_value = (int(random_value * 100)) / 100
    new_data = random.choice(accents)
    new_data['pitch'] = random_value
    write_to_file(message.sender, new_data)
    return read_from_file(message.sender)
