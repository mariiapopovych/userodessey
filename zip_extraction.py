import zipfile
import os
import shutil

def extract_zip(zip_path, extract_to):
    """Extract a zip file to the specified directory."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted: {zip_path} → {extract_to}")

def process_outer_zips(outer_zip_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(outer_zip_dir):
        if file.lower().endswith(".zip"):
            outer_zip_path = os.path.join(outer_zip_dir, file)
            temp_extract_path = os.path.join(outer_zip_dir, "__temp_extract__")

            # Clear and recreate temporary folder
            if os.path.exists(temp_extract_path):
                for f in os.listdir(temp_extract_path):
                    os.remove(os.path.join(temp_extract_path, f))
            else:
                os.makedirs(temp_extract_path)

            # Extract outer zip to temp folder
            with zipfile.ZipFile(outer_zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_path)

            # Look for inner zips
            for inner_file in os.listdir(temp_extract_path):
                if inner_file.lower().endswith(".zip"):
                    inner_zip_path = os.path.join(temp_extract_path, inner_file)
                    inner_name = os.path.splitext(inner_file)[0]
                    inner_extract_path = os.path.join(output_dir, inner_name)
                    os.makedirs(inner_extract_path, exist_ok=True)

                    try:
                        extract_zip(inner_zip_path, inner_extract_path)
                    except zipfile.BadZipFile:
                        print(f"⚠️ Could not extract: {inner_zip_path}")

            # Clean up temp folder
            for f in os.listdir(temp_extract_path):
                os.remove(os.path.join(temp_extract_path, f))

if __name__ == "__main__":
    outer_zips_dir = os.getcwd()         # Folder containing the outer zip files
    output_data_dir = os.path.join(os.getcwd(), "data")  # Output folder for inner zips
    process_outer_zips(outer_zips_dir, output_data_dir)
