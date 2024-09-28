import json
from SimplerLLM.tools.json_helpers import extract_json_from_text

def extract_json(text):
    try:
        json_data = extract_json_from_text(text)
        print(f"Extracted JSON: {json_data}")
        
        if json_data and json_data != 'Null':
            return json_data
        else:
            print("No JSON found in the text. Trying to parse manually...................")
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end != -1:
                json_str = text[start:end]
                json_data = json.loads(json_str)
                print(f"Manually Extracted JSON: {json_data}")
                return json_data
            else:
                print("No JSON found in the text.")
                return 
    except Exception as e:
        print(f"Error during extraction: {e}")
        return 
