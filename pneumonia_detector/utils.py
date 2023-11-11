import os
import csv
import tkcap
from PIL import Image


def create_pdf_file(root, personal_id):
    cap = tkcap.CAP(root)
    ID = "Report" + str(personal_id) + ".jpg"
    img = cap.capture(ID)
    img = Image.open(ID)
    img = img.convert("RGB")
    pdf_path = r"Report" + str(personal_id) + ".pdf"
    img.save(pdf_path)
    return pdf_path


def create_csv(data):
    file_exists = os.path.isfile("history.csv")

    with open("history.csv", "a", newline='') as csvfile:
        w = csv.writer(csvfile, delimiter="-")
        if not file_exists:
            w.writerow(["ID", "Health status", "Accuracy"])
        w.writerow(data)
