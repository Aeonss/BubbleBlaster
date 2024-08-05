#----------------------------------------------------------------------------------------------------#

#   References:
#   https://www.analyticsvidhya.com/blog/2021/06/text-detection-from-images-using-easyocr-hands-on-guide/
#   https://stackoverflow.com/a/39316695
#   https://stackoverflow.com/a/40795835

#   pyinstaller bubbleblaster.py -i icon.ico --onefile

#----------------------------------------------------------------------------------------------------#

import customtkinter as ctk
from tkinter import filedialog, messagebox

import util
import os
import easyocr
import magicinpaint as mi
import cv2
from deep_translator import GoogleTranslator
from matplotlib import pyplot as plt
from matplotlib.widgets import Button

#----------------------------------------------------------------------------------------------------#

class App(ctk.CTk):
    
    # Define constants
    WINDOW_SIZE = "500x500"
    PADDING_X = 20
    PADDING_Y = 5
    PADDING_Y_LARGE = 20
    LABEL_WIDTH = 20
    LABEL_HEIGHT = 20
    LABEL_FONT = ("Arial Bold", 14)
    TEXTBOX_WIDTH = 330
    TEXTBOX_HEIGHT = 32
    BUTTON_HEIGHT = 32
    BUTTON_CORNER_RADIUS = 8
    COMBOBOX_WIDTH = 460

    def __init__(self, tag):
        super().__init__()

        self.geometry(self.WINDOW_SIZE)
        self.title(f"BubbleBlaster v{tag}")
        self.eval('tk::PlaceWindow . center')

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.iconbitmap(os.path.join(script_dir, "icon.ico"))

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        self.inputFrame = ctk.CTkFrame(self, width=500, fg_color="transparent")
        self.inputFrame.grid_rowconfigure(0, weight=0)
        self.inputFrame.grid_columnconfigure(0, weight=0)
        self.inputFrame.grid(row=0, column=0)

        self.inputLabel = ctk.CTkLabel(master=self.inputFrame, width=self.LABEL_WIDTH, height=self.LABEL_HEIGHT, text="Input Location", font=self.LABEL_FONT)
        self.inputLabel.grid(row=0, column=0, sticky="nw", padx=25, pady=(self.PADDING_Y_LARGE, self.PADDING_Y))

        self.inputTextbox = ctk.CTkTextbox(master=self.inputFrame, width=self.TEXTBOX_WIDTH, height=self.TEXTBOX_HEIGHT, border_width=1, corner_radius=8, text_color="white")
        self.inputTextbox.grid(row=1, column=0, padx=self.PADDING_X)
        self.inputTextbox.configure(state="disabled")
        
        self.inputButton = ctk.CTkButton(master=self.inputFrame, width=50, height=self.BUTTON_HEIGHT, border_width=0, corner_radius=self.BUTTON_CORNER_RADIUS, text="Import Image(s)", command=self.importImages)
        self.inputButton.grid(row=1, column=1, padx=(0, 25))
        
        self.languageLabel = ctk.CTkLabel(master=self, width=self.LABEL_WIDTH, height=self.LABEL_HEIGHT, text="Detected Language", font=self.LABEL_FONT)
        self.languageLabel.grid(row=2, column=0, sticky="nw", padx=25, pady=(self.PADDING_Y_LARGE, self.PADDING_Y))
        
        self.languageCombobox = ctk.CTkComboBox(master=self, width=self.COMBOBOX_WIDTH, values=["Korean", "Japanese", "Simplified Chinese", "Traditional Chinese", "English", "Russian", "Spanish", "Italian"])
        self.languageCombobox.grid(row=3, column=0, sticky="nw", padx=self.PADDING_X)
        
        self.confidenceLabel = ctk.CTkLabel(master=self, width=self.LABEL_WIDTH, height=self.LABEL_HEIGHT, text="Confidence: (0.4)", font=self.LABEL_FONT)
        self.confidenceLabel.grid(row=4, column=0, padx=25, sticky="nw", pady=(self.PADDING_Y_LARGE, self.PADDING_Y))
        
        self.confidenceSlider = ctk.CTkSlider(master=self, from_=0, to=1, number_of_steps=100, width=self.COMBOBOX_WIDTH, command=self.updateConfidenceLabel)
        self.confidenceSlider.grid(row=5, column=0, sticky="nw", padx=self.PADDING_X)
        self.confidenceSlider.set(0.4)

        self.optionsFrame = ctk.CTkFrame(self, width=500, fg_color="transparent")
        self.optionsFrame.grid_rowconfigure(0, weight=0)
        self.optionsFrame.grid_columnconfigure(0, weight=1)
        self.optionsFrame.grid(row=6, column=0)
        
        self.cudaSwitch = ctk.CTkSwitch(master=self.optionsFrame, text="Use inpaint (CUDA recommended)", onvalue=1, offvalue=0)
        self.cudaSwitch.grid(row=0, column=0, pady=(self.PADDING_Y_LARGE, 0), padx=10)

        self.rawSwitch = ctk.CTkSwitch(master=self.optionsFrame, text="Export raw text", onvalue=1, offvalue=0)
        self.rawSwitch.grid(row=1, column=0, pady=(self.PADDING_Y_LARGE, 0), padx=10)
        
        self.translateSwitch = ctk.CTkSwitch(master=self.optionsFrame, text="Export translated text", onvalue=1, offvalue=0)
        self.translateSwitch.grid(row=1, column=1, pady=(self.PADDING_Y_LARGE, 0), padx=10)
        
        self.processButton = ctk.CTkButton(master=self, width=120, height=self.BUTTON_HEIGHT, corner_radius=self.BUTTON_CORNER_RADIUS, text="Blast!", command=self.blast)
        self.processButton.grid(row=7, column=0, pady=(50, 0))

        self.logLabel = ctk.CTkLabel(master=self, font=("Arial", 10), width=self.LABEL_WIDTH, height=self.LABEL_HEIGHT, text_color="white")
        self.logLabel.grid(row=9, column=0, pady=(50, 0))
        
        util.setLog(self.logLabel)
    

    # Import file to program, do not replace if nothing is chosen
    def importImages(self):
        path = filedialog.askopenfilenames(parent=self, title="Choose input image(s)")
        if path != "":
            self.inputTextbox.configure(state="normal")
            self.inputTextbox.delete("0.0", "end")
            self.inputTextbox.insert("0.0", path)
            self.inputTextbox.configure(state="disabled")
        
        
    def updateConfidenceLabel(self, value):
        self.confidenceLabel.configure(text=f"Confidence: ({round(value, 2)})")
        
    
    # Main function
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
        EXPORT_RAW = self.rawSwitch.get()
        EXPORT_TRANSLATE = self.translateSwitch.get()
        CUDA = self.cudaSwitch.get()
        LANGUAGE = util.language_map.get(LANGUAGE)
    
        for index, image in enumerate(images):
            # Copies image and remove non-unicode characters
            image = util.sanitize_image_name(image, index)
            
            # OCR
            reader = easyocr.Reader([LANGUAGE])
            result = reader.readtext(image)
        
            # Read the image
            original_image = cv2.imread(image)
            img_rect = original_image.copy()
            
            preview_rect = original_image.copy()
            
            raw_list = []
            rects = []
            confidences = []
            preview_boxes = set()
            box_clicked = [False]
            
            for r in result:
                if r[2] >= CONFIDENCE:
                    raw_list.append(r[1])
                    
                    bottom_left = tuple(int(x) for x in tuple(r[0][0]))
                    top_right = tuple(int(x) for x in tuple(r[0][2]))
                    
                    rects.append((top_right, bottom_left))
                    confidences.append(r[2])
            
                    # Draw a rectangle around the text
                    preview_rect = cv2.rectangle(img_rect, bottom_left, top_right, (0,255,0), 3)
                    
                    # Draw confidence level on detected text
                    cv2.putText(preview_rect, str(round(r[2], 2)), bottom_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, 1)
            
            def update_preview():
                updated_preview = original_image.copy()
                for i, (top_right, bottom_left) in enumerate(rects):
                    if i in preview_boxes:
                        cv2.rectangle(updated_preview, bottom_left, top_right, (255, 255, 255), -1)
                    cv2.rectangle(updated_preview, bottom_left, top_right, (0, 255, 0), 3)
                    cv2.putText(updated_preview, f'{confidences[i]:.2f}', bottom_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, 1)
                return updated_preview
            
            def inpaint_rects(partial):
                img_inpaint = original_image.copy()
                img_temp = original_image.copy()
                h, w, c = img_temp.shape

                img_temp = cv2.rectangle(img_temp, [0,0], [w, h], (0, 0, 0), -1)
                for i, (top_right, bottom_left) in enumerate(rects):

                    if partial and i in preview_boxes or not partial:
                        img_temp = cv2.rectangle(img_temp, bottom_left, top_right, (255, 255, 255), -1)

                    mask = cv2.cvtColor(img_temp, cv2.COLOR_BGR2GRAY)

                    #img_inpaint = cv2.inpaint(img_inpaint, mask, 3, cv2.INPAINT_TELEA)
                    img_inpaint = mi.inpaint(img_temp, mask, 15, mi.InpaintGPUfast, verbose = True) 


                cv2.imwrite(image.replace(".png", "").replace(".jpg", "") + "_ocr.png", img_inpaint)
                plt.close(fig)
                messagebox.showinfo(title="BubbleBlaster", message="All bubbles have been blasted!")
            
            def fill_rects(partial):
                updated_image = original_image.copy()
                for i, (top_right, bottom_left) in enumerate(rects):
                    if partial and i in preview_boxes or not partial:
                        updated_image = cv2.rectangle(updated_image, bottom_left, top_right, (255, 255, 255), -1)

                cv2.imwrite(image.replace(".png", "").replace(".jpg", "") + "_ocr.png", updated_image)
                plt.close(fig)
                messagebox.showinfo(title="BubbleBlaster", message="Bubbles have been blasted!")

            
            app.attributes("-disabled", True)
            fig, ax = plt.subplots(figsize=(7, 7))
            ax.imshow(cv2.cvtColor(preview_rect, cv2.COLOR_BGR2RGB))
            ax.axis('off')

            def onclick(event):
                # Get the x and y coordinates of the click
                x, y = int(event.xdata), int(event.ydata)

                for i, (top_right, bottom_left) in enumerate(rects):
                    if bottom_left[0] <= x <= top_right[0] and bottom_left[1] <= y <= top_right[1]:
                        box_clicked[0] = True
                        if i in preview_boxes:
                            preview_boxes.remove(i)
                        else:
                            preview_boxes.add(i)
                        # Update the preview image
                        updated_preview = update_preview()
                        ax.imshow(cv2.cvtColor(updated_preview, cv2.COLOR_BGR2RGB))
                        plt.draw()
                        break
            
            fig.canvas.mpl_connect('button_press_event', onclick)
            
            # Add "Done", "Cancel", and "Paint All" buttons
            ax_cancel = plt.axes([0.25, 0.02, 0.1, 0.05])
            btn_cancel = Button(ax_cancel, 'Cancel')

            ax_paint_selected = plt.axes([0.45, 0.02, 0.15, 0.05])
            btn_paint_selected = Button(ax_paint_selected, 'Paint Selected')

            ax_paint_all = plt.axes([0.7, 0.02, 0.1, 0.05])
            btn_paint_all = Button(ax_paint_all, 'Paint All')

            def on_cancel(event):
                plt.close(fig)

            def on_paint_selected(event):
                if CUDA:
                    inpaint_rects(True)
                else:
                    fill_rects(True)
                self.inputTextbox.delete("0.0", "end")

            def on_paint_all(event):
                if CUDA:
                    inpaint_rects(False)
                else:
                    fill_rects(False)
                self.inputTextbox.delete("0.0", "end")
                

            btn_cancel.on_clicked(on_cancel)
            btn_paint_selected.on_clicked(on_paint_selected)
            btn_paint_all.on_clicked(on_paint_all)

            plt.show()
            
            app.attributes("-disabled", False)
            app.focus_force()



            # Export raw list to a text file
            if EXPORT_RAW:
                util.exportRaw(image, raw_list, rects)
            
            # Export translated raw text to a text file
            if EXPORT_TRANSLATE:
                raw = util.exportRaw(image, raw_list, rects)
                translation = GoogleTranslator(source='auto', target='en').translate(raw)
                        
                path = os.path.dirname(image)
                with open(os.path.join(path, os.path.splitext(os.path.basename(image))[0] + "_translated.txt"), 'w', encoding='UTF-8') as fp:
                    fp.write(translation)
                    fp.close()

            
if __name__ == "__main__":
    util.install_dependencies()

    TAG = "2.0.0"
    util.checkUpdate(TAG)

    app = App(TAG)
    app.mainloop()
