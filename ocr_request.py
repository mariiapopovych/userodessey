import requests
import time
import base64

endpoint = 'http://localhost:5000/vision/v3.2/read/analyze' # Locally hosted OCR container
class OCRAgent:

    def read(base64_data=None):
        
        headers = {
            'Content-Type': 'application/octet-stream'
        }
        if base64_data == None:
            print("No data given to OCR")
        image_data = base64.b64decode(base64_data)

        response = requests.post(endpoint, headers=headers, data=image_data)
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

                    full_text = " ".join(lines)
                    return full_text
                elif status == 'failed':
                    print("OCR failed")
                    break
                else:
                    print("Waiting for result...")
                    time.sleep(1)

        else:
            print(f"Error: {response.status_code}")
            print(response.text)
