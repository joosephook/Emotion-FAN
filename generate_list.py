import os
import glob
from pathlib import Path

emotions = [
    'Disgust',
    'Surprise',
    'Sadness',
    'Anger',
    'Fear',
    'Neutral',
    'Happy'
]
emotions = dict(enumerate(emotions, start=1))


def write_list(file):
    lines = []
    for r, dirs, _ in os.walk(f'data/face'):
        for f in dirs:
            # fname = str(Path(f).with_suffix(''))
            fname = str(Path(f))
            *_, last = fname.split('_')
            i = int(last[2])
            emotion = emotions[i]
            lines.append(' '.join([fname, emotion]))
    file.write('\n'.join(lines))


if __name__ == '__main__':
    with open(f'list.txt', 'w') as out:
        write_list(out)
