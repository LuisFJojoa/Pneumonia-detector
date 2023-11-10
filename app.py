from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from utils import create_pdf_file, create_csv
from tkinter import END


class App:
    def __init__(self, image_processor, model_strategy, grad_cam):
        self.image_processor = image_processor
        self.model_strategy = model_strategy
        self.grad_cam = grad_cam
        self.reportID = 1

    def run_model(self, gui):
        self.label, self.proba, self.heatmap = self.model_strategy.predict(gui.array)
        gui.img2 = Image.fromarray(self.heatmap)
        gui.img2 = gui.img2.resize((250, 250), Image.LANCZOS)
        gui.img2 = ImageTk.PhotoImage(gui.img2)
        print("OK")
        gui.text_img2.image_create(END, image=gui.img2)
        gui.text2.insert(END, self.label)
        gui.text3.insert(END, "{:.2f}".format(self.proba) + "%")
        gui.button4["state"] = "enabled"
        gui.button6["state"] = "enabled"

    def create_csv(self):
        data = [self.reportID, self.label, "{:.2f}".format(self.proba) + "%"]
        create_csv(data)
        showinfo(title="Save", message="Data saved succesfully.")

    def create_pdf(self, root):
        self.reportID += 1
        create_pdf_file(self, root)
        showinfo(title="PDF", message="PDF generated succesfully.")
