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
        gui.new_image = Image.fromarray(self.heatmap)
        gui.new_image = gui.new_image.resize((250, 250), Image.LANCZOS)
        gui.new_image = ImageTk.PhotoImage(gui.new_image)
        print("OK")
        gui.heatmap_image.image_create(END, image=gui.new_image)
        gui.accuracy_text.insert(END, self.label)
        gui.result_text.insert(END, "{:.2f}".format(self.proba) + "%")
        gui.download_pdf_event["state"] = "enabled"
        gui.create_csv_event["state"] = "enabled"

    def create_csv(self, personal_id):
        data = [personal_id, self.label, "{:.2f}".format(self.proba) + "%"]
        create_csv(data)
        showinfo(title="Save", message="Data saved succesfully.")

    def create_pdf(self, root, personal_id):
        self.reportID = personal_id
        pdf_path = create_pdf_file(self, root)
        showinfo(title="PDF", message="PDF generated succesfully.")
        return pdf_path
