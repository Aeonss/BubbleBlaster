<h1 align="center">BubbleBlaster</h1>

<font size="3"><a href="https://github.com/Aeonss/BubbleBlaster/releases/latest/">Bubble Blaster</a> is a python script that remove text from speech bubbles in mangas/manhwas with OCR.

<br>
<p align="center">
<a href="https://github.com/Aeonss/BubbleBlaster/releases/latest/"><img src="https://img.shields.io/github/v/release/Aeonss/BubbleBlaster?style=for-the-badge&label=%20%F0%9F%93%A3%20Latest%20release&color=778beb&labelColor=2f3542"/></a>
<img src="https://img.shields.io/github/stars/Aeonss/BubbleBlaster?style=for-the-badge&label=%E2%AD%90%20Stars&color=786fa6&labelColor=2f3542"/>
<img src="https://img.shields.io/github/downloads/Aeonss/BubbleBlaster/total.svg?style=for-the-badge&label=%E2%AC%87%EF%B8%8FDownloads&color=4b6584&labelColor=2f3542"/>
</p>

<font size="3">

## 🔨 &nbsp; Installation
Install python:
``` bash
https://www.python.org/downloads/
```

Download the latest development release:
``` bash
pip install git+https://github.com/Aeonss/BubbleBlaster.git
```

Download the requirements:
``` bash
pip install -r requirements.txt
```


## ❤️ &nbsp; Examples
![example1](https://i.imgur.com/cyPm2cE.png)
![example2](https://i.imgur.com/TIS5yIo.png)
![example3](https://i.imgur.com/ivr6qv9.png)
![example4](https://i.imgur.com/pSdQp5V.png)
![example5](https://i.imgur.com/Fl3eCAm.png)
![example6](https://i.imgur.com/QrCLCAO.png)


## 🚀 &nbsp; Usage
Example usage:
``` bash
python bubbleblaster.py -i PATH/IMAGE.png
```

Remove Korean text:
``` bash
python bubbleblaster.py -l ko -i image.png
```

Remove Korean text and translate text to English:
``` bash
python bubbleblaster.py -l ko -i image.png --t
```

Remove Korean text and console logs:
``` bash
python bubbleblaster.py -l ko -i image.png --d
```

Remove Japanese text:
``` bash
python bubbleblaster.py -l ja -i image.png
```

Remove Japanese text with confidence levels above 0.5:
``` bash
python bubbleblaster.py -l ja -i image.png -c 0.5
```


Arguments:
``` bash
-i  <image>         ->  Path to image [Required]
-l  (language code) ->  (Default: English) -> Reference from: https://www.jaided.ai/easyocr/ [Optional]
--c (confidence)    ->  (Default: 0.15)    -> Any text below this number will not be removed [Optional]
```

Flags:
``` bash
--t     -> Any foreign text will be replaced with English text (Default: false)
--d     -> Show rectangle text and console message (Default: false)
```



## ✅ &nbsp; Additional Information
* BubbleBlaster was created with [**EasyOCR**](https://github.com/JaidedAI/EasyOCR) and [**Deep-Translator**](https://github.com/nidhaloff/deep-translator).
* Note that the machine translation is very bad, and the text placing is not optimized.
* Please request any features or report any bugs in [issues](https://github.com/Aeonss/BubbleBlaster/issues).


## 🤖 &nbsp; To Do
* Make integrated translations better


## 📘 &nbsp; License
BubbleBlaster is released under the [MIT license](https://github.com/Aeonss/BubbleBlaster/blob/master/LICENSE.md).

</font>