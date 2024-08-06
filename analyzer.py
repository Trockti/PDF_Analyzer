import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
from PIL import Image
import io
import os
import tabula
from tabulate import tabulate
import shutil

def extract_text_from_pdf(pdf_path, output_folder):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        with open(f"{output_folder}/extracted_text.txt", 'w', encoding='utf-8') as file:
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
    # Read all tables from all pages of the PDF
    # To extract the tables, we use tabula library
    dfs = tabula.read_pdf(pdf_path, pages="all")

    # Print the number of tables found
    print(f"Number of tables found: {len(dfs)}")

    # Save each table as a CSV file
    for i, df in enumerate(dfs):
        csv_filename =  f"{output_folder}/tables_csv/table_{i + 1}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Saved table {i + 1} to {csv_filename}")

    # Optionally, print each table
        # Print if necessary

        # print(f"\nTable {i + 1}:")
        # print(tabulate(df, headers='keys', tablefmt='grid'))
        with open(f"{output_folder}/tables/table_{i + 1}.txt", "w", encoding='utf-8') as f:
            # Save the table in a file in a table format using tabulate
            f.write(tabulate(df, headers='keys', tablefmt='grid'))

def main(pdf_path, output_folder):
    shutil.rmtree(output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(f"{output_folder}/images"):
        os.makedirs(f"{output_folder}/images")
    if not os.path.exists(f"{output_folder}/tables"):
        os.makedirs(f"{output_folder}/tables")
    os.makedirs(f"{output_folder}/tables_csv", exist_ok=True)

    print("Extracting text...")
    extract_text_from_pdf(pdf_path, output_folder)

    print(f"Text saved to {output_folder}/extracted_text.txt")

    print("Extracting images...")
    extract_images_from_pdf(pdf_path, output_folder)

    print("Extracting tables...")
    extract_tables_from_pdf(pdf_path, output_folder)

    print("All data extracted successfully!")

# Example usage
main('Cuentas-anuales-individuales-2023.pdf', 'output_folder')

# In case we need it

# class PDFProcessingError(Exception):
#     pass


# def extract_tables_from_pdf(pdf_path, output_folder):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page_num, page in enumerate(pdf.pages):
#                 tables = page.extract_tables()
#                 for table_index, table in enumerate(tables):
#                     if not table or not any(table):
#                         continue

#                     # Create DataFrame
#                     df = pd.DataFrame(table)
                    
#                     # Check if the first row is a header
#                     if df.iloc[0].isnull().sum() == 0:
#                         df.columns = df.iloc[0]
#                         df = df.drop(0).reset_index(drop=True)

#                     # Define filenames for CSV and Excel
#                     csv_filename = os.path.join(output_folder, f"page_{page_num + 1}_table_{table_index + 1}.csv")
#                     excel_filename = os.path.join(output_folder, f"page_{page_num + 1}_table_{table_index + 1}.xlsx")
#                     try:
#                         # Save DataFrame to CSV and Excel
#                         df.to_csv(csv_filename, index=False, encoding='utf-8')
#                         print(f"Saved table to CSV: {csv_filename}")
#                     except Exception as e:
#                         raise PDFProcessingError(f"Failed to save table: {e}")
#     except Exception as e:
#         raise PDFProcessingError(f"Failed to extract tables: {e}")
