import requests
import time

class OCRAgent:
    def __init__(self):
        self.endpoint = 'http://localhost:5000/vision/v3.2/read/analyze' # Locally hosted OCR container
        self.root_path = 'data/'

    def read(self, client='client_1', filename='passport.png'):
        
        headers = {
            'Content-Type': 'application/octet-stream'
        }

        image_path = self.root_path+client+"/"+filename

        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        response = requests.post(self.endpoint, headers=headers, data=image_data)
        if response.status_code == 200:
            operation_location = response.headers['Operation-Location']
            print(f"Operation URL: {operation_location}")
        elif response.status_code == 202:
            operation_location = response.headers['Operation-Location']
            while True:
                result = requests.get(operation_location, headers=headers)
                result_json = result.json()
                status = result_json.get('status')

                if status == 'succeeded':
                    lines = []
                    for read_result in result_json["analyzeResult"]["readResults"]:
                        for line in read_result.get("lines", []):
                            lines.append(line["text"])

                    full_text = "\n".join(lines)
                    print("Extracted Text:")
                    print(full_text)
                    break
                elif status == 'failed':
                    print("OCR failed")
                    break
                else:
                    print("Waiting for result...")
                    time.sleep(1)

        else:
            print(f"Error: {response.status_code}")
            print(response.text)


