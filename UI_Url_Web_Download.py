import os
import wx
from wx.lib.masked import *
import wx.lib.agw.floatspin as FS
from threading import Thread
from pydub import AudioSegment
from url_Web_PMV_Fn import genPMVs

beepDur = 500  # milliseconds
beepFreq = 440  # Hz

sampleWidth = 1280  # 360#
sampleHeight = 720  # 640#

AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = "C:\\ffmpeg\\bin\\ffprobe.exe"


class VideoDownload(Thread):
    def __init__(self, vidName, musicType, startEndTime, sd_scale, nSplits, randomise, videoURLs,
                 musicURL, songStart, songEnd, granularity, min_length, originalCrop, origCropFrac,
                 origVidScale, resize, flipBool, trimSong, pythonDir, addIntro, introVidDir, userName,
                 musicDir, vidDir, outDir):
        self.vidName = vidName
        self.musicType = musicType
        self.startTime = startEndTime[0]
        self.subtractEnd = startEndTime[1]
        self.sd_scale = sd_scale
        self.nSplits = nSplits
        self.randomise = randomise
        self.videoURLs = videoURLs
        self.musicURL = musicURL
        self.songStart = songStart
        self.songEnd = songEnd
        self.granularity = granularity
        self.min_length = min_length
        self.originalCrop = originalCrop
        self.origCropFrac = origCropFrac
        self.origVidScale = origVidScale
        self.resize = resize
        self.flipBool = flipBool
        self.trimSong = trimSong
        self.pythonDir = pythonDir
        self.addIntro = addIntro
        self.introVidDir = introVidDir
        self.userName = userName
        self.musicDir = musicDir
        self.vidDir = vidDir
        self.outDir = outDir
        Thread.__init__(self)
        self.start()


    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.

        genPMVs(self, dot, sampleHeight, sampleWidth, pythonDir)

pythonDir = r"" ########## Put your phython.exe directory here - e.g. C:/User/.../python.exe ###############
dot = "."
iProject = 0


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='PMV Editor (Public Release) v1.1', size=(900, 600))
        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        ### Predfined Variables
        projectDir = os.getcwd()
        self.customVidDir = projectDir + r"/TempVids//"
        self.customMusicDir = projectDir + r"/TempMusic//"
        self.customOutputDir = projectDir + r"/NewPMVs//"
        self.introVidName = r''  ########## Change this for own intro video file if available - e.g. C:/User/.../IntroVid.mp4 ##########
        self.username = '' ########## Change this to own username if desired ##########
        print(self.customVidDir)

        spacing = 2

        ######################
        ## Video Directories
        #####################

        dirSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vidDirectory = wx.Button(panel, label="Select Input Video Directory")
        self.vidDirectory.Bind(wx.EVT_BUTTON, self.OnOpenVid)
        dirSizer.Add(self.vidDirectory, 1, wx.ALL | wx.EXPAND, spacing)
        self.musicDirectory = wx.Button(panel, label="Select Input Music Directory")
        self.musicDirectory.Bind(wx.EVT_BUTTON, self.OnOpenMusic)
        dirSizer.Add(self.musicDirectory, 1, wx.ALL | wx.EXPAND, spacing)
        self.outputDirectory = wx.Button(panel, label="Select Output PMV Directory")
        self.outputDirectory.Bind(wx.EVT_BUTTON, self.OnOpenOutput)
        dirSizer.Add(self.outputDirectory, 1, wx.ALL | wx.EXPAND, spacing)
        mainSizer.Add(dirSizer, 0, wx.ALL | wx.EXPAND, spacing)

        musicSizerOptionsSelect = wx.BoxSizer(wx.HORIZONTAL)
        musicSizerOptions = wx.BoxSizer(wx.HORIZONTAL)
        musicSizerTrim = wx.BoxSizer(wx.HORIZONTAL)
        musicSizerOccurance = wx.BoxSizer(wx.HORIZONTAL)

        musicSizerBools = wx.BoxSizer(wx.HORIZONTAL)
        musicSizerBoolTitles = wx.BoxSizer(wx.VERTICAL)
        musicSizerBoolSelction = wx.BoxSizer(wx.VERTICAL)

        self.origVidLabel = wx.StaticText(panel, -1, 'Use Music Video:')
        musicSizerBoolTitles.Add(self.origVidLabel, 0, wx.ALL, spacing)
        self.origVidBool = wx.CheckBox(panel)
        self.origVidBool.SetValue(False)
        musicSizerBoolSelction.Add(self.origVidBool, 0, wx.ALL, spacing)

        self.origVidTrimLabel = wx.StaticText(panel, -1, 'Trim Music:')
        musicSizerBoolTitles.Add(self.origVidTrimLabel, 0, wx.ALL, spacing)
        self.origVidTrim = wx.CheckBox(panel)
        self.origVidTrim.SetValue(False)
        musicSizerBoolSelction.Add(self.origVidTrim, 0, wx.ALL, spacing)

        musicSizerBools.Add(musicSizerBoolTitles, 1, wx.ALL | wx.EXPAND, spacing)
        musicSizerBools.Add(musicSizerBoolSelction, 1, wx.ALL | wx.EXPAND, spacing)

        musicSizerOptions.Add(musicSizerBools, 0, wx.ALL, spacing)

        self.origVidStartLabel = wx.StaticText(panel, -1, 'Start:')
        musicSizerTrim.Add(self.origVidStartLabel, 0, wx.ALL | wx.EXPAND, spacing)
        self.origVidStart = NumCtrl(panel, value=0)
        musicSizerTrim.Add(self.origVidStart, 0, wx.ALL | wx.EXPAND, spacing)
        self.origVidEndLabel = wx.StaticText(panel, -1, 'End:')
        musicSizerTrim.Add(self.origVidEndLabel, 0, wx.ALL | wx.EXPAND, spacing)
        self.origVidEnd = NumCtrl(panel, value=240)
        musicSizerTrim.Add(self.origVidEnd, 0, wx.ALL | wx.EXPAND, spacing)

        musicSizerOptions.Add(musicSizerTrim, 0, wx.ALL | wx.EXPAND, spacing)

        self.occuranceLabel = wx.StaticText(panel, -1, 'Occurance Factor:')
        musicSizerOccurance.Add(self.occuranceLabel, 0, wx.ALL | wx.EXPAND, spacing)
        self.occuranceSlider = FS.FloatSpin(panel, value=0.4, min_val=0.0, max_val=5.0, increment=0.05, agwStyle=FS.FS_LEFT)
        self.occuranceSlider.SetDigits(3)
        musicSizerOccurance.Add(self.occuranceSlider, 0, wx.ALL | wx.EXPAND, spacing)

        musicSizerOptions.Add(musicSizerOccurance, 0, wx.ALL | wx.EXPAND, spacing)

        musicSizerOptionsSelect.Add(musicSizerOptions, 1, wx.ALL | wx.EXPAND, spacing)

        mainSizer.Add(musicSizerOptionsSelect, 0, wx.ALL | wx.EXPAND, spacing)

        ######################
        ## Music Selection
        #####################

        musicSelectSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.musicSelectSizerLabel = wx.StaticText(panel, -1, 'Enter Music URL Here: ')
        musicSelectSizer.Add(self.musicSelectSizerLabel, 0, wx.ALL | wx.EXPAND, spacing)
        self.musicSelectSizerEnter = wx.TextCtrl(panel, value='')
        musicSelectSizer.Add(self.musicSelectSizerEnter, 1, wx.ALL | wx.EXPAND, spacing)
        mainSizer.Add(musicSelectSizer, 0, wx.ALL | wx.EXPAND, spacing)

        ######################
        ## Video Selection
        #####################

        videoSelectSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.videoSelectSizerLabel = wx.StaticText(panel, -1, 'Enter Video URLs Here:')
        videoSelectSizer.Add(self.videoSelectSizerLabel, 0, wx.ALL | wx.EXPAND, spacing)
        self.videoSelectSizerEnter = wx.TextCtrl(panel, value='', style=wx.TE_MULTILINE)
        videoSelectSizer.Add(self.videoSelectSizerEnter, 1, wx.ALL | wx.EXPAND, spacing)
        mainSizer.Add(videoSelectSizer, 1, wx.ALL | wx.EXPAND, spacing)

        ######################
        ## Video Trimming
        #####################

        self.vidDetailsTitle = wx.StaticText(panel, -1, 'Video Details')
        mainSizer.Add(self.vidDetailsTitle, 0, wx.ALL | wx.EXPAND, spacing)

        vidDetSizer = wx.BoxSizer(wx.HORIZONTAL)

        cropBoolSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.origVidCropLabel = wx.StaticText(panel, -1, 'Crop to Wide View:')
        cropBoolSizer.Add(self.origVidCropLabel, 0, wx.ALL, spacing)
        self.origVidCrop = wx.CheckBox(panel)
        self.origVidCrop.SetValue(True)
        cropBoolSizer.Add(self.origVidCrop, 0, wx.ALL, spacing)
        vidDetSizer.Add(cropBoolSizer, 0, wx.ALL | wx.EXPAND, spacing)

        cropValSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.origVidCropFracLabel = wx.StaticText(panel, -1, 'Crop Percentage:')
        cropValSizer.Add(self.origVidCropFracLabel, 1, wx.ALL | wx.EXPAND, spacing)
        self.origVidCropFracSlider = FS.FloatSpin(panel, value=0.14, min_val=0.0, max_val=0.5, increment=0.005, agwStyle=FS.FS_LEFT)
        self.origVidCropFracSlider.SetDigits(3)
        cropValSizer.Add(self.origVidCropFracSlider, 0, wx.ALL | wx.EXPAND, spacing)
        vidDetSizer.Add(cropValSizer, 0, wx.ALL | wx.EXPAND, spacing)

        addIntroSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addIntroLabel = wx.StaticText(panel, -1, 'Add intro video:')
        addIntroSizer.Add(self.addIntroLabel, 0, wx.ALL | wx.EXPAND, spacing)
        self.addIntroBool = wx.CheckBox(panel)
        self.addIntroBool.SetValue(False)
        addIntroSizer.Add(self.addIntroBool, 0, wx.ALL | wx.EXPAND, spacing)
        vidDetSizer.Add(addIntroSizer, 0, wx.ALL | wx.EXPAND, spacing)


        self.introVidDirectory = wx.Button(panel, label="Select Intro Video (Optional)",)
        self.introVidDirectory.Bind(wx.EVT_BUTTON, self.OnOpenIntro)
        vidDetSizer.Add(self.introVidDirectory, 1, wx.ALL | wx.EXPAND, spacing)

        mainSizer.Add(vidDetSizer, 0, wx.ALL | wx.EXPAND, spacing)

        vidTrimSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.startTrimLabel = wx.StaticText(panel, -1, 'Start Time:')
        vidTrimSizer.Add(self.startTrimLabel, 1, wx.ALL | wx.EXPAND, spacing)
        self.startTrim = NumCtrl(panel, value=30)
        vidTrimSizer.Add(self.startTrim, 1, wx.ALL | wx.EXPAND, spacing)

        self.num2Label = wx.StaticText(panel, -1, 'End Trim:')
        vidTrimSizer.Add(self.num2Label, 1, wx.ALL | wx.EXPAND, spacing)
        self.endTrim = NumCtrl(panel, value=20)
        vidTrimSizer.Add(self.endTrim, 1, wx.ALL | wx.EXPAND, spacing)
        mainSizer.Add(vidTrimSizer, 0, wx.ALL | wx.EXPAND, spacing)

        ######################
        ## More configuration
        #####################

        vidDetailsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.nSplitsLabel = wx.StaticText(panel, -1, 'nSplits:')
        vidDetailsSizer.Add(self.nSplitsLabel, 1, wx.ALL | wx.EXPAND, spacing)
        self.nSplitsSlider = wx.Slider(panel, value=4, minValue=1, maxValue=100,
                                       style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        vidDetailsSizer.Add(self.nSplitsSlider, 1, wx.ALL | wx.EXPAND, spacing)

        self.sdLabel = wx.StaticText(panel, -1, 'SD for clip switch:')
        vidDetailsSizer.Add(self.sdLabel, 1, wx.ALL | wx.EXPAND, spacing)
        self.sdSlider = FS.FloatSpin(panel, value=1.4, min_val=0.0, max_val=3.0, increment=0.05, agwStyle=FS.FS_LEFT)
        self.sdSlider.SetDigits(3)
        vidDetailsSizer.Add(self.sdSlider, 1, wx.ALL | wx.EXPAND, spacing)
        mainSizer.Add(vidDetailsSizer, 0, wx.ALL | wx.EXPAND, spacing)

        vidDetailsSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.granularityLabel = wx.StaticText(panel, -1, 'Granularity:')
        vidDetailsSizer2.Add(self.granularityLabel, 1, wx.ALL | wx.EXPAND, spacing)
        self.granularitySlider = FS.FloatSpin(panel, value=0.04, min_val=0.0, max_val=0.4, increment=0.01, agwStyle=FS.FS_LEFT)
        self.granularitySlider.SetDigits(3)
        vidDetailsSizer2.Add(self.granularitySlider, 1, wx.ALL | wx.EXPAND, spacing)

        self.minClipLengthLabel = wx.StaticText(panel, -1, 'Min Clip Length')
        vidDetailsSizer2.Add(self.minClipLengthLabel, 1, wx.ALL | wx.EXPAND, spacing)
        self.minClipLengthSlider = FS.FloatSpin(panel, value=0.24, min_val=0.0, max_val=0.8, increment=0.01, agwStyle=FS.FS_LEFT)
        self.minClipLengthSlider.SetDigits(3)
        vidDetailsSizer2.Add(self.minClipLengthSlider, 1, wx.ALL | wx.EXPAND, spacing)
        mainSizer.Add(vidDetailsSizer2, 0, wx.ALL | wx.EXPAND, spacing)

        ######################
        ## Other flags
        #####################

        vidBoolSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.randomiseLabel = wx.StaticText(panel, -1, 'Randomise:')
        vidBoolSizer.Add(self.randomiseLabel, 1, wx.ALL, spacing)
        self.randomiseCB = wx.CheckBox(panel)
        self.randomiseCB.SetValue(True)
        vidBoolSizer.Add(self.randomiseCB, 1, wx.ALL, spacing)

        self.resizeLabel = wx.StaticText(panel, -1, 'Resize:')
        vidBoolSizer.Add(self.resizeLabel, 1, wx.ALL, spacing)
        self.resizeCB = wx.CheckBox(panel)
        self.resizeCB.SetValue(True)
        vidBoolSizer.Add(self.resizeCB, 1, wx.ALL, spacing)

        self.flipVidLabel = wx.StaticText(panel, -1, 'Flip Vids:')
        vidBoolSizer.Add(self.flipVidLabel, 1, wx.ALL, spacing)
        self.flipVidCB = wx.CheckBox(panel)
        self.flipVidCB.SetValue(False)
        vidBoolSizer.Add(self.flipVidCB, 1, wx.ALL, spacing)
        mainSizer.Add(vidBoolSizer, 0, wx.ALL | wx.EXPAND, spacing)

        ######################
        ## Output Name
        #####################

        outputFileSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.userNameLabel = wx.StaticText(panel, -1, 'User Name:')
        outputFileSizer.Add(self.userNameLabel, 1, wx.ALL | wx.EXPAND, spacing)
        self.userNameName = wx.TextCtrl(panel, value=self.username)
        outputFileSizer.Add(self.userNameName, 1, wx.ALL | wx.EXPAND, spacing)
        # vidDetSizer.Add(outputFileSizer, 0, wx.ALL | wx.EXPAND, spacing)

        self.outputFileLabel = wx.StaticText(panel, -1, 'Output File Name:')
        outputFileSizer.Add(self.outputFileLabel, 1, wx.ALL | wx.EXPAND, spacing)
        self.outputName2 = wx.TextCtrl(panel, value='')
        outputFileSizer.Add(self.outputName2, 1, wx.ALL | wx.EXPAND, spacing)


        mainSizer.Add(outputFileSizer, 0, wx.ALL | wx.EXPAND, spacing)

        ######################
        ## Log Display
        #####################

        self.logger = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        ######################
        ## Button
        #####################

        self.runButton = wx.Button(panel, label='Start')
        self.runButton.Bind(wx.EVT_BUTTON, self.on_press)
        mainSizer.Add(self.runButton, 0, wx.ALL | wx.CENTER, spacing)

        mainSizer.Add(self.logger, 0, wx.ALL | wx.EXPAND, spacing)

        panel.SetSizer(mainSizer)

        self.Show()

    def OnOpenIntro(self, event):
        dlg = wx.FileDialog(self, "Choose a file", style=wx.FD_OPEN, defaultFile=self.introVidName)
        if dlg.ShowModal() == wx.ID_OK:
            self.introVidName = dlg.GetPath()
        dlg.Destroy()

    def OnOpenVid(self, event):
        dlg = wx.DirDialog(self, "Choose a file", defaultPath=self.customVidDir, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.customVidDir = dlg.Path + "/"
        dlg.Destroy()

    def OnOpenMusic(self, event):
        dlg = wx.DirDialog(self, "Choose a file", defaultPath=self.customMusicDir, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.customMusicDir = dlg.Path + "/"
        dlg.Destroy()

    def OnOpenOutput(self, event):
        dlg = wx.DirDialog(self, "Choose a file", defaultPath=self.customOutputDir, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.customOutputDir = dlg.Path + "/"
        dlg.Destroy()

    def on_press(self, event):
        self.logger.ChangeValue("Making PMV, please wait...")

        if self.origVidBool.GetValue() == True:
            musicType = 'mp4'
        else:
            musicType = 'mp3'

        videoURL_List = self.videoSelectSizerEnter.GetValue().split('\n')

        self.Video = VideoDownload(vidName=self.outputName2.GetValue(),
                              musicType=musicType,
                              startEndTime=[self.startTrim.GetValue(), self.endTrim.GetValue()],
                              sd_scale=self.sdSlider.GetValue(),
                              nSplits=self.nSplitsSlider.GetValue(),
                              randomise=self.randomiseCB.GetValue(),
                              videoURLs = videoURL_List,
                              musicURL = self.musicSelectSizerEnter.GetValue(),
                              songStart = self.origVidStart.GetValue(),
                              songEnd = self.origVidEnd.GetValue(),
                              granularity = self.granularitySlider.GetValue(),
                              min_length = self.minClipLengthSlider.GetValue(),
                              originalCrop = self.origVidCrop.GetValue(),
                              origCropFrac = self.origVidCropFracSlider.GetValue(),
                              origVidScale = self.occuranceSlider.GetValue(),
                              resize = self.resizeCB.GetValue(),
                              flipBool = self.flipVidCB.GetValue(),
                              trimSong = self.origVidTrim.GetValue(),
                              pythonDir = pythonDir[iProject],
                              addIntro = self.addIntroBool.GetValue(),
                              introVidDir = self.introVidName, #.GetValue(),
                              userName = self.userNameName.GetValue(),
                              musicDir = self.customMusicDir,
                              vidDir = self.customVidDir,
                              outDir = self.customOutputDir
                              )

        self.logger.ChangeValue("Making PMV! Check terminal for progress.")

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()