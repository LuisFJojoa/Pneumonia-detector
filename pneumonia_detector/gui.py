# gui.py
import os

from tkinter import Tk, ttk, font, Text, StringVar, filedialog, END
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import ImageTk, Image

current_dir = os.path.dirname(os.path.realpath(__file__))
images_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 
                          "volumes")

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

        self.x_ray_image_label = ttk.Label(self.root, text="X Ray Image", font=fonti)
        self.heatmap_image_label = ttk.Label(self.root, text="Heatmap Image", font=fonti)
        self.personal_id_label = ttk.Label(self.root,
                                           text="Personal ID:", font=fonti)
        self.title_label = ttk.Label(
            self.root,
            text="SOFTWARE TO SUPPORT THE MEDICAL DIAGNOSIS OF PNEUMONIA",
            font=fonti,
        )
        self.accuracy_label = ttk.Label(self.root, text="Accuracy:", font=fonti)
        self.status_label = ttk.Label(self.root, text="Status:", font=fonti)

        self.ID = StringVar()
        self.result = StringVar()

        self.personal_id_text = ttk.Entry(self.root,
                                          textvariable=self.ID, width=10)

        self.x_ray_image = Text(self.root, width=31, height=15)
        self.heatmap_image = Text(self.root, width=31, height=15)
        self.accuracy_text = Text(self.root)
        self.result_text = Text(self.root)

        self.predict_event = ttk.Button(
            self.root, text="Predict", state="disabled", command=self.run_model
        )
        self.load_image_event = ttk.Button(
            self.root, text="Load X Ray image", command=self.load_image
        )
        self.clear_data_event = ttk.Button(
            self.root, text="Clear data", command=self.clear_gui
        )
        self.download_pdf_event = ttk.Button(
            self.root, text="Download Pdf", state="disabled",
            command=self.create_pdf
        )
        self.create_csv_event = ttk.Button(
            self.root, text="Save CSV file", state="disabled",
            command=self.create_csv
        )

        #   WIDGETS POSITIONS
        self.x_ray_image_label.place(x=160, y=65)
        self.heatmap_image_label.place(x=680, y=65)
        self.personal_id_label.place(x=65, y=430)
        self.title_label.place(x=160, y=25)
        self.accuracy_label.place(x=650, y=430)
        self.status_label.place(x=650, y=480)

        self.predict_event.place(x=220, y=600)
        self.load_image_event.place(x=70, y=600)
        self.clear_data_event.place(x=800, y=600)
        self.download_pdf_event.place(x=650, y=600)
        self.create_csv_event.place(x=500, y=600)

        self.personal_id_text.place(x=200, y=430, width=120, height=30)
        self.accuracy_text.place(x=750, y=480, width=90, height=30)
        self.result_text.place(x=750, y=430, width=90, height=30)

        self.x_ray_image.place(x=65, y=90,  width=310, height=310)
        self.heatmap_image.place(x=600, y=90,  width=310, height=310)

        self.personal_id_text.focus_set()
        self.array = None
        self.reportID = 0

    def run(self):
        self.root.mainloop()

    def run_model(self):

        self.logic.run_model(self)

    def create_csv(self):

        self.logic.create_csv(self.personal_id_text.get())

    def create_pdf(self):

        self.logic.create_pdf(self.root, self.personal_id_text.get())

    def load_image(self):

        if self.personal_id_text.get():

            filepath = filedialog.askopenfilename(
                initialdir=images_dir,
                title="Select image",
                filetypes=filetypes,
            )

            if filepath:
                self.array, img_from_array = self.image_loader.load_image(filepath)
                self.original_x_ray_image = img_from_array.resize((310, 310), Image.LANCZOS)
                self.original_x_ray_image = ImageTk.PhotoImage(self.original_x_ray_image)
                self.x_ray_image.image_create(END, image=self.original_x_ray_image)
                self.predict_event["state"] = "enabled"
        else:
            showinfo(title="Missed Data",
                     message="Please fill in the personal ID field")

    def clear_gui(self):
        answer = askokcancel(
            title="Confirm", message="All data will be deleted.", icon=WARNING
        )
        if answer:
            self.personal_id_text.delete(0, "end")
            self.accuracy_text.delete(1.0, "end")
            self.result_text.delete(1.0, "end")
            self.personal_id_label.focus_set()
            self.x_ray_image.delete(self.original_x_ray_image, "end")
            self.heatmap_image.delete(self.new_image, "end")
            showinfo(title="Delete", message="Data deleted succesfully")
