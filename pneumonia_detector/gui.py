# gui.py
import os

from tkinter import Tk, ttk, font, Text, filedialog, END
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import ImageTk, Image

current_dir = os.path.dirname(os.path.realpath(__file__), '../../volumes')
images_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "volumes")
                                    
filetypes = (
    ("DICOM", "*.dcm"),
    ("JPEG", ("*.jpg", "*.jpeg")),
)


class GUI:
    def __init__(self, logic, image_loader):
        self.image_loader = image_loader
        self.logic = logic
        self.root = Tk()
        self.root.title("Software for rapid detection of pneumonia")

        fonti = font.Font(weight="bold")

        self.root.geometry("1015x650")
        self.root.resizable(0, 0)

        self.lab1 = ttk.Label(self.root, text="X Ray Image", font=fonti)
        self.lab2 = ttk.Label(self.root, text="Heatmap Image", font=fonti)
        self.lab4 = ttk.Label(self.root, text="Personal ID:", font=fonti)
        self.lab5 = ttk.Label(
            self.root,
            text="SOFTWARE TO SUPPORT THE MEDICAL DIAGNOSIS OF PNEUMONIA",
            font=fonti,
        )
        self.lab6 = ttk.Label(self.root, text="Accuracy:", font=fonti)
        self.lab7 = ttk.Label(self.root, text="Status:", font=fonti)

        self.text_img1 = Text(self.root, width=31, height=15)
        self.text_img2 = Text(self.root, width=31, height=15)
        self.text2 = Text(self.root)
        self.text3 = Text(self.root)

        self.button1 = ttk.Button(
            self.root, text="Predict", state="disabled", command=self.run_model
        )
        self.button2 = ttk.Button(
            self.root, text="Load X Ray image", command=self.load_image
        )
        self.button3 = ttk.Button(
            self.root, text="Clear data", command=self.clear_gui
        )
        self.button4 = ttk.Button(
            self.root, text="Download Pdf", state="disabled",
            command=self.create_pdf
        )
        self.button6 = ttk.Button(
            self.root, text="Save CSV file", state="disabled",
            command=self.create_csv
        )

        #   WIDGETS POSITIONS
        self.lab1.place(x=160, y=65)
        self.lab2.place(x=680, y=65)
        self.lab4.place(x=65, y=350)
        self.lab5.place(x=160, y=25)
        self.lab6.place(x=650, y=430)
        self.lab7.place(x=650, y=480)
        self.button1.place(x=220, y=600)
        self.button2.place(x=70, y=600)
        self.button3.place(x=800, y=600)
        self.button4.place(x=650, y=600)
        self.button6.place(x=500, y=600)
        self.text2.place(x=750, y=480, width=90, height=30)
        self.text3.place(x=750, y=430, width=90, height=30)
        self.text_img1.place(x=65, y=90)
        self.text_img2.place(x=600, y=90)

        self.array = None
        self.reportID = 0

    def run(self):
        self.root.mainloop()

    def run_model(self):

        self.logic.run_model(self)

    def create_csv(self):

        self.logic.create_csv()

    def create_pdf(self):

        self.logic.create_pdf(self.root)

    def load_image(self):
        filepath = filedialog.askopenfilename(
            initialdir=images_dir,
            title="Select image",
            filetypes=filetypes,
        )

        if filepath:
            self.array, img2show = self.image_loader.load_image(filepath)
            self.img1 = img2show.resize((250, 250), Image.LANCZOS)
            self.img1 = ImageTk.PhotoImage(self.img1)
            self.text_img1.image_create(END, image=self.img1)
            self.button1["state"] = "enabled"

    def clear_gui(self):
        answer = askokcancel(
            title="Confirm", message="All data will be deleted.", icon=WARNING
        )
        if answer:
            self.text2.delete(1.0, "end")
            self.text3.delete(1.0, "end")
            self.text_img1.delete(self.img1, "end")
            self.text_img2.delete(self.img2, "end")
            showinfo(title="Delete", message="Data deleted succesfully")
