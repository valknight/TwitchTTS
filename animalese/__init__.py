import random
from pydub import AudioSegment


def animalese(text: str, pitch: float):
	if pitch < 0.25:
		pitch = "lowest"
	elif pitch < 0.5:
		pitch = "low"
	else:
		pitch = "high"
	text = text.lower()
	sounds = {}
	keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','th','sh',' ','.']
	for index,ltr in enumerate(keys):
		num = index+1
		if num < 10:
			num = '0'+str(num)
		sounds[ltr] = './animalese/sounds/'+pitch+'/sound'+str(num)+'.wav'

	if pitch == 'med':
		rnd_factor = .35
	else:
		rnd_factor = .25
	
	infiles = []

	for i, char in enumerate(text):
		try:
			if char == 's' and text[i+1] == 'h': #test for 'sh' sound
				infiles.append(sounds['sh'])
				continue
			elif char == 't' and text[i+1] == 'h': #test for 'th' sound
				infiles.append(sounds['th'])
				continue
			elif char == 'h' and (text[i-1] == 's' or text[i-1] == 't'): #test if previous letter was 's' or 's' and current letter is 'h'
				continue
			elif char == ',' or char == '?':
				infiles.append(sounds['.'])
				continue
			elif char == text[i-1]: #skip repeat letters
				continue
		except:
			pass
		if not char.isalpha() and char != '.': # skip characters that are not letters or periods. 
			continue
		infiles.append(sounds[char])
	combined_sounds = None

	for index,sound in enumerate(infiles):
		tempsound = AudioSegment.from_wav(sound)
		if text[len(text)-1] == '?':
			if index >= len(infiles)*.8:
				octaves = random.random() * rnd_factor + (index-index*.8) * .1 + 2.1 # shift the pitch up by half an octave (speed will increase proportionally)
			else:
				octaves = random.random() * rnd_factor + 2.0
		else:
			octaves = random.random() * rnd_factor + 2.3 # shift the pitch up by half an octave (speed will increase proportionally)
		new_sample_rate = int(tempsound.frame_rate * (1.8 ** octaves))
		new_sound = tempsound._spawn(tempsound.raw_data, overrides={'frame_rate': new_sample_rate})
		new_sound = new_sound.set_frame_rate(44100) # set uniform sample rate
		combined_sounds = new_sound if combined_sounds is None else combined_sounds + new_sound
	return combined_sounds
