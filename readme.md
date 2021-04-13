# ffmpeg-cheat-sheet
## Convert video format
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

## Extracting audio
https://trac.ffmpeg.org/wiki/Encode/MP3

Extract to mp3 with the different qualities
-b:a 320k -> 320 kb/s
```sh
ffmpeg -i azure_debian_10_alex.mkv -b:a 320k azure_debian_320KBps.mp3 #320 kb/s
```
-q:a 0: *best* variable bitrate -> 278 kb/s 
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 0 azure_debian_qa0.mp3 #278 kb/s
```
-q:a 1: *next best* variable bitrate -> 255 kb/s 
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 1 azure_debian_qa1.mp3 #255 kb/s
```
-q:a 9: *bad* variable bitrate -> 63 kb/s
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 9 azure_debian_qa9.mp3 #255 kb/s
```
-q:a 10: worst variable bitrate -> 49 kb/s
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 10 azure_debian_qa10.mp3 #255 kb/s
```


```sh
ffmpeg -i adobe.mkv -c:a mp3 -q:a 1 adobe.mp3 #ffprobe bitrate: 278 kb/s
#-q:a -> variable bit rate

Extract to mp3 with next-highest quality?
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 0 azure_debian_245KBps.mp3
ffprobe azure_debian_3.mp3 #bitrate: 278 kb/s
```



Keep different audio tracks
```sh
ffmpeg -i adobe.mkv -map 0:1 adobe.mp3 # keep first audio track
ffmpeg -i adobe.mkv -map 0:2 adobe.mp3 # keep second audio track
ffmpeg -i adobe.mkv -c copy -map 0 adobe.mp4 # keep all audio tracks

```
