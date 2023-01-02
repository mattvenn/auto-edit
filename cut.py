import os, json
# https://github.com/kkroening/ffmpeg-python
with open("cuts.json") as fh:
    cuts = json.load(fh)
safety = 1

index = 0
for cut in cuts:
    print(cut['type'], cut['timestamp'])
    if cut['type'] == 'start':
        start = float(cut['timestamp'])
    if cut['type'] == 'end':
        end = float(cut['timestamp'])
        print(f"cutting new clip {index} from {start} to {end}")
        start -= 1
        end += 1
        ffmpeg = f'ffmpeg -y -ss 00:{start} -to 00:{end} -i input.mov -c copy {index:03d}_output.mov'
        print(ffmpeg)
        os.system(ffmpeg)
        index += 1
