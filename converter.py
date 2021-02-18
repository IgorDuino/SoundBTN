from pydub import AudioSegment

AudioSegment.ffmpeg = "D:/Projects/SoundBTN/venv/Lib/site-packages/ffmpeg"
sound = AudioSegment.from_mp3("sounds/29-bruh.mp3")
