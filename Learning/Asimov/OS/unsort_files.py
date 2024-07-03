import os

for f in os.listdir():
    if os.path.isdir(f):
        for i in os.listdir(f):
            os.rename(os.path.join(f, i), os.path.basename(i))
        os.rmdir(f)
