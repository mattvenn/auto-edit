import ffmpeg, json
# https://github.com/kkroening/ffmpeg-python
with open("cuts.json") as fh:
    cuts = json.load(fh)

init_time = cuts[0]['timestamp']
index = 0
for cut in cuts:
    print(cut['type'], cut['timestamp'] - init_time)
    if cut['type'] == 'start':
        start = cut['timestamp'] - init_time
    if cut['type'] == 'end':
        end = cut['timestamp'] - init_time
        print(f"cutting new clip {index} from {start} to {end}")
        stream = ffmpeg.input('input.mkv')
        stream = ffmpeg.trim(stream, start=start, end=end)
        audio_stream = ffmpeg.input(stream).audio
        trimed_audio_stream = audio_stream.filter('atrim', start=start, end=end)
        stream = ffmpeg.output(stream, trimmed_audio_stream, f'output{index}.mkv')
        ffmpeg.run(stream)
        index += 1
