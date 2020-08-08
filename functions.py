import numpy as np
import random

def properTitles(row):
    try:
        return str.title(row['Title'].replace("/", "_"))
    except AttributeError:
        return 0

def reshapeData(data, time_scale):
    reshaped = np.mean(data[:(len(data)//time_scale)*time_scale].reshape(-1,time_scale), axis=1)

    return reshaped

def getElementDiff(data):
    
    differenceList = [abs(x - data[i - 1]) for i, x in enumerate(data)][1:]

    return differenceList


def getHighValues(reshaped_data, diff_data, sd_scale, nSplits, granularity):
    output=[0]
    
    timeChunks = np.array_split(diff_data, nSplits)
    j=0
    
    print('SmallerArrays: ', len(timeChunks))
    TotalLength=0
    while j < len(timeChunks):        
        data=timeChunks[j]
    
    
        max_element = np.amax(data)
        sd_element = np.std(data)
        av_element = np.mean(data)
        
        print(max_element, sd_element, av_element, (av_element+1.5*sd_element)/max_element)
        
        i=0
        result=[]
        while i< len(data):
            if data[i] >= (av_element+sd_scale*sd_element):
                result.append[i]
            i=i+1
        
        new_result = result
        
        print(new_result)
        
        i=1
        while i < len(new_result):
            if new_result[i]-new_result[i-1]>0.2/granularity:
                output.append(new_result[i]+TotalLength)
            i=i+1
        
        TotalLength=TotalLength + len(timeChunks[j])
        j=j+1
    
    return output

def getHighValues2(reshaped_data, diff_data, sd_scale, nSplits, granularity, min_length):
    output=[0]
    
    
    timeChunks = np.array_split(diff_data, nSplits)
    timeChunks2 = np.array_split(reshaped_data, nSplits)
    j=0
    
    print('SmallerArrays: ', len(timeChunks))
    TotalLength=0
    while j < len(timeChunks):        
        data=timeChunks[j]        
        data2=timeChunks2[j]

        sd_element = np.std(data)
        av_element = np.mean(data)
        
        
        result = np.where(data >= (av_element+sd_scale*sd_element))
        
        new_result = result[0].tolist()
        
#        print(new_result)
        
        i=1
        prevStopped=False
        prevDif=0
        while i < len(new_result):
#            print(new_result[i]+TotalLength, prevDif, prevStopped)
            if new_result[i]-new_result[i-1]>((min_length/granularity)-prevDif):
                output.append(new_result[i]+TotalLength)
                prevDif=0
                prevStopped=False
            else:
                prevDif=prevDif+(new_result[i]-new_result[i-1])
                prevStopped=True
            i=i+1
        
        TotalLength=TotalLength + len(timeChunks[j])
        j=j+1
    
    return output

def checkSwitch(data, max_scale, max_element, sd_element, av_element):
    if data >= max_scale * max_element:
        return True
    else:
        return False

def videoSplits(audioSplits, videos, videoData, first_data, bitrate, granularity, randomise, origVidName):
    
    audVidRatio=[0]*len(videos)
    clips=[]
    
    i=0
    while i < len(videos):
        audVidRatio[i]=(videoData[i].customEnd-videoData[i].customStart)/(len(first_data)/(granularity*(bitrate)))
        i=i+1
      
    print(len(audioSplits))
    i=0
    while i <= len(audioSplits):
        deck=[k for k in range(len(videos))]
        random.shuffle(deck)
        j=0
        while j<len(videos):
            try:
                if randomise==True:
                    iVid=deck[j]
                    print(videoData[iVid].name) ####If Breaking, uncomment this line to find corrupt video!!!
                else:
                    iVid=j
                if i+len(videos)+1<=len(audioSplits) or len(videos) >= len(audioSplits) or videoData[iVid].name == origVidName:
                    clips.append(videos[iVid].subclip(videoData[iVid].customStart+audioSplits[i+j]*audVidRatio[iVid], videoData[iVid].customStart + audioSplits[i+j] * audVidRatio[iVid] + (audioSplits[i+j+1] - audioSplits[i+j])*granularity))
                    print(i, j, iVid, i+j, 'False', audioSplits[i+j], audioSplits[i+j] + (audioSplits[i+j+1] - audioSplits[i+j]), audioSplits[i+j+1])
                else:
                    clips.append(videos[iVid].subclip(videoData[iVid].customEnd - (audioSplits[i+j+1] - audioSplits[i+j])*granularity, videoData[iVid].customEnd))
                    print(i, j, iVid, i+j, 'True', audioSplits[i+j], audioSplits[i+j] + (audioSplits[i+j+1] - audioSplits[i+j]), audioSplits[i+j+1])
            except:
                print('End')
                pass
            j=j+1
        i=i+len(videos)
        
    print('length: ', len(clips))
    return(clips)
        
    

