import os
from PIL import Image
import imagehash

def compare_images(image_path1, image_path2):
    """
    Compare two images using pHash from imagehash.
    
    Returns:
       accepted (bool): True if similarity is above 35%.
       diff (int): The computed Hamming difference.
       similarity_percent (float): Similarity percentage computed as:
            (1 - diff/64)*100
    """
    try:
        hash1 = imagehash.phash(Image.open(image_path1))
        hash2 = imagehash.phash(Image.open(image_path2))
    except Exception as e:
        print(f"Error reading images: {e}")
        return False, None, None

    diff = hash1 - hash2
    max_diff = 64  
    similarity_percent = (1 - diff / max_diff) * 100
    accepted = similarity_percent > 15  
    print(f"Hamming difference: {diff}  |  Similarity: {similarity_percent:.1f}%")
    return accepted, diff, similarity_percent

def main():
    pdfs_folder = "extracted_pdfs"           
    signatures_folder = "extracted_signatures"  
    
    accepted_clients = {}
    rejected_clients = {}
    
    
    for client in os.listdir(pdfs_folder):
        client_path = os.path.join(pdfs_folder, client)
        if not os.path.isdir(client_path):
            print(f"[{client}] is not a directory; skipping.")
            continue
        
        client_passport_folder = client_path
        client_signature_folder = os.path.join(signatures_folder, client)
        
        passport_path = os.path.join(client_passport_folder, "passport.png")
        signature_path = os.path.join(client_signature_folder, "signature_page.png")
        
        if not os.path.exists(passport_path) or not os.path.exists(signature_path):
            print(f"[{client}] Missing passport.png or signature_page.png.")
            continue
        
        print(f"\nProcessing client: {client}")
        accepted, diff, similarity = compare_images(passport_path, signature_path)
        if accepted:
            print(f"[{client}] ACCEPT (similarity: {similarity:.1f}%)")
            accepted_clients[client] = similarity
        else:
            print(f"[{client}] REJECT (similarity: {similarity:.1f}%)")
            rejected_clients[client] = similarity

    
    print("\nSummary:")
    if accepted_clients:
        print("Accepted clients:")
        for client, sim in accepted_clients.items():
            print(f"  - {client}: {sim:.1f}% similar")
    else:
        print("No client accepted.")
    
    if rejected_clients:
        print("Rejected clients:")
        for client, sim in rejected_clients.items():
            print(f"  - {client}: {sim:.1f}% similar")
    else:
        print("No client rejected.")

if __name__ == "__main__":
    main()
