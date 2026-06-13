from Transcribe import transcribe
import sounddevice as sd
import scipy.io.wavfile as wav

SAMPLE_RATE = 16000
DURATION = 5

print("Recording for 5 seconds... speak now!")
audio = sd.rec(int(DURATION * SAMPLE_RATE),
               samplerate=SAMPLE_RATE,
               channels=1, dtype='int16')
sd.wait()
wav.write("test_audio.wav", SAMPLE_RATE, audio)
print("Done recording!")

result = transcribe("test_audio.wav")
print(f"Transcribed text: '{result}'")