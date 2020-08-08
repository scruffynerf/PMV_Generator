PMV Editor for Python v1.1

///////////////////////////////////////
Setup
///////////////////////////////////////

Install python and an interpreter:
	https://www.jetbrains.com/pycharm/ & https://www.python.org/downloads/
	Or
	https://www.anaconda.com/products/individual

Install ffmpeg as well
	https://ffmpeg.org/download.html

Install ImageMagick if choose to use text on intro videos
	https://imagemagick.org/script/download.php


Once python and interpreter are set up, will need to install the relevant python packages.
(can be found at the top of the relevant scripts).

If issues occur installing certain packages, please refer to the individual help pages.


Need to also change a couple of lines of code to apply to your PC.
In "UI_Url_Web_Download.py"
	line 61 - Add your own python.exe in here r"___"
		  Can find this exe in pycharm by File->Settings->Project->Project Interpreter
	line 77 - (Optional) Add path to your own intro video
	line 78 - (Optional) Add your own username


///////////////////////////////////////
Launch UI
///////////////////////////////////////
Run UI_Url_Web_Download.py to launch the UI

///////////////////////////////////////
How to use
///////////////////////////////////////
Selecting Directories
	Top 3 buttons default to TempVids, TempMusic and NewPMVs folders in current directory so don't need to be changed unless you want a different location to store downloaded music, videos and outputs
	The program works by downloading videos from urls entered by the user. For music files, this is a neccessity but for videos it will take all videos in the selected video folder.
	So you don't need to download videos, can use those already stored in your seelected folder.
	But will always need to download music.

Using music videos
	Tick the Use Music Video checkbox and the video from the downloaded music file will also be included in your PMV
	The occurance factor determines how much it will be used. (1 will be the same amount as the rest of your videos, >1 is more often, <1 is less often)
	Can also choose to trim the music file with the Trim Music checkbox and the STart, End boxes (seconds) this works whether you choose to integrate the music video or not.

Entering URLS
	For music urls I prefer to use youtube
	For video urls I prefer pornhub
		This can be left blank if you don't want to download any vids but just use those in your selected folder.
	The downloading works via a package called youtube-dl so in theory any of these supported sites will work: https://ytdl-org.github.io/youtube-dl/supportedsites.html
	If you get errors on a certain video, try a different one. If the error persists, update the youtube-dl package to the latest version or post your issue on the youtube-dl forum
	If the file your trying to download is already in the folder (for both music and videos) it will skip that file

VideoDetails
	Crop to Wide View will crop the top and bottom of the video by the selected percentage.
		Helps get rid of watermarks and the like.
	Add video intro will add your video intro to the start of the PMV (needs imagemagick installed)
	Can select the intro video manually here as well which will overwrite the file selected via line 77
	Start Time and End Trim - these trim the videos in the selected vid folder (not the music video) to get rid oftitle and credit scenes from the videos

PMV Parameters
	The program works by looking at the audio profile and selecting the largest changes in volume as the points to split the PMV up
	The files tend to have a granularity of 0.001s so to stop the program just changing every ms we can control the rate of switching with 4 parameters.
	If these are left to their current values, you'll still get a good PMV but you can gain more control by changing them accordingly.
	Granularity		- Essentially averages the audio profile into chunks of this size and then compares them to each other to see where there are large changes.
	nSplits 		- Once the audio profile is averaged, this then splits it up into n parts (this allows you to still get changes in the videos even if the song has some very loud and other very quiet parts)
	SD for slip switch	- The change between the granular volume values is averaged and the standard deviation found for each nSplit. To be classed as a changing point, the change needs to be larger than the Mean(change) + (SD for clip switch) * SD(change)
	Min Clip Length		- Removes the change points found above if the time difference between them is less than this value (seconds)

More Parameters
	Randomise 	- Randomly shuffles the order the videos appear. The program cycles through the videos in the selected folder then restarts once all videos have been used
				e.g if you have 4 videos it could do: 		1, 3, 4, 2 / 3, 2, 1, 4 / 4, 1, 2, 3 etc.
				if randomise is unchecked then it will be 	1, 2, 3, 4 / 1, 2, 3, 4 / 1, 2, 3, 4 etc.
	Resize		- Will resize all the videos to be the same size and aspect ratio (so you can still use old ratio vids, but you'll lose more as it's zoomed to a wide view)
	Flip Vids	- Will flip the videos so that watermarks appear backwards and are less likely to get picked up by autom-remove algos

Names
	User Name 		- Your username that will appear in the introvid and at the end of your file name
	Output File Name 	- The name your pmv will be given (automatically adds username to the end)
					If left blank, the name given will be "[Username] PMV - [youtubeMusicName]

Start button
	When the above otions are set, press the button to start the download and generating process!
	Can see the progress in the python terminal.