import subprocess
import threading
from pathlib import Path
import shutil

class FFmpegBatch:
    def __init__(self, ffmpeg_path=None, ocio_path=None):
        self.input_dir = None
        self.exr_files = []
        self.ffmpeg_exe = ffmpeg_path or self._find_ffmpeg()

    def _find_ffmpeg(self):
        if shutil.which("ffmpeg"):
            return "ffmpeg"
        lib_ffmpeg = Path(__file__).parent.parent / "resources" / "ffmpeg.exe"
        if lib_ffmpeg.exists():
            return str(lib_ffmpeg)
        raise FileNotFoundError("ffmpeg executable not found. Please install ffmpeg or bundle it with your app.")

    def add_dir(self, dir_path):
        self.input_dir = Path(dir_path)
        self.exr_files = sorted(self.input_dir.glob("*.exr"))

    def render_mp4(self, output_path, fps=24, on_complete=None):
        def run():
            if not self.exr_files:
                if on_complete:
                    on_complete(False, "No EXR files found.")
                return

            first_file = self.exr_files[0].name
            prefix, frame = first_file.rsplit('.', 1)[0].rsplit('_', 1)
            pattern = f"{prefix}_%0{len(frame)}d.exr"
            input_pattern = str(self.input_dir / pattern)
            output_path_str = str(output_path)

            vf_filter = "format=rgb24,eq=gamma=2.2"

            cmd = [
                self.ffmpeg_exe,
                "-y",
                "-framerate", str(fps),
                "-i", input_pattern,
                "-vf", vf_filter,
                "-colorspace", "1",
                "-color_primaries", "1",
                "-color_trc", "1",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                output_path_str
            ]
            try:
                subprocess.run(cmd, check=True)
                if on_complete:
                    on_complete(True, output_path_str)
            except subprocess.CalledProcessError as e:
                if on_complete:
                    on_complete(False, str(e))

        threading.Thread(target=run, daemon=True).start()

    def generate_previews(self, preview_subfolder="previews", width=512, on_complete=None):
        def run():
            if not self.exr_files:
                if on_complete:
                    on_complete(False, "No EXR files found.")
                return

            preview_dir = self.input_dir / preview_subfolder
            preview_dir.mkdir(exist_ok=True)

            total_frames = len(self.exr_files)
            num_previews = max(3, total_frames // 10)
            if num_previews >= total_frames:
                selected_frames = self.exr_files
            else:
                step = total_frames / num_previews
                selected_frames = [self.exr_files[int(i * step)] for i in range(num_previews)]

            success_count = 0
            for exr_file in selected_frames:
                jpg_file = preview_dir / (exr_file.stem + ".jpg")
                vf_filter = f"scale={width}:-1,format=rgb24,eq=gamma=2.2"

                cmd = [
                    self.ffmpeg_exe,
                    "-y",
                    "-i", str(exr_file),
                    "-vf", vf_filter,
                    "-q:v", "2",
                    str(jpg_file)
                ]
                try:
                    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                    success_count += 1
                    print(f"Generated preview: {jpg_file.name}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to generate preview for {exr_file.name}: {e.stderr}")
                    continue

            if success_count > 0:
                if on_complete:
                    on_complete(True, str(preview_dir))
            else:
                if on_complete:
                    on_complete(False, "No preview frames were generated.")

        threading.Thread(target=run, daemon=True).start()