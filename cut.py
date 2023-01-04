#!/usr/bin/env python3
from datetime import timedelta
import json
import subprocess

safety = 0.25 # second

with open("cuts.json") as fh:
    data = json.load(fh)
cuts = data['cuts']
input_file = data['input_file']
output_file = data['output_file']
filename, extension = os.path.splitext(input_file)
print(f"working from {input_file}")
index = 0
for cut in cuts:
    if cut['type'] == 'start':
        start = timedelta(seconds=round(cut['timestamp'],2) - safety)
    if cut['type'] == 'end':
        end = timedelta(seconds=round(cut['timestamp'],2) + safety)
        print(f"cutting new clip {index} from {start} to {end} to {index:03}_{output_file}{extension}")
        ffmpeg = f'ffmpeg -y -ss {start} -to {end} -i {input_file} -c copy -map 0 {index:03d}_{output_file}{extension}'
        subprocess.run(['ffmpeg', '-y', '-ss', str(start), '-to', str(end), '-i', input_file, '-c', 'copy', '-map', '0', f'{index:03d}_{output_file}{extension}'])
        index += 1
