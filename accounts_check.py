import re
class AccountsCheck:
    def completeness(data):
        complete = False
        kw = ["Name of Account", "Name","Surname",
              "Unique ID","Currency","Building Number","Street Name",
              "Postal Code","City","Country","Name","Phone Number","Email","Signature","BANK"]
        data = re.sub(r'\s+', ' ', data).strip()

        # Check for each keyword if the text is followed by non-whitespace content
        for i in range(len(kw) - 1):
            # Find each keyword's position in the text
            start_pos = data.find(kw[i])
            if start_pos == -1:
                # If a keyword is not found, it's incomplete
                return False
            
            # Find the next keyword after the current one
            next_kw = kw[i + 1]
            end_pos = data.find(next_kw, start_pos + len(kw[i]))
            
            if end_pos == -1:
                # If there's no next keyword found, it's incomplete
                return False
            
            # Ensure that the space between the current keyword and next keyword is not just empty spaces
            if data[start_pos + len(kw[i]):end_pos].strip() == "":
                return False
        
            # If all checks passed
            return True

        return complete