<h1 align="center">BubbleBlaster</h1>

<font size="3"><a href="https://github.com/Aeonss/BubbleBlaster/releases/latest/">Bubble Blaster</a> is a python script that remove text from speech bubbles in mangas/manhwas with OCR.

<font size="3">

## 🔨 &nbsp; Installation
Install python:
``` bash
https://www.python.org/downloads/
```

### Option 1:
Download the latest [release](https://github.com/Aeonss/BubbleBlaster/releases/latest/), and run the exe file (windows only)

### Option 2:
Clone the repository:
``` bash
git clone https://github.com/Aeonss/BubbleBlaster
```

Download the requirements:
``` bash
pip install -r requirements.txt
```
Run with:
```bash
python bubbleblaster.py
```

## ❤️ &nbsp; Examples

### Program
<img src="https://i.imgur.com/jCIFmG6.png" width="50%" height="50%">

### Original Raw Manhwa
<img src="https://i.imgur.com/GK9WTEE.png" width="50%" height="50%">

### After BubbleBlast
<img src="https://i.imgur.com/i5P85uJ.png" width="50%" height="50%">

### Raw Text
<img src="https://i.imgur.com/vMNrrIj.png">

### Translated Text
<img src="https://i.imgur.com/Xvjn5Ls.png">

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
4. Select any additional options
    * "Export raw text" option will give a text file (.txt) of the text that the program OCR'd
    * "Export translated text" option will give a text file (.txt) of the translated text that the program OCR'd
    * "Preview image before exporting" option will give a preview window of all found text in the image along with the confidence level. This is so that you can play with the confidence level to get all the text you want to be removed.

## ✅ &nbsp; Additional Information
* BubbleBlaster was created with [**EasyOCR**](https://github.com/JaidedAI/EasyOCR) and [**Deep-Translator**](https://github.com/nidhaloff/deep-translator).
* Note that due to the way the text is exported, the translation is not entirely accurate.
* Please request any features or report any bugs in [issues](https://github.com/Aeonss/BubbleBlaster/issues).


## 🤖 &nbsp; To Do
* Make translations better



## 📘 &nbsp; License
BubbleBlaster is released under the [MIT license](https://github.com/Aeonss/BubbleBlaster/blob/master/LICENSE.md).

</font>