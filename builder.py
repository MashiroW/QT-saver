import os
import shutil

dirpath  = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, "gui_new.py")
iconpath = os.path.join(dirpath, "res/splash-removebg-preview.ico")

customtkinter_path = os.popen('pip show customtkinter').readlines()[7].split("Location: ")[1]
cmd   = 'pyinstaller --noconfirm --onedir --windowed --icon="{0}" --add-data "{1}/customtkinter;customtkinter/"  "{2}" -n "QTSaver"'.format(iconpath, customtkinter_path.strip(), filepath.replace("\\","/"))
output = os.popen(cmd).readlines()


"""
files_to_copy     = ["crash.py", "QT_saver.py", "config.ini"]
files_to_delete   = [".spec"]
folders_to_copy   = ["res"]
folders_to_delete = ["build"]

def remove(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def copy(src, dst):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    shutil.copyfile(src, dst)

for file in os.listdir(os.fsencode(dirpath)):
    f = os.fsdecode(file)

    for syntax in files_to_delete:
        if syntax in f:
            print(f)
            remove(f)

    for syntax in folders_to_delete:
        if syntax in f:
            print(f)
            remove(f)

    for syntax in folders_to_copy:
        if syntax in f:
            print(f)
            copytree(f, "./dist/gui_new")

    for syntax in files_to_copy:
        if syntax in f:
            print(f)
            shutil.copyfile(f, "./dist/gui_new", symlinks=False, ignore=None)
"""