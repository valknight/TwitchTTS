# TwitchTTS

*give your chat a voice!*

## what is this?

this program connects to your twitch chat, and uses Google TTS to **speak** it out loud!

## why is this?

### tldr

- unique voices per chat user with persistency
- animalese (animal crossing style voice) support
- filtering
- prefixes
- ignoring

### long version
many streamers use TTS solutions for their chat. existing TTS solutions like those included in Restream are tied to system TTS voices, and others don't give the flexibility of replacing words, and filtering

this project also assigns each user in your chat their own unique-ish "voice". params such as pitch & accent are chosen randomly.

these values are saved to disk. they can be edited by the streamer, but, is otherwise set-and-forget, with new chatters being given a new identity on their first message sent. previous chatters have their voice remembered, giving each person a little unique attribute compared to the sea of chatters in traditional twitch TTS solutions.

we also have animalese support (more on this below) if you carte about that!

## how to use

### setup 

1. download the project
2. create a python virtual environment
3. activate the virtual env
4. install requirements with `pip install -r requirements.txt`
5. copy `config.example.py` to `config.py`
6. head [here](https://twitchapps.com/tmi/) to get your Twitch chat OAuth token
7. set this in the config file
8. run `python main.py` to connect to chat

### changing the filters / ignored prefixes

head into `prefix.json`. all values in the list in that file will be ignored by default if the sentence begins with it. for example, links are ignored, as well as messages beginning with a `!` (commands!)

you can add or remove your prefixes for your chat bots here

you can also head into `words.json` and change the word replacements in that file. by default i have my channel's word replacements committted, so feel free to go and change them if you do not wish to use the same ones as me. 

an example of what you may wish to do - add your emotes here, so your emotes don't say your channel name every time or make more sense when spoken.

### changing voices

if you have a busy chat, it is recommended to do this while the script isn't running, just to ensure the JSON file isn't written to while in use.

head into the `people.json` file inside the directory `lookup`, and you should find each person have attributes looking as follows

```json
"vknilive": {
        "language": "en",
        "accent": "com",
        "pitch": 0.5
}
```

change these attributes as per the gTTD docs. some examples of working pairs are found in `lookup`. the snippet is below.

```python
accents = [{'language': 'en', 'accent': 'com'},
           {'language': 'en', 'accent': 'com.au'},
           {'language': 'en', 'accent': 'co.uk'},
           {'language': 'en', 'accent': 'co.za'},
           {'language': 'en', 'accent': 'ca'},
           {'language': 'fr', 'accent': 'fr'},
           {'language': 'fr', 'accent': 'ca'},
           {'language': 'es', 'accent': 'es'}]
```

### ignoring users
if you would like to mute a user from TTS (for example - for your bots) add an attribute called `ignored` in `people.json` and set it to true. for example:

```json
"nightbot": {
        "language": "es",
        "accent": "es",
        "pitch": 0.85,
        "ignored": true
}
```

### animalese

currently animalese is supported experimentally. we use work by equalo-official for this - it can be found in `animalese`, and their GitHub repo is [here](https://github.com/equalo-official/animalese-generator).

to enable animalese for a **single** user, set the attribute `animalese` to true, similar to ignored. for example:

```json
"vknilive": {
        "language": "en",
        "accent": "com",
        "pitch": 0.5,
        "animalese": true
}
```

pitch values are used for animalese (vaguely - improvements do need to be made here) so feel free to play around. language and accent do not matter when animalese is enabled, but, please keep them so you can easily turn animalese off for someone.

to enable animalese for *all*, add an option to config.py of

```python
animalese=True
```

with this set, animalese will be the default, and will require users to have an explicit `"animalese": false` set to go back to using google TTS.

animalese may be preferred for users who cannot access google for whatever reason, or, just as a fun novelty for your stream.

## planned features

- sub only TTS 
- vip only TTS
- sub option to change voice attributes via command
- ability to set animalese on and off for specific roles (e.g: animalese for subs only, gTTS for subs only, etc etc)

## contributing

why, thank you! i am very sorry about the state of this code - it's written to work, but, isn't particularly performant or good. cleanup as contributions would be great, as well as building out documentation. anything is appreciated!

i would just like to ask that if you add a library to requirements as part of your contribution that you provide a reasoning for it.

## thanks

many thanks to the maintainers of the following tech

- pydub
- gTTS
- google translate text to speech
- https://github.com/equalo-official/animalese-generator

and finally, thank you to all my viewers on twitch who helped me debug this live! if you'd like to be one of them, feel free to check out my channel at [twitch.tv/VKniLive](https://twitch.tv/VKniLive)