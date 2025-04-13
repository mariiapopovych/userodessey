from api_caller import *
from ocr_request import OCRAgent
from accounts_check import AccountsCheck


def pipeline(data_agent):
    # check for pdf completeness
    pdf_data = OCRAgent.read(base64_data=data_agent.get_account())
    print(pdf_data)
    if not(AccountsCheck.completeness(pdf_data)):
        return "Reject"
    print("Accepted")
    return "Accept"

if __name__=="__main__":
    api_agent = APICaller()
    gameover = False

    while not gameover:
        decision = pipeline(data_agent=api_agent) # TODO
        status, score = api_agent.send_decision(decision)
        if status == "gameover": 
            gameover = True
            print("Score: ", score)
