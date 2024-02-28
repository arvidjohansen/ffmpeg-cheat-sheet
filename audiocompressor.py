import os


DEBUG = False
INCLUDE_VIDEO = True # Set to False to only compress audio
TARGET_PATH = '.'
SEARCH_FILE = 'E18'

# Compressor settings
COMP_SETTINGS = {
    'threshold': 0.089,
    'ratio': 9,
    'attack': 3,
    'release': 1000,
    'makeup': 10,
}

# convert comp_settings to a string
comp_settings_str = ':'.join([f'{k}={v}' for k, v in COMP_SETTINGS.items()])

file_names = os.listdir(TARGET_PATH)
if SEARCH_FILE:
    file_names = [f for f in file_names if SEARCH_FILE in f]

print(file_names)

# -af acompressor=threshold=0.089:ratio=9:attack=3:release=1000:makeup=10  # backup
def compress_audio(file_name, include_video = True):
    print(f'Compressing {file_name}...')
    file_ext = file_name.split(',')[-1]
    if include_video:
        # render video also
        cmd = f'''ffmpeg -i "{file_name}" -c:v copy -af acompressor={comp_settings_str} "{file_name}_compressed.{file_ext}"'''
    else:
        # render only audio
        cmd = f'''ffmpeg -i "{file_name}" -af acompressor={comp_settings_str} "{file_name}_compressed.wav"'''
    
    if DEBUG: print(f"Running command: {cmd}")
    
    os.system(cmd) # do the actual conversion
    
    print(f'Finished {file_name}.')

for file_name in file_names:
    compress_audio(file_name)

print("fin")