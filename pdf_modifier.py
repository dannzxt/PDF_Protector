from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.colors import orange
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os


def modify_pdf(filename, id, position, color, upload_folder):
    packet = (
        BytesIO()
    )  # Cria um buffer de memória para armazenar temporariamente o conteúdo do PDF gerado
    can = canvas.Canvas(packet, pagesize=A4)

    match position:
        case "top-left":
            x, y = 50, 800
        case "top-right":
            x, y = 500, 800
        case "bottom-left":
            x, y = 50, 50
        case "bottom-right":
            x, y = 500, 50
        case _:
            raise ValueError("Invalid position")

    print(f"ID insertion at position: ({x}, {y})")

    can.setFillColor(color)
    can.setFont("Helvetica", 10)
    can.drawString(x, y, id)
    can.save()

    try:
        packet.seek(0)
        new_pdf = PdfReader(packet)
        print("Successfully created new PDF with ID.")

    except Exception as e:
        print(f"Error creating new PDF with ID: {str(e)}")

    try:
        path = os.path.join(upload_folder, filename)
        existing_pdf = PdfReader(open(path, "rb"))
        print("Successfully opened existing PDF.")
        num_pages = len(existing_pdf.pages)
        print(f"Number of pages in existing PDF: {num_pages}")
        output = PdfWriter()

        for i in range(num_pages):
            page = existing_pdf.pages[i]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

        with open(path, "wb") as outputStream:
            output.write(outputStream)

        print(f"Modified PDF saved at: {path}")

    except Exception as e:
        print(f"Error opening existing PDF: {str(e)}")
