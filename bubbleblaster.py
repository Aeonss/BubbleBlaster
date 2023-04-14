#----------------------------------------------------------------------------------------------------#

#   References:
#   https://www.analyticsvidhya.com/blog/2021/06/text-detection-from-images-using-easyocr-hands-on-guide/
#   https://stackoverflow.com/a/39316695
#   https://stackoverflow.com/a/40795835

#----------------------------------------------------------------------------------------------------#

import customtkinter as ctk
from tkinter import filedialog, messagebox

import sys, os
import easyocr
import cv2
from deep_translator import GoogleTranslator
from matplotlib import pyplot as plt
from PIL import Image

#----------------------------------------------------------------------------------------------------#

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.geometry('500x500')
        self.title("BubbleBlaster")
        self.eval('tk::PlaceWindow . center')


        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        
        self.inputFrame = ctk.CTkFrame(self, width=500, fg_color="transparent")
        self.inputFrame.grid_rowconfigure(0, weight=0)
        self.inputFrame.grid_columnconfigure(0, weight=0)
        self.inputFrame.grid(row=0, column=0)

        self.inputLabel = ctk.CTkLabel(master=self.inputFrame, width=20, height=20, text="Input Location", font=("Arial Bold", 14))
        self.inputLabel.grid(row=0, column=0, sticky="nw", padx=25, pady=(20, 5))

        self.inputTextbox = ctk.CTkTextbox(master=self.inputFrame, width=330, height=32, border_width=1, corner_radius=8, text_color="white")
        self.inputTextbox.grid(row=1, column=0, padx=20)
        self.inputTextbox.configure(state="disabled")
        
        self.inputButton = ctk.CTkButton(master=self.inputFrame, width=50, height=32, border_width=0, corner_radius=8, text="Import Image(s)", command=self.importImages)
        self.inputButton.grid(row=1, column=1, padx=(0, 25))
        
        
        
        self.languageLabel = ctk.CTkLabel(master=self, width=20, height=20, text="Detected Language", font=("Arial Bold", 14))
        self.languageLabel.grid(row=2, column=0, sticky="nw", padx=25, pady=(20, 5))
        
        self.languageCombobox = ctk.CTkComboBox(master=self, width=460, values=["Korean", "Japanese", "Simplified Chinese", "Traditional Chinese", "English"])
        self.languageCombobox.grid(row=3, column=0, sticky="nw", padx=20)
        
        self.confidenceLabel = ctk.CTkLabel(master=self, width=20, height=20, text="Confidence: (0.4)", font=("Arial Bold", 14))
        self.confidenceLabel.grid(row=4, column=0, padx=25, sticky="nw", pady=(20, 5))
        
        self.confidenceSlider = ctk.CTkSlider(master=self, from_=0, to=1, number_of_steps=100, width=460, command=self.updateConfidenceLabel)
        self.confidenceSlider.grid(row=5, column=0, sticky="nw", padx=20)
        self.confidenceSlider.set(0.4)
    


        self.optionsFrame = ctk.CTkFrame(self, width=500, fg_color="transparent")
        self.optionsFrame.grid_rowconfigure(0, weight=0)
        self.optionsFrame.grid_columnconfigure(0, weight=1)
        self.optionsFrame.grid(row=6, column=0)
        
        self.rawSwitch = ctk.CTkSwitch(master=self.optionsFrame, text="Export raw text", onvalue=1, offvalue=0)
        self.rawSwitch.grid(row=0, column=0, pady=(20, 0), padx=10)
        
        self.translateSwitch = ctk.CTkSwitch(master=self.optionsFrame, text="Export translated text", onvalue=1, offvalue=0)
        self.translateSwitch.grid(row=0, column=1, pady=(20, 0), padx=10)
        
        self.previewSwitch = ctk.CTkSwitch(master=self.optionsFrame, text="Preview image before exporting", onvalue=1, offvalue=0)
        self.previewSwitch.grid(row=1, column=0, pady=(20, 0), padx=10)
        
        #self.pngSwitch = ctk.CTkSwitch(master=self.optionsFrame, text="Export as png", onvalue=1, offvalue=0)
        #self.pngSwitch.grid(row=1, column=1, pady=(20, 0), padx=10)
        

        self.processButton = ctk.CTkButton(master=self, width=120, height=32, corner_radius=8, text="Blast!", command=self.blast)
        self.processButton.grid(row=7, column=0, pady=(100, 0))
    
    
    def importImages(self):
        path = filedialog.askopenfilenames(parent=self, title="Choose input image(s)")
        self.inputTextbox.configure(state="normal")
        self.inputTextbox.delete("0.0", "end")
        self.inputTextbox.insert("0.0", path)
        self.inputTextbox.configure(state="disabled")
        
        
    def updateConfidenceLabel(self, value):
        self.confidenceLabel.configure(text=f"Confidence: ({round(value, 2)})")
        
    
    def blast(self):
        
        # Check if any images are imported
        imageInput = self.inputTextbox.get("0.0", "end").strip()
        if imageInput == "":
            messagebox.showerror("Error", "No images are inputed.")
            return
        
        
        # Get list of images to be OCR'd
        images = list(self.tk.splitlist(imageInput))
        
        # Options
        CONFIDENCE = self.confidenceSlider.get()
        LANGUAGE = self.languageCombobox.get()
        PREVIEW = self.previewSwitch.get()
        EXPORT_RAW = self.rawSwitch.get()
        EXPORT_TRANSLATE = self.translateSwitch.get()
        
        # Get language code
        if LANGUAGE == "Korean":
            LANGUAGE = "ko"
        elif LANGUAGE == "Japanese":
            LANGUAGE = "ja"
        elif LANGUAGE == "Simplified Chinese":
            LANGUAGE = "ch_sim"
        elif LANGUAGE == "Traditional Chinese":
            LANGUAGE = "ch_tra"
        elif LANGUAGE == "English":
            LANGUAGE = "en"

    
        for image in images:
            # OCR
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
                    # Bottom Left = r[0][0]
                    # Bottom Right = r[0][1]
                    # Top Right = r[0][2]
                    # Top Left = r[0][3]
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
                    
            # Export raw list to a text file
            if EXPORT_RAW:
                self.exportRaw(image, raw_list, rects)
            
            # Export translated raw text to a text file
            if EXPORT_TRANSLATE:
                raw = self.exportRaw(image, raw_list, rects)
                
                translation = GoogleTranslator(source='auto', target='en').translate(raw)
                        
                path = os.path.dirname(image)
                with open(os.path.join(path, os.path.splitext(os.path.basename(image))[0] + "_translated.txt"), 'w', encoding='UTF-8') as fp:
                    fp.write(translation)
                    fp.close()
            
            # Export image
            cv2.imwrite(image.replace(".png", "").replace(".jpg", "") + "_ocr.png", img_inpaint)
        
        messagebox.showinfo(title=None, message="Bubbles have been blasted!")
        self.inputTextbox.delete("0.0", "end")
    
    
    
    
    # Checks if two rectangles are intersecting using Separating Axis Theorem
    # (top right(x,y)), bottom left(x,y))
    def intersect(self, top_right1, bottom_left1, top_right2, bottom_left2):    
        return not (top_right1[0] < bottom_left2[0] or bottom_left1[0] > top_right2[0] or top_right1[1] < bottom_left2[1] or bottom_left1[1] > top_right2[1])



    # Exports raw text in the image into a text file
    def exportRaw(self, image, raw_list, rects):
        path = os.path.dirname(image)
        raw_string = ""
        with open(os.path.join(path, os.path.splitext(os.path.basename(image))[0] + "_raw.txt"), 'w', encoding='UTF-8') as fp:
            for index, obj in enumerate(raw_list):
                if index > 0:
                    if self.intersect(rects[index][0], rects[index][1], rects[index-1][0], rects[index-1][1]):
                        fp.write(f"{obj}")
                        raw_string += obj
                    else:
                        fp.write(f"\n{obj}")
                        raw_string += "\n" + obj
                else:
                    fp.write(f"{obj}")
                    raw_string += obj
            fp.close()
        return raw_string
    
if __name__ == "__main__":
    app = App()
    app.mainloop()


