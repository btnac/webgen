import os, shutil

def public_deletion(dir_path_public):
    if os.path.exists(f"./{dir_path_public}"):
        shutil.rmtree(f"./{dir_path_public}")

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

