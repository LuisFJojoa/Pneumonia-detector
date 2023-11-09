# gui.py
import os

from tkinter import Tk, ttk, font, StringVar, Text, filedialog, END
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import ImageTk, Image

project_directory = os.path.dirname(os.path.realpath(__file__))
                                    
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
        # self.lab3 = ttk.Label(self.root, text="Result:", font=fonti)
        self.lab4 = ttk.Label(self.root, text="Personal ID:", font=fonti)
        self.lab5 = ttk.Label(
            self.root,
            text="SOFTWARE TO SUPPORT THE MEDICAL DIAGNOSIS OF PNEUMONIA",
            font=fonti,
        )
        self.lab6 = ttk.Label(self.root, text="Accuracy:", font=fonti)
        self.lab7 = ttk.Label(self.root, text="Status:", font=fonti)

        self.ID = StringVar()
        self.result = StringVar()

        self.text1 = ttk.Entry(self.root, textvariable=self.ID, width=10)

        self.ID_content = self.text1.get()


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
        self.button3 = ttk.Button(self.root, text="Clear data", command=self.clear_gui)
        # self.button4 = ttk.Button(self.root, text="PDF", command=self.create_pdf)
        # self.button6 = ttk.Button(
        #     self.root, text="Guardar", command=self.save_results_csv
        # )

        #   WIDGETS POSITIONS
        self.lab1.place(x=160, y=65)
        self.lab2.place(x=680, y=65)
        # self.lab3.place(x=650, y=530)
        self.lab4.place(x=65, y=350)
        self.lab5.place(x=160, y=25)
        self.lab6.place(x=650, y=430)
        self.lab7.place(x=650, y=480)
        self.button1.place(x=220, y=600)
        self.button2.place(x=70, y=600)
        self.button3.place(x=670, y=600)
        # self.button4.place(x=520, y=460)
        # self.button6.place(x=370, y=460)
        self.text1.place(x=750, y=530, width=90, height=30)
        self.text2.place(x=750, y=480, width=90, height=30)
        self.text3.place(x=750, y=430, width=90, height=30)
        self.text_img1.place(x=65, y=90)
        self.text_img2.place(x=600, y=90)

        self.text1.focus_set()

        self.array = None
        self.reportID = 0

    def run(self):
        self.root.mainloop()
    
    def run_model(self):
        
        self.logic.run_model(self)

    def load_image(self):
        filepath = filedialog.askopenfilename(
            initialdir=project_directory,
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
            self.text1.delete(0, "end")
            self.text2.delete(1.0, "end")
            self.text3.delete(1.0, "end")
            self.text_img1.delete(self.img1, "end")
            self.text_img2.delete(self.img2, "end")
            showinfo(title="Delete", message="Data deleted succesfully")
