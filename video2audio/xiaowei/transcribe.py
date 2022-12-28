# Uses OpenAI Whisper:
# https://github.com/openai/whisper

# to install: pip install git+https://github.com/openai/whisper.git
# to update: pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
import whisper

lang = ["-ru", "-zh"]

model = whisper.load_model("small")

for l in lang:
    audio = "xiaowei" + l + ".mp3"
    text = "xiaowei" + l + ".txt"
    # tiny (32x), base (16x), small (6x), medium (2x), large (1x) to choose
    result = model.transcribe(audio)
    with open(text, "w") as f:
        f.write(result["text"])
