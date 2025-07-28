import sounddevice as sd
import soundfile as sf

print("🎤 开始录音，说点什么吧（录5秒）...")
duration = 5  # 秒
fs = 16000
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
sf.write("your_voice.wav", audio, fs)
print("✅ 已保存到 your_voice.wav")
