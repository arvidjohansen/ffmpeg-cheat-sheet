import os

# documentation
# https://ffmpeg.org/ffmpeg-filters.html#acompressor
# 
# this script makes this job a lot less manual


DEBUG = False
INCLUDE_VIDEO = True # Set to False to only compress audio
TARGET_PATH = '.'
SEARCH_FILE = ''

# Compressor settings
COMP_SETTINGS = {
    'threshold': 0.089,
    'ratio': 9,
    'attack': 3,
    'release': 1000,
    'makeup': 7.5,
}
# convert comp_settings to a string
comp_settings_str = ':'.join([f'{k}={v}' for k, v in COMP_SETTINGS.items()])

file_names = os.listdir(TARGET_PATH)

# if no search specified, ask user...
if not SEARCH_FILE:
    if input('Search for a specific file? (y/n) ').lower() == 'y':
        SEARCH_FILE = input('Enter (part of) file name: ')

# if search target is specified, filter it down...
if SEARCH_FILE:
    file_names = [f for f in file_names if SEARCH_FILE in f]

# check if user wants to continue
print(f'Files to compress: {file_names}')
if not input('Continue? (y/n) ').lower() != 'y':
    raise SystemExit('Exiting...')

# function to compress audio
def compress_audio(file_name, include_video = True):
    print(f'Compressing {file_name}...')
    file_ext = file_name.split(',')[-1]
    cmd = ''
    if include_video:
        # render video also
        cmd = f'''ffmpeg -i "{file_name}" -c:v copy -af acompressor={comp_settings_str} "{file_name}_compressed.{file_ext}"'''
    else:
        # render only audio
        cmd = f'''ffmpeg -i "{file_name}" -af acompressor={comp_settings_str} "{file_name}_compressed.wav"'''
    
    if DEBUG: print(f"Running command: {cmd}")
    
    os.system(cmd) # do the actual conversion
    
    print(f'Finished {file_name}.')

# compress all files
for file_name in file_names:
    compress_audio(file_name)

print("fin")
