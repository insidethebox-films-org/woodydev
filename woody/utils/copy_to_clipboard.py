import subprocess

def copy_to_clipboard(text):
    subprocess.run('clip', universal_newlines=True, input=text.strip())