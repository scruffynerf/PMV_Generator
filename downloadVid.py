import youtube_dl
import sys

arg = sys.argv
selectDir = arg[1]
line = arg[2]

print(line)

ydl_opts = {'outtmpl': selectDir + '%(title)s' + '.mp4',
            'format': 'worstaudio/best[height<=720]',
            'videoformat': "mp4",
            'playlist': 'no'}

for attempt in range(3):
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([line])
        break
    except:
        print("Error retrying - Attempt: ", attempt)
        ydl_opts = {'outtmpl': selectDir + '%(title)s' + '.%(ext)s',
                    'format': 'worstaudio/best[height<=480]'}
        pass
