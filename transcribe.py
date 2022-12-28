'''
a simplest case of speech recognition with OpenAI Whisper
interesting libs for audio processing:
- pydub
- pyaudio
- noisereduce
- speech_recognition
- ffmpeg-python
- moviepy
- pygtrans
- nltk
'''

# Uses OpenAI Whisper:
# https://github.com/openai/whisper

# to install: pip install git+https://github.com/openai/whisper.git
# to update: pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
import whisper
import sys
import string
# import pygtrans

from nltk.tokenize import word_tokenize, sent_tokenize

if len(sys.argv) < 2:
    print("please provide the filename")
    sys.exit(1)

path_audio = sys.argv[1]

dot_index = path_audio.rfind(".")
if dot_index == -1:
    title = path_audio
else:
    title = path_audio[:dot_index]
path_md = title + ".md"
path_vocab = title + "_vocab.md"

# tiny (32x), base (16x), small (6x), medium (2x), large (1x) to choose
model = whisper.load_model("small")

result = model.transcribe(path_audio)

with open("vocab_list/target.txt") as f:
    vocab_list = set((l.strip() for l in f.readlines() if l != ""))

# vocab_list = vocab_list.difference({"well"})

with open("vocab_list/gre_1.csv") as f:
    gre_list1 = set((l.split(',')[0] for l in f.readlines()))

with open("vocab_list/gre_2.csv") as f:
    gre_list2 = set((l.split(',')[0] for l in f.readlines()))

gre_list = gre_list1.intersection(gre_list2)

gre_list = gre_list.difference({"list", "court", "check", "weather"})

# google translate
# https://github.com/foyoux/pygtrans
# client = pygtrans.Translate()

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

vocab_set_res = set()
gre_set_res = set()

with open(path_md, "w") as f:
    res = result["text"]
    sentences = sent_tokenize(res)
    f.write("# {}\n\n".format(title))
    for sen in sentences:
        words = word_tokenize(sen)
        for i_w, w in enumerate(words):
            # retrieve vocab from lists
            if w in vocab_list:
                vocab_set_res.add(w)
                w = "**{}**".format(w)
            elif w in gre_list:
                gre_set_res.add(w)
                w = "*{}*".format(w)
            
            # add spaces
            if i_w > 0 and words[i_w - 1] == " $" and isfloat(w):
                pass
            elif w in {"$"}:
                w = " {}".format(w)
            elif w in string.punctuation:
                pass
            elif w in {"n't", "'s", "'ll", "'d", "'m", "'re", "'ve", "..."}:
                pass
            else:
                w = " {}".format(w)

            words[i_w] = w

        sen_res = ''.join(words).strip() + "\n"
        f.write(sen_res)
    # f.write("\n")
    # f.write(client.translate(res, target="zh-CN").translatedText)

# generate vocab
with open(path_vocab, "w") as f:
    f.write("# {}\n\n".format(title))
    f.write("## Frequent\n\n")
    for w in vocab_set_res:
        f.write("- {}\n".format(w))
    f.write("\n")
    f.write("## GRE\n\n")
    for w in gre_set_res:
        f.write("- {}\n".format(w))
