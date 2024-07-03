import os

for f in os.listdir():
    if os.path.isfile(f):
        ext = os.path.splitext(f)[1].lstrip('.')
        if ext == "py":
            continue
        elif ext is None or ext == "":
            ext = "data"
        if not os.path.exists(ext) or not os.path.isdir(ext):
            os.mkdir(ext)
        os.replace(f, ext + '/' + f)
