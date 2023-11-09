import csv
import tkcap

from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from tkinter import END


class App:
    def __init__(self, image_processor, model_strategy, grad_cam):
        self.image_processor = image_processor
        self.model_strategy = model_strategy
        self.grad_cam = grad_cam

    #   METHODS
    def preprocess_image(self, array):
        processed_array = self.image_processor.preprocess(array)
        return processed_array

    def run_model(self, gui):
        self.label, self.proba, self.heatmap = self.model_strategy.predict(gui.array)
        gui.img2 = Image.fromarray(self.heatmap)
        gui.img2 = gui.img2.resize((250, 250), Image.LANCZOS)
        gui.img2 = ImageTk.PhotoImage(gui.img2)
        print("OK")
        gui.text_img2.image_create(END, image=gui.img2)
        gui.text2.insert(END, self.label)
        gui.text3.insert(END, "{:.2f}".format(self.proba) + "%")
    
    def save_results_csv(self):
        with open("historial.csv", "a") as csvfile:
            w = csv.writer(csvfile, delimiter="-")
            w.writerow(
                [self.text1.get(), self.label, "{:.2f}".format(self.proba) + "%"]
            )
            showinfo(title="Save", message="Data saved succesfully.")

    def create_pdf(self):
        cap = tkcap.CAP(self.root)
        ID = "Report" + str(self.reportID) + ".jpg"
        img = cap.capture(ID)
        img = Image.open(ID)
        img = img.convert("RGB")
        pdf_path = r"Report" + str(self.reportID) + ".pdf"
        img.save(pdf_path)
        self.reportID += 1
        showinfo(title="PDF", message="PDF generated succesfully.")