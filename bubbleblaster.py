#----------------------------------------------------------------------------------------------------#

#   References:
#   https://github.com/JaidedAI/EasyOCR
#   https://www.analyticsvidhya.com/blog/2021/06/text-detection-from-images-using-easyocr-hands-on-guide/
#   https://stackoverflow.com/questions/39316447/opencv-giving-wrong-color-to-colored-images-on-loading

#----------------------------------------------------------------------------------------------------#

import sys, os.path, argparse
import easyocr
from deep_translator import GoogleTranslator
import cv2
from matplotlib import pyplot as plt
from PIL import Image

#----------------------------------------------------------------------------------------------------#

def OCR():
    
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "-image", help="Image path", required=True)
    parser.add_argument("-l", "-lang", help="Language code (https://www.jaided.ai/easyocr/)", nargs='?', const="en", default="en", required=False) # Default = en
    parser.add_argument("-c", "-conf", help="Confidence value", nargs='?', const=0.15, default=0.15, type=float) # Default = 0.15
    parser.add_argument("--t", "--translate", action='store_true', help="Replace foreign text with english text") # Default = False
    parser.add_argument("--d", "--debug", action='store_true', help="Show rectangles around text") # Default = False
    parser.add_argument("--png", action='store_true', help="Auto convert jpgs to png") # Default = False
        
    args = parser.parse_args()
       
    IMAGE = args.i
    LANG = args.l
    TRANSLATE = args.t
    CONFIDENCE = args.c
    DEBUG = args.d
    AUTO_PNG = args.png
    
    if not os.path.exists(IMAGE) or (not os.path.splitext(IMAGE)[-1].lower() == ".png" and not os.path.splitext(IMAGE)[-1].lower() == ".jpg"):
        print("ERROR: File does not exist or File is not a PNG or JPG!")
        return

    
    if AUTO_PNG:
        print(IMAGE)
        PNG_IMAGE = Image.open(IMAGE)
        NEW_NAME = IMAGE.split(".")[0] + "_png.png"
        PNG_IMAGE.save(NEW_NAME)
        IMAGE = NEW_NAME
    
    
    # OCR
    reader = easyocr.Reader([LANG])
    result = reader.readtext(IMAGE)


    # Images
    print(IMAGE)
    img_rect = cv2.imread(IMAGE)
    img_temp = cv2.imread(IMAGE)
    h, w, c = img_temp.shape


    # Fill temp image with black
    img_temp = cv2.rectangle(img_temp, [0,0], [w, h], (0, 0, 0), -1)
    img_inpaint = cv2.imread(IMAGE)
    
    trans_list = []

    # For each detected text
    for r in result:
        
        # If the OCR text is above the CONFIDENCE
        if r[2] >= CONFIDENCE:
            
            # Save the tuple of top left and bottom right of where the text is
            top_left = tuple(int(x) for x in tuple(r[0][0]))
            bottom_right = tuple(int(x) for x in tuple(r[0][2]))
            
            # Draw a rectangle around the text
            img_rect = cv2.rectangle(img_rect, top_left, bottom_right, (0,255,0), 3)        
            
            # Fill text with white rectangle
            img_temp = cv2.rectangle(img_temp, top_left, bottom_right, (255, 255, 255), -1)
            
            # Convert temp image to black and white for mask
            mask = cv2.cvtColor(img_temp, cv2.COLOR_BGR2GRAY)
            
            # "Content-Fill" using mask (INPAINT_NS vs INPAINT_TELEA)
            img_inpaint = cv2.inpaint(img_inpaint, mask, 3, cv2.INPAINT_TELEA)
            
            
            if DEBUG:
                print(r)
            
            
            # Add text translation and location to a list
            if TRANSLATE:
                if not r[1].isnumeric():
                    translation = GoogleTranslator(source='auto', target='en').translate(r[1])
                    trans_list.append((translation, top_left))
                    
                    if DEBUG:
                        print(r[1] + "\t" + translation)
                
                else:
                    trans_list.append((r[1], top_left))


    # Add text from list to image
    if TRANSLATE:
        for t in trans_list:
            cv2.putText(img_inpaint, t[0], t[1], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, 2)
    
    
    # Show images (with rectangles and with text removed)
    if DEBUG:
        plt.figure(figsize=(7, 7))
        plt.axis('off')
        plt.imshow(cv2.cvtColor(img_rect, cv2.COLOR_BGR2RGB))
        

        # Final image
        plt.figure(figsize=(7, 7))
        plt.axis('off')
        
        #    cv2.imwrite("mask.png", mask)
        
        plt.imshow(cv2.cvtColor(img_inpaint, cv2.COLOR_BGR2RGB))
        plt.show()
        
    
    
    cv2.imwrite(IMAGE.replace(".png", "").replace(".jpg", "") + "_ocr.png", img_inpaint)
    

# Main
if __name__ == "__main__":
    OCR()
    
