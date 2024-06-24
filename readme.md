# ffmpeg-cheat-sheet
Various useful commands for ffmpeg

## Blanking the screen for a segment (from Django London)

If a speaker accidentally shows private information, such as their email inbox, we can black out the screen in the video before uploading it to YouTube. This can be done with another ffmpeg command:

ffmpeg -i talk.mp4 -f lavfi -i "color=black:s=1920x1200:r=25" -filter_complex \
"[0:v][1]overlay=enable='between(t,1333,1339)'[video]" \
-map "[video]" -map 0:a:0 -c:a copy -to 30:20 talk-blanked.mp4
-f lavfi enables generating a video stream inside ffmpeg.

-i "color=black:s=1920x1200:r=25" generates a stream representing a black screen. The resolution and framerate (r=) must match the input video.

The multiline -filter_complex arguament. The between() value selects the start and end in seconds where black overlay will appear.

The -map arguments select what will be output.

-c:a copy copies the audio from the original video without re-encoding it. Unfortunately re-encoding the video required with this setup, so it will lose some quality.

-to should specify the length of the original video. This stops ffmpeg generating an infinite length video, since the overlay stream is infinite.

Multiple blankings can be done by specifying a more complex filter. See the original stack exchange question.

# Convert video format
Convert lossless (only repack, don't reencode)
```sh
ffmpeg -i input.mkv -codec copy output.mp4
```

Parameters to remember
```sh
-map 0:a #includes all audio tracks
-map 0:a #includes all video tracks
-q:a # variable bit rate
```

convert to mp4, keep all audio tracks
```sh
ffmpeg -i adobe.mkv -c copy -map 0 adobe.mp4
```

cut video starting at 00:13:50 for duration 00:01:00
```sh
ffmpeg -i azure_debian_10_alex.mkv -ss 00:13:50 -t 00:01:00 azure_debian_cut.mp4
```

cut video at 00:13 but re-render so necessary intermiddent frames are in place (?) 
```sh
ffmpeg -i video-to-cut.mp4 -c:a copy -c:v libx264 -ss 00:13 out3.mp4
```
instead of `-c:copy` use `-c:a copy -c:v libx264`, this seems to be a fix for the first 2-5 seconds of the video being "screwed up" due to missing frames

# Extracting audio
https://trac.ffmpeg.org/wiki/Encode/MP3

## mp3 with static bitrate
usage:
```sh
ffmpeg ... -b:a xxxk ...
```
-b:a 320k
```sh
ffmpeg -i azure_debian_10_alex.mkv -b:a 320k azure_debian_320KBps.mp3 #320 kb/s
```
-b:a 256k 
```sh
ffmpeg -i azure_debian_10_alex.mkv -b:a 256k azure_debian_256KBps.mp3 #256 kb/s
```
-b:a 96k
```sh
ffmpeg -i azure_debian_10_alex.mkv -b:a 96k azure_debian_96KBps.mp3 #96 kb/s
```

## mp3 with variable bitrate
usage:
```sh
ffmpeg ... -q:a <0-9> ...
```

-q:a 0 -> best
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 0 azure_debian_qa0.mp3 #278 kb/s
```
-q:a 1 -> next best
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 1 azure_debian_qa1.mp3 #255 kb/s
```
-q:a 9 -> bad
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 9 azure_debian_qa9.mp3 #63 kb/s
```
-q:a 10 -> worst
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 10 azure_debian_qa10.mp3 #49 kb/s
```

```sh
ffmpeg -i adobe.mkv -c:a mp3 -q:a 1 adobe.mp3 #ffprobe bitrate: 278 kb/s
#-q:a -> variable bit rate
```

Keep different audio tracks
```sh
ffmpeg -i adobe.mkv -map 0:1 adobe.mp3 # keep first audio track
ffmpeg -i adobe.mkv -map 0:2 adobe.mp3 # keep second audio track
ffmpeg -i adobe.mkv -c copy -map 0 adobe.mp4 # keep all audio tracks
```

## Converting stereo to mono
Keep left audio channel without losing (too much?) quality:
```sh
ffmpeg -i video.mov -map_channel 0.1.0 -ab 512k -c:v copy videomono.mov
```
Keep right audio channel without losing (too much?) quality:
```sh
ffmpeg -i video.mov -map_channel 0.1.1 -ab 512k -c:v copy videomono.mov
```

## Combine two clips
I have two files: clip1.mov and clip2.mov - both 1 minute long.  
I want to combine both files to a clip that is two min long, without reencoding them.  
First we have to create a list of the files we want to combine:
```sh
(echo file 'clip1.mov' & echo file 'clip2.mov')>list.txt)
```
We could also have created the text-file manually.    

When we have a list containing the filenames we want to combine, simply use this command to combine them:
```sh
ffmpeg -safe 0 -f concat -i list.txt -c copy combined.mov 
```

## Combine video and audio from different clips
[How to merge audio and video in ffmpeg - Stackoverflow](https://superuser.com/questions/277642/how-to-merge-audio-and-video-file-in-ffmpeg)  
Filename of video: DSC_0562.MOV
Lets say I recorded a video on my camera that I want to remove background noise from using audacity 
1) Export audio to out.wav
```sh
ffmpeg -i DSC_0562.MOV out.wav
```
2) Open wav in audacity, remove noise, export to out-noise-removed.wav
3) Combine video from original clip and audio from noise-removed clips:
```sh
ffmpeg -i DSC_0562.MOV i out-noise-removed.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 out.mp4
```


# Extracting parts of the video
Lets say I want to remove the last 5 seconds of a 40 second clip  
To extract parts of the video simply input starting point with `-ss 00:00:00` and length with `-t 00:00:35`   
```sh
ffmpeg -i input.mp4 -ss 00:00:00 -t 00:00:35 -c copy output.mp4
```
> Note that the -ss and -t arguments has to come **before** encoding parameters 

To avoid re-encoding the entire thing simply use `-c copy` which will copy both the audio and the video codec

# Reducing size of video files
Original file (mostly powerpoint presentation with still images):   
prosjekt-intro.mp4 4.137807 GB  
>encoder         : Lavf57.84.100  
>  Duration: 00:46:34.47, start: 0.000000, bitrate: 12130 kb/s
>  Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p, 1920x1080, 11999 kb/s, 30 fps, 30 tbr, 15360 tbn, 60 tbc >(default)   

`ffmpeg -i prosjekt-intro.mp4 -c:a copy -c:v libx265 -preset fast -crf <VALUE> -qphist -tune stillimage output-file.mp4`   
 
 
File sizes with different values for the `-crf`-parameter:    

|crf-value|size|ratio|bitrate|description
|---|---|---|---|---|
|-|4 137 807 MB|100%|12130 KB/s|Original file|
|0|1 277 728 MB|30.9%|3745 KB/s|Barely noticable
|1|---|---|---|---|
|5|1 103 092 MB|26.6%|3233 KB/s|Barely noticable
|10|629 MB|15.2%|2051 KB/s|Good - somewhat noticable
|20|264 MB|6.4%|774 KB/s|Noticable - but still ok
|51|55 MB|1.3%|161 KB/s|Useless - barely watchable






Resouces
* quick guide using ffmpeg to convert media files - https://opensource.com/article/17/6/ffmpeg-convert-media-file-formats
* high quality audio - https://trac.ffmpeg.org/wiki/Encode/HighQualityAudio
* mp3 - https://trac.ffmpeg.org/wiki/Encode/MP3


## Streaming with ffmpeg
https://trac.ffmpeg.org/wiki/StreamingGuide#Pointtopointstreaming

To stream a file to a standard debian/nginx/rtmp setup:
```sh
ffmpeg -re -i "My Video.mkv" -c:v copy -c:a aac -ar 44100 -ac 1 -f flv rtmp://localhost/live/stream
```
