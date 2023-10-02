from PIL import Image, ImageTk
from tkinter import ttk

def showImg(self, imagedir):
        load = Image.open(imagedir)
        load.thumbnail((500, 400))
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = ttk.Label(self, image=render)
        img.image = render
        return img