import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import green
import io
import os
import glob
import argparse
from datetime import datetime

# Set the font sizes here
MAIN_FONT_SIZE = 70
THANK_YOU_FONT_SIZE = 30

def overlay_text_on_pdf(input_pdf_path, output_pdf_path, main_text, date_text):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    page_width, page_height = letter

    # Prepare the main text
    can.setFont("Helvetica-Bold", MAIN_FONT_SIZE)
    can.setFillColor(green)
    main_text_width = can.stringWidth(main_text, "Helvetica-Bold", MAIN_FONT_SIZE)
    x_main = (page_width - main_text_width) / 2
    y_main = (page_height + MAIN_FONT_SIZE) / 2

    # Apply rotation to the entire canvas and draw the main text
    can.translate(page_width / 2, page_height / 2)
    can.rotate(10)  # Counter-clockwise rotation
    can.translate(-page_width / 2, -page_height / 2)
    can.drawString(x_main, y_main, main_text)

    # Prepare the "Thank You" text
    can.setFont("Helvetica", THANK_YOU_FONT_SIZE)
    thank_you_text = "Thank You"
    thank_you_text_width = can.stringWidth(thank_you_text, "Helvetica", THANK_YOU_FONT_SIZE)
    date_text_width = can.stringWidth(date_text, "Helvetica-Bold", MAIN_FONT_SIZE)
    x_thank_you = x_main + main_text_width - thank_you_text_width
    y_thank_you = y_main - MAIN_FONT_SIZE + THANK_YOU_FONT_SIZE  # Adjusted vertical offset

    # Draw the "Thank You" text
    can.drawString(x_thank_you, y_thank_you, thank_you_text)

    can.save()
    packet.seek(0)
    new_pdf = PyPDF2.PdfReader(packet)
    existing_pdf = PyPDF2.PdfReader(open(input_pdf_path, "rb"))
    output = PyPDF2.PdfWriter()
    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
    with open(output_pdf_path, "wb") as f:
        output.write(f)

def get_most_recent_pdf(directory):
    list_of_pdfs = glob.glob(os.path.join(directory, '*.pdf'))
    return max(list_of_pdfs, key=os.path.getmtime) if list_of_pdfs else None

def build_output_filename(input_filename, output_directory):
    base = os.path.basename(input_filename)
    name, ext = os.path.splitext(base)
    return os.path.join(output_directory, f'{name}R{ext}')

def main():
    parser = argparse.ArgumentParser(description="Overlay text on PDF.")
    parser.add_argument('--input', help="Input PDF file path", default=None)
    parser.add_argument('--output', help="Output PDF file path", default=None)
    parser.add_argument('--date', help="Date to be used in the overlay text", default=None)
    args = parser.parse_args()

    input_directory = '/home/inigo/Documents/Pending invoices'
    output_directory = '/home/inigo/Documents/Pending invoices/Sent Receipts'
    date_text = args.date if args.date else datetime.now().strftime('%d.%m.%y')

    if args.input:
        input_filename = args.input
    else:
        input_filename = get_most_recent_pdf(input_directory)
        if input_filename is None:
            print("No PDF files found in the directory.")
            return

    if args.output:
        output_filename = args.output
    else:
        output_filename = build_output_filename(input_filename, output_directory)

    os.makedirs(output_directory, exist_ok=True)
    overlay_text_on_pdf(input_filename, output_filename, f"PAID: {date_text}", date_text)

if __name__ == "__main__":
    main()
