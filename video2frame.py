import subprocess
import os

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


if __name__ == '__main__':
    videos = 'data/video'
    frames = 'data/frame'
    index = 'list.txt'
    with open(index, 'w') as labels:
        for root, dirs, files in os.walk(videos):
            for file in files:
                # videos into frames using ffmpeg
                video_in = os.path.join(root, file)
                frame_out = os.path.join(frames, file)
                os.makedirs(frame_out, exist_ok=True)
                command = f'ffmpeg -v 16 -i {video_in} -f image2 {frame_out}/%07d.jpg'
                subprocess.run(command.split(' '))
                print(video_in, 'done')

                # map video to emotion, write to list.txt
                fname = str(Path(file).with_suffix(''))
                *_, last = fname.split('_')
                i = int(last[2])
                emotion = emotions[i]
                labels.write(' '.join([fname, emotion]))
                labels.write('\n')

