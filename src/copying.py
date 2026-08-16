import os, shutil

def public_deletion():
    if os.path.exists("../public"):
        shutil.rmtree("../public")

def copy(path, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            if os.path.isfile(f"{path}/{file}"):
                shutil.copy(f"{path}/{file}", f"{dest}")
            else:

                copy(f"{path}/{file}", f"{dest}/{file}")
    else:
        raise Exception("folder or file is missing")

