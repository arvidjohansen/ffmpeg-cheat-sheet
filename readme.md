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

Extract to mp3 with the *highest* quality
```
ffmpeg -i azure_debian_10_alex.mkv -b:a 320k azure_debian_320KBps.mp3
```

Extract to mp3 with next-highest quality
``` 
ffmpeg -i azure_debian_10_alex.mkv -qscale:a 0 azure_debian_3.mp3
ffmpeg -i azure_debian_10_alex.mkv -q:a 0 azure_debian_245KBps.mp3
# these two commands are the same
```

ffmpeg -i adobe.mkv -c:a mp3 -q:a 1 adobe.mp3
#-q:a -> variable bit rate

Keep different audio tracks
```
ffmpeg -i adobe.mkv -map 0:1 adobe.mp3 # keep first audio track
ffmpeg -i adobe.mkv -map 0:2 adobe.mp3 # keep second audio track
ffmpeg -i adobe.mkv -c copy -map 0 adobe.mp4 # keep all audio tracks

```
