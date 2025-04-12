import os
import zipfile
from pdf2image import convert_from_path
import cv2
import numpy as np

# -------------------------------
# Step 1: Extract PDFs from the Zip
# -------------------------------
zip_file_path = 'client_001_200.zip'
extract_dir = 'extracted_pdfs'
os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# -------------------------------
# Step 2: Convert PDFs to Images
# -------------------------------
# You can adjust 'dpi' based on the quality of your PDFs.
# Iterate over each PDF file in the extracted folder.
for file in os.listdir(extract_dir):
    if file.lower().endswith('.pdf'):
        pdf_path = os.path.join(extract_dir, file)
        try:
            # Convert all pages in the PDF to image(s)
            pages = convert_from_path(pdf_path, dpi=300)
        except Exception as e:
            print(f"Error converting {pdf_path}: {e}")
            continue

        # Process each page
        for page_num, page in enumerate(pages):
            image_filename = f"{os.path.splitext(file)[0]}_page_{page_num}.png"
            page.save(image_filename, 'PNG')

            # -------------------------------
            # Step 3: Preprocess the Image
            # -------------------------------
            # Read image using OpenCV
            img = cv2.imread(image_filename)
            if img is None:
                print(f"Error reading image: {image_filename}")
                continue

            # Convert to grayscale for processing
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to obtain a binary image. 
            # (Fine-tune '150' or use adaptive thresholding depending on your docs.)
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

            # -------------------------------
            # Step 4: Locate & Extract the Signature
            # -------------------------------
            # Option A: If you know the approximate location of the signature (e.g. lower quarter)
            h, w = binary.shape
            roi = binary[int(h*0.75):, :]  # Adjust the region as needed

            # Option B: Dynamically detect signature-like regions using contours.
            contours, _ = cv2.findContours(roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            signature_contour = None
            max_area = 0
            for cnt in contours:
                area = cv2.contourArea(cnt)
                # You might set a minimum area threshold to skip small noise.
                if area > max_area:
                    max_area = area
                    signature_contour = cnt

            if signature_contour is not None:
                # Note: the coordinates here are relative to the ROI.
                x, y, w_contour, h_contour = cv2.boundingRect(signature_contour)
                # Adjust the coordinates back relative to the full image:
                y_absolute = int(h*0.75) + y
                signature_img = img[y_absolute:y_absolute + h_contour, x:x + w_contour]
                sig_filename = f"{os.path.splitext(file)[0]}_page_{page_num}_signature.png"
                cv2.imwrite(sig_filename, signature_img)
                print(f"Saved signature image: {sig_filename}")
            else:
                print(f"No signature-like region found in {image_filename}")

            # -------------------------------
            # Step 5: (Optional) Apply OCR if Required
            # -------------------------------
            # If you want to parse text around the signature, you could use pytesseract.
            # For example:
            # import pytesseract
            # text_near_signature = pytesseract.image_to_string(roi)
            # print(f"OCR result: {text_near_signature}")
