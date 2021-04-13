# ffmpeg-cheat-sheet
Various useful commands for ffmpeg

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

# Extracting audio
https://trac.ffmpeg.org/wiki/Encode/MP3

static bitrate
```sh
ffmpeg ... -b:a xxxk ...
``` 
variable bitrate
```sh
ffmpeg ... -q:a <0-9> ...
```

## mp3 with static bitrate
320kbps (best) static bitrate: -b:a 320k -> 320 kb/s
```sh
ffmpeg -i azure_debian_10_alex.mkv -b:a 320k azure_debian_320KBps.mp3 #320 kb/s
```
256kbps static bitrate: -b:a 256k -> 256kb/s
```sh
ffmpeg -i azure_debian_10_alex.mkv -b:a 256k azure_debian_256KBps.mp3 #256 kb/s
```

## mp3 with variable bitrate
Best variable bitrate: -q:a 0 -> 278 kb/s 
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 0 azure_debian_qa0.mp3 #278 kb/s
```
Next best variable bitrate: -q:a 1 -> 255 kb/s 
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 1 azure_debian_qa1.mp3 #255 kb/s
```
Bad variable bitrate: -q:a 9 -> 63 kb/s
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 9 azure_debian_qa9.mp3 #63 kb/s
```
Worst variable bitrate: -q:a 10 -> 49 kb/s
```sh
ffmpeg -i azure_debian_10_alex.mkv -q:a 10 azure_debian_qa10.mp3 #49 kb/s
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

Resouces
* quick guide using ffmpeg to convert media files - https://opensource.com/article/17/6/ffmpeg-convert-media-file-formats
* high quality audio - https://trac.ffmpeg.org/wiki/Encode/HighQualityAudio
* mp3 - https://trac.ffmpeg.org/wiki/Encode/MP3

