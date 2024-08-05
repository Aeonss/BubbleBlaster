import sys, os, subprocess, requests, json, shutil, string, webbrowser
from tkinter import messagebox
import torch

language_map = {
    "Korean": "ko",
    "Japanese": "ja",
    "Simplified Chinese": "ch_sim",
    "Traditional Chinese": "ch_tra",
    "English": "en",
    "Russian": "ru",
    "Spanish": "es",
    "Italian": "it"
}

def checkUpdate(tag):
    try:
        r = requests.get("https://api.github.com/repos/Aeonss/BubbleBlaster/releases/latest")
        latest_tag = json.loads(r.content).get("tag_name")
        if latest_tag > tag:
            res = messagebox.askquestion(title="BubbleBlaster", message=f"A new update has been released for BubbleBlaster (v{latest_tag})! Do you want to download it?")
            if res == 'yes':
                webbrowser.open(f"https://github.com/Aeonss/BubbleBlaster/releases/tag/{latest_tag}/")
    except:
        print("Error getting latest update")

def install_dependencies():
    try:
        import pkg_resources
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "setuptools"])
        import pkg_resources

    required = []
    
    cwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cwd)

    with open('requirements.txt') as f:
        for line in f:
            required.append(line.strip())

    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = [pkg for pkg in required if pkg not in installed]

    if missing:
        print("Installing missing packages: ", missing)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", *missing])
    else:
        print("All required packages are already installed.")

def setLog(self):
    if not torch.cuda.is_available():
        self.configure(text="Cuda is HIGHLY recommended. Click to download here.")
        self.configure(state="disabled")
        self.bind("<Button-1>", lambda e:webbrowser.open("https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html"))

# Checks if two rectangles are intersecting using Separating Axis Theorem
# (top right(x,y)), bottom left(x,y))
def intersect(top_right1, bottom_left1, top_right2, bottom_left2):    
    return not (top_right1[0] < bottom_left2[0] or bottom_left1[0] > top_right2[0] or top_right1[1] < bottom_left2[1] or bottom_left1[1] > top_right2[1])

# Exports raw text in the image into a text file
def exportRaw(image, raw_list, rects):
    path = os.path.dirname(image)
    raw_string = ""
    for index, obj in enumerate(raw_list):
        if index > 0:
            if intersect(rects[index][0], rects[index][1], rects[index-1][0], rects[index-1][1]):
                raw_string += obj
            else:
                raw_string += "\n" + obj
        else:
            raw_string += obj
    with open(os.path.join(path, os.path.splitext(os.path.basename(image))[0] + "_raw.txt"), 'w', encoding='UTF-8') as fp:
        fp.write(raw_string)

    return raw_string

def sanitize_image_name(image, index):
    if not image.isascii():
        name = ''.join(c for c in image if c in string.printable)
        basename, ext = os.path.splitext(os.path.basename(name))

        # Handle the case where there is no extension
        if not ext:
            ext = ''
        else:
            basename = os.path.splitext(basename)[0]
        
        new_name = os.path.join(os.path.dirname(image), f"{basename}{index}{ext}")
        shutil.copy(image, new_name)
        return new_name

    return image