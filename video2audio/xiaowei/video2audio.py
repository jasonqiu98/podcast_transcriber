import moviepy.editor as mp

# extract audio from video
# the original video ignored here
with mp.VideoFileClip("xiaowei.mp4") as my_clip:
    audio = my_clip.audio
    ru_part = audio.subclip(0, 61)
    zh_part = audio.subclip(61)
    # export
    audio.write_audiofile("xiaowei.mp3")
    ru_part.write_audiofile("xiaowei-ru.mp3")
    zh_part.write_audiofile("xiaowei-zh.mp3")
