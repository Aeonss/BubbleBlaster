import argparse
from pathlib import Path
import os
import easyocr
import cv2
from matplotlib import pyplot as plt

VERSION = "1.2.4"

parser = argparse.ArgumentParser(prog='bb', description='BubbleBlaster')
parser.add_argument("path",
                    help='Location of the image or folder of images')
parser.add_argument("--c", "--confidence", 
                    type=float,
                    default=0.4,
                    help='Confidence level of OCR (default=0.4), must be value between 0 and 1. Higher values are stricter.')
parser.add_argument("--l", "--language", 
                    default='ko',
                    choices=['ko', 'ja', 'ch_sim', 'ch_tra', 'en', 'ru'],
                    help='Language to OCR (default=ko). [ko, ja, ch_sim, ch_tra, en, ru]')

parser.add_argument("--p", "--preview",
                    action="store_true",
                    help="Preview the OCR")

parser.add_argument("--v", "--version",
                    action="version",
                    version=f"BubbleBlaster v{VERSION}",
                    help="Show the version of the program")

args = parser.parse_args()


PATH = args.path
LANGUAGE = args.language
CONFIDENCE = args.confidence
PREVIEW = args.preview


# Check if file path exists
target_dir = Path(PATH)

if not target_dir.exists():
    print("The target file/directory doesn't exist")
    raise SystemExit(1)


# Get list of images to be OCR'd
if os.path.isdir(PATH):
    files = os.listdir(PATH)
    images = [file for file in files if any(file.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png'])]
else:
    images = [PATH]
    

# OCR the images
for image in images:
    reader = easyocr.Reader([LANGUAGE])
    result = reader.readtext(image)

    # Read the image
    img_rect = cv2.imread(image)
    img_temp = cv2.imread(image)
    h, w, c = img_temp.shape

    # Fill temp image with black
    img_temp = cv2.rectangle(img_temp, [0,0], [w, h], (0, 0, 0), -1)
    img_inpaint = cv2.imread(image)

    preview_rect = cv2.imread(image)

    raw_list = []
    rects = []

    # For each detected text
    for r in result:
        
        # If the OCR text is above the CONFIDENCE
        if r[2] >= CONFIDENCE:
            
            # Add text to raw list
            raw_list.append(r[1])
            
            # Save the tuple of top right and bottom left of where the text is
            bottom_left = tuple(int(x) for x in tuple(r[0][0]))
            top_right = tuple(int(x) for x in tuple(r[0][2]))
            
            # Add rectangles to a list
            rects.append((top_right, bottom_left))
            
            # Draw a rectangle around the text
            img_rect = cv2.rectangle(img_rect, bottom_left, top_right, (0,255,0), 3)        
            
            # Fill text with white rectangle
            img_temp = cv2.rectangle(img_temp, bottom_left, top_right, (255, 255, 255), -1)
            
            # Convert temp image to black and white for mask
            mask = cv2.cvtColor(img_temp, cv2.COLOR_BGR2GRAY)
            
            # "Content-Fill" using mask (INPAINT_NS vs INPAINT_TELEA)
            img_inpaint = cv2.inpaint(img_inpaint, mask, 3, cv2.INPAINT_TELEA)

            # Draw a rectangle around the text
            preview_rect = cv2.rectangle(img_rect, bottom_left, top_right, (0,255,0), 3)
            
            # Draw confidence level on detected text
            cv2.putText(preview_rect, str(round(r[2], 2)), bottom_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, 1)


    # Show all detected text and their confidence level
    if PREVIEW:
        plt.figure(figsize=(7, 7))
        plt.axis('off')
        plt.imshow(cv2.cvtColor(preview_rect, cv2.COLOR_BGR2RGB))
        plt.show()
            
    # Export image
    cv2.imwrite(image.replace(".png", "").replace(".jpg", "") + "_ocr.png", img_inpaint)
