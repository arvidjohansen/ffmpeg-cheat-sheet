# ffmpeg-cheat-sheet
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
ffmpeg -i adobe.mkv -c:a mp3 -q:a 1 adobe.mp3
#-q:a -> variable bit rate

Keep different audio tracks
```
ffmpeg -i adobe.mkv -map 0:1 adobe.mp3 # keep first audio track
ffmpeg -i adobe.mkv -map 0:2 adobe.mp3 # keep second audio track
ffmpeg -i adobe.mkv -c copy -map 0 adobe.mp4 # keep all audio tracks

```

convert to mp4, keep all audio tracks
```sh
ffmpeg -i adobe.mkv -c copy -map 0 adobe.mp4
```

