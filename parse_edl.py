#!/usr/bin/env python3
import argparse
import re

def parse():
    with open(args.edl, 'r') as f:
        lines = f.readlines()

    timestamps = []
    for line_num in range(len(lines)):
        if re.search('^\d{3}', lines[line_num]):
            m = re.search('(\d{2}):(\d{2}):(\d{2}):\d{2}', lines[line_num])
            if m is not None:
                timecode_h = int(m.group(1)) - 1 # davinci starts at 1 hour
                timecode_m = int(m.group(2))
                timecode_s = int(m.group(3))
            else:
                print("error reading file - couldn't match timecode")
                exit(1)

            # next get the description
            m = re.search('M:([^|]+)', lines[line_num+1])
            if m is not None:
                description = m.group(1)
                timestamps.append({'h': timecode_h, 'm': timecode_m, 's': timecode_s, 'desc': description})
            else:
                print("error reading file - couldn't match description")
                exit(1)

    print(f"read {len(timestamps)} timestamps")
    return timestamps 

def dump(timestamps):
    use_hours = False
    for ts in timestamps:
        if ts['h'] > 0:
            use_hours = True

    for ts in timestamps:
        if args.youtube:
            if use_hours:
                print(f"{ts['h']:02}:{ts['m']:02}:{ts['s']:02} {ts['desc']}")
            else:
                print(f"{ts['m']:02}:{ts['s']:02} {ts['desc']}")

        elif args.vlc:
            timecode = ts['h'] * 3600 + ts['m'] * 60 + ts['s']
            print(f"{{name={ts['desc']},time={timecode}}},") # VLC
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Davinci EDL parser")

    parser.add_argument('--vlc', help="vlc mode", action='store_const', const=True)
    parser.add_argument('--youtube', help="youtube mode", action='store_const', const=True)
    parser.add_argument('--edl', help="edl file to use", required=True)

    args = parser.parse_args()

    timestamps = parse()
    dump(timestamps)
