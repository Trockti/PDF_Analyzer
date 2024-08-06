import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
from PIL import Image
import io
import os

def extract_text_from_pdf(pdf_path, output_folder):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        with open(f"{output_folder}/extracted_text.txt", 'w') as file:
            for page in pdf.pages:
                try:
                    file.write(page.extract_text() + "\n")
                except Exception as e:
                    print(f"Error extracting text from page")
                text += page.extract_text() + "\n"
    return text

def extract_images_from_pdf(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            image_filename = f"{output_folder}/images/page_{page_num + 1}_img_{img_index + 1}.png"
            image.save(image_filename)
            print(f"Saved image: {image_filename}")

def extract_tables_from_pdf(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                for table_index, table in enumerate(tables):
                    df = pd.DataFrame(table[1:], columns=table[0])
                    csv_filename = f"{output_folder}/tables/page_{page_num + 1}_table_{table_index + 1}.csv"
                    # excel_filename = f"{output_folder}/page_{page_num + 1}_table_{table_index + 1}.xlsx"
                    try:
                        df.to_csv(csv_filename, index=False)
                        print(f"Saved table to CSV: {csv_filename}")
                        # df.to_excel(excel_filename, index=False)
                        # print(f"Saved table to Excel: {excel_filename}")
                    except Exception as e:
                        print("Failed to save table")
    except Exception as e:
        print("Failed to extract tables")

def main(pdf_path, output_folder):
    print("Extracting text...")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(f"{output_folder}/images"):
        os.makedirs(f"{output_folder}/images")
    if not os.path.exists(f"{output_folder}/tables"):
        os.makedirs(f"{output_folder}/tables")
    text = extract_text_from_pdf(pdf_path, output_folder)

    print(f"Text saved to {output_folder}/extracted_text.txt")

    print("Extracting images...")
    extract_images_from_pdf(pdf_path, output_folder)

    print("Extracting tables...")
    extract_tables_from_pdf(pdf_path, output_folder)

# Example usage
main('Cuentas-anuales-individuales-2023.pdf', 'output_folder')
