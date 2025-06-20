import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarker")

        self.canvas = tk.Canvas(root, width=500, height=400)
        self.canvas.pack()

        self.btn_load = tk.Button(root, text="Load Image", command=self.load_image)
        self.btn_load.pack()

        self.entry = tk.Entry(root)
        self.entry.insert(0, "Enter watermark")
        self.entry.pack()

        self.btn_add_watermark = tk.Button(root, text="Add Watermark", command=self.add_watermark)
        self.btn_add_watermark.pack()

        self.btn_save = tk.Button(root, text="Save Image", command=self.save_image)
        self.btn_save.pack()

        self.img = None
        self.tk_img = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.img = Image.open(file_path).convert("RGBA")
            self.display_image(self.img)

    def display_image(self, img):
        img_resized = img.resize((500, 400))
        self.tk_img = ImageTk.PhotoImage(img_resized)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

    def add_watermark(self):
        if self.img:
            text = self.entry.get()
            watermark = self.img.copy()
            draw = ImageDraw.Draw(watermark)

            # Choose font
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except IOError:
                font = ImageFont.load_default()

            # Get text size using textbbox (preferred for accuracy)
            bbox = draw.textbbox((0, 0), text, font=font)
            textwidth = bbox[2] - bbox[0]
            textheight = bbox[3] - bbox[1]

            # Position: bottom right with 10px padding
            x = watermark.width - textwidth - 10
            y = watermark.height - textheight - 10

            draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))  # white semi-transparent
            self.img = watermark
            self.display_image(self.img)

    def save_image(self):
        if self.img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                self.img.convert("RGB").save(file_path)
                print("Image saved.")