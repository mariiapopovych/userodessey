import os
import fitz
import pytesseract
from PIL import Image
import io

def extract_signatures_with_pymupdf(input_folder='extracted_pdfs',
                                    output_folder='extracted_signatures',
                                    signature_keyword="Signature",
                                    zoom=2.0,
                                    margin=5,
                                    crop_height=100):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for client_dir in os.listdir(input_folder):
        client_path = os.path.join(input_folder, client_dir)
        if not os.path.isdir(client_path):
            continue
        pdf_path = os.path.join(client_path, 'account.pdf')
        if not os.path.exists(pdf_path):
            print(f"Skipping {client_dir}: 'account.pdf' not found.")
            continue
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"Error opening {pdf_path}: {e}")
            continue
        signature_found = False
        for page_num in range(len(doc)):
            page = doc[page_num]
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix)
            img_bytes = pix.tobytes("png")
            try:
                image = Image.open(io.BytesIO(img_bytes))
            except Exception as e:
                print(f"Error converting page {page_num} of {client_dir}: {e}")
                continue
            search_rects = page.search_for(signature_keyword)
            if not search_rects:
                print(f"No signature keyword found on page {page_num} of {client_dir}'s PDF.")
                continue
            rect = search_rects[0]
            rect_scaled = fitz.Rect(rect.x0 * zoom, rect.y0 * zoom, rect.x1 * zoom, rect.y1 * zoom)
            original_width = rect_scaled.width
            center_x = rect_scaled.x0 + original_width / 2
            new_width = original_width * 4
            left = int(center_x - new_width / 3)
            right = int(center_x + new_width / 2)
            upper = int(rect_scaled.y1 + margin * 2.5)
            lower = int(upper + crop_height / 1.5)
            if left < 0:
                left = 0
            if right > image.width:
                right = image.width
            if lower > image.height:
                lower = image.height
            cropped_image = image.crop((left, upper, right, lower))
            client_output_folder = os.path.join(output_folder, client_dir)
            if not os.path.exists(client_output_folder):
                os.makedirs(client_output_folder)
            output_filepath = os.path.join(client_output_folder, "signature_page.png")
            cropped_image.save(output_filepath, 'PNG')
            print(f"Saved signature snippet to: {output_filepath}")
            signature_found = True
            break
        if not signature_found:
            print(f"No signature found in {client_dir}.")
        doc.close()

if __name__ == "__main__":
    extract_signatures_with_pymupdf()
