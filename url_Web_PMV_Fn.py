import youtube_dl
from os import listdir
from os.path import isfile, join
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from pydub import AudioSegment
from functions import getHighValues2
from functions import getElementDiff
from functions import videoSplits
from functions import reshapeData
import numpy as np
from IntroTitle import getIntroVid
import subprocess

beepDur = 500  # milliseconds
beepFreq = 440  # Hz


AudioSegment.converter = r"C:/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffmpeg = r"C:/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffprobe = r"C:/ffmpeg/bin/ffprobe.exe"


class Video:
    def __init__(self, name, customStart, customEnd, directory):
        self.name = name
        self.customStart = customStart
        self.customEnd = customEnd
        self.directory = directory



def genPMVs(PMV, dot, sampleHeight, sampleWidth, pythonDir):
    #    file
    #    outDir

    ydl_opts = {'outtmpl': PMV.musicDir + '%(title)s' + '.mp4',
                'format': 'best',
                'playlist': 'no'}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        info_dict = ydl.extract_info(PMV.musicURL, download=False)
        print('downloading?', PMV.musicURL)
        ydl.download([PMV.musicURL])
        musicName = info_dict.get('title', None)

    for vid in PMV.videoURLs:
        print(vid)
        subprocess.call([pythonDir, r"downloadVid.py", PMV.vidDir, vid])

    vidDir = PMV.vidDir

    if PMV.musicType == 'mp4':
        originalVidBool = True
    elif PMV.musicType == 'mp3':
        originalVidBool = False
    else:
        originalVidBool = False

    print(AudioSegment.ffmpeg)

    ################################

    mp3_dir = PMV.musicDir + musicName + dot + 'mp4' # PMV.musicType
    ###############################

    if len(PMV.vidName) == 0:
        PMV.vidName = PMV.userName + ' PMV - ' + musicName
    elif len(PMV.userName) > 0:
        PMV.vidName = PMV.vidName + ' - ' + PMV.userName

    file_out = PMV.outDir + PMV.vidName + dot + 'mp4' #  filetypeout

    print(mp3_dir)


    audioclip = AudioFileClip(mp3_dir)

    print('error1')

    sound = AudioSegment.from_file(mp3_dir, 'mp4')
    print('error2')

    if PMV.trimSong == True:
        sound = sound[PMV.songStart * 1000:PMV.songEnd * 1000]
        audioclip = audioclip.subclip(PMV.songStart, PMV.songEnd)

    print('error3')
    tenSecs = 10 * 1000
    first_10_seconds = sound[:tenSecs]

    ten_data = first_10_seconds._data

    first_ten_data = np.fromstring(ten_data, dtype=np.int16)
    new_ten_data = np.absolute(first_ten_data)

    # %% Music Data

    bitrate = len(new_ten_data) / 10  # raw data to 1 s
    print(bitrate)
    ratio = int(round(bitrate * PMV.granularity, 0))
    raw_data = sound._data

    first_data = np.fromstring(raw_data, dtype=np.int16)
    new_data = np.absolute(first_data)

    reshaped_data = reshapeData(new_data, ratio)

    diff_data = getElementDiff(reshaped_data)

    result = getHighValues2(reshaped_data, diff_data, PMV.sd_scale, PMV.nSplits, PMV.granularity, PMV.min_length)

    print('List of Indices of maximum element :', len(result))

    print(result)

    print(vidDir)

    result.append(len(first_data) / ratio)

    videosIn = list()
    iVids = 0

    for f in listdir(vidDir):
        if isfile:
            if f.endswith(".mp4"):
                if iVids < 120:
                    videosIn.append(f)
                iVids = iVids + 1

    videoData = list()

    for i in videosIn:
        videoData.append(Video(name=i, customStart=0, customEnd=0, directory=vidDir))
        print(i)

    nInVids = len(videosIn)

    iOrig = 0
    origVidName = musicName + dot + PMV.musicType
    if originalVidBool == True:
        while iOrig <= nInVids * PMV.origVidScale:
            videoData.append(Video(name=origVidName, customStart=0, customEnd=0, directory=PMV.musicDir))
            iOrig = iOrig + 1

    nVideos = len(videoData)

    videos = [0] * nVideos

    i = 0
    while i < nVideos:
        if PMV.resize == True:
            vidTemp = VideoFileClip(videoData[i].directory + videoData[i].name).resize(width = sampleWidth) #(sampleWidth, sampleHeight))
            if PMV.flipBool == True and videoData[i].name != origVidName:
                vidTemp2 = mirror_x(vidTemp)
            else:
                vidTemp2 = vidTemp
            videos[i] = vidTemp2
        else:
            videos[i] = VideoFileClip(vidDir + videoData[i].name)

        print('name', 'duration', 'customStart', 'customEnd')

        if originalVidBool == True and videoData[i].name == origVidName:
            if PMV.trimSong == True:
                videoData[i].customEnd = PMV.songEnd
                videoData[i].customStart = PMV.songStart
            else:
                videoData[i].customEnd = videos[i].duration
                videoData[i].customStart = 0  #
            print(videoData[i].name, videos[i].duration, videoData[i].customStart, videoData[i].customEnd, 'Original Video')
        else:
            customStart = PMV.startTime
            subtractEnd = 40

            videoData[i].customEnd = videos[i].duration - subtractEnd
            videoData[i].customStart = customStart
            print(videoData[i].name, videos[i].duration, videoData[i].customStart, videoData[i].customEnd)

        i = i + 1

    clips = videoSplits(result, videos, videoData, first_data, bitrate, PMV.granularity, PMV.randomise, origVidName)


    for attempt in range(3):
        try:

            print('stage 1')
            finalVideo = concatenate_videoclips(clips, method='compose')

            if PMV.originalCrop == True:
                (w, h) = finalVideo.size
                print(PMV.origCropFrac, int(sampleHeight * PMV.origCropFrac), int((1 - PMV.origCropFrac) * sampleHeight), w, h)
                finalVideo = finalVideo.crop(height=int(round((1 - PMV.origCropFrac*2) * sampleHeight, 0)), width = w, x_center=w/2, y_center=h/2)


            print('stage 2')
            finalVideo.volumex(0)

            print('stage 3')
            finalVideo2 = finalVideo.set_audio(audioclip)

            print('stage 4')
            finalVideo2a = fadeout(finalVideo2, 1, final_color=None)

            finalVideo2c = fadein(finalVideo2a, 1, initial_color=None)

            if PMV.addIntro:
                introVideo = getIntroVid(PMV.vidName, PMV.origCropFrac, sampleHeight, PMV.introVidDir, PMV.userName)
                finalVideo3 = concatenate_videoclips([introVideo, finalVideo2c], method='compose')
            else:
                finalVideo3 = finalVideo2c


            print('stage 4')

            print('stage 5')

            finalVideo3.write_videofile(file_out, threads=4, fps=25)
        except OSError as OSErrorMessage:
            print("OSError retrying - Attempt: ", attempt)
            print(OSErrorMessage)
            pass
        else:
            break


    print('stage 6')
    i = 0
    while i < len(videos):
        videos[i].reader.close()
        del videos[i].reader
        del videos[i]
        i = i + 1

    del audioclip.reader
    del audioclip

    print('Finished!')
