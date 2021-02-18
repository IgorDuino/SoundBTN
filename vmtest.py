from pygame._sdl2 import get_num_audio_devices, get_audio_device_name
from pygame import mixer

mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
mixer.music.load("sounds/29-bruh.mp3")
mixer.music.play()
