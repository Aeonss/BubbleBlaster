<p align="center"><img src="https://i.imgur.com/rGZx1Wu.png" width="230" height="160"/></p>

<h1 align="center">BubbleBlaster</h1>

<font size="3"><a href="https://github.com/Aeonss/BubbleBlaster/releases/latest/">Bubble Blaster</a> is a python script that remove text from speech bubbles in mangas/manhwas with OCR.</font>

<br>
<p align="center">
<a href="https://github.com/Aeonss/BubbleBlaster/releases/latest/"><img src="https://img.shields.io/github/v/release/Aeonss/BubbleBlaster?style=for-the-badge&label=%20%F0%9F%93%A3%20Latest%20release&color=778beb&labelColor=2f3542"/></a>
<img src="https://img.shields.io/github/stars/Aeonss/BubbleBlaster?style=for-the-badge&label=%E2%AD%90%20Stars&color=786fa6&labelColor=2f3542"/>
<img src="https://img.shields.io/github/downloads/Aeonss/BubbleBlaster/total.svg?style=for-the-badge&label=%E2%AC%87%EF%B8%8FDownloads&color=4b6584&labelColor=2f3542"/>
</p>
<br>


## 🔨 &nbsp; Installation
Install python (Make sure your python version is **NOT** more than 3.11):
``` bash
https://www.python.org/downloads/release/python-3119/
```

Download the [latest](https://github.com/Aeonss/BubbleBlaster/releases/latest/) release and unzip it.
``` bash
https://github.com/Aeonss/BubbleBlaster/releases/latest/
```

If you have a compatible GPU, install [CUDA](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html) for faster OCRs.
``` bash
https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html
```

<br>Run the "INSTALL_DEPENDENCIES.bat" file on the first run
<br>Run the "BubbleBlaster.bat" file included in the release.

<br>To install manually, git clone the repository, install dependencies and run bubbleblaster.py
``` bash
git clone https://github.com/Aeonss/BubbleBlaster
pip install -r requirements.txt
python bubbleblaster.py
```


## ❤️ &nbsp; Examples

### Program
<img src="https://i.imgur.com/aVx2UfH.png" width="50%" height="50%">

<img src="https://i.imgur.com/SvsIrfI.png" width="50%" height="50%">

### Original Raw Manhwa
<img src="https://i.imgur.com/GK9WTEE.png" width="50%" height="50%">

### After BubbleBlaster
<img src="https://i.imgur.com/i5P85uJ.png" width="50%" height="50%">

### Raw Text
<img src="https://i.imgur.com/GNipEw1.png">

### Translated Text vs Scanlation Translation
<img src="https://i.imgur.com/sFmAxh8.png">
<img src="https://i.imgur.com/DpzX9NX.png">

### Preview Image
<img src="https://i.imgur.com/kcB9xUh.png">

### Files
<img src="https://i.imgur.com/Ok8tzNV.png">


## 🚀 &nbsp; Usage
1. Click on the "Import Image(s)" button to select the images you want to OCR (remove the text of)
    * You can select 1 image, or multiple by ctrl + clicking the images or drag selecting them
2. Select the language that the text is in
    * By default, the language is Korean, but Chinese, Japanese, and English is also supported.
    * Please request for more languages [here](https://github.com/Aeonss/BubbleBlaster/issues)
3. Select the confidence level by dragging the slider
    * Confidence level is how "sure" the AI is that the text is the language you selected
    * By default, the confidence level is 0.4.
    * The higher the number, the less likely text is recognized and OCR'd, but the text is more likely to be the selected language
    * The lower the number, the more likely that more text is recognized and OCR'd, but the text may include symbols or parts of the art
4. Select which texts to remove
    * You can select chosen outlined text or click the "select all" button to remove all chosen text
5. Select any additional options
    * "Export raw text" option will give a text file (.txt) of the text that the program OCR'd
    * "Export translated text" option will give a text file (.txt) of the translated text that the program OCR'd

## ✅ &nbsp; Additional Information
* BubbleBlaster was created with [**EasyOCR**](https://github.com/JaidedAI/EasyOCR) and [**Deep-Translator**](https://github.com/nidhaloff/deep-translator).
* Please request any features or report any bugs in [issues](https://github.com/Aeonss/BubbleBlaster/issues).


## 🤖 &nbsp; To Do
* Add a drag and select in the preview to manually select areas to inpaint
* Add zoom feature for large images in preview
* Add right click to move around in preview


## 📘 &nbsp; License
BubbleBlaster is released under the [MIT license](https://github.com/Aeonss/BubbleBlaster/blob/master/LICENSE.md).

</font>