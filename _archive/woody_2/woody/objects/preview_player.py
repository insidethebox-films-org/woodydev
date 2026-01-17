from PIL import Image
import time
import os
from pathlib import Path

class PreviewPlayer:
    def __init__(self, image_dir, fps=24, exts=(".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".exr")):
        self.image_dir = Path(image_dir)
        self.fps = fps
        self.exts = exts
        self._stop_playback = False
        self.frames = self.load_images()

    def load_images(self):
        files = sorted([f for f in self.image_dir.iterdir() if f.suffix.lower() in self.exts])
        images = []
        for f in files:
            try:
                img = Image.open(f)
                images.append(img)
            except Exception:
                continue
        return images

    def frame_count(self):
        return len(self.frames)

    def play(self, callback, delay=None, loop=False):
        if delay is None:
            delay = 1.0 / self.fps
        self._stop_playback = False
        try:
            while not self._stop_playback:
                for frame in self.frames:
                    if self._stop_playback:
                        break
                    try:
                        callback(frame)
                    except Exception:
                        pass
                    time.sleep(delay)
                if not loop:
                    break
        finally:
            self._stop_playback = True

    def stop(self):
        self._stop_playback = True